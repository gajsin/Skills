# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Windows test-process lifetime: assign a suspended process to a kill-on-close job."""

from __future__ import annotations

import ctypes
from ctypes import wintypes as w
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
from threading import Lock, Thread


def is_reparse(path):
    try:
        return bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except FileNotFoundError:
        return False


def skipped_names(root, directory, names, exclusions):
    # dist/build/out can be package entrypoints, not disposable project outputs.
    if any(part.casefold() == "node_modules" for part in Path(directory).relative_to(root).parts):
        return set()
    excluded = {name.casefold() for name in exclusions}
    return {name for name in names if name.casefold() in excluded}


def new_run_dir():
    parent = Path(tempfile.gettempdir()) / "mutation-workers"
    parent.mkdir(parents=True, exist_ok=True)
    if is_reparse(parent):
        raise RuntimeError(f"Worker temporary root is a reparse point: {parent}")
    return Path(tempfile.mkdtemp(prefix="run-", dir=parent))


def copy_worker(root, worker, relative, original, exclusions):

    def ignored(directory, names):
        skipped = skipped_names(root, directory, names, exclusions)
        for name in names:
            path = Path(directory) / name
            if name not in skipped and is_reparse(path):
                raise RuntimeError(f"Worker input is a reparse point, not an independent file: {path}")
        return skipped

    shutil.copytree(root, worker, ignore=ignored)
    if (worker / relative).read_bytes() != original:
        raise RuntimeError(f"Source changed before creating the worker: {relative}")


def validate_snapshot(root, exclusions):
    def checked(path):
        if is_reparse(path):
            raise ValueError(f"Snapshot path is a reparse point: {path}")
        info = path.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_nlink > 1:
            raise ValueError(f"Snapshot path is a hard link, not an independent copy: {path}")

    def failed(error):
        raise error

    # Excluded outputs are still writable by the tool and must be independent.
    trees = [(root, exclusions)]
    trees.extend((root / name, ()) for name in ("target", ".metrics") if os.path.lexists(root / name))
    for tree, ignored in trees:
        checked(tree)
        for directory, directories, files in os.walk(tree, followlinks=False, onerror=failed):
            skipped = skipped_names(tree, directory, (*directories, *files), ignored)
            directories[:] = [name for name in directories if name not in skipped]
            for name in (*directories, *files):
                if name not in skipped:
                    checked(Path(directory) / name)


def remove_tree(path):
    if is_reparse(path):
        if path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_DIRECTORY:
            path.rmdir()
        else:
            path.unlink()
    elif path.is_dir():
        # Python 3.8+ removes nested Windows junctions without traversing them.
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def record_result(root, directory, token, command, cwd, result=None, error=None):
    report = root / "target" / "mutator-diagnostics"
    report.mkdir(parents=True, exist_ok=True)
    data = {"worker": str(directory), "case": token, "command": command, "cwd": str(cwd)}
    if result is not None:
        data.update(code=result.code, timed_out=result.timed_out, output=result.output)
    if error is not None:
        data["execution_error"] = f"{type(error).__name__}: {error}"
    # Keep diagnostic paths within ordinary Windows limits for deep snapshots.
    name = hashlib.sha256(token.encode("utf-8")).hexdigest()[:24] + ".json"
    (report / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class BasicLimits(ctypes.Structure):
    _fields_ = [
        ("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
        ("flags", w.DWORD), ("min_working_set", ctypes.c_size_t),
        ("max_working_set", ctypes.c_size_t), ("active_processes", w.DWORD),
        ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD),
    ]


class IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in (
        "read_operations", "write_operations", "other_operations",
        "read_bytes", "write_bytes", "other_bytes",
    )]


class ExtendedLimits(ctypes.Structure):
    _fields_ = [
        ("basic", BasicLimits), ("io", IoCounters),
        ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
        ("peak_process_memory", ctypes.c_size_t), ("peak_job_memory", ctypes.c_size_t),
    ]


class ThreadEntry(ctypes.Structure):
    _fields_ = [
        ("size", w.DWORD), ("usage", w.DWORD), ("id", w.DWORD),
        ("process_id", w.DWORD), ("base_priority", w.LONG),
        ("delta_priority", w.LONG), ("flags", w.DWORD),
    ]


def kernel_api():
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    signatures = {
        "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
        "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
        "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
        "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
        "CloseHandle": ([w.HANDLE], w.BOOL),
        "CreateToolhelp32Snapshot": ([w.DWORD, w.DWORD], w.HANDLE),
        "Thread32First": ([w.HANDLE, ctypes.POINTER(ThreadEntry)], w.BOOL),
        "Thread32Next": ([w.HANDLE, ctypes.POINTER(ThreadEntry)], w.BOOL),
        "OpenThread": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
        "ResumeThread": ([w.HANDLE], w.DWORD),
    }
    for name, (args, result) in signatures.items():
        function = getattr(api, name)
        function.argtypes, function.restype = args, result
    return api


def checked(value):
    if not value:
        raise ctypes.WinError(ctypes.get_last_error())
    return value


class ProcessJob:
    def __init__(self):
        self.api = kernel_api()
        self.lock = Lock()
        self.handle = checked(self.api.CreateJobObjectW(None, None))
        limits = ExtendedLimits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        try:
            checked(self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)))
        except BaseException:
            self.close()
            raise

    def close(self):
        with self.lock:
            if self.handle is not None:
                checked(self.api.CloseHandle(self.handle))
                self.handle = None

    def assign_and_resume(self, pid):
        # Popen's thread handle is already closed. Enumerate this still-suspended
        # process's threads through the documented Tool Help API, then resume them.
        process = checked(self.api.OpenProcess(0x0101, False, pid))  # SET_QUOTA | TERMINATE
        try:
            checked(self.api.AssignProcessToJobObject(self.handle, process))
        finally:
            checked(self.api.CloseHandle(process))
        snapshot = self.api.CreateToolhelp32Snapshot(0x00000004, 0)  # SNAPTHREAD
        if snapshot == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        found = False
        try:
            entry = ThreadEntry()
            entry.size = ctypes.sizeof(entry)
            present = self.api.Thread32First(snapshot, ctypes.byref(entry))
            while present:
                if entry.process_id == pid:
                    thread = checked(self.api.OpenThread(0x0002, False, entry.id))
                    try:
                        if self.api.ResumeThread(thread) == 0xFFFFFFFF:
                            raise ctypes.WinError(ctypes.get_last_error())
                    finally:
                        checked(self.api.CloseHandle(thread))
                    found = True
                present = self.api.Thread32Next(snapshot, ctypes.byref(entry))
            if not found:
                raise RuntimeError("No thread found for the suspended test process")
        finally:
            checked(self.api.CloseHandle(snapshot))


def run_command(command, cwd, timeout, environment):
    job = ProcessJob()
    process = None
    watcher = None
    try:
        process = subprocess.Popen(
            command, cwd=cwd, shell=isinstance(command, str),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", env=environment,
            creationflags=0x00000004 | subprocess.CREATE_NO_WINDOW,  # SUSPENDED
        )
        job.assign_and_resume(process.pid)

        def close_on_exit():
            process.wait()
            job.close()  # Also closes inherited pipes held by orphaned children.

        watcher = Thread(target=close_on_exit, daemon=True)
        watcher.start()
        try:
            output, _ = process.communicate(timeout=timeout)
            return process.returncode, False, output
        except subprocess.TimeoutExpired:
            job.close()  # Terminates every process in the job, not just the parent.
            output, _ = process.communicate(timeout=10)
            return 124, True, output
    finally:
        job.close()
        if process is not None:
            if watcher is None and process.poll() is None:
                process.kill()  # Assignment failed while the process was suspended.
            process.wait(timeout=10)
            if process.stdout is not None:
                process.stdout.close()
        if watcher is not None:
            watcher.join(timeout=10)
            if watcher.is_alive():
                raise RuntimeError("Test process did not terminate after closing its Windows job")

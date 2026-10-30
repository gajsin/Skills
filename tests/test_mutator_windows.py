# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Native execution regressions. Run quality_tools.py setup before this suite."""

import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv
from unittest import mock

REPO = Path(__file__).resolve().parents[1]
HELPER = REPO / "Codex/skills/spec-review/scripts/quality_tools.py"
spec = importlib.util.spec_from_file_location("quality_tools", HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def hashes(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file() and "target" not in p.relative_to(root).parts
            and ".metrics" not in p.relative_to(root).parts and "__pycache__" not in p.parts}


class MutationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mutator-native-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "project с пробелом"
        self.root.mkdir()

    def python_project(self, *, strong=True, newline="\n", worker_error=False):
        original = ("def accept(value):" + newline + "    return value > 10 and value < 20" + newline).encode()
        (self.root / "app.py").write_bytes(original)
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "__init__.py").write_bytes(b"")
        text = "import unittest\nfrom pathlib import Path\nimport app\n"
        if worker_error:
            text += "if 'worker-' in str(Path.cwd()): raise RuntimeError('worker environment failure')\n"
        allowed = (original, original.replace(b" > ", b" >= "), original.replace(b" < ", b" <= "), original.replace(b" and ", b" or "))
        text += "class Check(unittest.TestCase):\n    def test_rule(self):\n        self.assertEqual(Path(app.__file__).resolve(), Path.cwd() / 'app.py')\n        print('__source__=' + app.__file__)\n        self.assertTrue(app.accept(15))\n"
        text += "        self.assertIn(Path(app.__file__).read_bytes(), " + repr(allowed) + ")\n"
        if strong:
            text += "        self.assertFalse(app.accept(10))\n"
            text += "        self.assertFalse(app.accept(20))\n"
        (tests / "test_app.py").write_text(text, encoding="utf-8")
        return subprocess.list2cmdline([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"])

    def mutate(self, source, command, expected):
        before = hashes(self.root)
        run = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(HELPER), "mutate", "--snapshot", str(self.root), "--files", source, "--test-command", command, "--max-workers", "2"], capture_output=True, encoding="utf-8")
        self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
        self.assertEqual(before, hashes(self.root), "Snapshot source, tests or configuration changed")
        self.assertFalse(any((self.root / "target/mutation-workers").glob("run-*")))
        if os.name == "nt":
            for path in (self.root / "target/mutator-diagnostics").glob("*.json"):
                self.assertFalse(Path(json.loads(path.read_text(encoding="utf-8"))["worker"]).exists())
        return run

    def test_real_python_killed_and_survived_with_lf_and_crlf(self):
        base = self.root
        for strong, newline in ((True, "\n"), (False, "\r\n")):
            with self.subTest(strong=strong, newline=repr(newline)):
                self.root = base / ("strong" if strong else "weak")
                self.root.mkdir()
                command = self.python_project(strong=strong, newline=newline)
                run = self.mutate("app.py", command, 0 if strong else 3)
                if os.name == "nt":
                    summary = json.loads(run.stdout.strip().splitlines()[-1])
                    self.assertEqual(summary["mutation_tests"], "executed")
                    self.assertEqual(summary["count"], 3)
                    records = [json.loads(p.read_text(encoding="utf-8")) for p in (self.root / "target/mutator-diagnostics").glob("*.json")]
                    self.assertTrue(any("worker-" in r.get("output", "") for r in records))
                    mutations = [r for r in records if not r["case"].startswith("baseline:")]
                    self.assertEqual(mutations[0]["code"], 1 if strong else 0)

    @unittest.skipUnless(os.name == "nt", "Windows worker baseline")
    def test_worker_failure_is_not_a_killed_mutation(self):
        command = self.python_project(worker_error=True)
        run = self.mutate("app.py", command, 2)
        self.assertIn("Unchanged worker baseline failed", run.stderr)
        self.assertFalse((self.root / ".metrics").exists())
        self.assertNotIn('"mutation_tests": "executed"', run.stdout)

    @unittest.skipUnless(os.name == "nt", "Windows short temporary workers")
    def test_deep_snapshot_does_not_add_worker_path_length(self):
        self.root = self.root / ("deep-" + "x" * max(1, 194 - len(str(self.root))))
        self.root.mkdir()
        command = self.python_project()
        self.mutate("app.py", command, 0)
        records = [json.loads(p.read_text(encoding="utf-8")) for p in (self.root / "target/mutator-diagnostics").glob("*.json")]
        self.assertTrue(records)
        self.assertTrue(all(len(record["worker"]) < len(str(self.root)) for record in records))

    @unittest.skipUnless(os.name == "nt", "Windows independent workers")
    def test_worker_files_and_cleanup_are_independent(self):
        from mutator.workers import create_workers, delete_tree, new_run_dir
        self.python_project()
        (self.root / "config.json").write_text('{"value": 1}')
        (self.root / "sibling.py").write_text("VALUE = 1\n")
        before = hashes(self.root)
        base = new_run_dir(self.root)
        self.addCleanup(lambda: delete_tree(base))
        self.assertFalse(base.is_relative_to(self.root))
        workers = create_workers(base, self.root, "app.py", (self.root / "app.py").read_bytes(), 2)
        for name in ("app.py", "tests/test_app.py", "config.json", "sibling.py"):
            original = (self.root / name).read_bytes()
            (workers[0] / name).write_bytes(b"changed")
            self.assertEqual((workers[1] / name).read_bytes(), original)
            self.assertEqual((self.root / name).read_bytes(), original)
        self.assertFalse((workers[0] / "target").exists())
        delete_tree(base)
        self.assertEqual(hashes(self.root), before)

    @unittest.skipUnless(os.name == "nt", "Windows junctions")
    def test_junction_is_rejected_on_copy_and_not_followed_on_cleanup(self):
        import _winapi
        from mutator.workers import create_workers, delete_tree, new_run_dir
        self.python_project()
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        marker = outside / "keep.txt"
        marker.write_text("preserve")
        link = self.root / "linked"
        _winapi.CreateJunction(str(outside), str(link))
        self.addCleanup(lambda: link.rmdir() if link.exists() else None)
        base = new_run_dir(self.root)
        self.addCleanup(lambda: delete_tree(base))
        with self.assertRaisesRegex(RuntimeError, "reparse point"):
            create_workers(base, self.root, "app.py", (self.root / "app.py").read_bytes(), 1)
        delete_tree(base)
        cleanup = Path(self.temporary.name) / "cleanup"
        cleanup.mkdir()
        _winapi.CreateJunction(str(outside), str(cleanup / "linked"))
        delete_tree(cleanup)
        self.assertEqual(marker.read_text(), "preserve")
        self.assertFalse(cleanup.exists())

    @unittest.skipUnless(os.name == "nt", "Windows Scripts interpreter")
    def test_project_virtualenv_interpreter(self):
        from mutator.runner import _project_interpreter, test_plan
        self.python_project()
        venv.EnvBuilder(with_pip=False).create(self.root / ".venv")
        expected = self.root / ".venv/Scripts/python.exe"
        self.assertEqual(_project_interpreter(self.root), str(expected))
        command, cwd = test_plan(self.root, self.root / "app.py", "python", None)
        self.assertEqual(command[0], str(expected))
        from mutator.runner import CommandRunner
        self.assertEqual(CommandRunner().run(command, cwd, 10).code, 0)

    @unittest.skipUnless(shutil.which("node"), "Node runtime unavailable")
    def test_real_node_esmodule_mutation(self):
        node = shutil.which("node")
        (self.root / "package.json").write_text('{"type":"module"}', encoding="utf-8")
        dependency = self.root / "node_modules/local-dep"
        dependency.mkdir(parents=True)
        (dependency / "package.json").write_text('{"type":"module","exports":"./dist/index.js"}')
        (dependency / "dist").mkdir()
        (dependency / "build").mkdir()
        (dependency / "dist/index.js").write_text('export {normalize} from "../build/normalize.js";\n')
        (dependency / "build/normalize.js").write_text('export const normalize = value => value;\n')
        launcher = self.root / "node_modules/local-runner"
        launcher.mkdir()
        (launcher / "cli.cjs").write_text('const {spawnSync}=require("node:child_process");const p=spawnSync(process.execPath,["--test","tests/app.test.js"],{stdio:"inherit"});process.exit(p.status ?? 1);\n')
        (self.root / "app.js").write_text('import {normalize} from "local-dep";\nexport const owner = import.meta.url;\nexport function accept(value) { return normalize(value) > 10; }\n', encoding="utf-8")
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "app.test.js").write_text('import assert from "node:assert/strict";\nimport {test} from "node:test";\nimport {fileURLToPath} from "node:url";\nimport path from "node:path";\nimport {accept, owner} from "../app.js";\ntest("rule",()=>{assert.equal(fileURLToPath(owner),path.join(process.cwd(),"app.js")); assert.equal(accept(10),false);assert.equal(accept(11),true);});\n', encoding="utf-8")
        command = subprocess.list2cmdline([node, "node_modules/local-runner/cli.cjs"])
        run = self.mutate("app.js", command, 0)
        if os.name == "nt":
            self.assertEqual(json.loads(run.stdout.strip().splitlines()[-1])["count"], 1)

    @unittest.skipUnless(os.name == "nt", "Windows process jobs")
    def test_timeout_and_parent_exit_terminate_descendants(self):
        from mutator.runner import CommandRunner
        api = ctypes.WinDLL("kernel32", use_last_error=True)
        api.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        api.OpenProcess.restype = ctypes.c_void_p
        api.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        api.CloseHandle.argtypes = [ctypes.c_void_p]
        child = self.root / "child.py"
        child.write_text("import time\ntime.sleep(30)\n", encoding="utf-8")
        for parent_waits in (True, False):
            with self.subTest(parent_waits=parent_waits):
                pidfile = self.root / "pid.txt"
                pidfile.unlink(missing_ok=True)
                script = self.root / "parent.py"
                script.write_text('import subprocess, sys, time\nfrom pathlib import Path\np=subprocess.Popen([sys.executable,"-B","child.py"])\nPath("pid.txt").write_text(str(p.pid))\n' + ('time.sleep(30)\n' if parent_waits else ''), encoding="utf-8")
                result = CommandRunner().run([sys.executable, "-B", str(script)], self.root, 2)
                self.assertEqual(result.timed_out, parent_waits)
                pid = int(pidfile.read_text())
                process = api.OpenProcess(0x00100000, False, pid)
                if process:
                    try:
                        self.assertEqual(api.WaitForSingleObject(process, 1000), 0, "Descendant still running")
                    finally:
                        api.CloseHandle(process)

    @unittest.skipUnless(os.name == "nt", "Windows launch error")
    def test_launch_error_is_explicit(self):
        from mutator.runner import CommandRunner
        with self.assertRaises(OSError):
            CommandRunner().run([str(self.root / "missing.exe")], self.root, 1)

    @unittest.skipUnless(os.name == "nt", "Windows batch launchers")
    def test_generated_batch_commands(self):
        from mutator.runner import CommandRunner, test_plan
        binaries = Path(self.temporary.name) / "tools с пробелом"
        binaries.mkdir()
        (self.root / "package.json").write_text("{}")
        (self.root / "pom.xml").write_text("<project/>")
        (self.root / "deps.edn").write_text("{}")
        with mock.patch.dict(os.environ, {"PATH": str(binaries) + os.pathsep + os.environ["PATH"]}):
            for language, tool in (("typescript", "npm"), ("java", "mvn"), ("clojure", "clj")):
                (binaries / (tool + ".cmd")).write_text("@echo off\necho batch-ready\n", encoding="ascii")
                command, cwd = test_plan(self.root, self.root / "source", language, None)
                result = CommandRunner().run(command, cwd, 5)
                self.assertEqual(result.code, 0, result.output)
                self.assertIn("batch-ready", result.output)

    @unittest.skipUnless(os.name == "nt", "Windows suspended process setup")
    def test_job_assignment_and_resume_failures_leave_no_process(self):
        import mutator.windows as windows
        api = windows.kernel_api()
        real_popen = subprocess.Popen
        for failure in ("AssignProcessToJobObject", "ResumeThread"):
            with self.subTest(failure=failure):
                created = []
                marker = self.root / "child-ran"
                marker.unlink(missing_ok=True)
                class ApiFailure:
                    def __getattr__(self, name):
                        if name == failure:
                            def fail(*args):
                                ctypes.set_last_error(5)
                                return 0xFFFFFFFF if name == "ResumeThread" else 0
                            return fail
                        return getattr(api, name)
                def track(*args, **kwargs):
                    process = real_popen(*args, **kwargs)
                    created.append(process)
                    return process
                with mock.patch.object(windows, "kernel_api", return_value=ApiFailure()), mock.patch.object(subprocess, "Popen", side_effect=track):
                    with self.assertRaises(OSError):
                        windows.run_command([sys.executable, "-B", "-c", 'from pathlib import Path;Path("child-ran").write_text("bad")'], self.root, 2, os.environ.copy())
                self.assertEqual(len(created), 1)
                self.assertIsNotNone(created[0].poll())
                self.assertFalse(marker.exists())

    @unittest.skipUnless(os.name == "nt", "Windows snapshot preflight")
    def test_snapshot_links_are_rejected_before_baseline(self):
        import _winapi
        command = self.python_project()
        test = self.root / "tests/test_app.py"
        test.write_text('from pathlib import Path\nPath("baseline-ran").write_text("bad")\n' + test.read_text(encoding="utf-8"), encoding="utf-8")
        outside = Path(self.temporary.name) / "external"
        outside.mkdir()
        source = outside / "source.py"
        source.write_text("VALUE = 1\n")
        for relative, kind in (("junction", "junction"), ("hardlink", "hardlink"), ("target", "junction"), (".metrics", "junction"), ("target/nested", "junction"), (".metrics/mutation.json", "hardlink"), ("node_modules/local-dep/dist", "junction")):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if kind == "junction":
                _winapi.CreateJunction(str(outside), str(path))
            else:
                os.link(source, path)
            try:
                run = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(HELPER), "mutate", "--snapshot", str(self.root), "--files", "app.py", "--test-command", command], capture_output=True, encoding="utf-8")
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertFalse((self.root / "baseline-ran").exists())
                self.assertEqual(source.read_text(), "VALUE = 1\n")
            finally:
                path.rmdir() if kind == "junction" else path.unlink()

    @unittest.skipUnless(os.name == "nt", "Windows preflight traversal")
    def test_snapshot_traversal_error_is_not_suppressed(self):
        from mutator.windows import validate_snapshot
        def denied(*args, onerror, **kwargs):
            onerror(PermissionError("unreadable input"))
        with mock.patch("mutator.windows.os.walk", side_effect=denied):
            with self.assertRaisesRegex(PermissionError, "unreadable input"):
                validate_snapshot(self.root, ())

    @unittest.skipUnless(os.name == "nt", "Windows baseline timeout")
    def test_root_baseline_timeout_does_not_produce_mutation_results(self):
        command = self.python_project()
        test = self.root / "tests/test_app.py"
        test.write_text("import time\ntime.sleep(30)\n" + test.read_text(encoding="utf-8"), encoding="utf-8")
        with mock.patch.dict(os.environ, {"MUTATOR_BASELINE_TIMEOUT": "0.2"}):
            run = self.mutate("app.py", command, 2)
        self.assertIn("Baseline failed", run.stderr)
        self.assertFalse((self.root / ".metrics").exists())
        self.assertNotIn('"mutation_tests": "executed"', run.stdout)


if __name__ == "__main__":
    python = helper.tool_python(helper.runtime_dir())
    if Path(sys.prefix).resolve() != python.parent.parent.resolve():
        if not helper.ready(helper.runtime_dir()):
            raise SystemExit("Run Codex/skills/spec-review/scripts/quality_tools.py setup first")
        raise SystemExit(subprocess.run([str(python), "-I", "-B", "-X", "utf8", str(Path(__file__).resolve()), *sys.argv[1:]]).returncode)
    unittest.main()

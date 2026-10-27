# SPDX-License-Identifier: MIT
# Copyright (c) 2026 gajsin
"""Isolated tool setup and read-only evidence from pinned upstream analyzers."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import urllib.request
import venv


TOOLS = {
    "crapper": ("6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d", "8fb0f46d3f22188f66b2fc08685015819e424eec82df58ed3407b0c8a82f6b8d"),
    "dryer": ("66ff6d21a42c04afcad89c78a80066176d1294b0", "1f2d7c6b6cd55d6ae7a4194e0061177031941c53b938872ff43d7d4853fc7015"),
    "mutator": ("a5a0cb803b66e0cdb8bf471b3b08af701d424a41", "61bc8acf160c2c5ceb241039848f02414b174c4479995e310051b440d45c5c79"),
}
DEPENDENCIES = ("tree-sitter==0.26.0", "tree-sitter-language-pack==1.22.1")


def runtime_dir() -> Path:
    home = Path(os.environ.get("SPEC_REVIEW_TOOLS_HOME", Path.home() / ".cache" / "spec-review-tools"))
    identity = json.dumps([TOOLS, DEPENDENCIES, sys.version_info[:2]], sort_keys=True)
    return home.expanduser().resolve() / hashlib.sha256(identity.encode()).hexdigest()[:16]


def tool_python(runtime: Path) -> Path:
    return runtime / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ready(runtime: Path) -> bool:
    stamp = runtime / "ready.json"
    if not stamp.is_file() or not tool_python(runtime).is_file():
        return False
    return json.loads(stamp.read_text(encoding="utf-8")) == {"tools": {k: v[0] for k, v in TOOLS.items()}, "dependencies": list(DEPENDENCIES)}


def setup(runtime: Path) -> None:
    if ready(runtime):
        return
    runtime.mkdir(parents=True, exist_ok=True)
    lock = runtime / ".setup-lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise RuntimeError(f"Setup lock exists: {lock}. Another setup may be running; inspect an interrupted setup before removing its lock.") from error
    try:
        install(runtime)
    finally:
        lock.rmdir()


def install(runtime: Path) -> None:
    sources = []
    for name, (revision, digest) in TOOLS.items():
        destination = runtime / "sources" / name
        stamp = destination / ".revision"
        if destination.exists():
            if not stamp.is_file() or stamp.read_text(encoding="ascii") != revision:
                raise ValueError(f"Unrecognized existing tool directory: {destination}")
            sources.append(destination)
            continue
        request = urllib.request.Request(
            f"https://api.github.com/repos/unclebob/{name}/tarball/{revision}",
            headers={"User-Agent": "spec-review-quality-tools"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Archive checksum mismatch: {name}")
        members = {}
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            for member in archive:
                if member.isdir():
                    continue
                parts = PurePosixPath(member.name).parts
                if not member.isfile() or len(parts) < 2 or ".." in parts or PurePosixPath(member.name).is_absolute():
                    raise ValueError(f"Unsafe archive member: {member.name}")
                target = (destination / Path(*parts[1:])).resolve()
                if not target.is_relative_to(destination):
                    raise ValueError(f"Archive member escapes tool directory: {member.name}")
                members[target] = archive.extractfile(member).read()
        for target, content in members.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        stamp.write_text(revision, encoding="ascii")
        sources.append(destination)
    if not tool_python(runtime).is_file():
        venv.EnvBuilder(with_pip=True).create(runtime / "venv")
    python = str(tool_python(runtime))
    subprocess.run([python, "-I", "-m", "pip", "install", "--disable-pip-version-check", "--no-input", *DEPENDENCIES], check=True)
    subprocess.run([python, "-I", "-m", "pip", "install", "--disable-pip-version-check", "--no-input", "--no-deps", *(str(p) for p in sources)], check=True)
    subprocess.run([python, "-I", "-B", "-c", "import crapper.cli, dryer.cli, mutator.cli"], check=True)
    stamp = {"tools": {k: v[0] for k, v in TOOLS.items()}, "dependencies": list(DEPENDENCIES)}
    (runtime / "ready.json").write_text(json.dumps(stamp, indent=2), encoding="utf-8")


def select_files(root: Path, args) -> tuple[list[Path], list[str]]:
    from crapper.discover import iter_source_files, is_test_file, language_of

    if args.all:
        files = iter_source_files([root])
    else:
        files = []
        for value in args.files:
            path = Path(value)
            path = (root / path).resolve() if not path.is_absolute() else path.resolve()
            if not path.is_file():
                raise ValueError(f"Expected an existing file, not a filter or directory: {value}")
            files.append(path)
    selected, excluded = [], []
    for path in sorted(set(files)):
        if not path.is_relative_to(root):
            raise ValueError(f"Source escapes the project: {path}")
        if language_of(path) is None or is_test_file(path):
            excluded.append(path.relative_to(root).as_posix())
        else:
            selected.append(path)
    return selected, excluded


def observed_coverage(bundle, function):
    if bundle is None:
        return None
    if function.language == "java":
        return bundle.percent_for(function)
    if function.language == "go":
        from crapper.coverage import _profile_segments
        segments = _profile_segments(bundle.go_profile, function.path, bundle.source_parts) or []
        measured = any(total > 0 and start <= function.end_line and end >= function.start_line for start, end, total, _hits in segments)
    else:
        record = bundle._html_lines(function.path)
        if record is None:
            record = bundle._lcov_lines(function.path)
        ranges = [record or {}, getattr(record, "branches", {})]
        measured = any(total > 0 and function.start_line <= line <= function.end_line for hits in ranges for line, (_covered, total) in hits.items())
    return bundle.percent_for(function) if measured else None


def inspect_crapper(files: list[Path], root: Path, args) -> dict:
    from crapper.coverage import load_bundle
    from crapper.crap import make_entry
    from crapper.discover import language_of
    from crapper.languages import functions_in_file

    bundle = load_bundle(root) if args.existing_coverage else None
    if bundle is not None:
        bundle.bind_sources([p.relative_to(root).as_posix() for p in files])
    entries = []
    unknown = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        source = path.read_text(encoding="utf-8")
        for function in functions_in_file(language_of(path), source, relative, str(root)):
            coverage = observed_coverage(bundle, function)
            if coverage is None:
                unknown += 1
            # Preserve missing evidence as N/A, rather than upstream CLI's 0%.
            entry = asdict(make_entry(function, coverage))
            entry.update(start_line=function.start_line, end_line=function.end_line)
            entries.append(entry)
    return {"status": "completed", "mode": "existing_coverage" if bundle is not None else "complexity_only", "coverage_evidence": args.coverage_evidence, "unknown_coverage_functions": unknown, "functions": len(entries), "entries": entries}


def inspect_dryer(files: list[Path], root: Path) -> dict:
    from dryer.cli import parse_args
    from dryer.scan import find_duplicates, scan_files

    defaults = parse_args([])
    entries, warnings = scan_files(files, root, defaults.min_lines, defaults.min_nodes)
    candidates = find_duplicates(entries, defaults.threshold)
    return {"status": "partial" if warnings else "completed", "analyzed_forms": len(entries), "candidate_count": len(candidates), "candidates": [asdict(c) for c in candidates], "warnings": warnings}


def inspect_mutator(files: list[Path], root: Path) -> dict:
    from mutator.functions import sites_in_file

    sites = []
    for path in files:
        sites.extend(sites_in_file(path.read_text(encoding="utf-8"), path, root, path.relative_to(root).as_posix()))
    reason = (
        "Pinned upstream mutation workers and timeout handling do not support native Windows; an existing POSIX environment is required."
        if os.name == "nt" else
        "Site discovery only. Actual mutation requires an isolated project snapshot and a verified project test command; follow automated-checks.md."
    )
    return {"status": "scan_only", "mutation_tests": "not_run", "reason": reason, "candidate_count": len(sites), "sites": [asdict(site) for site in sites]}


def inspect_project(args) -> dict:
    from crapper.discover import language_of
    from crapper.languages.treesitter import parse

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    if args.existing_coverage and not args.coverage_evidence:
        raise ValueError("Existing coverage requires --coverage-evidence explaining its match to this reviewed snapshot.")
    files, excluded = select_files(root, args)
    source_hashes = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    report = {"schema": 1, "root": str(root), "scope": "project" if args.all else "explicit_files", "files": list(source_hashes), "source_sha256": source_hashes, "excluded": excluded, "tools": {}}
    analyzed, parse_issues = [], []
    for path in files:
        try:
            language = language_of(path)
            if language != "clojure":
                if path.suffix in {".js", ".jsx", ".mjs", ".cjs"}:
                    language = "javascript"
                elif path.suffix == ".tsx":
                    language = "tsx"
                _data, tree = parse(path.read_text(encoding="utf-8"), language)
                if tree.root_node.has_error:
                    raise ValueError("Parser reported syntax errors; metrics omitted for this file.")
            analyzed.append(path)
        except Exception as error:
            parse_issues.append({"file": path.relative_to(root).as_posix(), "reason": f"{type(error).__name__}: {error}"})
    files = analyzed
    report["parse_issues"] = parse_issues
    actions = {"crapper": lambda: inspect_crapper(files, root, args), "dryer": lambda: inspect_dryer(files, root), "mutator": lambda: inspect_mutator(files, root)}
    for name, action in actions.items():
        if not files:
            report["tools"][name] = {"status": "error" if parse_issues else "not_applicable", "reason": "No analyzable files; inspect parse_issues and exclusions."}
            continue
        try:
            report["tools"][name] = action()
            if parse_issues:
                report["tools"][name]["status"] = "partial"
                report["tools"][name]["omitted_files"] = parse_issues
        except Exception as error:
            report["tools"][name] = {"status": "error", "reason": f"{type(error).__name__}: {error}"}
    changed = [name for name, digest in source_hashes.items() if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest]
    if changed:
        raise RuntimeError(f"Reviewed source changed during inspection: {changed}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup", help="Install pinned tools in a dedicated user cache, never in the reviewed project.")
    commands.add_parser("status", help="Report runtime availability without installing anything.")
    inspect = commands.add_parser("inspect", help="Read-only upstream analysis; mutation discovery is explicitly not mutation testing.")
    inspect.add_argument("--root", type=Path, required=True)
    scope = inspect.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true")
    scope.add_argument("--files", nargs="+")
    inspect.add_argument("--existing-coverage", action="store_true")
    inspect.add_argument("--coverage-evidence")
    inspect.add_argument("--output", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error("Python 3.11 or newer is required.")
    runtime = runtime_dir()
    if args.command == "setup":
        setup(runtime)
    if args.command in {"setup", "status"}:
        print(json.dumps({"ready": ready(runtime), "tool_python": str(tool_python(runtime)), "runtime": str(runtime), "mutator_native_execution": os.name == "posix"}, indent=2))
        return 0
    if not ready(runtime):
        print(json.dumps({"tools": {name: {"status": "unavailable", "reason": "Run quality_tools.py setup in the host's permitted environment first."} for name in TOOLS}}))
        return 2
    if Path(sys.prefix).resolve() != (runtime / "venv").resolve():
        return subprocess.run([str(tool_python(runtime)), "-I", "-B", "-X", "utf8", str(Path(__file__).resolve()), *sys.argv[1:]]).returncode
    root = args.root.expanduser().resolve()
    if args.output and args.output.expanduser().resolve().is_relative_to(root):
        parser.error("Keep the generated report outside the reviewed project.")
    report = inspect_project(args)
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded + "\n", encoding="utf-8")
        print(json.dumps({"report": str(output), "files": len(report["files"]), "tools": {name: {k: v for k, v in value.items() if k not in {"entries", "candidates", "sites"}} for name, value in report["tools"].items()}}, ensure_ascii=False, indent=2))
    else:
        print(encoded)
    return 1 if any(value["status"] in {"error", "partial"} for value in report["tools"].values()) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"quality_tools: {error}", file=sys.stderr)
        raise SystemExit(2)

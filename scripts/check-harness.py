#!/usr/bin/env python3
"""Run read-only structural checks for the installed DeepInterview harness."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


REQUIRED_PATHS = (
    Path("AGENTS.md"),
    Path(".gitattributes"),
    Path(".agents/skills/onboard-repository/SKILL.md"),
    Path(".agents/skills/audit-onboarding-proposal/SKILL.md"),
    Path(".agents/skills/encode-invariant/SKILL.md"),
    Path(".agents/skills/improve-harness/SKILL.md"),
    Path("docs/README.md"),
    Path("docs/HARNESS.md"),
    Path("docs/WORKFLOW.md"),
    Path("docs/plans/active/README.md"),
    Path("docs/plans/deferred/README.md"),
    Path("docs/plans/completed/README.md"),
    Path(".agents/skills/onboard-repository/scripts/render_patch.py"),
    Path(".agents/skills/onboard-repository/scripts/emit_evidence_bundle.py"),
    Path(".agents/skills/audit-onboarding-proposal/scripts/validate_evidence_capsule.py"),
)

MARKDOWN_LINK = re.compile(r'(?<!!)\[[^\]]+\]\(\s*<?([^)>\s]+)>?(?:\s+["\'].*?["\'])?\s*\)')
HARNESS_MARKDOWN = (
    Path("AGENTS.md"),
    Path("docs"),
    Path(".agents"),
)


class CheckFailure(RuntimeError):
    """A deterministic harness-check failure."""


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def required_paths(root: Path) -> None:
    missing = [str(path).replace("\\", "/") for path in REQUIRED_PATHS if not (root / path).is_file()]
    require(not missing, "missing required harness paths: " + ", ".join(missing))


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for entry in HARNESS_MARKDOWN:
        candidate = root / entry
        if candidate.is_file() and candidate.suffix.lower() == ".md":
            files.append(candidate)
        elif candidate.is_dir():
            files.extend(path for path in candidate.rglob("*.md") if path.is_file())
    return sorted(set(files))


def local_target(source: Path, raw_target: str, root: Path) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    candidate = (source.parent / path_text).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise CheckFailure(
            f"{source.relative_to(root)} links outside the repository: {raw_target}"
        ) from exc
    return candidate


def internal_links(root: Path) -> None:
    failures: list[str] = []
    for source in markdown_files(root):
        in_fence = False
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError as exc:
            failures.append(f"{source.relative_to(root)} is not UTF-8: {exc}")
            continue
        for line_number, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in MARKDOWN_LINK.finditer(line):
                try:
                    candidate = local_target(source, match.group(1), root)
                except CheckFailure as exc:
                    failures.append(f"{source.relative_to(root)}:{line_number}: {exc}")
                    continue
                if candidate is not None and not candidate.exists():
                    failures.append(
                        f"{source.relative_to(root)}:{line_number} target does not exist: {match.group(1)}"
                    )
    require(not failures, "internal Markdown link failures:\n- " + "\n- ".join(failures))


def self_tests(root: Path) -> None:
    scripts = (
        Path(".agents/skills/onboard-repository/scripts/render_patch.py"),
        Path(".agents/skills/onboard-repository/scripts/emit_evidence_bundle.py"),
        Path(".agents/skills/audit-onboarding-proposal/scripts/validate_evidence_capsule.py"),
    )
    failures: list[str] = []
    for script in scripts:
        result = subprocess.run(
            [sys.executable, str(root / script), "--self-test"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().replace("\n", "")
            failures.append(f"{script.as_posix()} exited {result.returncode}: {detail}")
    require(not failures, "evidence-tool self-tests failed:\n- " + "\n- ".join(failures))


def main() -> int:
    root = repository_root()
    try:
        required_paths(root)
        internal_links(root)
        self_tests(root)
    except (CheckFailure, OSError) as exc:
        print(f"harness check failed: {exc}", file=sys.stderr)
        return 1
    print("harness check passed: required paths, internal links, and evidence self-tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

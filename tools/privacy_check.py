"""Last-line privacy check using generic patterns only.

Flags user-home paths, email addresses, and Obsidian wikilinks in Markdown.
Usage: python3 tools/privacy_check.py [PATH ...]
Exit codes: 0 clean, 1 findings, 2 usage or IO error.
A line containing the marker "privacy-check: allow" is skipped.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

MARKER = "privacy-check: allow"
EXCERPT_LEN = 100
SKIP_DIRS = {".git", "__pycache__"}

PLACEHOLDERS = {"you", "username", "<you>", "<username>", "name", "example", "Shared"}
ALLOWED_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "users.noreply.github.com",
}
ALLOWED_SUFFIXES = (".invalid", ".example")
ALLOWED_ADDRESSES = {"noreply@anthropic.com"}

MAC_RE = re.compile(r"/Users/([^/\\\s]+)/")  # privacy-check: allow
LINUX_RE = re.compile(r"/home/([^/\\\s]+)/")  # privacy-check: allow
WIN_RE = re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}([^/\\\s]+)")  # privacy-check: allow
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)")
WIKILINK_RE = re.compile(r"\[\[[^\]\n]+\]\]")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def _first_real_path(regex: re.Pattern[str], line: str) -> bool:
    return any(m.group(1) not in PLACEHOLDERS for m in regex.finditer(line))


def _first_real_email(line: str) -> bool:
    for m in EMAIL_RE.finditer(line):
        domain = m.group(1).lower()
        if m.group(0).lower() in ALLOWED_ADDRESSES:
            continue
        if domain in ALLOWED_DOMAINS or domain.endswith(ALLOWED_SUFFIXES):
            continue
        return True
    return False


def find_issues(text: str, *, markdown: bool) -> list[tuple[int, str, str]]:
    """Return (line number, label, excerpt) findings, once per pattern per line."""
    issues: list[tuple[int, str, str]] = []
    fence: tuple[str, int] | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        in_fence = False
        if markdown:
            m = FENCE_RE.match(line)
            if fence is None and m:
                fence = (m.group(1)[0], len(m.group(1)))
                in_fence = True
            elif fence is not None:
                in_fence = True
                if (
                    m
                    and m.group(1)[0] == fence[0]
                    and len(m.group(1)) >= fence[1]
                    and not line.strip().strip(fence[0])
                ):
                    fence = None
        if MARKER in line:
            continue
        found: list[str] = []
        if _first_real_path(MAC_RE, line):
            found.append("macOS user path")
        if _first_real_path(LINUX_RE, line):
            found.append("Linux home path")
        if _first_real_path(WIN_RE, line):
            found.append("Windows user path")
        if _first_real_email(line):
            found.append("email address")
        if (
            markdown
            and not in_fence
            and WIKILINK_RE.search(INLINE_CODE_RE.sub("", line))
        ):
            found.append("Obsidian wikilink")
        if found:
            excerpt = line.strip()[:EXCERPT_LEN]
            issues.extend((number, label, excerpt) for label in found)
    return issues


def _walk(root: Path) -> list[Path]:
    files: list[Path] = []
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        files.extend(Path(base, n) for n in sorted(names))
    return files


def _git_files() -> list[Path] | None:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    names = sorted(set(result.stdout.decode("utf-8", "replace").split("\0")) - {""})
    return [
        Path(n)
        for n in names
        if not SKIP_DIRS & set(Path(n).parts) and Path(n).is_file()
    ]


def _collect(args: list[str]) -> list[Path]:
    if not args:
        files = _git_files()
        return files if files is not None else _walk(Path("."))
    files = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            files.extend(_walk(path))
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(arg)
    return files


def _read_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a.startswith("-") for a in args):
        print("usage: privacy_check.py [PATH ...]", file=sys.stderr)
        return 2
    try:
        files = _collect(args)
        total = 0
        for path in files:
            text = _read_text(path)
            if text is None:
                continue
            for number, label, excerpt in find_issues(
                text, markdown=path.suffix.lower() == ".md"
            ):
                print(f"{path}:{number}: {label}: {excerpt}")
                total += 1
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if total:
        print(f"{total} finding(s) in {len(files)} file(s) checked")
        return 1
    print(f"OK: {len(files)} file(s) checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())

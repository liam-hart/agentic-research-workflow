"""Tests for privacy_check. Sensitive-looking samples are assembled from parts
so this file passes the checker it tests."""

import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import privacy_check as pc

ROOT = Path(__file__).resolve().parent.parent
BS = "\\"


def mac(name: str) -> str:
    return "/" + "Users" + "/" + name + "/docs"


def linux(name: str) -> str:
    return "/" + "home" + "/" + name + "/docs"


def win(name: str, drive: str = "C", slashes: int = 1) -> str:
    sep = BS * slashes
    return drive + ":" + sep + "Users" + sep + name + sep + "docs"


def addr(local: str, domain: str) -> str:
    return local + chr(64) + domain


def labels(text: str, *, markdown: bool = False) -> list[str]:
    return [label for _, label, _ in pc.find_issues(text, markdown=markdown)]


PLACEHOLDERS = ["you", "username", "<you>", "<username>", "name", "example", "Shared"]


class PathTests(unittest.TestCase):
    def test_mac_flagged(self):
        self.assertEqual(labels("see " + mac("person-1")), ["macOS user path"])

    def test_linux_flagged(self):
        self.assertEqual(labels(linux("person-1")), ["Linux home path"])

    def test_windows_flagged_variants(self):
        for drive in ("C", "D", "z"):
            for slashes in (1, 2):
                with self.subTest(drive=drive, slashes=slashes):
                    self.assertEqual(
                        labels(win("person-1", drive, slashes)), ["Windows user path"]
                    )

    def test_placeholders_allowed(self):
        for name in PLACEHOLDERS:
            with self.subTest(name=name):
                self.assertEqual(labels(mac(name)), [])
                self.assertEqual(labels(linux(name)), [])
                self.assertEqual(labels(win(name)), [])
                self.assertEqual(labels(win(name, "E", 2)), [])

    def test_placeholder_then_real_on_same_line(self):
        self.assertEqual(
            labels(mac("you") + " and " + mac("person-1")), ["macOS user path"]
        )

    def test_once_per_pattern_per_line(self):
        self.assertEqual(
            len(pc.find_issues(mac("a1") + " " + mac("b2"), markdown=False)), 1
        )

    def test_line_number_and_excerpt(self):
        issues = pc.find_issues("ok\n" + mac("person-1"), markdown=False)
        self.assertEqual(issues[0][0], 2)
        self.assertIn("person-1", issues[0][2])

    def test_excerpt_truncated(self):
        issues = pc.find_issues(mac("person-1") + " " + "x" * 500, markdown=False)
        self.assertLessEqual(len(issues[0][2]), 105)


class EmailTests(unittest.TestCase):
    def test_flagged(self):
        self.assertEqual(
            labels("mail " + addr("person-1", "mail.test") + " now"), ["email address"]
        )

    def test_allowed_domains(self):
        allowed = [
            "example.com",
            "example.org",
            "example.net",
            "host.invalid",
            "host.example",
            "users.noreply.github.com",
            "EXAMPLE.ORG",
        ]
        for dom in allowed:
            with self.subTest(dom=dom):
                self.assertEqual(labels("person-1@" + dom), [])

    def test_noreply_anthropic_allowed(self):
        self.assertEqual(labels("noreply@anthropic.com"), [])

    def test_other_anthropic_address_flagged(self):
        self.assertEqual(labels(addr("person-1", "anthropic.com")), ["email address"])

    def test_lookalike_domain_flagged(self):
        self.assertEqual(labels(addr("person-1", "notexample.org")), ["email address"])
        self.assertEqual(
            labels(addr("person-1", "example.org.mail.test")), ["email address"]
        )

    def test_trailing_period(self):
        self.assertEqual(labels("write to person-1@example.org."), [])

    def test_decorator_not_email(self):
        self.assertEqual(
            labels(chr(64) + "property\n" + chr(64) + "pytest.mark.skip"), []
        )


class WikilinkTests(unittest.TestCase):
    def test_flagged_in_markdown(self):
        self.assertEqual(
            labels("see [[Some Note]]", markdown=True), ["Obsidian wikilink"]
        )

    def test_alias_flagged(self):
        self.assertEqual(labels("[[Note|alias]]", markdown=True), ["Obsidian wikilink"])

    def test_ignored_outside_markdown(self):
        self.assertEqual(labels("see [[Some Note]]", markdown=False), [])

    def test_ignored_in_backtick_fence(self):
        text = "```\n[[Some Note]]\n```\n[[Real]]"
        issues = pc.find_issues(text, markdown=True)
        self.assertEqual([i[0] for i in issues], [4])

    def test_ignored_in_tilde_fence(self):
        text = "~~~md\n[[Some Note]]\n~~~\n"
        self.assertEqual(labels(text, markdown=True), [])

    def test_fence_needs_matching_closer(self):
        text = "````\n```\n[[Hidden]]\n```\n````\n[[Shown]]"
        issues = pc.find_issues(text, markdown=True)
        self.assertEqual([i[0] for i in issues], [6])

    def test_ignored_in_inline_code(self):
        self.assertEqual(labels("use `[[Some Note]]` syntax", markdown=True), [])

    def test_inline_code_does_not_hide_other_link(self):
        self.assertEqual(
            labels("`[[A]]` and [[B]]", markdown=True), ["Obsidian wikilink"]
        )

    def test_paths_still_flagged_inside_fence(self):
        text = "```\n" + mac("person-1") + "\n```"
        self.assertEqual(labels(text, markdown=True), ["macOS user path"])


class MarkerTests(unittest.TestCase):
    def test_marker_skips_line(self):
        line = mac("person-1") + " person-1@mail.test  # privacy-check: allow"
        self.assertEqual(labels(line), [])

    def test_marker_only_affects_its_line(self):
        text = mac("person-1") + " privacy-check: allow\n" + mac("person-2")
        self.assertEqual([i[0] for i in pc.find_issues(text, markdown=False)], [2])

    def test_marker_does_not_break_fence_tracking(self):
        text = "```\nx privacy-check: allow\n[[A]]\n```\n[[B]]"
        self.assertEqual([i[0] for i in pc.find_issues(text, markdown=True)], [5])

    def test_marker_skips_wikilink(self):
        self.assertEqual(labels("[[A]] privacy-check: allow", markdown=True), [])


class MainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def run_main(self, args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = pc.main(args)
        return code, out.getvalue(), err.getvalue()

    def write(self, name: str, data) -> Path:
        path = self.dir / name
        if isinstance(data, str):
            data = data.encode("utf-8")
        path.write_bytes(data)
        return path

    def test_clean_exit_0(self):
        p = self.write("a.txt", "hello\n")
        code, out, _ = self.run_main([str(p)])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "OK: 1 file(s) checked")

    def test_findings_exit_1(self):
        p = self.write("a.txt", "ok\n" + mac("person-1") + "\n")
        code, out, _ = self.run_main([str(p)])
        self.assertEqual(code, 1)
        self.assertIn(str(p) + ":2: macOS user path: ", out)
        self.assertIn("1 finding", out)

    def test_missing_path_exit_2(self):
        code, _, err = self.run_main([str(self.dir / "nope.txt")])
        self.assertEqual(code, 2)
        self.assertTrue(err)

    def test_unknown_option_exit_2(self):
        code, _, _ = self.run_main(["--bogus"])
        self.assertEqual(code, 2)

    def test_directory_walk_skips_git(self):
        (self.dir / ".git").mkdir()
        (self.dir / ".git" / "config").write_text(mac("person-1"))
        self.write("a.txt", "fine")
        code, out, _ = self.run_main([str(self.dir)])
        self.assertEqual(code, 0)
        self.assertIn("1 file(s)", out)

    def test_binary_skipped(self):
        p = self.write("b.bin", b"abc\x00" + mac("person-1").encode())
        code, out, _ = self.run_main([str(p)])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "OK: 1 file(s) checked")

    def test_non_utf8_skipped(self):
        p = self.write("c.txt", b"\xff\xfe" + mac("person-1").encode())
        code, out, _ = self.run_main([str(p)])
        self.assertEqual(code, 0)
        self.assertNotIn("macOS", out)

    def test_markdown_extension_enables_wikilinks(self):
        md = self.write("n.md", "[[A]]\n")
        txt = self.write("n.txt", "[[A]]\n")
        self.assertEqual(self.run_main([str(md)])[0], 1)
        self.assertEqual(self.run_main([str(txt)])[0], 0)

    def test_no_paths_uses_cwd(self):
        self.write("a.txt", "fine")
        old = os.getcwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, old)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("OK:", out)


class SelfCheckTests(unittest.TestCase):
    def test_repository_is_clean(self):
        old = os.getcwd()
        os.chdir(ROOT)
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = pc.main([])
        finally:
            os.chdir(old)
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()

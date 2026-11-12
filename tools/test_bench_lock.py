"""Tests for tools/bench-lock and tools/chat-name, run against throwaway git repositories."""
import os
import shutil
import subprocess
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.join(TOOLS, "bench-lock")
CHAT = os.path.join(TOOLS, "chat-name")
SID1 = "aaaaaaaa-1111-2222-3333-444444444444"
SID2 = "bbbbbbbb-1111-2222-3333-444444444444"
KEYS = ("owner", "session", "name", "branch", "purpose", "acquired", "return_to")


def git(cwd, *args):
    ident = "test@" + "example.invalid"  # built at runtime so no address is written as a literal
    base = ["git", "-c", "user.name=test", "-c", "user.email=" + ident]
    return subprocess.run(base + list(args), cwd=cwd, capture_output=True, text=True, check=True)


class BenchTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.repo = os.path.join(self.tmp, "repo")
        self.tmpdir = os.path.join(self.tmp, "t")
        os.makedirs(self.repo)
        os.makedirs(self.tmpdir)
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "commit", "-q", "--allow-empty", "-m", "first")

    def env(self, sid=SID1):
        e = dict(os.environ)
        e.pop("CLAUDE_CODE_SESSION_ID", None)
        if sid is not None:
            e["CLAUDE_CODE_SESSION_ID"] = sid
        e["TMPDIR"] = self.tmpdir
        e["PATH"] = TOOLS + os.pathsep + e.get("PATH", "")
        return e

    def run_tool(self, tool, *args, sid=SID1, cwd=None):
        return subprocess.run([tool, *args], cwd=cwd or self.repo, env=self.env(sid),
                              capture_output=True, text=True)

    def bench(self, *args, **kw):
        return self.run_tool(BENCH, *args, **kw)

    def chat(self, *args, **kw):
        return self.run_tool(CHAT, *args, **kw)

    @property
    def lock(self):
        return os.path.join(os.path.realpath(self.repo), ".bench-lock")

    def lock_text(self):
        with open(self.lock) as fh:
            return fh.read()


class BenchLockTests(BenchTestCase):
    def test_take_free_bench_writes_all_keys(self):
        r = self.bench("take", "--purpose", "testing")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("bench taken:", r.stdout)
        text = self.lock_text()
        for key in KEYS:
            self.assertIn(key + ":", text)
        self.assertIn("session: " + SID1, text)
        self.assertIn("purpose: testing", text)

    def test_status_free(self):
        r = self.bench("status")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "free")

    def test_status_holder_and_other(self):
        self.bench("take", "--purpose", "x")
        mine = self.bench("status")
        self.assertEqual(mine.returncode, 0)
        self.assertTrue(mine.stdout.startswith("yours"))
        other = self.bench("status", sid=SID2)
        self.assertEqual(other.returncode, 1)
        self.assertTrue(other.stdout.startswith("held by another chat"))

    def test_second_session_cannot_take(self):
        self.bench("take", "--purpose", "x")
        before = self.lock_text()
        r = self.bench("take", "--purpose", "y", sid=SID2)
        self.assertEqual(r.returncode, 1)
        self.assertIn("bench taken by another chat", r.stdout)
        self.assertEqual(self.lock_text(), before)

    def test_holder_second_take_is_already_yours(self):
        self.bench("take", "--purpose", "x")
        r = self.bench("take", "--purpose", "again")
        self.assertEqual(r.returncode, 0)
        self.assertIn("bench already yours", r.stdout)

    def test_release_by_non_holder_fails_and_force_works(self):
        self.bench("take", "--purpose", "x")
        r = self.bench("release", sid=SID2)
        self.assertEqual(r.returncode, 1)
        self.assertTrue(os.path.exists(self.lock))
        f = self.bench("release", "--force", sid=SID2)
        self.assertEqual(f.returncode, 0)
        self.assertFalse(os.path.exists(self.lock))

    def test_release_by_holder_prints_return_to(self):
        self.bench("take", "--purpose", "x")
        head = git(self.repo, "rev-parse", "--short", "HEAD").stdout.strip()
        r = self.bench("release")
        self.assertEqual(r.returncode, 0)
        self.assertIn("released.", r.stdout)
        self.assertIn("main " + head, r.stdout)
        self.assertFalse(os.path.exists(self.lock))

    def test_release_when_free(self):
        r = self.bench("release")
        self.assertEqual(r.returncode, 0)
        self.assertIn("bench already free", r.stdout)

    def test_wait_times_out_on_held_bench(self):
        self.bench("take", "--purpose", "x")
        r = self.bench("wait", "--purpose", "y", "--timeout", "1", "--poll", "1", sid=SID2)
        self.assertEqual(r.returncode, 3)
        self.assertIn("timed out", r.stderr)

    def test_take_without_session_id_fails(self):
        r = self.bench("take", "--purpose", "x", sid=None)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(self.lock))

    def test_lock_lands_at_main_checkout_from_linked_worktree(self):
        wt = os.path.join(self.tmp, "wt")
        git(self.repo, "worktree", "add", "-q", wt, "-b", "side")
        r = self.bench("take", "--purpose", "x", cwd=wt)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(self.lock))
        self.assertFalse(os.path.exists(os.path.join(wt, ".bench-lock")))
        self.assertIn("branch: side", self.lock_text())

    def test_outside_a_repository_fails(self):
        r = self.bench("status", cwd=self.tmpdir)
        self.assertNotEqual(r.returncode, 0)

    def test_lock_records_chat_name(self):
        self.chat("my chat")
        self.bench("take", "--purpose", "x")
        self.assertIn("name: my chat", self.lock_text())


class ChatNameTests(BenchTestCase):
    def test_set_and_get(self):
        self.assertEqual(self.chat("hand toggle").returncode, 0)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "ghostty-pane-%s.name" % SID1)))
        self.assertEqual(self.chat("--get").stdout.strip(), "hand toggle")

    def test_truncates_to_40_characters(self):
        self.chat("x" * 60)
        self.assertEqual(self.chat("--get").stdout.strip(), "x" * 40)

    def test_newlines_become_spaces(self):
        self.chat("one\ntwo")
        self.assertEqual(self.chat("--get").stdout.strip(), "one two")

    def test_clear(self):
        self.chat("name")
        self.assertEqual(self.chat("--clear").returncode, 0)
        self.assertEqual(self.chat("--get").stdout, "")

    def test_no_session_id_exits_2(self):
        r = self.chat("name", sid=None)
        self.assertEqual(r.returncode, 2)

    def test_no_argument_exits_2(self):
        self.assertEqual(self.chat().returncode, 2)


if __name__ == "__main__":
    unittest.main()

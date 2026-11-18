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
    ident = "test@" + "example.invalid"
    base = [
        "git",
        "-c",
        "user.name=test",
        "-c",
        "user.email=" + ident,
        "-c",
        "commit.gpgsign=false",
    ]
    return subprocess.run(
        base + list(args), cwd=cwd, capture_output=True, text=True, check=True
    )


SESSION_ENV_KEYS = (
    "CLAUDE_CODE_SESSION_ID",
    "AGY_CONVERSATION_ID",
    "ANTIGRAVITY_CONVERSATION_ID",
    "CODEX_THREAD_ID",
    "CURSOR_SESSION_ID",
)


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

    def env(self, sid=SID1, env_var="CLAUDE_CODE_SESSION_ID"):
        e = dict(os.environ)
        for key in SESSION_ENV_KEYS:
            e.pop(key, None)
        if sid is not None and env_var is not None:
            e[env_var] = sid
        e["TMPDIR"] = self.tmpdir
        e["PATH"] = TOOLS + os.pathsep + e.get("PATH", "")
        return e

    def run_tool(
        self, tool, *args, sid=SID1, env_var="CLAUDE_CODE_SESSION_ID", cwd=None
    ):
        return subprocess.run(
            [tool, *args],
            cwd=cwd or self.repo,
            env=self.env(sid, env_var=env_var),
            capture_output=True,
            text=True,
        )

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
        r = self.bench(
            "wait", "--purpose", "y", "--timeout", "1", "--poll", "1", sid=SID2
        )
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
        self.assertTrue(
            os.path.exists(os.path.join(self.tmpdir, "ghostty-pane-%s.name" % SID1))
        )
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


class MultiHarnessTests(BenchTestCase):
    def test_claude_default_owner_prefix(self):
        r = self.bench(
            "take",
            "--purpose",
            "claude work",
            sid=SID1,
            env_var="CLAUDE_CODE_SESSION_ID",
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("owner: claude:" + SID1[:8], self.lock_text())

    def test_agy_conversation_id_and_chat_name(self):
        self.assertEqual(
            self.chat(
                "agy bench run", sid=SID1, env_var="AGY_CONVERSATION_ID"
            ).returncode,
            0,
        )
        r = self.bench(
            "take", "--purpose", "agy check", sid=SID1, env_var="AGY_CONVERSATION_ID"
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.lock_text()
        self.assertIn("owner: agy:" + SID1[:8], text)
        self.assertIn("session: " + SID1, text)
        self.assertIn("name: agy bench run", text)
        # Cross-harness collision: Claude session with SID2 cannot take or release
        blocked = self.bench(
            "take", "--purpose", "other", sid=SID2, env_var="CLAUDE_CODE_SESSION_ID"
        )
        self.assertEqual(blocked.returncode, 1)
        rel_fail = self.bench("release", sid=SID2, env_var="CLAUDE_CODE_SESSION_ID")
        self.assertEqual(rel_fail.returncode, 1)
        # Holder releases cleanly under ANTIGRAVITY_CONVERSATION_ID
        rel_ok = self.bench("release", sid=SID1, env_var="ANTIGRAVITY_CONVERSATION_ID")
        self.assertEqual(rel_ok.returncode, 0, rel_ok.stderr)
        self.assertFalse(os.path.exists(self.lock))

    def test_codex_thread_id_prefix(self):
        r = self.bench(
            "take", "--purpose", "codex pass", sid=SID1, env_var="CODEX_THREAD_ID"
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("owner: codex:" + SID1[:8], self.lock_text())

    def test_explicit_session_flag_before_and_after_subcommand(self):
        self.assertEqual(
            self.chat("--session", "agy:" + SID1, "explicit chat", sid=None).returncode,
            0,
        )
        r = self.bench(
            "--session", "agy:" + SID1, "take", "--purpose", "cli flag", sid=None
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        text = self.lock_text()
        self.assertIn("owner: agy:" + SID1[:8], text)
        self.assertIn("name: explicit chat", text)
        st = self.bench("status", "--session", SID1, sid=None)
        self.assertEqual(st.returncode, 0)
        self.assertTrue(st.stdout.startswith("yours"))
        rel = self.bench("release", "--session", SID1, sid=None)
        self.assertEqual(rel.returncode, 0)
        self.assertFalse(os.path.exists(self.lock))

    def test_status_and_force_release_work_without_session_id(self):
        self.bench("take", "--purpose", "held", sid=SID1)
        st = self.bench("status", sid=None)
        self.assertEqual(st.returncode, 1)
        self.assertTrue(st.stdout.startswith("held by another chat"))
        forced = self.bench("release", "--force", sid=None)
        self.assertEqual(forced.returncode, 0, forced.stderr)
        self.assertFalse(os.path.exists(self.lock))

    def test_path_traversal_session_rejected(self):
        self.assertEqual(
            self.chat("--session", "../escape", "bad", sid=None).returncode, 2
        )
        self.assertNotEqual(
            self.bench(
                "--session", "../escape1234", "take", "--purpose", "x", sid=None
            ).returncode,
            0,
        )

    def test_prefix_hijack_and_newline_injection_blocked(self):
        # Exact match prevents `task-1234-hijack` from releasing `task-1234`
        self.assertEqual(
            self.bench(
                "take",
                "--purpose",
                "edit\nsession: hijack-2222",
                sid="task-1234",
                env_var="CLAUDE_CODE_SESSION_ID",
            ).returncode,
            0,
        )
        # Newline in --purpose cannot forge a second `session:` key
        self.assertEqual(
            self.bench(
                "release", sid="hijack-2222", env_var="CLAUDE_CODE_SESSION_ID"
            ).returncode,
            1,
        )
        # Prefix extension `task-1234-hijack` cannot release `task-1234`
        self.assertEqual(
            self.bench(
                "release", sid="task-1234-hijack", env_var="CLAUDE_CODE_SESSION_ID"
            ).returncode,
            1,
        )
        # Cross-harness same suffix `agy:task-1234` cannot release `claude:task-1234`
        self.assertEqual(
            self.bench(
                "release", sid="task-1234", env_var="AGY_CONVERSATION_ID"
            ).returncode,
            1,
        )
        # Original holder still releases cleanly
        self.assertEqual(
            self.bench(
                "release", sid="task-1234", env_var="CLAUDE_CODE_SESSION_ID"
            ).returncode,
            0,
        )

    def test_help_outside_git_repo_and_chat_name_arg_order(self):
        help_res = self.bench("--help", cwd=self.tmpdir, sid=None)
        self.assertEqual(help_res.returncode, 0)
        self.assertEqual(
            self.chat("order check", "--session", "agy:" + SID1, sid=None).returncode,
            0,
        )
        get_res = self.chat("--get", "--session", "agy:" + SID1, sid=None)
        self.assertEqual(get_res.returncode, 0)
        self.assertEqual(get_res.stdout.strip(), "order check")


if __name__ == "__main__":
    unittest.main()

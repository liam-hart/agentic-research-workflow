"""Tests for list_skills. Temp dirs only."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import list_skills as ls


class ListSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def skill(self, name: str, front: str) -> None:
        folder = self.root / ".agents" / "skills" / name
        folder.mkdir(parents=True)
        (folder / "SKILL.md").write_text(f"---\n{front}\n---\n\nBody.\n")

    def run_main(self, *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = ls.main(["--root", str(self.root), *argv])
        return code, out.getvalue()

    def test_plain_quoted_and_folded_descriptions(self) -> None:
        self.assertEqual(
            ls.description("name: a\ndescription: Plain: text."), "Plain: text."
        )
        self.assertEqual(
            ls.description('description: "Quoted \\"x\\" text."'), 'Quoted "x" text.'
        )
        self.assertEqual(ls.description("description: 'It''s single.'"), "It's single.")
        self.assertEqual(
            ls.description("description: >-\n  Folded over\n  two lines.\nname: a"),
            "Folded over two lines.",
        )

    def test_list_is_sorted_and_names_every_shipped_skill(self) -> None:
        self.skill("beta", "name: beta\ndescription: Second.")
        self.skill("alpha", "name: alpha\ndescription: First.")
        (self.root / ".agents" / "skills" / "README.md").write_text("# Skills\n")
        text = ls.build(self.root)
        self.assertTrue(text.startswith(ls.HEADER))
        self.assertLess(text.index("**alpha**"), text.index("**beta**"))
        self.assertIn(
            "- [**alpha**](../../.agents/skills/alpha/SKILL.md): First.", text
        )
        self.assertIn("2 skills", text)

    def test_name_must_match_folder_and_description_must_exist(self) -> None:
        self.skill("alpha", "name: other\ndescription: First.")
        with self.assertRaises(ls.SkillError):
            ls.build(self.root)
        self.skill("gamma", "name: gamma")
        with self.assertRaises(ls.SkillError):
            ls.build(self.root)

    def test_check_fails_when_the_list_is_stale_and_write_fixes_it(self) -> None:
        self.skill("alpha", "name: alpha\ndescription: First.")
        self.assertEqual(self.run_main("--check")[0], 1)
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(self.run_main("--check")[0], 0)
        self.skill("beta", "name: beta\ndescription: Second.")
        code, out = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertIn("out of date", out)


if __name__ == "__main__":
    unittest.main()

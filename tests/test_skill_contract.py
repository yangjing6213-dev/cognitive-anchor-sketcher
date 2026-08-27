"""Repository-level checks for the distributable Codex Skill."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "cognitive-anchor-sketcher"


class SkillContractTests(unittest.TestCase):
    def test_skill_front_matter_and_references_exist(self) -> None:
        skill = SKILL_ROOT / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---"))
        self.assertIn("name: cognitive-anchor-sketcher", text)
        references = sorted(set(re.findall(r"references/[A-Za-z0-9_.-]+[.]md", text)))
        self.assertTrue(references)
        for reference in references:
            self.assertTrue((SKILL_ROOT / reference).is_file(), reference)

    def test_ci_runs_repository_contract_tests(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "validate-skill.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "python3 -m unittest discover -s tests -p 'test_*.py' -v",
            workflow,
        )

    def test_codeql_workflow_scans_github_actions(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "codeql.yml"
        self.assertTrue(workflow_path.is_file())
        workflow = workflow_path.read_text(encoding="utf-8")
        self.assertIn("github/codeql-action/init@v4", workflow)
        self.assertIn("languages: actions", workflow)
        self.assertIn("build-mode: none", workflow)
        self.assertIn("github/codeql-action/analyze@v4", workflow)
        self.assertIn("security-events: write", workflow)

    def test_readme_example_images_are_present(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        image_paths = re.findall(r"!\[[^]]*\]\((docs/examples/[^)]+)\)", readme)
        self.assertEqual(len(image_paths), 4)
        for image_path in image_paths:
            self.assertTrue((ROOT / image_path).is_file(), image_path)


if __name__ == "__main__":
    unittest.main()

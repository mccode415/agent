#!/usr/bin/env python3
"""Audit local Codex skills and agent prompt docs for common reliability issues."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def iter_skill_files(skills_root: Path) -> Iterable[Path]:
    return sorted(skills_root.glob("**/SKILL.md"))


def parse_frontmatter(skill_md: Path) -> tuple[str | None, str | None]:
    text = skill_md.read_text(errors="ignore")
    match = FRONTMATTER_RE.search(text)
    if not match:
        return None, None
    name = None
    description = None
    for line in match.group(1).splitlines():
        line = line.strip()
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"').strip("'")
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
    return name, description


def check_markdown_links(md_path: Path) -> list[str]:
    text = md_path.read_text(errors="ignore")
    issues: list[str] = []
    for match in MD_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target_path = (md_path.parent / target).resolve()
        if not target_path.exists():
            issues.append(f"Broken link `{target}` in `{md_path}`")
    return issues


def check_script_exec_bits(script_path: Path) -> str | None:
    if not script_path.is_file():
        return None
    first_line = ""
    with script_path.open(errors="ignore") as handle:
        first_line = handle.readline()
    if first_line.startswith("#!") and not os.access(script_path, os.X_OK):
        return f"Script has shebang but is not executable: `{script_path}`"
    return None


def run_quick_validate(skills_root: Path) -> list[str]:
    validator = skills_root / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not validator.exists():
        return [f"Missing validator script: `{validator}`"]

    issues: list[str] = []
    for skill_md in iter_skill_files(skills_root):
        skill_dir = skill_md.parent
        proc = subprocess.run(
            [sys.executable, str(validator), str(skill_dir)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            details = (proc.stdout + proc.stderr).strip()
            issues.append(f"quick_validate failed for `{skill_dir}`: {details}")
    return issues


def check_agent_docs(agent_root: Path) -> list[str]:
    issues: list[str] = []
    for md_path in sorted(agent_root.glob("**/*.md")):
        issues.extend(check_markdown_links(md_path))

    readme = agent_root / "README.md"
    if readme.exists():
        text = readme.read_text(errors="ignore")
        if "change-validator +" in text:
            issues.append("README references deprecated `change-validator` alias.")

    orchestrator = agent_root / "prompts" / "agent-orchestrator.md"
    if orchestrator.exists():
        text = orchestrator.read_text(errors="ignore").lower()
        if "run agents in parallel" in text or "dispatch in parallel" in text:
            issues.append("Orchestrator prompt expects parallel skill runs.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        default=str(Path.home() / ".codex" / "skills"),
        help="Path to the local Codex skills directory",
    )
    parser.add_argument(
        "--agent-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to local agent prompt repository",
    )
    args = parser.parse_args()

    skills_root = Path(args.skills_root).expanduser().resolve()
    agent_root = Path(args.agent_root).expanduser().resolve()

    issues: list[str] = []

    skill_files = list(iter_skill_files(skills_root))
    if not skill_files:
        issues.append(f"No SKILL.md files found under `{skills_root}`.")
    else:
        for skill_md in skill_files:
            name, description = parse_frontmatter(skill_md)
            if not name or not description:
                issues.append(f"Missing frontmatter fields in `{skill_md}`.")
            issues.extend(check_markdown_links(skill_md))

        for script in sorted(skills_root.glob("**/scripts/*")):
            issue = check_script_exec_bits(script)
            if issue:
                issues.append(issue)

        issues.extend(run_quick_validate(skills_root))

    issues.extend(check_agent_docs(agent_root))

    print(f"Skills scanned: {len(skill_files)}")
    if issues:
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Issues found: 0")
    print("Audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

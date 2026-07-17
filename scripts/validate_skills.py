#!/usr/bin/env python3
"""
validate_skills.py — clean-room skill validator for lifecycle-skills.

Standard library only. Read-only. No network, no subprocess, no eval.
Walks every */skills/*/SKILL.md, checks the frontmatter is well-formed and
carries the required keys, checks the folder name matches the declared name,
and checks any evals/evals.json parses as JSON.

Exit 0 = all good. Exit 1 = one or more problems (prints them). Intended to be
the entire CI gate; keep it dependency-free so the gate never installs anything.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_KEYS = ("name", "description")
VALID_NAME = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def parse_frontmatter(text):
    """Return (dict, error). Minimal YAML: top-level `key: value` pairs only.

    Supports single-line values and folded scalars introduced with `>-` / `>`
    (subsequent more-indented lines are joined with spaces). This is enough for
    our SKILL.md frontmatter and avoids a third-party YAML dependency.
    """
    if not text.startswith("---"):
        return None, "missing opening '---' frontmatter fence"
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, "first line must be exactly '---'"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "missing closing '---' frontmatter fence"

    data = {}
    i = 1
    while i < end:
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in raw:
            return None, f"frontmatter line {i + 1} is not 'key: value': {raw!r}"
        key, val = raw.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val in (">-", ">", "|", "|-"):
            # folded/literal scalar: consume more-indented following lines
            base_indent = len(raw) - len(raw.lstrip())
            parts = []
            j = i + 1
            while j < end:
                nxt = lines[j]
                if not nxt.strip():
                    j += 1
                    continue
                indent = len(nxt) - len(nxt.lstrip())
                if indent <= base_indent:
                    break
                parts.append(nxt.strip())
                j += 1
            data[key] = " ".join(parts)
            i = j
        else:
            data[key] = val.strip('"').strip("'")
            i += 1
    return data, None


def check_skill(skill_md):
    problems = []
    folder = skill_md.parent.name
    text = skill_md.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        problems.append(f"{skill_md.relative_to(ROOT)}: {err}")
        return problems

    for key in REQUIRED_KEYS:
        if not fm.get(key):
            problems.append(f"{skill_md.relative_to(ROOT)}: missing required key '{key}'")

    name = fm.get("name", "")
    if name:
        if set(name) - VALID_NAME:
            problems.append(
                f"{skill_md.relative_to(ROOT)}: name '{name}' must be lowercase letters, digits, hyphens"
            )
        if name != folder:
            problems.append(
                f"{skill_md.relative_to(ROOT)}: name '{name}' does not match folder '{folder}'"
            )

    desc = fm.get("description", "")
    if desc and len(desc) < 40:
        problems.append(
            f"{skill_md.relative_to(ROOT)}: description is suspiciously short ({len(desc)} chars) — say when to use it"
        )

    evals = skill_md.parent / "evals" / "evals.json"
    if evals.exists():
        try:
            json.loads(evals.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{evals.relative_to(ROOT)}: invalid JSON — {e}")

    return problems


def main():
    skill_files = sorted(ROOT.rglob("*/skills/*/SKILL.md"))
    if not skill_files:
        print("ERROR: no SKILL.md files found under */skills/*/", file=sys.stderr)
        return 1

    all_problems = []
    for skill_md in skill_files:
        all_problems.extend(check_skill(skill_md))

    if all_problems:
        print(f"FAIL — {len(all_problems)} problem(s) across {len(skill_files)} skill(s):")
        for p in all_problems:
            print(f"  - {p}")
        return 1

    print(f"OK — {len(skill_files)} skill(s) validated:")
    for skill_md in skill_files:
        print(f"  - {skill_md.parent.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

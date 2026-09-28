# Contributing

Lifecycle and retention skills welcome. The bar here is the philosophy, not just
valid YAML — a skill that produces a generic tactic list will be sent back even
if it passes CI.

## Add a skill

1. Create `Retention-Architect/skills/<skill-name>/SKILL.md`.
   - `<skill-name>` is lowercase-hyphenated and must match the frontmatter `name`.
2. Frontmatter requires at least:
   ```yaml
   ---
   name: your-skill-name
   description: >-
     When to use this skill and what it does, in third person. Say the trigger
     out loud ("use when...") — this is what the agent matches on.
   license: MIT
   ---
   ```
3. Add `evals/evals.json` with at least two evals — one that checks the skill
   does its core job, one that checks it *refuses* the wrong thing (skips
   validation, claims lift with no holdout, writes copy before architecture).
4. Adding a lifecycle *program* (welcome, abandonment, winback, and so on)?
   It goes in `Lifecycle-Programs/skills/<program-slug>/` instead. Copy
   `Lifecycle-Programs/skills/program-template/` and follow
   `Lifecycle-Programs/PROGRAM-CONVENTIONS.md`: named leak zone, kill condition
   in the SKILL.md, frameworks not finished copy, fictional examples only.
5. Run the validator locally:
   ```
   python scripts/validate_skills.py
   ```

## The philosophy (non-negotiable)

- **Bet-driven** — recommendations are sized bets with kill conditions.
- **Sacrifice-first** — name what you're *not* doing.
- **Evidence-labeled** — `[Fact]` / `[Evidence]` / `[Inference]` / `[Assumption]`
  on every number that matters.
- **Incrementality-honest** — anything claiming retention lift must ride on a
  holdout. This is the house rule; a skill that lets a renewal rate masquerade as
  lift does not merge.
- **Human tone** — short sentences, opinions, "I think," "I worry."

## Cross-skill state

Skills read and write project-local `.claude/` files
(`lifecycle-context.md`, `retention-snapshot.md`, `decisions.md`) to hand off
context. Keep writes project-local and gitignored — never global `~/.claude/`,
never a committed client data file.

## PRs

Fork, branch, keep the diff scoped to one skill where you can, and make sure
`python scripts/validate_skills.py` exits 0. CI runs the same check.

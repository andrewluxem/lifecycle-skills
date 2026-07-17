# Lifecycle Skills — Retention-Architect

Open-source agent skills for **lifecycle and retention marketing** — the
keep-and-grow half of the growth stack. Where PLG and acquisition skills get
users in the door, these keep them, grow them, and win them back. Built for
Claude Code, Cursor, Gemini CLI, and any agent on the Agent Skills spec.

Opinionated on purpose: every recommendation is a sized bet with a kill
condition, strategy is stated as what you **won't** do, and no flow gets to claim
lift without a holdout. If it isn't incremental, we don't call it a win.

## Why this exists

Acquisition suites answer "how do we get users?" This one answers the harder,
less-glamorous question: "now that we have them, why are they leaving, and what
would actually keep them?" It pairs naturally with any PLG/growth suite — run
those to fill the top of the funnel, run these to stop the bucket leaking.

## The suite

Run it in order — **diagnose the leak before you design anything** — or invoke
any skill directly.

| # | Skill | Phase | What it does | Status |
|---|-------|-------|--------------|--------|
| 1 | `lifecycle-context` | Context | URL/description → auto-drafted business model, lifecycle stages, stack, active-metric, economics. Confirms by options, saves `.claude/lifecycle-context.md`. | 🚧 draft |
| 2 | `retention-diagnosis` | Diagnose | Reads the retention curve, locates the dominant leak (activation / early-life / mid-life / resurrection), sizes it, and runs the incrementality gut-check. | ✅ live |
| 3 | `segmentation-model` | Strategy | RFM + behavioral/lifecycle segments as hypotheses with a validation plan, tied to the leak. | 🚧 draft |
| 4 | `journey-architecture` | Strategy → Execution | Triggers, branches, timing, channel logic, suppression, exits, and a holdout hook per journey. | 🚧 draft |
| 5 | `lifecycle-messaging` | Execution | The actual sequences + cadence, inside the fatigue caps, optimized for behavior not opens. | 🚧 draft |
| 6 | `retention-metrics` | Execution | North Star + guardrails, cohort-stage targets, holdout experiments with kill criteria. | 🚧 draft |

**Why this order:** `retention-diagnosis` is the anchor, not an afterthought.
Segmenting, journey-building, and messaging all inherit the leak it finds, so the
whole suite spends effort on the hole that's actually draining the bucket instead
of the one that's easiest to see.

## The one non-negotiable: incrementality

A retained customer is not a saved customer. Email an at-risk segment and some of
them would have stayed without you. Every skill that touches a retention claim
defaults to a holdout, because a renewal rate is a report, and lift over control
is the truth. This is the through-line of the suite.

## Install

### Claude Code plugin (recommended)

Run inside a Claude Code session:

```
/plugin marketplace add andrewluxem/lifecycle-skills
/plugin install retention-architect@lifecycle-skills
```

Then `/reload-skills` (or restart the session). Update later with
`/plugin marketplace update lifecycle-skills` then
`/plugin update retention-architect@lifecycle-skills`.

### Cross-agent CLI

Works in Claude Code, Cursor, Gemini CLI, and other Agent Skills–spec agents:

```
npx skills add andrewluxem/lifecycle-skills
```

> Note: `npx skills` runs a third-party CLI that executes install-time code. It's
> the cross-agent standard and fine for most users; if you audit your supply
> chain, prefer the plugin path above or the manual copy below.

### Claude.ai (ZIP upload)

ZIP an individual skill folder so `SKILL.md` sits at the ZIP root
(e.g. `Retention-Architect/skills/retention-diagnosis/`), then
claude.ai → Customize → Skills → Upload skill.

### Project-local (team sharing)

```
mkdir -p .claude/skills
cp -r /path/to/lifecycle-skills/Retention-Architect/skills/* .claude/skills/
```

Commit `.claude/skills/` and everyone gets them on clone.

## How to use

Describe your problem and the right skill activates, or name one:

- "Diagnose our retention — churn's up and I don't know where." → `retention-diagnosis`
- "Set up my lifecycle context for bigdillpickleball.com." → `lifecycle-context`
- "Prove our new winback flow actually works." → `retention-metrics`

## A note on your data

The skills write working state (`lifecycle-context.md`, `retention-snapshot.md`,
`decisions.md`) into a **project-local** `.claude/` directory, and this repo
gitignores those files. A real customer's retention data should never land in a
public repo — keep it in the project it belongs to.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New lifecycle skills welcome; the bar is
the philosophy below, not just working YAML.

## Philosophy

Bet-driven — every recommendation is a quantified bet with a kill condition, not
a tactic list. Sacrifice-first — strategy is the three things you're deliberately
not doing so the one that matters gets the budget. Evidence-labeled — `[Fact]`,
`[Evidence]`, `[Inference]`, `[Assumption]` on every number that matters.
Incrementality-honest — no holdout, no lift claim. Human tone — short sentences,
real opinions, "I think," "I worry."

## License

MIT — Andrew Luxem / Some Luck Productions LLC. Independent work; not affiliated
with any employer.

# Program Conventions

The authoring contract for every skill in `Lifecycle-Programs`. Retention-Architect
is the strategy brain: it diagnoses the leak, segments, designs journeys, writes
messages, and proves lift. Lifecycle-Programs is the hands: deployable program
blueprints that inherit that strategy and turn it into something a CRM team can
build this week.

If a program skill breaks one of these rules, it doesn't merge, even if it passes
`scripts/validate_skills.py`.

## Voice (non-negotiable)

- **Bet-driven** — every recommendation is a quantified bet with a kill
  condition, not a tactic list.
- **Sacrifice-first** — state what the program deliberately does NOT do and
  which sibling skill owns the adjacent problem.
- **Evidence-labeled** — `[Fact]`, `[Evidence]`, `[Inference]`, `[Assumption]`
  on every number that matters. Benchmarks are `[Assumption]` unless cited.
- **Incrementality-honest** — every program ships with a holdout recipe. No
  holdout, no lift claim. "A retained customer is not a saved customer" applies
  to every program, including welcome.
- **Human tone** — short sentences, real opinions, "I think," "I worry."

## Program rules

1. **No program without a leak** — each skill names the leak zone(s) it fixes
   (activation / early-life / mid-life / resurrection). If the leak is unknown,
   the skill routes to `retention-diagnosis` first and refuses to design in the
   dark.
2. **Every program declares its kill condition in the SKILL.md**, not buried in
   references.
3. **Copy is frameworks, never finished copy** — each touch gets purpose,
   timing + rationale, channel, job, proof element, CTA, and anti-goal. No swipe
   files.
4. **Platform-agnostic by default** — SKILL.md speaks in primitives (trigger,
   filter, split, wait, exit). ESP specifics (Braze Canvas, Klaviyo flows,
   Iterable journeys, SFMC Journey Builder) live in
   `references/platform-build.md`.
5. **Fictional examples only** — invented brands, labeled-assumption numbers. No
   employer or client data, ever.
6. **The skill is read-only**: it guides QA and measurement, it never sends email
   or SMS.

## Evidence labels, applied

| Label | Means | Example |
|---|---|---|
| `[Fact]` | The user gave it to me, or it is documented | "AOV is $84 `[Fact]`" |
| `[Fact — author's record]` | The author's own operator experience, reported not measured here | Field notes only |
| `[Evidence]` | Computed from the user's data in this session | "Second-purchase rate is 22% `[Evidence]`" |
| `[Inference]` | Reasoned across a gap | "The drop is likely the day-3 shipping delay `[Inference]`" |
| `[Assumption]` | A placeholder or uncited benchmark — go verify it | "Plan for a 5–10% recovery rate `[Assumption]`" |

An illustrative benchmark is never a measured result. If a number isn't the
user's and isn't cited, it's `[Assumption]`, full stop.

## Skill anatomy (every program follows this exactly)

```
skills/<program-slug>/
  SKILL.md
  references/benchmarks.md       # timing/split/content detail; assumptions labeled
  references/platform-build.md   # ESP primitive mapping (Braze / Klaviyo / Iterable / SFMC)
  references/qa-checklist.md     # pre-send checks for this program
  references/measurement.md      # KPIs, guardrails, attribution, holdout recipe, kill condition
  examples/example-brief.md      # brief → build-spec walkthrough on a fictional brand
  evals/evals.json               # repo convention: ≥2 evals, one core job, one refusal
```

`evals/evals.json` is not in the original program anatomy; it's here because the
repo's `CONTRIBUTING.md` requires it of every skill and `validate_skills.py`
parses it when present.

### SKILL.md sections, in order

1. `## When to use this skill` — trigger phrases; what it is NOT for and which
   sibling skill owns that.
2. `## What I need before I start` — required vs. optional inputs; what I can do
   with partial inputs.
3. `## The thesis` — the program's point of view: what most teams get wrong and
   what this program does instead.
4. `## Program blueprint` — objective/audience; message architecture; splits and
   personalization; exits and suppression; content blocks.
5. `## Platform build mapping`
6. `## QA`
7. `## Measurement` — primary KPI, guardrails, holdout recipe, kill condition.
8. `## Field notes` — optional; the author's real operator experience, labeled
   `[Fact — author's record]`.
9. `## Worked example`

### Frontmatter

```yaml
---
name: <program-slug>          # must equal the folder name; lowercase, digits, hyphens
description: >-
  What the program does in one or two sentences. Use when ... (the trigger,
  said out loud — this is what the agent matches on). 40+ characters.
license: MIT
---
```

## The touch framework

Every touch in a message architecture is specified with the same seven fields.
This is the whole copy deliverable; the words themselves belong to
`lifecycle-messaging` or the brand's writers.

| Field | What it answers |
|---|---|
| Purpose | Why this touch exists in the sequence |
| Timing + rationale | When it fires, and why then instead of earlier or later |
| Channel | Email, SMS, push, in-app, and the reason for that channel |
| Job | The one thing the reader should believe or do after it |
| Proof element | The evidence that makes the job credible (review, stat, guarantee, demo) |
| CTA | The single action, and where it lands |
| Anti-goal | What this touch must not do (discount too early, compete with the order confirmation, etc.) |

## Primitives

SKILL.md describes builds in five primitives. `references/platform-build.md`
translates them.

- **Trigger** — the event or entry condition that puts someone in the program.
- **Filter** — who is allowed in or kept in (consent, suppression, segment).
- **Split** — a branch on attribute, behavior, or random assignment (holdouts
  are random splits).
- **Wait** — a time delay or wait-until-event.
- **Exit** — the condition that removes someone, and where they go next.

## Sibling map

| Adjacent problem | Owner |
|---|---|
| Where is the leak? Is this program even the right fix? | `retention-diagnosis` |
| Business model, stack, active metric, economics | `lifecycle-context` |
| Which customers, cut how | `segmentation-model` |
| Cross-program collisions, priority, frequency caps | `journey-architecture` |
| The finished words | `lifecycle-messaging` |
| North Star, experiment design beyond one program | `retention-metrics` |
| Specific program blueprints | this plugin |

## Cross-skill state

Program skills read `.claude/lifecycle-context.md` and
`.claude/retention-snapshot.md` if they exist, and append decisions to
`.claude/decisions.md`. Project-local and gitignored, never global, never a
committed client data file.

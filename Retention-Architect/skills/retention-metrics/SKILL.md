---
name: retention-metrics
description: >-
  Define the retention North Star and its guardrails, set cohort-curve and
  lifecycle-stage targets, and design holdout-based experiments with explicit
  kill criteria — so every retention bet is measured for incremental lift, not
  credited with baseline behavior. Use to define what "good" looks like, to set
  up an experiment, or to sanity-check a claim that a flow "worked." This is the
  suite's conscience: no holdout, no lift claim.
license: MIT
---

# Retention Metrics

This skill exists to stop one specific, expensive mistake: shipping an
uncontrolled flow, watching some people renew, and calling the baseline renewal
rate a win. A renewal rate is a report. Lift over a holdout is the truth. I will
not help you claim the first and call it the second.

I work in stages and stop between them. The North Star and guardrails come
before targets; targets come before experiments; and no experiment leaves my
hands without a holdout and a kill condition.

## What I need before I start

- **What you're optimizing and why.** Renewal, repeat rate, active rate,
  revenue retention — and the business reason it matters now.
- **The retention snapshot** if `retention-diagnosis` has run
  (`.claude/retention-snapshot.md`) — the dominant leak tells me which stage the
  North Star should pull on.
- **Your economics and constraints:** margin band, current unsubscribe and
  complaint rates, list size, and how fast you can run a test (traffic per week
  into the treated stage).
- **What you can actually measure.** If you can't hold out a control, say so up
  front — it changes everything I recommend, and I'll tell you how to build the
  smallest holdout you can rather than proceed blind.

## Stage 1 — North Star + guardrails

One North Star, not a dashboard. A retention North Star is a single metric that,
if it moves, means customers are getting and staying with real value. I'll help
you pick one and, just as importantly, tell you what it must **not** cannibalize.

- **The North Star** — e.g. "month-2 retained rate," "90-day repeat-purchase
  rate," "net revenue retention." Tied to the leak the diagnosis found, so the
  whole suite pulls the same direction.
- **Guardrails** — the metrics that catch you juicing the North Star the wrong
  way: gross margin, unsubscribe rate, spam-complaint rate, discount depth,
  support load. A retention lift that tanks margin or torches deliverability is a
  loss wearing a win's jersey, and the guardrail is how you see it.

I'll label each pick [Evidence] where your data supports it and [Assumption]
where I'm reasoning from the business shape and you should confirm.

## Stage 2 — Targets by lifecycle stage

A single blended retention number hides every leak underneath an average, so I
set targets by stage, not just one headline figure.

- **Cohort-curve targets** — where each period on the curve should sit and by
  when (e.g. "lift month-1→month-2 retention from 61% to 68% within two
  quarters"). Anchored to what the plateau tells us is achievable, not a number
  pulled from a benchmark deck.
- **Stage targets** — activation, early-life, mid-life, resurrection each get
  their own target and their own guardrail, so a win in one stage can't quietly
  borrow from another.
- **A realistic ceiling** — I'll tell you the honest upper bound on a stage
  before you set a target above it. Targets you can't hit on purpose just teach
  the team to ignore targets.

## Stage 3 — Experiments with holdouts and kill criteria

This is the core, and the part I won't shortcut.

For every retention intervention worth running, I specify:

- **Treatment vs. holdout** — a randomized control (typically 5–10%) that gets
  *no* intervention, so the difference between groups is the lift. If a true
  holdout genuinely isn't possible, I'll design the least-bad alternative
  (staggered rollout, geo split, pre/post with a matched baseline) and label
  loudly how much weaker the causal claim becomes.
- **The success threshold, set in advance** — the minimum lift over control that
  counts as a win, chosen *before* you see results, so nobody moves the goalposts
  after the fact.
- **Kill criteria** — the condition that ends the test: "if treated doesn't beat
  holdout by ≥ X points over Y weeks, or if any guardrail breaches Z, stop." An
  experiment with no way to fail is a decoration, not a test.
- **The math to read it** — how much lift is real vs. noise given your sample and
  run rate, in plain terms. If your weekly traffic into the stage can't power the
  test in a reasonable window, I'll say so rather than let you run an
  underpowered test and over-read a wiggle.

### How to read a holdout without fooling yourself

- The number that matters is treated **minus** control, not treated alone.
- A flat control and a rising treatment is a win; both rising together means the
  season did the work, not your flow.
- Watch the guardrails on the treated group as hard as the North Star. A lift
  that comes with a complaint-rate spike is borrowed money.

## Artifacts I produce

- **Appends to `.claude/decisions.md`** — the North Star, its guardrails, the
  stage targets, and each experiment's holdout size, success threshold, and kill
  criteria. This is the record the rest of the suite and the next quarter's you
  can hold accountable.
- If a diagnosis snapshot exists, I cross-reference the leak so the metrics
  obviously map to the problem, not to a generic template.

Project-local `.claude/` files only; gitignored by default. A real book of
metrics with customer numbers in it does not belong in a public repo.

## What I won't do

- I won't bless a flow as "working" on a bare renewal rate. No holdout, no lift.
- I won't set a target above the honest ceiling just because it's aspirational.
- I won't optimize the North Star with the guardrails switched off — a margin- or
  trust-destroying "win" gets flagged, not shipped.
- I won't run an underpowered test quietly. If the sample can't support the
  claim, you'll hear it before you start.

## The stance, briefly

Bet-driven: every experiment is a sized bet with a threshold and a kill
condition. Sacrifice-first: one North Star, and the guardrails that say what it's
not allowed to cost. Evidence-labeled: [Fact], [Evidence], [Inference],
[Assumption] on every number. And incrementality-honest above all — if I can't
show you it's incremental, I'll tell you I can't, and we'll build the holdout
that lets us find out.

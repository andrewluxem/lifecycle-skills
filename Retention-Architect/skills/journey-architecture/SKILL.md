---
name: journey-architecture
description: >-
  Design the lifecycle journeys that treat each segment against the leak — the
  triggers, the branches, the timing, the channel logic, and the exit and
  suppression rules — without writing a single message yet. Use after segments
  exist, when mapping onboarding, activation, engagement, churn-risk, or winback
  flows, or when existing journeys overlap and fatigue the same people.
license: MIT
status: draft
---

# Journey Architecture

> Status: drafted outline (v0.1). Full staged body lands next.

The blueprint layer. It decides *when and to whom* a message fires and how
journeys interact, before anyone worries about copy. Get this wrong and great
copy still fatigues your best customers.

## What it produces
- **Trigger map** per segment: entry condition, branch logic, timing, channel
  (email / push / SMS / in-app), and the value the step delivers.
- **Frequency and suppression rules** — global caps, quiet hours, and priority
  when journeys collide. This is where fatigue gets prevented, not apologized for.
- **Exit criteria** — every journey has a defined way out, including "they did
  the thing, stop messaging them."
- A **holdout hook** on any journey making a retention claim, so lift is
  measurable from day one.

## Principles
- Suppression is a first-class citizen, not an afterthought.
- Every journey has an exit and, where it claims lift, a holdout.
- Maps to the leak and segments upstream — no orphan flows.

## Reads / writes
- Reads context, snapshot, and segments from `.claude/`.
- Appends journey decisions to `.claude/decisions.md`.

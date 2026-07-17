---
name: segmentation-model
description: >-
  Turn a customer base into lifecycle segments you can actually act on — RFM plus
  behavioral and lifecycle-stage cuts — stated as hypotheses with a validation
  plan, not as permanent truth. Use after retention-diagnosis has located the
  leak, when you need to define who gets which treatment, or when existing
  segments are too coarse to target the leak the diagnosis found.
license: MIT
status: draft
---

# Segmentation Model

> Status: drafted outline (v0.1). Full staged body lands next.

Segments are bets about who behaves differently and is worth treating
differently. This skill builds the minimum set that maps to the leak the
diagnosis found — not fourteen personas nobody will ever build a journey for.

## What it produces
- An **RFM base** (recency / frequency / monetary) where it fits the model.
- **Behavioral / lifecycle-stage overlays** tied to the stages captured in
  `lifecycle-context` — activated, habitual, at-risk, dormant, resurrected.
- Each segment written as a **hypothesis**: "we believe X behaves differently and
  a different treatment moves them," plus how you'd validate it in 30 days.

## Principles
- Sized, not exhaustive — a segment nobody will build a journey for shouldn't
  exist.
- Anchored to the leak — segmentation exists to target the dominant leak, not to
  admire the data.
- Evidence-labeled — [Evidence] where the cut is in the data, [Assumption] where
  it isn't yet.

## Reads / writes
- Reads `.claude/lifecycle-context.md` and `.claude/retention-snapshot.md`.
- Appends the chosen segments to `.claude/decisions.md`.

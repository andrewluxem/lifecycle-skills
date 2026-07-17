---
name: lifecycle-messaging
description: >-
  Write the actual lifecycle messages and cadence for a journey the architecture
  already defined — onboarding, activation, engagement, churn-risk, winback —
  with subject lines, body, CTA, and send-timing that respect the frequency caps.
  Use after journey-architecture, when drafting a specific sequence, or when
  rewriting messages that get opens but no behavior change.
license: MIT
status: draft
---

# Lifecycle Messaging

> Status: drafted outline (v0.1). Full staged body lands next.

The copy layer. It writes messages that earn the next action, inside the
suppression and timing rules the architecture set — never in spite of them.

## What it produces
- Per-step **subject / preview / body / CTA**, matched to the segment and the
  step's job.
- **Cadence and timing** recommendations that live within the global frequency
  caps — no sequence that quietly blows the fatigue budget.
- A **value-first bias**: each message delivers or reminds of value, rather than
  just asking for the renewal.

## Principles
- Behavior over opens — a message that gets opened and changes nothing failed.
- Honest urgency — no fake scarcity or manufactured deadlines.
- Fatigue-aware — respects caps; flags any sequence that would breach them.
- Brand-voice aware — defers to a project's saved brand voice when one exists.

## Reads / writes
- Reads context, segments, and the journey spec from `.claude/`.
- Message drafts are returned in-session; final copy is the operator's to place.

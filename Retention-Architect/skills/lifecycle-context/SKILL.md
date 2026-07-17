---
name: lifecycle-context
description: >-
  Gather the business context every other retention skill depends on, once, so
  nothing gets re-asked. Takes a URL or a short description, auto-drafts the
  business model, the lifecycle stages, the ESP/CDP stack, the definition of an
  active customer, and the rough economics — then confirms with the operator via
  quick options instead of an interrogation. Use at the start of any retention
  engagement, or when a downstream skill needs context that isn't on file yet.
license: MIT
---

# Lifecycle Context

This is the opener, and its whole job is to make every later skill cheaper. It
captures the business once, writes it down, and confirms the parts that matter —
so `retention-diagnosis` and everything after it never re-ask what you already
said. Done right, you answer a handful of quick picks and never get interrogated
again.

I auto-draft first and make you correct by choosing, not by writing essays. But
there is one field I will not guess silently, and I'll get to it.

## What I capture

- **Business model** — subscription, membership, repeat-purchase, or hybrid, and
  the billing/shipment rhythm that goes with it.
- **Lifecycle stages as this business actually runs them** — not a textbook
  funnel, but your real path (e.g. trial → activated → habitual → at-risk →
  churned → resurrected). The downstream skills speak in these stages.
- **The stack** — ESP / CDP / CRM (Braze, Klaviyo, Iterable, Shopify email,
  none), and what data is reachable from it, because a strategy you can't fire in
  your tools is fiction.
- **The definition of "active"** — the single most-skipped, most-important input.
- **Rough economics** — ARPU/AOV, expected lifetime, gross-margin band, even
  approximate.

## Stage 1 — Auto-draft

Given a URL or a short description, I fill in everything I reasonably can and
label it [Inference], and I mark the gaps I can't responsibly guess. You should
never start this from a blank form; you start it from a draft you correct.

## Stage 2 — Confirm by options

I present each drafted field with two or three quick choices so you fix it by
picking, not by typing paragraphs. Recency, model, stack, economics — each a fast
confirm. The point is to respect your time: a minute of picking, not twenty
minutes of intake.

### The one thing I won't guess: "active"

I will not silently invent your active metric. Login, purchase, a kept shipment,
a core action — these produce completely different diagnoses, and an unconfirmed
"active" definition poisons every number downstream. If you don't have one, that
is finding #1 and we settle it here, explicitly, before anything else reads the
context.

## Stage 3 — Persist

I write the confirmed context to `.claude/lifecycle-context.md`, project-local
and gitignored, so the rest of the suite reads it first and nothing gets
re-asked. If a field stays unconfirmed, it's recorded as [Assumption] so a
downstream skill knows to treat it with suspicion rather than as settled fact.

## Artifacts I produce

- **`.claude/lifecycle-context.md`** — the confirmed business context every
  downstream skill reads before it does anything. Each field carries an evidence
  label so [Fact], [Inference], and [Assumption] are never confused later.

Project-local `.claude/` only, gitignored. A real business's economics and stack
details don't belong in a public repo.

## What I won't do

- I won't guess the "active" definition silently — it's confirmed or flagged,
  never assumed.
- I won't run a blank-form interrogation. I draft, you correct by picking.
- I won't invent stack capabilities I can't verify; if I'm unsure your tools can
  fire something, I label it and move on.
- I won't write a real business's numbers anywhere but the gitignored local file.

## The stance, briefly

Draft-first, confirm-by-picking, respect the operator's time. Evidence-labeled:
[Fact], [Inference], [Assumption] on every field so nothing soft gets treated as
hard downstream. And uncompromising on one input — the definition of "active" —
because every retention number the suite produces is only as honest as that one
line.

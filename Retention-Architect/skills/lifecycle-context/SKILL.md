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
status: draft
---

# Lifecycle Context

> Status: drafted outline (v0.1). Full staged body lands next.

The opener for the suite. Its job is to make every later skill cheaper by
capturing the business once and writing it down, so `retention-diagnosis` and the
rest never re-ask what you already said.

## What it captures
- Business model: subscription / membership / repeat-purchase / hybrid.
- The lifecycle stages *as this business actually runs them* (not a textbook
  funnel) — e.g. trial → activated → habitual → at-risk → churned → resurrected.
- The stack: ESP/CDP/CRM (Braze, Klaviyo, Iterable, Shopify, etc.), and what
  data is reachable from it.
- The definition of "active" — the single most-skipped, most-important input.
- Rough economics: ARPU/AOV, expected lifetime, gross margin band.

## How it works (staged)
1. **Auto-draft** from the URL / description — fill everything it reasonably can,
   labeled [Inference], and mark the gaps.
2. **Confirm by options** — present each drafted field with 2–3 quick choices so
   the operator corrects by picking, not by writing essays.
3. **Persist** to `.claude/lifecycle-context.md` (project-local, gitignored).

## Artifact
- `.claude/lifecycle-context.md` — the confirmed context every downstream skill
  reads first.

## Won't do
- Won't guess the "active" definition silently — an unconfirmed active metric is
  flagged, not assumed.
- Won't store a real client's data anywhere but the gitignored project-local file.

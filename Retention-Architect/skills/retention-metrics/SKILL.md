---
name: retention-metrics
description: >-
  Define the retention North Star and guardrails, set cohort-curve and
  lifecycle-stage targets, and design holdout-based experiments with explicit
  kill criteria — so every retention bet is measured for incremental lift, not
  credited with baseline behavior. Use to define what "good" looks like, to set
  up experiments, or to sanity-check a claim that a flow "worked."
license: MIT
status: draft
---

# Retention Metrics

> Status: drafted outline (v0.1). Full staged body lands next.

The measurement layer, and the suite's conscience. It exists so nobody ships an
uncontrolled flow and calls the baseline renewal rate a win.

## What it produces
- A **North Star + guardrails**: one retention metric that matters, plus the
  guardrails (margin, unsub rate, complaint rate) that keep you from juicing it
  the wrong way.
- **Cohort-curve and lifecycle-stage targets** — where each stage should sit and
  by when.
- **Experiments with holdouts and kill criteria**: treatment vs. control, the
  lift threshold that counts as success, and the condition that ends the test.

## Principles
- Incrementality or it doesn't count — every claim rides on a holdout.
- Guardrails are non-negotiable — a retention lift that tanks margin or trust is
  a loss.
- Kill criteria up front — an experiment with no way to fail is a decoration.

## Reads / writes
- Reads context, snapshot, and decisions from `.claude/`.
- Appends metric definitions and experiment specs to `.claude/decisions.md`.

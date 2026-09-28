# Measurement: post-purchase

The primary KPI, guardrails, holdout recipe, and kill condition also appear in
SKILL.md. This file carries the detail.

## Primary KPI

**First→second purchase rate within 60 days of first delivery, treated vs.
holdout.**

```
second_purchase_rate(arm) =
  customers in arm with a second order within 60 days of first delivery
  ÷ customers in arm who entered the program
```

- **Window:** 60 days is a default `[Assumption]`. Set it to roughly 1.5x your
  median days between orders 1 and 2, capped so the read happens inside a
  quarter. Long-cycle categories (furniture) may need 120+ days; say so up
  front and accept the slower read.
- **Denominator:** everyone assigned at entry, including those who returned the
  product or unsubscribed. Intent-to-treat. Dropping returners from one arm
  only would bias the read.
- **Why not opens, clicks, or review count:** order and shipping opens are high
  no matter what you do. Reviews are a means. The early-life leak closes only
  when a second order happens that wouldn't have happened otherwise.

Secondary outcomes (reported, not decided on): review submissions per 100
delivered orders, UGC items collected, cross-sell attach rate, revenue per
entrant at 60 days.

## Guardrails

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Marketing unsubscribe rate, touches 3–6 | Above your promotional-campaign average `[Assumption]` | Cut the touch with the highest unsubscribe rate; review timing |
| Spam complaint rate | Above 0.1% per send `[Assumption]` | Pause marketing touches; check consent filter and frequency |
| First-order return rate, treated vs. control | Treated higher by any meaningful margin `[Inference]` that a touch is prompting returns | Review how-to and cross-sell content; check the return exit |
| Discount rate on second orders | Rising vs. pre-program baseline | Confirm no one added a code; lift bought with margin isn't lift |
| "Where is my order" contact rate | Up vs. pre-launch baseline | Check transactional content ratio and tracking links |
| Transactional deliverability (inbox placement, bounces) | Any drop after modules were added | Strip modules from touches 1–2 first |
| Review rating distribution | Sudden shift after the ask launches | Check for sentiment-gated routing or incentive wording |

Breach for two consecutive weekly reads triggers the kill-condition review,
not just the listed action.

## Attribution

- **Window:** the same 60-day window as the KPI.
- **Program-influenced:** any second order from a treated customer inside the
  window. That's a reporting convenience, not lift.
- **Lift:** treated rate minus holdout rate. That's the only number that goes
  in the business case.
- The holdout comparison overrides last-touch attribution every time. Last-touch
  will credit the cross-sell email with orders that the how-to email, the
  product, or a paid ad actually caused, and it will credit all of them to a
  program that some of those customers didn't need. A retained customer is not
  a saved customer.

## Holdout recipe

- **What can't be held out:** touches 1–2. Order and shipping messages are
  owed to every customer. The holdout measures the marketing layer only.
- **What the control receives:** touches 1–2 without the added modules (via a
  conditional block on the stored flag). If your transactional templates
  can't read the flag, both arms get the modules and the read measures touches
  3–6 only. Document which one you ran.
- **Size:** 10–20% of entrants. Pick the smallest control that hits your
  minimum detectable lift within the enrollment time you can tolerate.
- **Randomization unit:** the customer, not the order or the send.
- **Assignment point:** at entry (first-order event), once, stored on the
  profile. Never at send time — that lets exits and consent filters leak into
  the comparison.
- **Duration:** enrollment period (from the sample math below) + the full KPI
  window for the last cohort enrolled.
- **Both arms** keep receiving business-as-usual campaigns. The comparison is
  "BAU + program" vs. "BAU."

### Sample-size reasoning

Two-proportion test, two-sided α = 0.05, power 0.80.

```
N_total ≈ (z_α/2 + z_β)² × p̄(1 − p̄) × (1/share_treated + 1/share_control) ÷ d²
```

| Input | Value | Label |
|---|---|---|
| Baseline 60-day second-purchase rate (p) | 20% | `[Assumption]` |
| Minimum detectable lift (d), absolute | 1.5 points | `[Assumption]` |
| α (two-sided) / power | 0.05 / 0.80 → (1.96 + 0.84)² ≈ 7.85 | `[Fact]` (standard convention) |
| Control share | 20% | `[Assumption]` |

Resulting sizes, computed from those inputs `[Inference]`:

| MDE (abs.) | 50/50 total | 80/20 total (control) | 90/10 total (control) |
|---|---|---|---|
| 1.0 pt | ~51,000 | ~80,000 (~16,000) | ~142,000 (~14,000) |
| 1.5 pt | ~23,000 | ~36,000 (~7,200) | ~64,000 (~6,400) |
| 2.0 pt | ~13,000 | ~20,000 (~4,100) | ~36,000 (~3,600) |
| 3.0 pt | ~5,900 | ~9,200 (~1,800) | ~16,000 (~1,600) |

How to use it: divide the total by your monthly first-order volume to get
enrollment months. If that's longer than a quarter, either accept a larger MDE
or enlarge the control. Your kill threshold should never be smaller than your
MDE; you can't kill on a difference you can't detect.

## Kill condition

Stated exactly as in SKILL.md:

> If the treated group doesn't beat holdout on 60-day first→second purchase rate
> by at least 1.5 points absolute `[Assumption — set from your margin and
> baseline]` at the final read (enrollment end + 9 weeks), or any guardrail
> breaches its threshold for two consecutive weeks, we cut the cross-sell touch,
> keep review capture only if it isn't hurting return or unsubscribe rates, and
> go back to `retention-diagnosis` to test whether early-life is a message
> problem at all.

**What I'd try next if it triggers:**

1. Check the timing inputs first. If touch 4 was actually firing off ship date
   because the delivery event was missing, the thesis was never tested.
2. Run review capture alone as a smaller bet with a review-volume KPI. It may
   still pay for itself through conversion on product pages, but that's a
   different business case, owned outside this program.
3. Go back to `retention-diagnosis`. If second purchases don't respond to
   well-timed help and one relevant recommendation, the early-life leak may be
   product, price, or assortment, not messaging.

## Readout template

Fill in at the read date. Append the result to `.claude/decisions.md`.

| Field | Treated | Holdout | Difference | Label |
|---|---|---|---|---|
| Entrants | | | | `[Evidence]` |
| 60-day second-purchase rate | | | | `[Evidence]` |
| 95% confidence interval on the difference | — | — | | `[Evidence]` |
| Revenue per entrant, 60 days | | | | `[Evidence]` |
| Discount rate on second orders | | | | `[Evidence]` |
| First-order return rate | | | | `[Evidence]` |
| Unsubscribe rate, touches 3–6 | | n/a | | `[Evidence]` |
| Review submissions per 100 delivered orders | | | | `[Evidence]` |
| Guardrail breaches (count, which) | | | | `[Evidence]` |
| **Decision:** keep / cut cross-sell / kill and re-diagnose | | | | |
| Read date, enrollment window, what the control received | | | | `[Fact]` |

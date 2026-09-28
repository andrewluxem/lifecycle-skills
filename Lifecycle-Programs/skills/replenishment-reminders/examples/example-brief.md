# Example brief: Tidewell Coffee

Tidewell Coffee is an invented brand. Every number below is invented for this
walkthrough. The labels show how each number would be labeled if the brand were
real: `[Fact]` for what the team told me, `[Evidence]` for what I'd compute from
their data, `[Assumption]` for placeholders. None of it is a measured result.

## The brief

> "We sell whole-bean coffee online: 12oz bags and 2lb bags. People buy once and
> disappear. We want a reorder reminder at 14 days for every 12oz bag, since
> that's two weeks of coffee at a normal pace, with 15% off to get them back.
> Send it to everyone who bought, subscribers too, so nobody misses the deal."

Three things in there I'd push back on: timing to the label, a discount in every
reminder, and sending reminders to subscribers who already get coffee on a
schedule.

## Inputs

| Input | Value | Label |
|---|---|---|
| Catalog | Whole-bean coffee, 12oz and 2lb bags; ~90% of revenue is consumable | `[Fact]` |
| Label cycle, 12oz bag | 14 days ("two weeks of coffee") | `[Fact]` |
| Observed median repeat interval, 12oz x 1 bag | 23 days, from ~1,400 repeat pairs | `[Evidence]` |
| Observed median repeat interval, 12oz x 2 bags | 38 days (not 46: two-bag buyers drink more) | `[Evidence]` |
| Observed median repeat interval, 2lb x 1 bag | 44 days | `[Evidence]` |
| Delivery lead time | 3 days median | `[Fact]` |
| First-to-second-order rate within 60 days | 26% | `[Evidence]` |
| Baseline on-time repeat rate (last year, no reminders) | 29% | `[Evidence]` |
| New non-subscriber buyers of coffee per month | ~6,000 | `[Fact]` |
| Active subscribers | ~4,500 | `[Fact]` |
| Gross margin | 55% | `[Fact]` |
| Reorder link | None yet; reorder means rebuilding the cart by hand | `[Fact]` |
| SMS consent rate | 18% of buyers | `[Fact]` |

## Diagnosis check

Tidewell had run `retention-diagnosis` the previous month. The snapshot put the
dominant leak in early life: first-time buyers who never place a second order,
with the steepest drop between weeks 3 and 6 `[Evidence]`. That lines up with a
23-day median cycle: people run out, and the moment passes. A secondary mid-life
leak shows repeat buyers stretching intervals over time `[Inference]`, possibly
buying grocery-store coffee in between.

The catalog is consumable, the leak is early-life and mid-life, and a message
plausibly fixes a "forgot to reorder" problem. This program fits. If the
snapshot had pointed at activation (bad first bag, bad reviews), I'd have sent
them to fix the product experience first.

## Build spec

**Build item #1, before any message:** a signed prefilled-cart link that works
logged out. Without it, "one tap" is a lie and the program tests nothing.

**Cycle table (v1):** 12oz x1 = 23 days; 12oz x2 = 38 days; 2lb x1 = 44 days
`[Evidence]`. Single-origin limited SKUs with under 30 repeat pairs fall back to
the 12oz category cycle, labeled `[Assumption]`.

**Message architecture, 12oz x1 (C = 23 days):**

| # | Fires | Channel | Job | Proof | CTA | Anti-goal |
|---|---|---|---|---|---|---|
| 1 | Day 17 (75% of C; delivery lead time is 3 days, under the threshold) | Email | "I'm nearly out, and reordering takes one tap" | Last bag, roast, order date, estimated run-out date, arrives-by date | Prefilled cart; "not yet" snooze | No 15% off. No "try our new roasts" block |
| 2 | Day 22 (~95% of C) | SMS if consented (18%), else email | "Order today, no morning without coffee" (as a job, not a line) | Arrives-by date vs. run-out date | Same reorder link | No same-day SMS + email; no countdown timer |
| 3 | Day 28 (~120% of C) | Email | "Reorder, or tell us you're set" | Order history | Reorder; "switched to 2lb" and snooze controls | No incentive escalation |
| G | Replaces touch 1 after the 2nd on-time reorder | Email | "A subscription at my pace" | Their streak; their observed cadence (e.g. every 3 weeks); skip/pause/cancel terms | Prefilled subscription at their cadence | Not the label's 14 days |

Day 46 (2x C) with no reorder: exit to `winback-series` eligibility.

**Splits:** holdout 10% customer-level, sticky; graduation at 2 on-time reorders
(3 tested later); touch 2 channel by SMS consent; multi-SKU consolidation for
customers who bought two different roasts.

**Exits:** reorder of any 12oz or 2lb of the same roast, or a mapped substitute
roast; subscription start; refund; unsubscribe; 2x C.

**Filters:** active subscribers never enter. That alone removes ~4,500 people
from the team's original send list `[Fact]`. Gift orders excluded.

**Primitives:** trigger = daily entry from the episode table on `reminder_date`;
filter = consent, not subscriber, not gift, not holdout; split = holdout,
graduation, SMS consent; wait = until day 22, until day 28; exit = reorder,
subscription start, refund, 2x C.

## Measurement plan

- **Primary KPI:** on-time repeat rate: reorder by day 29 (depletion + 25% of C)
  for 12oz x1; per-bucket windows for the others. Baseline 29% `[Evidence]`.
- **Holdout:** 10%, customer-level, assigned at first entry, sticky. Needs about
  2,100 holdout customers for a 3-point lift `[Inference]`, about 20,900 entrants
  in total. At ~6,000 new buyers a month `[Fact]`, entry closes in roughly 3.5
  months. Entry opens 2026-10-05 and closes 2027-01-18 `[Assumption: dates for
  illustration]`.
- **Read date:** two median cycles of the top SKU (12oz x1) after entry closes,
  so 46 days after 2027-01-18: 2027-03-05. The 12-weeks-after-launch floor
  (2026-12-28) is earlier, so it doesn't bind. 46 days also covers the last
  cohort's 29-day window and the 2x C lapse guardrail.
- **Kill condition:** if on 2027-03-05 treated on-time repeat rate doesn't beat
  holdout by 3 points with the 90% interval excluding zero, and orders per
  customer over two cycles isn't higher in treated, we cut touches 2 and 3, keep
  touch 1 only if it's net-positive on orders, and go back to
  `retention-diagnosis` to look at grocery-store and marketplace switching.
- **Guardrails:** unsubscribe per send, SMS opt-out, 2x C repeat rate, discount
  spend per reorder (should be zero).

## What we deliberately didn't do

- **No 15% off in reminders.** At 55% margin `[Fact]`, a 15% discount on every
  reorder gives away about a quarter of the gross profit on that order
  `[Inference]`, including on the ~29% who'd reorder anyway
  `[Evidence]`. If the team insists on testing an incentive, it goes on touch 3
  only, with its own holdout, after the first read.
- **No cross-sell of new roasts in the reminder.** That's `post-purchase` and
  campaigns; it competes with the one job.
- **No chase past day 46.** Those customers left; `winback-series` owns them.
- **No copy.** The jobs above are frameworks. The words belong to
  `lifecycle-messaging` and Tidewell's writers.
- **No change to the subscription program itself.** Graduation hands off to it;
  `journey-architecture` owns how the two programs share a customer.

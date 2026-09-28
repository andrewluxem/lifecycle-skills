# Benchmarks: Replenishment Reminders

Every number in this file is `[Assumption]`. None of it is cited and none of it
is a measured result. These are starting points for a test, never targets. The
whole point of this program is that your own inter-purchase data replaces the
defaults within one cycle.

## Cycle estimation defaults

The cycle drives every timing below, so get it right first.

| Input | Default | Why | Label |
|---|---|---|---|
| Cycle statistic | Median interval between consecutive purchases of the same SKU by the same customer | Means get dragged out by lapsed-then-returned customers | `[Assumption]` |
| Lookback | 12 months, or 3x the longest cycle you care about | Enough repeat pairs without mixing in old pack sizes | `[Assumption]` |
| Minimum repeat pairs per SKU x quantity bucket | 30 | Below this the median wobbles by days | `[Assumption]` |
| Fallback order | SKU x qty bucket → SKU → category → label | Each step is less specific; label it so | `[Assumption]` |
| Quantity buckets | 1, 2, 3+ units | Multi-unit orders rarely last exactly N times longer; don't assume linear | `[Assumption]` |
| Outlier trim | Drop intervals under 20% or over 300% of the SKU median before the final median | Duplicate orders and long lapses aren't usage | `[Assumption]` |
| Personal cycle | Switch to the customer's own median after 2+ reorders of the SKU | Households differ more than SKUs do | `[Assumption]` |
| Exclusions | Gift orders, subscription orders, B2B/wholesale accounts, orders later refunded | They don't reflect one household's usage | `[Assumption]` |

A useful sanity check: compare the observed median to the label. If observed is
shorter than the label, suspect shared use or multi-buyers in the bucket. If it's
much longer (1.5x+), customers are rationing, skipping days, or topping up
elsewhere. Both are worth knowing before you set a single wait.

## Timing defaults

C = expected cycle for this customer, SKU, and quantity.

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| 1 — Reminder | 75% of C, minus delivery lead time beyond 3 days | 65–85% of C | `[Assumption]` |
| 2 — Pre-run-out nudge | 95% of C | 90–100% of C | `[Assumption]` |
| 3 — Check-in | 120% of C | 110–135% of C | `[Assumption]` |
| Hand-off to `winback-series` | 200% of C | 175–250% of C | `[Assumption]` |
| G — Graduation | Replaces touch 1 after the 2nd on-time reorder | 2nd vs. 3rd on-time reorder | `[Assumption]` |
| Consolidation window | SKUs due within 7 days share one reminder | 5–10 days | `[Assumption]` |
| Send hour | The customer's historical order hour, else late morning local | Order hour vs. fixed hour | `[Assumption]` |

For short cycles (under ~14 days) the gaps between touches get cramped. Drop
touch 3 and let the grace window do its job. For long cycles (90+ days), the
reminder arrives long after the customer last thought about you, so the
last-order block matters more than anything else in the email.

## Split defaults

- **Holdout:** 10% of customers, sticky across cycles and SKUs `[Assumption]`.
  Drop to 5% only if volume forces it, and accept a longer read.
- **Timing test (touch 1 at 70% vs. 80%):** 50/50 within the treated group,
  after the holdout read is in. Don't stack a timing test on top of the first
  holdout read; you'll muddy both.
- **Minimum audience per cell:** roughly 2,000 customers per cell for a
  3-point difference on a 30% baseline `[Assumption]`. Math in
  `measurement.md`. If a cell can't get there in a quarter, don't run the split.

## Content defaults

What each touch typically carries, and the tests worth running first, ranked by
expected value.

| Touch | Carries | First test | Why this one first |
|---|---|---|---|
| 1 | Last-order block, run-out date, delivery-by strip, one-tap reorder, snooze | Timing (70% vs. 80% of C) | Timing is the biggest lever; content is second |
| 2 | Delivery-by date, reorder link | SMS vs. push for consented customers | Channel matters more than words in a nudge |
| 3 | Order history, reorder, "I'm set / switched size" controls | Keep vs. drop the touch entirely | It may be doing nothing; the holdout arm by touch tells you |
| G | Streak, observed cadence, terms, prefilled subscription link | Graduate at 2 vs. 3 on-time reorders | Too early annoys, too late misses the habit |

Incentive tests go last, if ever. If you test one, do it on touch 3 only, capped
by margin, with its own holdout.

## How to replace these numbers

1. **Observed cycle per SKU x quantity bucket.** Pair each order line with the
   same customer's next order line for that SKU; take the interval in days;
   trim outliers; take the median by SKU and quantity bucket; count pairs.
2. **Baseline on-time repeat rate.** For last year's first purchases of each SKU,
   the share with a reorder by depletion + 25% of C. This is your holdout's
   expected rate and the input to the sample-size math.
3. **Delivery lead time.** Median days from order to delivery by region, from
   your shipping data.
4. **Lapse point.** The interval beyond which fewer than ~10% of customers ever
   reorder `[Assumption]`. That's your real winback hand-off, replacing the 2x C
   default.

After one full cycle with the holdout, rerun steps 1 and 2 and overwrite this
table with your own numbers, labeled `[Evidence]`.

# Benchmarks: Winback Series

Starting points for a test, never targets and never results. Every number in
this file is `[Assumption]`: none of it is cited, and none of it is anyone's
measured outcome. The goal is to replace each one with your own data after one
cycle, and the last section says how.

Timing is expressed in the brand's own cycle: **M** is the median
inter-purchase interval for repeat buyers, **L** is the lapse line (P80 of that
interval), **G** is the gone line.

## Band defaults

| Band boundary | Default | Range worth testing | Label |
|---|---|---|---|
| At-risk starts | 1.25×M | 1.1×M to 1.5×M | `[Assumption]` |
| Lapse line (L) | P80 of repeat-buyer interval | P75 to P90 | `[Assumption]` |
| Deep-lapsed starts | 2L | 1.75L to 2.5L | `[Assumption]` |
| Gone line (G) | 3L | Where untreated return rate flattens in your data | `[Assumption]` |

For very long cycles (durables, M over 12 months), percentile lines get noisy
and the at-risk band may be meaningless. Use replenishment or warranty dates if
you have them, and expect the program to be mostly touch 2, 3, and 6.

## Timing defaults

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| 1 At-risk nudge | 1.25×M | 1.1×M to 1.5×M | `[Assumption]` |
| 2 Recognition | L | L to L + 3 days | `[Assumption]` |
| 3 Reason to return | L + 0.25×M | L + 0.15×M to L + 0.4×M | `[Assumption]` |
| 4 First offer (gated) | L + 0.5×M | L + 0.35×M to L + 0.75×M | `[Assumption]` |
| 5 Escalation (High tier) | Touch 4 + 7 days | 5 to 14 days | `[Assumption]` |
| 6 Stay or go | 2L | 1.75L to 2.5L | `[Assumption]` |

Floor every gap at 3 days and cap at 30 days `[Assumption]`, so a 12-day
consumable doesn't get daily email and a 2-year durable doesn't wait a season
between touches.

## Split defaults

- **Holdout:** 10% of entrants, sticky by customer ID `[Assumption]`. Go to 20%
  if monthly entrants are under ~15,000 and you want a read inside a quarter.
- **Offer vs. no-offer test (High tier):** 50/50 within the treated High tier,
  only when each arm will reach the sample size in `measurement.md`.
- **Minimum cell size before a split is worth running:** enough entrants to
  detect the lift you'd act on. Below that, don't split; ship the default path.

## Incentive ladder defaults

| Step | Typical form | When it's allowed | Label |
|---|---|---|---|
| 0 | No incentive | Always the default | `[Assumption]` |
| 1 | Modest percent or fixed amount, single-use, 7–10 day expiry | Tier break-even positive at this cost | `[Assumption]` |
| 2 | Larger step, or a non-price form (shipping, gift) | High tier only, break-even positive at this cost | `[Assumption]` |
| Cap | No step 3 | Always | `[Assumption]` |

Non-price forms often cost less per redemption than the same headline percent.
Test them before raising the percent.

## Illustrative return-rate inputs (not results)

Use these only to size a holdout before you have your own. They are placeholders
for the break-even and sample-size math.

| Input | Placeholder | Label |
|---|---|---|
| Untreated return within window, Standard tier | 2–4% | `[Assumption]` |
| Untreated return within window, High tier | 6–10% | `[Assumption]` |
| Incremental lift from no-incentive touches | 0.5–1.5 points | `[Assumption]` |
| Additional lift from a step-1 offer | 1–4 points | `[Assumption]` |
| Follow-on orders per reactivator in the next L days | 0.2–0.6 | `[Assumption]` |

## Content defaults

What each touch typically carries, and the tests worth running first, ranked
by expected value:

1. **Offer vs. no offer in the High tier.** The single biggest money question.
   Run it before any creative test.
2. **Offer form at step 1:** percent vs. non-price. Same expected cost, often
   different margin.
3. **Touch 1 on vs. off** for the at-risk band. If it doesn't move the lapse
   rate, it's frequency cost.
4. **Personalized category block vs. brand-level block** in touches 2 and 3.
5. Subject-line and layout tests last. They move opens, rarely margin.

## How to replace these numbers

- **M and L:** for each customer with 2+ orders, compute days between
  consecutive orders; take the median and P80 across all gaps in the last 24
  months.
- **G:** for customers who went past L with no winback, plot the share who
  ordered again by days since last order. G is where that curve flattens.
- **Untreated return rates:** the holdout gives you these directly after one
  window. Until then, use the historical curve above for customers who received
  no winback.
- **Follow-on orders:** from past reactivators, count orders in the L days
  after the reactivation order, split by whether the reactivation order used a
  code.
- **Incentive cost per redeemed order:** average discount dollars per
  code-redeemed order, plus any shipping or gift cost.

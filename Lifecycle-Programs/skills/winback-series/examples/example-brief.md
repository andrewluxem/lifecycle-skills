# Example brief: Tallgrass Pantry

Tallgrass Pantry is an invented DTC spice and pantry brand. Every number below
is invented for this walkthrough and labeled as if the team had supplied it or
we had computed it in session. No employer or client data.

## The brief

> "Our repeat rate is sliding and we've got a big dormant list. Build a winback:
> everyone who hasn't bought in 90 days gets 25% off, then a reminder, then 30%
> off if they still haven't come back. We want it live before the holidays."

What they get right: they want it shipped, and they're looking at the file
they already own. What they get wrong:

- **90 days is someone else's number.** Their own reorder cycle is much
  shorter, so 90 days is already a month past their lapse line.
- **Everyone gets the code.** That pays the discount to people who would have
  reordered at full price.
- **The escalation is automatic.** 30% for everyone who ignored 25% is the
  fastest way to teach a file to wait.
- **No holdout.** The ESP's revenue report would call it a win no matter what.

## Inputs

| Input | Value | Label |
|---|---|---|
| Median inter-purchase interval (M), repeat buyers, last 24 months | 38 days | `[Evidence]` |
| Lapse line (L), P80 of that interval | 64 days | `[Evidence]` |
| Gone line (G), where untreated return flattens | ~190 days | `[Evidence]` |
| New entrants crossing L per month | ~9,000 | `[Evidence]` |
| Lapsed pool (L to 2L) at launch, for backfill | ~31,000 | `[Evidence]` |
| One-time buyers as share of entrants | 41% | `[Evidence]` |
| High tier share of entrants (top 30% trailing 12-month margin) | 30% | `[Evidence]` |
| AOV / gross margin rate, High tier | $46 / 55% → $25.30 margin per order | `[Fact]` |
| AOV / gross margin rate, Standard tier | $34 / 55% → $18.70 margin per order | `[Fact]` |
| Step-1 offer | 20% off, single-use, 10-day expiry | `[Assumption]` |
| Untreated return in window, High / Standard | 8% / 3% | `[Assumption]` |
| Return with step-1 offer, High / Standard | 12% / 4% | `[Assumption]` |
| Follow-on orders per reactivator in window, High / Standard | 0.5 / 0.3 | `[Assumption]` |

## Diagnosis check

Tallgrass had a `.claude/retention-snapshot.md` from `retention-diagnosis`. It
places the dominant leak in resurrection among customers with two or more
orders: they reorder on a steady cycle, then stop `[Fact]` (from the snapshot).
The early-life tell passes, barely: one-time buyers are 41% of entrants
`[Evidence]`, a minority but a big one. I flagged it in `.claude/decisions.md`
as the next bet to size, and one-time buyers get the no-offer path here.

If the snapshot hadn't existed, I'd have routed to `retention-diagnosis` and
stopped.

## Build spec

**Bands and timing** (M = 38, L = 64):

| # | Touch | Fires at (days since last order) | Who |
|---|---|---|---|
| 1 | At-risk nudge | Day 48 (1.25×M) | All at-risk, not holdout |
| 2 | Recognition | Day 64 (L) | All entrants, not holdout |
| 3 | Reason to return | Day 74 (L + 0.25×M) | All entrants, not holdout |
| 4 | First offer, 20% | Day 83 (L + 0.5×M) | High tier, offer arm, eligible only |
| 5 | Escalation | Day 90 (touch 4 + 7) | High tier, offer arm, and only if step-2 break-even holds |
| 6 | Stay or go | Day 128 (2L) | Everyone still in |
| — | Exit to sunset policy | Day ~190 (G) or no response to 6 | — |

Their "90 days" would have fired the first email on day 90, after most of the
recoverable window had already closed.

**The incentive decision, by tier** (net margin per entrant, from the
break-even formula in `SKILL.md`):

```
High:     0.04 × ($25.30 + 0.5 × $25.30) − 0.12 × $9.20
        = $1.52 − $1.10 ≈ +$0.41 per entrant       → offer allowed
Standard: 0.01 × ($18.70 + 0.3 × $18.70) − 0.04 × $6.80
        = $0.24 − $0.27 ≈ −$0.03 per entrant       → no offer
```

Both results are `[Inference]` from `[Assumption]` lift inputs. The point isn't
the exact cents: the Standard tier loses money because the code is paid to
the 3% who were coming back anyway, and the extra point of lift doesn't cover
it. Step 2 (their 30%, $13.80 per redemption) at an assumed 14% return nets
about +$0.35 per High entrant `[Inference]`, less than step 1's +$0.41, so
escalating loses money relative to stopping at 20%. Touch 5 ships as a
non-price form (free shipping) or not at all. I'd rather ship it off.

**Splits:**

- 10% holdout at entry, sticky by customer ID.
- Value tier: High vs. Standard.
- High tier treated: 50/50 offer vs. no-offer arm. The backfill gives ~8,400
  treated High entrants `[Inference]`; at 8% vs. 12% each arm needs ~880
  `[Inference]`, so the test is affordable.
- One-time buyers: touches 2, 3, 6 only.
- Offer eligibility filter excludes anyone who reactivated on a code in the
  last 12 months without a later full-price order.

**Exits:** purchase (site plus their marketplace storefront, which syncs
nightly, so offer touches re-check after the sync); unsubscribe, complaint,
hard bounce; day ~190 or no response to touch 6 → sunset policy; cart abandon
pauses the series.

**Primitives:** scheduled daily entry on days since last order = 64; filters
on consent, suppression, tier, eligibility; random splits for holdout and offer
arm; waits of 10, 9, 7, and 38 days with wait-until-purchase on each; exits as
above.

**Backfill:** the ~31,000 already-lapsed customers enter over 7 days, and
anyone past 2L goes straight to touch 6 or the sunset review, not touch 2.

## Measurement plan

- **Primary KPI:** incremental net reactivated margin per entrant, window 64
  days (L) from entry.
- **Guardrail:** full-price follow-on orders per entrant, treated vs. holdout.
- **Holdout:** 10% of entrants. Backfill alone puts ~3,100 in holdout
  `[Inference]`, above the ~2,620 needed for a 3% vs. 4% read.
- **Launch:** 2026-10-05 (illustrative). **Read date:** 2026-12-15, one
  window (64 days) after the last backfill entrant lands. **Hard deadline:** 2027-01-25, 16
  weeks after launch. Backfill entrants are read separately from steady-state
  entrants, because they were lapsed longer on average.
- **Kill condition:** if net margin per entrant is at or below $0 vs. holdout,
  or full-price follow-on orders per entrant are lower in treated, touches 4
  and 5 go off and the no-incentive series runs one more window. If that fails
  to beat holdout on reactivation rate, the program stops, the pool goes to the
  sunset policy, and we go back to `retention-diagnosis`.

## What we deliberately didn't do

- **No offer for Standard or one-time buyers.** The math says it costs more
  than it returns. `segmentation-model` owns whether the tier cut is right.
- **No automatic 30%.** Escalation is earned per tier, not a timer.
- **No fix for the one-time-buyer share.** That's an early-life question for
  `retention-diagnosis` to size, and likely a second-purchase program, not this
  one.
- **No copy.** Subject lines and bodies go to `lifecycle-messaging` with the
  touch framework above.
- **No suppression decisions.** Tallgrass's deliverability owner decides what
  happens past G. There's no sunset skill in this plugin yet.

# Example brief: Fernhollow Coffee Co.

Fernhollow is invented. Every number is `[Assumption]` (a fictional input) or
`[Inference]` (arithmetic on those inputs). Nothing here is employer or client
data.

## The brief

"We sell whole-bean coffee and pods direct. Customers buy once or twice and then
drift. We want a loyalty program: three tiers (Bronze, Silver, Gold), 10% back
in points, and a big launch email. Finance is nervous about cost, but about half
of points never get redeemed in programs like this, so the real cost is 5%.
Can you build the emails?"

What they get wrong: they're funding the program on breakage, they picked tiers
for a high-frequency, low-AOV category, and they asked for the launch email
before anyone did the math.

## Inputs

| Input | Value | Label |
|---|---|---|
| AOV | $32 | `[Assumption]` |
| Gross margin | 55% | `[Assumption]` |
| Median days between orders | 35 | `[Assumption]` |
| Third-purchase rate within 90 days of order 2 | 38% | `[Assumption]` |
| Customers placing a 2nd order per month | ~3,000 | `[Assumption]` |
| Proposed earn/burn | 10% back | `[Assumption]` |
| Proposed breakage | 50% | `[Assumption]` |
| Ledger | Loyalty platform, emits events to the ESP | `[Assumption]` |
| App | None; email and SMS only | `[Assumption]` |

## Diagnosis check

`.claude/retention-snapshot.md` exists from a prior `retention-diagnosis` run and
names the dominant leak as early-life: customers who place a second order often
don't place a third. That's a leak loyalty can plausibly treat, so I proceed. If
the snapshot had been missing, I'd have stopped and routed there first.

## Economics first

**Their proposal:** 10% face reward rate.

- Full redemption: break-even lift = 0.10 ÷ (0.55 − 0.10) = **22.2%** `[Inference]`.
- At their 50% breakage: 0.05 ÷ (0.55 − 0.05) = **10.0%** `[Inference]`.

The whole gap between 10% and 22% is breakage. That's the plan depending on
half the members forgetting. I won't design comms on top of it.

**My recommendation:** 1 point per $1, 100 points = $5 off, so 5% face.

- Full redemption: 0.05 ÷ (0.55 − 0.05) = **10.0%** `[Inference]`.
- At 70% redemption: 0.035 ÷ (0.55 − 0.035) = **6.8%** `[Inference]`.

Honestly, 10% incremental member spend at full redemption is still a real bar
for a coffee brand. I think it's a bet worth making, because the accelerator
read will tell us within a quarter whether the mechanic moves behavior at all.
If it doesn't, we stop before the base program becomes a permanent 5% subsidy.

**Accelerator:** 2× points on order 3 if placed within 28 days of order 2
(0.8 × 35). Extra face per accelerated order $1.60, about $1.12 expected at 70%
redemption `[Inference]`.

**Liability:** flagged to Fernhollow's finance lead with a rough sizing. How
it's booked is theirs to decide. I don't advise on it.

**Tiers vs. points:** points. Orders every ~5 weeks at $32 is a frequency
business. Nobody's identity is tied to their coffee tier. Tiers can come later
if the base mechanic proves out.

## Build spec

**Touches shipped in v1 (week 1):** 1, 2, 3, 9. Touches 4, 5, 10 follow in
week 3. Tier touches 6, 7, 8 are cut.

| # | Timing | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|
| 1 Enrollment | Folded into order confirmation for checkout joiners; immediate otherwise | Email | Knows the earn rule and distance to first $5 | Live balance | View account | No second-order push |
| 2 First earn | On `points_posted` after shipment | Email | Points are real | Posted balance | See progress | No pending points shown |
| 3 Accelerator | Day 3 after order 2; window ends day 28 | Email; SMS reminder day 21 with consent | Order 3 earns double | Their accelerated total on a typical order | Shop their last roast | No discount; not to holdout; not same day as replenishment reminder |
| 9 Expiry | 30 and 7 days before; balance ≥ 100 points | Email | Points expire on a date | Balance, date, $ value | Redeem | Never on < 100 points |

**Primitives:**

- **Trigger:** `order_placed` with order count = 2.
- **Filter:** enrolled, email consent, not in winback, `accelerator_bucket` =
  treated.
- **Split:** holdout on upstream `accelerator_bucket` (30% holdout).
- **Wait:** 3 days, then wait-until `order_placed` or day 28.
- **Exit:** `order_placed` (accelerator earned), lapse at 70 days to
  `winback-series`, unenroll.

**Suppression:** touch 3 holds on days `replenishment-reminders` fires. Cross-
program caps come from `journey-architecture`.

## Measurement plan

- **Primary KPI:** net spend per member after reward cost, treated vs. holdout,
  180 days from order 2.
- **Powered metric:** third-purchase rate within 90 days. Baseline 38%, MDE +4
  points: 7.84 × (0.2356 + 0.2436) ÷ 0.0016 ≈ **2,350 per arm** `[Inference]`.
- **Holdout:** 30%, randomized per member at order 2 in the loyalty platform.
  2,350 ÷ 0.30 ≈ 7,830 eligible, about 2.6 months at 3,000/month
  `[Inference]`.
- **Dates (invented):** accelerator launches Monday 2026-11-02; both arms reach
  sample size around 2027-01-18; third-purchase interim read 2027-04-18;
  26-week spend read and kill decision Monday 2027-07-19.
- **Kill condition:** if on 2027-07-19 treated doesn't beat holdout on net spend
  per member after reward cost with the 90% CI lower bound above $0, the
  accelerator goes off, base earn stays, and the next bet goes back to
  `retention-diagnosis`. If observed redemption runs above 70% for two straight
  quarters and the P&L only clears on breakage, we redesign the earn rate with
  finance before any new creative.

## What we deliberately didn't do

- **No tiers.** Wrong category for status. Revisit after the accelerator read.
- **No 10% back.** It only worked on breakage.
- **No launch blast to the whole file.** Enrollment happens at checkout and via
  `post-purchase`; acquisition isn't this program's job.
- **No winback in points.** Lapsed members go to `winback-series`.
- **No copy.** The touch specs go to `lifecycle-messaging`.
- **No accounting guidance.** Liability sizing went to finance as a flag.

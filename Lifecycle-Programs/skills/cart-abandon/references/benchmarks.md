# Benchmarks: Cart Abandon

Every number here is `[Assumption]`. None of it is cited, and none of it is a
measured result. These are starting points for a test, never targets. The goal
is for this file to be replaced by your own numbers after one cycle.

## Timing defaults

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| Abandon threshold | 30 min of inactivity after last cart update | 15–60 min | `[Assumption]` |
| 1 (email) | 45 min after abandon | 20–90 min | `[Assumption]` |
| 2 (SMS, consented only) | 4 h after abandon, inside 9 a.m.–8 p.m. local | 2–8 h | `[Assumption]` |
| 3 (email) | 24 h after abandon | 18–36 h | `[Assumption]` |
| 4 (email, incentive-eligible only) | 60 h after abandon | 48–96 h | `[Assumption]` |
| Re-entry lockout | 14 days | 7–30 days | `[Assumption]` |

Why touch 1 is the one to get right: most of a cart program's recoveries tend to
land on the first touch `[Assumption]`. If you only test one thing, test the
delay on touch 1.

Quiet hours are not a benchmark. They're a legal and consent question. Use the
window your counsel and SMS provider set; 9 a.m.–8 p.m. recipient-local is a
conservative placeholder `[Assumption]`.

## Rate placeholders for planning

| Metric | Placeholder | Label |
|---|---|---|
| Holdout (no-program) recovery within 7 days | 5–12% of entrants | `[Assumption]` |
| Treated recovery within 7 days, no incentive | holdout + 1–4 points | `[Assumption]` |
| Share of recoveries on touch 1 | 40–60% | `[Assumption]` |
| Unsubscribe rate per cart email | 0.1–0.4% | `[Assumption]` |
| SMS opt-out rate per cart SMS | 0.5–2% | `[Assumption]` |
| Habitual abandoners (3+ abandons / 90 days) | 10–25% of entrants | `[Assumption]` |

The one I'd distrust most is the holdout recovery rate. It varies wildly by
category and price point, and it is the number that decides whether the program
is worth anything. Measure it yourself.

## Split defaults

- **Holdout:** 20% for the first read (faster), dropping to 10% once the
  program is proven and you want the ongoing guard. `[Assumption]`
- **Incentive test:** 50/50 inside the eligible branch. `[Assumption]`
- **Minimum per cell:** don't run a content A/B inside the program until each
  cell sees roughly 2,000 entrants per read window. Below that you're reading
  noise. `[Assumption]`
- **Don't split touch 1 timing and touch 1 content at once.** One variable at a
  time.

## Content defaults

What each touch typically carries, and the variants worth testing, ranked by
expected value:

1. **Touch 1 delay** (e.g. 30 vs. 60 min). Highest expected value; costs
   nothing.
2. **Incentive vs. no incentive at touch 4.** Already built in as Split C.
3. **Incentive form** for the eligible branch: free shipping vs. percent off vs.
   fixed amount. Free shipping often costs less margin for the same objection
   `[Inference]`. Test only after Split C shows the incentive is incremental.
4. **Touch 3 proof element:** returns/shipping strip vs. reviews. Match to the
   objection your support tickets and exit surveys name.
5. **Touch 2 SMS on vs. off** for consented shoppers. SMS costs money per send
   and burns consent; it has to beat email-only.

Subject-line tests are last. They move opens, and opens aren't the KPI.

## How to replace these numbers

- **Holdout recovery rate:** after 4 weeks, recovered orders in the holdout ÷
  holdout entrants, 7-day window. This replaces the most important placeholder.
- **Timing:** distribution of time from abandon to organic purchase in the
  holdout. If most organic returns happen inside 2 hours, touch 1 is competing
  with them, not rescuing them.
- **Habitual share:** count of entrants with 3+ abandon events in the prior 90
  days ÷ entrants.
- **Discount-seeker share:** customers whose last 3 orders all used a code ÷
  customers with 3+ orders.
- **Recovery by touch:** last-touch before purchase, treated arm only, for
  diagnosis, never for lift.

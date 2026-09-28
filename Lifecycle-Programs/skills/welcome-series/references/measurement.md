# Measurement: Welcome Series

The primary KPI, guardrails, holdout recipe, and kill condition also appear in
`SKILL.md`. This file carries the detail.

## Primary KPI

**Revenue per new subscriber, 30-day window.**

```
RPS_30 = total order revenue from entrants, in the 30 days after each one's entry
         ÷ number of entrants (buyers and non-buyers)
```

Computed separately for treated and holdout. Lift is `RPS_30(treated) −
RPS_30(holdout)`, and relative lift is that difference divided by holdout.

Why this and not opens, clicks, or flow-attributed revenue:

- Opens and clicks measure attention, not money. A welcome can win on clicks and
  lose on revenue if the offer pulls forward orders that would have come anyway.
- Flow-attributed revenue credits the program for every buyer who opened an
  email, including the ones who signed up mid-checkout. It is always higher than
  the true lift, and it can't tell you when the program is doing nothing.
- Revenue per subscriber, not conversion rate, because the offer changes order
  value. A program that converts more people at a steep discount can lose money.
- 30 days, not 14, because welcome hands buyers to `post-purchase`, and a second
  order inside the window is part of what welcome is for. The chain gets the
  credit together; the holdout doesn't care which program sent the last email.

Secondary, for diagnosis only: 30-day first-purchase rate, average first-order
value, and offer redemption rate on touch 4.

## Guardrails

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Unsubscribe rate per send | Under 0.5% `[Assumption]` | Check the touch and its timing; pause that touch if it persists two sends |
| Spam complaint rate per send | Under 0.1% `[Assumption]`; check your mailbox providers' current published ceilings | Pause the program and check consent source and touch-1 relevance |
| Discount cost per treated subscriber | Below the incremental gross margin per subscriber | Cut offer size or switch type before anything else |
| Full-price first-purchase rate, treated vs. holdout | Treated not lower than holdout | The offer is cannibalizing; move it later or shrink it |
| Purchasers receiving touch 4 or 5 | Zero | Stop the program until the exit is fixed |
| 60-day second-purchase rate, welcome buyers vs. holdout buyers | Not lower | Lagging check; hand to `post-purchase` and `retention-metrics` |

Discount break-even, with invented inputs:

```
AOV                               $60     [Assumption]
Gross margin                      55%     [Assumption]
Offer                             15% off [Assumption]
Discount per redeemed order       $9.00
Margin per full-price order       $33.00
Margin per discounted order       $24.00
```

Every redeemed order from someone who would have bought anyway costs $9 of
margin. Every redeemed order from someone who wouldn't have costs nothing and
earns $24. The offer pays only if the incremental orders' margin covers the
subsidy on the non-incremental ones. You can only see that split with a
holdout.

## Attribution

- **Window:** 30 days from entry, per subscriber.
- **What counts:** every order by the entrant in the window, any channel you can
  match, whether or not they opened anything.
- **What overrides what:** the holdout comparison overrides last-touch, first-
  touch, and flow-attributed revenue every time. Flow reports are fine for
  debugging which touch people click. They are not evidence of lift.
- **Shared credit with `post-purchase`:** welcome's lift includes second orders
  inside 30 days. Don't also count them as `post-purchase` lift in the same
  readout. `retention-metrics` owns the rule across programs.

## Holdout recipe

- **Size:** 10% of entrants by default. 20% for the first read when volume is
  thin. Permanent 5% after two proven reads `[Assumption]`.
- **Randomization unit:** the subscriber (profile or customer ID), not the send.
- **Assignment point:** at entry, once. Never re-randomized per message.
- **What the control receives:** nothing from this program. They still get
  transactional mail and BAU campaigns under the same frequency caps as anyone
  who isn't in welcome. That's the honest counterfactual: "no welcome," not "no
  email."
- **Duration:** enroll continuously. The decision read at week 6 uses the
  cohort that entered in the first 12 days, since each of them has a complete
  30-day window by day 42.

**Sample-size reasoning.** Revenue per subscriber is mostly zeros with a long
right tail, which makes it noisy. I power on 30-day first-purchase rate, the
biggest driver of the revenue difference, and treat the answer as a floor.

| Input | Value | Label |
|---|---|---|
| Baseline 30-day purchase rate (holdout) | 3.0% | `[Assumption]` |
| Target purchase rate (treated) | 4.5% | `[Assumption]` |
| Minimum detectable effect | +1.5 points (50% relative) | `[Assumption]` |
| Significance | 5%, two-sided | `[Assumption]` |
| Power | 80% | `[Assumption]` |
| Allocation | 90/10 or 80/20 treated/holdout | `[Assumption]` |

Two-proportion formula with unequal arms, holdout size `h`, treated size `r·h`:

```
h = (z_α/2 + z_β)² × [ p_c(1−p_c) + p_t(1−p_t)/r ] ÷ (p_t − p_c)²
  = 7.85 × [ 0.0291 + 0.0430/r ] ÷ 0.000225
```

| Allocation | Holdout needed | Total entrants | Label |
|---|---|---|---|
| 50/50 | ~2,500 | ~5,000 | `[Inference]` from the inputs above |
| 80/20 | ~1,390 | ~6,950 | `[Inference]` |
| 90/10 | ~1,180 | ~11,800 | `[Inference]` |

What this means:

- The read cohort (12 days of entrants) must reach the total for your
  allocation. If it can't at 80/20, the 6-week read isn't possible. I say that
  up front and set a later, honest read date rather than calling noise a result.
- A smaller real lift needs far more. Halving the detectable effect roughly
  quadruples the sample.
- For the revenue read itself, compare per-subscriber revenue including zeros
  with a Welch t-test or a bootstrap, and winsorize the top 1% of order values
  `[Assumption]` so one bulk order doesn't decide the test. Report the
  confidence interval, not just the point estimate.

## Kill condition

As stated in `SKILL.md`: if, at the week-6 read, treated revenue per new
subscriber doesn't beat holdout with a lift whose confidence interval excludes
zero, we stop and redesign the offer touch first: size, fence, timing, then
expiry. One redesign, one more 6-week read. If that fails too, the problem is
upstream of the offer, and it goes back to `retention-diagnosis`.

What I'd try, in order, if it triggers:

1. **Offer type.** Swap percent-off for free shipping or a fixed amount. Often a
   different cost at similar perceived value `[Assumption]`.
2. **Offer timing.** Move from day 7 to day 5 or day 9 based on when holdout
   buyers naturally buy.
3. **Fence.** Confirm the offer isn't leaking to purchasers or cart-abandon
   holders. A leaky fence can erase a real lift.
4. **Expiry.** Shorter and real, or longer if the category has a long consider
   cycle.

Also stop early, before week 6, if a guardrail breaks hard: purchasers receiving
the offer, complaints above threshold, or discount cost clearly above
incremental margin.

## Readout template

Fill this in at the read date. Label every number.

| Metric | Treated | Holdout | Difference | 95% CI | Label |
|---|---|---|---|---|---|
| Entrants in read cohort | | | | n/a | `[Evidence]` |
| RPS_30 (primary) | | | | | `[Evidence]` |
| 30-day first-purchase rate | | | | | `[Evidence]` |
| Average first-order value | | | | | `[Evidence]` |
| Full-price first-purchase rate | | | | | `[Evidence]` |
| Offer redemption rate (touch 4) | | n/a | n/a | n/a | `[Evidence]` |
| Discount cost per subscriber | | n/a | n/a | n/a | `[Evidence]` |
| Unsubscribe rate per send | | n/a | n/a | n/a | `[Evidence]` |
| Complaint rate per send | | n/a | n/a | n/a | `[Evidence]` |
| Purchasers who received touch 4/5 | | n/a | n/a | n/a | `[Evidence]` |

Decision (one line): keep, redesign the offer, or kill. Then the date of the
next read, and append both to `.claude/decisions.md`.

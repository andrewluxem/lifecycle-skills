# Example brief: Tidewell Coffee Co.

Tidewell Coffee Co. is an invented DTC brand selling whole-bean coffee and
brewing gear. Every number below is invented and labeled. No employer or client
data.

## The brief

From Tidewell's retention lead, in their words:

> "Our welcome is one email with 15% off and it barely moves. We want five
> emails, all leading with the 15%, going to everyone who signs up. Can you have
> it ready next week? Also, some people who just bought are complaining they
> got the 'first order' email. Probably a one-off."

What they get right: five touches, and shipping next week. What they get wrong:
leading every touch with the discount, sending the same series to past buyers,
and treating the purchaser complaint as a one-off. It's the bug.

## Inputs

| Input | Value | Label |
|---|---|---|
| New email subscribers per week | ~5,000 | `[Assumption]` |
| Share of new subscribers with a prior order | 12% | `[Assumption]` |
| AOV | $48 | `[Assumption]` |
| Gross margin | 58% | `[Assumption]` |
| Current 30-day purchase rate, new subscribers | Unknown; plan on 3.0% | `[Assumption]` |
| Signup pop-up promises a code | No | `[Fact]` from the brief's form description |
| Order data reaches ESP | Nightly batch at 02:00 | `[Assumption]` |
| SMS consent captured at signup | Yes, optional checkbox | `[Assumption]` |
| Category of interest captured | Beans vs. gear, on the form | `[Assumption]` |

## Diagnosis check

Tidewell's `.claude/retention-snapshot.md` exists and names activation as the
dominant leak: most subscribers never place a first order within 60 days
`[Assumption]` for this example. That's this program's zone, so we proceed. If
the snapshot didn't exist, or named mid-life erosion, I'd stop here and route
to `retention-diagnosis`. A better welcome doesn't fix a subscription that
bleeds in month four.

## Build spec

**Message architecture (five-touch, new subscribers)**

| # | Purpose | Timing | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Promise | Day 0, on opt-in | Email | Believe Tidewell's roast-to-ship window is the difference | The roast-date-on-bag policy | Shop the house blends | Any discount |
| 2 | Proof | Day 2 | Email | Believe people like them reorder | Review strip for the top three blends | Shop most-reviewed | Unsupported "best coffee" claims |
| 3 | Guide | Day 4 | Email | Know which beans fit their brewer | Brew-method guide; beans or gear per the form | Take the brew-match quiz | Incentive; full catalog |
| 4 | Offer | Day 7, non-purchasers | Email | Have a reason to try it this week | Free shipping on the first order, expires day 11 | Redeem on the house blends | Reaching buyers; 15% off by default |
| 5 | Last call | Day 10 | Email; SMS if consented | Act before day 11, or not | Expiry; the "reroast or refund" guarantee | Redeem before expiry | Extending the offer |

**Re-subscriber variant (12% of entrants `[Assumption]`)**

| # | Purpose | Timing | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| R1 | Welcome back | Day 0 | Email | Know what's new since their last order | New single-origins since last order date | Set preferences | Any first-order offer |
| R2 | Next step | Day 3 | Email | See the reorder that fits their history | Replenishment timing from their last bag size | Reorder their last blend | Discounting |

**Splits**

- Holdout, random at entry: **20%** for the first read (see measurement).
- Prior order: yes to the variant, no to the five-touch path.
- Category (beans vs. gear) on touches 2 and 3. The form captures it for most
  entrants `[Assumption]`, so the split clears the one-third threshold.

**Exits and suppression**

- Order event: exit to `post-purchase`. Because orders land at 02:00, touches 4
  and 5 are scheduled for 10:00 local, after the batch, and a pre-send filter
  re-checks "no order since entry." Tidewell's engineering team also gets a
  ticket to stream the order event. Until it ships, anyone who orders before the
  02:00 batch is covered, but someone who orders after 02:00 on send day still
  gets that day's touch. That residual gap is written into the decisions log,
  not ignored.
- Unsubscribe, bounce, complaint: exit.
- Day 14: exit to BAU.
- BAU discount campaigns suppressed for welcome entrants days 0–11.
- Cart abandon takes priority; touch 4 skipped if cart abandon already sent an
  incentive.

**Primitives**

- Trigger: opt-in event with source and category.
- Filter: email consent; never entered before; no order since entry (every
  send).
- Split: holdout 20%; prior order; category.
- Wait: 2d, 2d, 3d, 3d, each listening for the order event.
- Exit: order (to `post-purchase`); unsub/bounce/complaint; day 14 (to BAU).

**Why free shipping, not 15% off.** At a $48 AOV `[Assumption]`, 15% is $7.20
per redeemed order. Tidewell's blended shipping cost is about $5.50 per order
`[Assumption]`. Free shipping costs less per redemption and doesn't reset the
price anchor on the product. It's the first thing we test against 15% in cycle
two, not a settled answer.

## Measurement plan

- **Primary KPI:** revenue per new subscriber, 30 days from entry, treated vs.
  holdout.
- **Holdout:** 20% at entry. The read cohort is 12 days of entrants, about
  8,570 people at ~5,000 a week `[Assumption]`. At a 3.0% baseline and a 4.5%
  target `[Assumption]`, 80/20 needs about 6,950 `[Inference]`, so it fits. A
  10% holdout would need about 11,800 `[Inference]`, which Tidewell can't reach
  in 12 days. That's why the first read runs at 20% and drops to 10% after the
  program proves lift.
- **Guardrails:** unsubscribe under 0.5% per send, complaints under 0.1% per
  send `[Assumption]`; zero purchasers receiving touch 4 or 5; full-price
  first-purchase rate in treated no lower than holdout.
- **Kill condition:** launch on a Monday; read on the Monday six weeks later
  (day 42). If treated revenue per new subscriber doesn't beat holdout with a
  confidence interval that excludes zero, redesign the offer touch first, then
  run one more 6-week read. If that fails, back to `retention-diagnosis`.

## What we deliberately didn't do

- **No discount in touch 1**, and no 15% by default. The team asked for both.
  I think they'd be paying a subsidy to people already in the checkout.
- **No second-purchase push inside welcome.** Buyers leave for
  `post-purchase` the moment the order lands.
- **No re-engagement of quiet subscribers after day 14.** BAU owns them.
- **No finished copy.** The frame above goes to `lifecycle-messaging` or
  Tidewell's writers.
- **No global frequency rule.** Welcome's defaults are stated; the cross-program
  priority is `journey-architecture`'s call.

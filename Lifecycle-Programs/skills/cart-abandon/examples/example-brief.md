# Example brief: Tidewater Tackle Co.

Tidewater Tackle Co. is invented. So is every number below. Nothing here comes
from a real employer or client.

## The brief

From Tidewater's ecommerce lead:

> "Our abandoned cart email goes out 24 hours later and barely recovers
> anything. Competitors all put 15% off in the first email, so let's do that and
> send it faster. Our ESP says the current flow drove $40K last quarter, so
> imagine what it'll do with a discount."

Three things in there I'd push back on:

1. **"15% off in the first email."** That pays every shopper, including the
   ones already coming back. It's the most expensive way to recover a cart.
2. **"The ESP says it drove $40K."** That's last-touch attribution with no
   holdout. We don't know how much of it the flow caused.
3. **"Send it faster."** Right instinct. That part we keep.

## Inputs

| Input | Value | Label |
|---|---|---|
| AOV | $96 | `[Assumption]` |
| Gross margin | 42% | `[Assumption]` |
| Gross margin per full-price order | $40.32 | `[Inference]` (96 × 0.42) |
| Known-identity cart abandoners per week | 2,500 | `[Assumption]` |
| Organic 7-day recovery with no program | 9% | `[Assumption]` |
| Share of abandoners with no prior order | 60% | `[Assumption]` |
| Share with explicit SMS consent | 18% | `[Assumption]` |
| Habitual abandoners (3+ in 90 days) | 20% of entrants | `[Assumption]` |
| Current flow | One email at 24 h, no holdout | `[Fact]` (from the brief) |
| Order channels | Web and a phone line for bulk orders | `[Fact]` (from the brief) |

## Diagnosis check

Tidewater ran `retention-diagnosis` last month. The snapshot puts the dominant
leak at **activation**: most visitors who add to cart never place a first order,
and the repeat curve after a first order is healthy `[Assumption]`. So this is
the right program, and the first-time path is the one that matters. If the
snapshot had pointed at mid-life erosion, I'd have said so and not built this.

## The discount math, per 1,000 entrants

| Scenario | Recovery | Orders | Margin per order | Total margin | Revenue |
|---|---|---|---|---|---|
| No program (holdout) | 9% `[Assumption]` | 90 | $40.32 | $3,629 | $8,640 |
| 15% off in touch 1, everyone | 14% `[Assumption]` | 140 | $25.92 | $3,629 | $11,424 |
| Timing-first, no code (touches 1–3) | 12% `[Assumption]` | 120 | $40.32 | $4,838 | $11,520 |

`[Inference]` from the rows above: the blanket discount lifts recovered revenue
about 32% and adds exactly zero margin. Every one of the 90 organic buyers now
costs $14.40. The timing-first build recovers fewer orders than the discount
and makes about $1,210 more margin per 1,000 entrants. Message costs are left
out for simplicity; they'd make the discount row slightly worse.

## Build spec

**Primitives.**

- **Trigger:** cart updated, then 30 min with no purchase and no activity.
- **Filter:** email consent; not purchased in 24 h; not in this program in 14
  days; entry removes them from browse-abandon.
- **Split A:** 20% holdout, per person, sticky, at entry.
- **Split D:** first-time (60%) vs. repeat.
- **Split B:** incentive eligibility. First-time only, not a habitual abandoner,
  cart margin above $30 `[Assumption]` so the incentive can't flip an order
  negative.
- **Split C:** 50/50 incentive test inside the eligible branch.
- **Exit:** purchase via web or phone line (the phone orders reach the ESP
  through a nightly file today, so we fixed that to an hourly feed before
  launch), cart emptied, consent revoked.

**Message architecture, filled in.**

| # | Timing | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|
| 1 | 45 min | Email | "My gear is saved" | The cart, live price and stock | Restored cart | No code, no cross-sell of other rods and reels ahead of the cart |
| 2 | 4 h, 9 a.m.–8 p.m. local | SMS (18% consented) | "Right, finish that" | Item name and link | Restored cart | No incentive; skip if outside window until morning |
| 3 | 24 h | Email | "Returns and shipping are handled" (first-time); "You bought from us before, same guarantee" (repeat) | 60-day returns, free-shipping threshold, one review for the item | Restored cart | Not a re-send of touch 1 |
| 4 | 60 h, eligible only | Email | "Free shipping on this cart" | Terms and 48 h expiry | Checkout with offer applied | Never to fenced shoppers; paused during any sitewide sale |

The finished words go to `lifecycle-messaging`. Free shipping was picked for
touch 4 over percent-off because the brief's exit survey names shipping cost as
the top objection `[Assumption]`, and it costs less margin per order than 15%
here `[Inference]`.

## Measurement plan

- **Co-primary KPI:** incremental revenue per entrant and incremental margin
  per entrant, 7-day window, treated vs. holdout. Margin per recovered order
  reported alongside.
- **Holdout:** 20% per person, sticky, assigned at entry; control gets nothing
  from this program or browse-abandon.
- **Sample:** ~3,000 per arm on margin `[Inference]`; at 2,500 entrants a week
  and a 20% holdout that's about 6 weeks.
- **Dates:** launch Monday 2026-10-05; read Monday 2026-11-16. Chosen so the read
  closes before the late-November sale season, when a sitewide promo would
  contaminate both arms.
- **Kill condition:** if incremental margin per entrant isn't positive on
  2026-11-16, touch 4 comes out and we re-read on 2026-12-14. If the
  no-incentive version still isn't positive, the program stops and we go back to
  `retention-diagnosis`. Touch 4 also comes out on 2026-11-16 if its margin
  against its own no-incentive arm isn't positive.

## What we deliberately didn't do

- **No discount in touch 1**, which was the headline ask. The math above is the
  reason.
- **No incentive for repeat buyers or habitual abandoners.** Tidewater's repeat
  curve is healthy; paying repeat buyers to come back is paying for the
  counterfactual. `segmentation-model` will replace the working fence with a
  real one.
- **No browse-abandon build this cycle.** It's suppressed while someone's in
  cart-abandon, and it waits until this program has a read.
- **No subject lines or body copy.** `lifecycle-messaging` owns those.
- **No frequency-cap policy.** `journey-architecture` decides whether touch 1
  is exempt from the global cap.

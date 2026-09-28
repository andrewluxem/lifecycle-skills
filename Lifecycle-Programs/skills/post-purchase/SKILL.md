---
name: post-purchase
description: >-
  Blueprint for the post-purchase program that turns a first order into a
  second one: keeps order and shipping messages transactional, spends the
  attention they earn on a how-to, a review/UGC ask timed to when the product
  has actually been used, and one relevant cross-sell, then hands off to
  replenishment-reminders or loyalty-program. Use when someone says "build a
  post-purchase flow," "our second-purchase rate is soft," "we need more
  reviews," "what should go in the shipping confirmation," or "first-time
  buyers never come back."
license: MIT
---

# Post-Purchase

The first order is the most attention a customer will ever give you. They open
the order confirmation, then the shipping email, then check tracking twice. Most
teams spend that attention on nothing, or they spend it badly: a discount code
jammed into the shipping notice and a review request that lands before the box
does. This program spends it on the one thing that predicts a second order —
the product working — and only then asks for anything.

I work from the leak outward. If you don't know the leak is early-life, I stop
and send you to `retention-diagnosis` first.

## When to use this skill

Trigger phrases I listen for:

- "Build me a post-purchase flow" or "what should happen after the first order?"
- "Our first-to-second purchase rate is bad."
- "We need more reviews / more UGC."
- "Can we put an offer in the shipping confirmation?"
- "Welcome converts fine but new buyers disappear."
- "Where does someone go after the order ships?"

**Leak zone: early-life.** The customer bought once and the product delivered,
or should have, but no second purchase followed. That's the gap this fixes.

What this skill is NOT for, and who owns it:

- Unknown leak, or "retention is bad" with no curve behind it →
  `retention-diagnosis`. I won't design in the dark.
- Pre-first-purchase conversion → `welcome-series` (this plugin). Welcome
  purchasers exit into this program; I don't re-onboard them.
- Repeat buyers of consumables on a cycle → `replenishment-reminders` (this
  plugin). I hand off; I don't run the reorder clock.
- Points, tiers, VIP recognition → `loyalty-program` (this plugin).
- Frequency caps and collisions with promo campaigns → `journey-architecture`.
- The finished words → `lifecycle-messaging`.
- Who counts as "first-time" vs. "returning" when the data is messy →
  `segmentation-model`.

## What I need before I start

**Required** — without these the program is a guess:

- **A detectable first-order event**, and a way to tell a first order from a
  repeat one (customer-level order count, not session-level).
- **A delivery signal.** Carrier "delivered" event, or at minimum ship date plus
  a transit-time estimate. Without delivery, every downstream timing is a
  guess, and I'll say so on every row.
- **Time-to-first-use by category** — how long between "box arrives" and
  "customer has actually used it." Rough is fine; unknown means I'll label it
  `[Assumption]` and make it the first thing you test.
- **Consent status** for marketing email and SMS, separate from the
  transactional right to send order updates.
- **Who owns the transactional templates** (ops, eng, the ESP team) and whether
  they can carry a conditional content block.

**Optional** — each one sharpens a decision:

- Baseline first→second purchase rate and the median days between orders 1 and 2.
- Review platform and current review volume per 100 orders.
- Product affinity data ("bought together," or even a merchandiser's list).
- Return and cancellation rates by category.
- AOV and margin, if anyone wants a discount on the second order.

With partial inputs I can still produce the full architecture, exit logic, and
holdout plan. Every missing number becomes `[Assumption]`, and the measurement
plan tells you which assumption to replace first. I read
`.claude/lifecycle-context.md` and `.claude/retention-snapshot.md` if they exist
and append my decisions to `.claude/decisions.md`.

## The thesis

I think most post-purchase programs fail because they're built around the
calendar of the warehouse, not the calendar of the customer. The review ask
fires at ship date plus seven days because that's easy to trigger, and it lands
on someone who hasn't opened the box yet. The cross-sell fires the day after
purchase, before the first product has earned any trust. And somebody always
wants to turn the shipping confirmation into a promo.

Order and shipping messages earn open rates far above promotional mail — plan on
2–3x `[Assumption]` until you pull your own numbers. That attention is borrowed
from the transaction. Keep those messages primarily transactional: they carry
compliance limits on promotional content, and they carry the customer's trust.
The program adds light, relevant modules to them and layers separate marketing
touches on top, each timed to product experience: delivery, then
time-to-first-use, then the ask.

**The sacrifice:** no discount in the transactional messages, no second-order
coupon by default, no review ask before the product has been used, and no
loyalty or replenishment logic in here. Those belong to siblings. I'd rather
this program do three things well and hand off cleanly.

## Program blueprint

### Objective and audience

- **Outcome:** raise the first→second purchase rate, measured against a holdout.
- **Entry audience:** customers placing their first order, including welcome
  purchasers exiting `welcome-series`. Repeat buyers don't enter; they belong to
  `replenishment-reminders` or `loyalty-program`.
- **Leak zone:** early-life.

### Message architecture

Touches 1–2 are transactional and always send. Touches 3–6 are the marketing
layer, and the only part the holdout measures. `TTFU` = time-to-first-use for
the product category.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Order confirmation (transactional) plus one "what happens next" module | Immediately on order — the customer is waiting for it | Email; SMS only if they opted in to order updates | Trust the order went through and know what's coming | Order details, delivery estimate | View order status | Promo takeover; cross-sell grids; anything that pushes the order details below the fold |
| 2 | Shipping confirmation (transactional) plus a "get ready" module | On ship event — it's the highest-attention moment in the program | Email; SMS for tracking if opted in | Know when it arrives and what to do on day one | Tracking link, carrier ETA | Track package | Review ask (they don't have it yet); discount codes |
| 3 | How-to / first-use guide | Delivery + 1 day; setup-heavy products on delivery day — help lands when the box is open | Email; in-app/push if the product has an app | Use the product correctly the first time | Setup video, care guide, top FAQ | Open the guide | Selling anything; asking for a review |
| 4 | Review / UGC ask | Delivery + TTFU + a few days of use — the verdict exists only after use | Email; SMS if marketing-consented and SMS earns better response for you | "My experience helps the next buyer" | Review count or how reviews get used on the site | Leave a rating (one click to start) | Incentives tied to positive sentiment; gating reviews by rating; asking before delivery |
| 5 | Review reminder, non-responders only | Touch 4 + 5–7 days — one reminder, then stop | Email | Same as 4, lower friction | Same as 4 | Same as 4 | A third ask; nagging people who already reviewed |
| 6 | Cross-sell: one complementary product | Delivery + TTFU + 7–14 days, only if no second order yet — after the first product earned trust | Email | "This makes what I bought better" | Affinity data ("bought with"), or a use case tied to item 1 | Shop the one item | Default discount; a generic bestseller grid; recommending what they just bought |

Every timing above is a starting default `[Assumption]`. Replace with your
measured delivery lag and TTFU after the first cycle (see
`references/benchmarks.md`).

### Splits and personalization

- **Default path:** touches 1–6 in order, one product category, one TTFU.
- **Split on TTFU class** (instant / days / weeks). This is the split that earns
  its place: it moves touch 4 and 6 timing, which is the whole thesis. Apparel,
  furniture, and skincare don't get used on the same clock.
- **Split on consumable vs. durable** at exit — decides whether the handoff goes
  to `replenishment-reminders` or `loyalty-program`.
- **Split on "reviewed yet?"** before touch 5 — reviewers skip the reminder.
- **Random holdout split at entry** — see Measurement.
- **Cut:** first-name tokens, weather, "because you're in Denver." None of it
  changes a decision. Product-specific how-to content does; keep that.

### Exits and suppression

- **Second purchase** → exit immediately, skip the cross-sell, hand to
  `loyalty-program` (durable) or `replenishment-reminders` (consumable).
- **Return, refund, or cancellation** → exit the marketing layer at once. Never
  ask someone returning the product for a review or a second purchase. Route to
  service recovery if you have it.
- **Delivery exception** (lost, damaged, delayed past threshold) → pause
  touches 3–6 until resolved; restart the clock from actual delivery.
- **Unsubscribe from marketing** → stop 3–6; transactional 1–2 still send.
- **Program end** (touch 6 + wait, no second order) → hand off by product type.
- **Suppressed while in 3–6:** generic promo blasts that would cross-sell a
  different item, and any other review-request program. Collision rules beyond
  that belong to `journey-architecture`.

The expensive bug lives upstream: welcome-series purchasers who never exit
welcome and get "first order, 10% off" after they've bought. Test the welcome →
post-purchase handoff with a live profile before launch.

### Content blocks

| Block | Used in | Data it needs |
|---|---|---|
| What-happens-next strip | 1 | Fulfillment SLA, delivery estimate |
| Get-ready module | 2 | Product category → setup content map |
| How-to block | 3 | Category/SKU → guide URL, video URL |
| Review module | 4, 5 | Review platform link, product ID, reviewed flag |
| Single-product recommendation | 6 | Affinity map, inventory, exclusion of purchased SKUs |
| Holdout flag | 1, 2 (conditional blocks) | Random assignment stored on the profile at entry |

## Platform build mapping

- **Trigger:** first-order event (customer order count = 1). Delivery event
  starts the marketing clock.
- **Filter:** first-order customers only; marketing consent for 3–6; exclude
  returned/cancelled orders; exclude employees and test accounts.
- **Split:** random holdout at entry; TTFU class; reviewed-yet; consumable vs.
  durable at exit.
- **Wait:** wait-until-event for ship and delivery (with a timeout fallback);
  time delays for TTFU and reminder spacing.
- **Exit:** second order, return/refund/cancel, marketing unsubscribe, program
  end → handoff.

Braze Canvas, Klaviyo Flows, Iterable Journeys, and SFMC Journey Builder specifics
are in `references/platform-build.md`.

## QA

I never send anything. These are the checks a human runs before activation, most
expensive first. Full list in `references/qa-checklist.md`.

1. **Welcome → post-purchase handoff.** A test profile that buys during welcome
   leaves welcome and enters here, once.
2. **Return/cancel exit.** A test order marked returned stops touches 3–6 before
   the review ask.
3. **Holdout integrity.** Control profiles get touches 1–2 without the added
   modules and nothing from 3–6.
4. **Transactional content ratio.** Touches 1–2 read as transactional; any
   module is secondary and non-promotional. Your compliance owner signs off.
5. **Delivery-based timing.** Touch 4 fires off the delivered event, not ship
   date, with a sane fallback when no delivery event arrives.

## Measurement

- **Primary KPI:** first→second purchase rate within 60 days of first delivery,
  treated vs. holdout. Adjust the window to about 1.5x your median days between
  orders 1 and 2 `[Assumption]`.
- **Guardrails:** marketing unsubscribe rate on touches 3–6; spam complaints;
  return rate on first orders (treated vs. control); discount rate and margin on
  second orders; "where is my order" contact rate; transactional deliverability.
  Review volume and average rating are secondary outcomes, not the goal.
- **Holdout recipe:** random 10–20% of entrants at the first-order event,
  customer as the unit, assigned once and stored on the profile. Control
  receives transactional touches 1–2 without the added modules, and none of
  3–6. The transactional messages themselves can't be held out; the holdout
  measures only the marketing layer on top. Run enrollment until the sample
  supports your minimum detectable lift (math in `references/measurement.md`),
  then wait out the 60-day window.
- **Kill condition:** if the treated group doesn't beat holdout on 60-day
  first→second purchase rate by at least 1.5 points absolute `[Assumption — set
  from your margin and baseline]` at the final read (enrollment end + 9 weeks),
  or any guardrail breaches its threshold for two consecutive weeks, we cut the
  cross-sell touch, keep review capture only if it isn't hurting return or
  unsubscribe rates, and go back to `retention-diagnosis` to test whether
  early-life is a message problem at all.

## Field notes

- `[Fact — author's record]` The most common catch in skill-driven pre-send QA
  on a welcome program was the purchaser-exit bug: buyers not leaving welcome
  when they bought. That's the exact seam this program sits on, which is why
  it's QA check #1.
- `[Fact — author's record]` When rebuilding a lifecycle program suite, welcome
  shipped first because it had the cleanest holdout and the fastest read.
  Post-purchase reads slower (the KPI window is weeks, not days), so start its
  holdout early.
- `[Fact — author's record]` Campaign output went from 7 to 21 per week with
  the same team. The lesson: a shippable v1 in week one beats a perfect program
  in quarter two. Here that means touches 1–4 plus the holdout first, the
  cross-sell after.

## Worked example

Tallgrass Kitchen Co. (invented) sells cast-iron cookware. Their team asked for
a 15%-off code and a review ask inside the shipping confirmation. I kept the
shipping email transactional with a seasoning "get ready" module, moved the
review ask to delivery + 10 days `[Assumption]` (skillets get used the first
weekend; the verdict takes a few cooks), and made the cross-sell one item: the
seasoning oil, which hands buyers to `replenishment-reminders`. At about 4,500
first orders a month `[Assumption]`, a 20% holdout needs roughly 12 weeks of
enrollment to detect a 2.5-point lift. Full walkthrough in
`examples/example-brief.md`.

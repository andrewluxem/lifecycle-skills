---
name: replenishment-reminders
description: >-
  Blueprint for a replenishment reminder program on genuinely consumable
  products: reminders timed to 70–80% of each SKU's observed usage cycle (from
  the brand's own inter-purchase data, not the label), a one-tap prefilled
  reorder, graduation of repeat replenishers into subscription, and a holdout
  that proves the reminders pull reorders forward instead of taking credit for
  ones that were coming anyway. Use when someone says "customers don't come
  back to reorder," "build a replenishment flow," "our reorder reminders fire
  at the wrong time," or "how do we get one-time buyers of a consumable onto
  subscription."
license: MIT
---

# Replenishment Reminders

A replenishment program has one job: be in the inbox a few days before the
customer runs out, with a reorder that takes one tap. That's it. Most of the
craft is in the timing, and most teams get the timing from the wrong place.

I build this program in primitives, spec every touch as a framework, and ship it
with a holdout and a kill condition. I don't write the copy and I never send
anything. A human reviews the build and presses the button.

## When to use this skill

Say it like an operator would:

- "People buy once and we never see them again, and it's a product they use up."
- "Build me a replenishment or reorder-reminder flow."
- "Our reminder goes out at 30 days for everything and it feels wrong."
- "How do I get repeat buyers onto subscription without nagging first-timers?"
- "Customers reorder, but late, and I think some of them are buying it on a
  marketplace in between."

**Leak zones this fixes:** early-life (the first purchase never becomes a second
one because the moment of need passes unnoticed) and mid-life (repeat buyers
drift late, then lapse to a competitor or a marketplace).

**It only works on products that get used up.** Coffee, pet food, supplements,
skincare, filters, razors, cleaning refills. If the catalog is furniture,
apparel, or electronics, there is no usage cycle to time against, and I'll say
so and route you to `post-purchase` (reviews, care, cross-sell) or `loyalty-program`
instead. I won't invent a "replenishment" cadence for a sofa.

**What it is NOT for:**

- Unknown leak. If you can't tell me where customers are dropping, I stop and
  send you to `retention-diagnosis` first. I won't design in the dark.
- The first days after an order (confirmation, shipping, how-to-use, review ask):
  that's `post-purchase`, which hands customers into this program.
- Customers far past their cycle (roughly 2x the expected depletion date): they
  aren't running low, they've left. That's `winback-series`.
- The finished words: `lifecycle-messaging`. Collisions with other programs and
  frequency caps: `journey-architecture`. Which customers, cut how:
  `segmentation-model`.

## What I need before I start

**Required**

- **Order-line data with SKU, variant/size, quantity, and timestamp** for at
  least one full cycle of your slowest meaningful SKU. This is how I compute the
  observed cycle. Without it, every timing in the program is an `[Assumption]`.
- **Proof the catalog is consumable.** A list of top SKUs by repeat-purchase
  volume is enough.
- **A reorder mechanism that actually works in one tap:** a prefilled cart deep
  link or a reorder endpoint that survives a logged-out click. If you don't have
  one, that's build item #1, before any message.
- **Consent status by channel** (email, SMS, push) and your subscription status
  field, so subscribers never enter.

**Optional (sharpens it)**

- Delivery lead time by region, so the reminder lands with time to ship.
- Marketplace or retail sales signals, so a reorder elsewhere can exit the flow.
- Margin by SKU, if anyone wants an incentive on the table.
- `.claude/lifecycle-context.md` and `.claude/retention-snapshot.md` if they
  exist.

**With partial inputs** I can still produce the full architecture, exits, QA,
and measurement plan. I'll time touches off the label or your best guess, label
every one `[Assumption]`, and make "replace label timing with observed cycles"
the first post-launch task. I'd rather ship an honest v1 than wait a quarter for
perfect data.

## The thesis

Most replenishment programs are timed to the manufacturer's label. "Thirty
servings, so thirty days." I think that's the single most common reason these
programs underperform. Real households don't use products the way the label
does. They skip days, share, ration, or double up. The label is a starting
assumption. The answer is in your own data: the median days between repeat
purchases of that SKU, adjusted for how many units were bought. Then I fire the
first reminder at 70–80% of that observed cycle, early enough to arrive and ship
before they run out, late enough that it doesn't feel like a sales email.

The second thing teams get wrong is the incentive. I worry about programs that
put a discount in every reminder. A customer who is running low was going to
need more anyway; the reminder's job is convenience and timing, not price. A
discount there trains people to wait for the code, and it's margin you give to
people who'd have paid full price.

The third is credit. Lots of these customers would reorder with no reminder at
all. A replenishment program that reports "38% reordered" is reporting
baseline behavior. The real question is whether reminders pull the reorder
earlier and keep people from lapsing to a competitor. Only a holdout answers
that.

**The sacrifice.** This program does not discount by default, does not
cross-sell the catalog, does not chase lapsed customers past ~2x their cycle,
and does not touch non-consumables. Those belong to `post-purchase`,
`winback-series`, and `loyalty-program`. It does one thing: the right reorder,
at the right moment, in one tap.

## Program blueprint

### Objective and audience

- **Objective:** raise the on-time repeat rate: the share of replenishable
  purchases followed by a reorder of the same SKU (or an approved substitute or
  size) before the customer runs out, plus a grace window.
- **Entry audience:** any customer whose order contains a replenishable SKU
  with a known cycle, who is not an active subscriber to that SKU, and who has
  email or SMS consent. One episode per customer-SKU; the next purchase starts a
  fresh one.
- **Leak zones:** early-life (first to second purchase) and mid-life (repeat
  buyers drifting late and lapsing).

**Cycle rule.** Expected depletion date = purchase date + observed cycle for
that SKU at that quantity bucket (1, 2, 3+ units). Compute the cycle as the
median interval between consecutive purchases of the SKU by the same customer.
Don't assume two units last twice as long; bucket by quantity and let the data
say. Once a customer has two or more reorders of a SKU, use their personal
median instead. SKUs with too few repeat pairs to trust (I use 30 as a floor
`[Assumption]`) fall back to the category cycle, then the label, labeled as such.

### Message architecture

C = the customer's expected cycle for this SKU and quantity. Percentages are of C,
measured from the purchase date.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | The reminder. The only touch that has to exist. | 75% of C (test 70–80%), minus delivery lead time if shipping takes more than a few days. Early enough to arrive before run-out, late enough to feel useful, not salesy. | Email: carries the product image, last-order detail, and the reorder button. | "I'm about to run low, and reordering takes one tap." | Their own order: product, size, date bought, estimated run-out date, and the delivery date if they order today. | One-tap reorder: prefilled cart, same SKU, size, and quantity. Secondary: "not yet," which snoozes and updates their cycle. | No discount. No catalog cross-sell. Never fires after a reorder already happened. |
| 2 | Pre-run-out nudge for those who haven't reordered. | ~95% of C. They are days from empty; this is the last moment a reorder arrives in time. | SMS or push if consented (short, time-sensitive); email fallback. | "Order today and there's no gap." | Delivery-by date versus estimated run-out date. | Same one-tap reorder link. | No fake scarcity or urgency theater. Never SMS and email the same day. |
| 3 | Check-in. Learn whether they switched, stocked up, or forgot. | ~120% of C. Past run-out, but still inside the normal spread of repeat intervals. | Email. | "Still using it? Reorder, or tell us you're set." | Honest: their order history plus what other customers pick when they switch sizes (only if the data supports it). | Reorder (primary). Snooze or "I switched to a bigger size" (secondary; both update the record). | Not a winback: no escalating incentive. Past ~2x C they hand to `winback-series`, which owns that. |
| G | Subscription graduation. Only for proven replenishers. | Replaces touch 1 in the cycle after the customer's 2nd or 3rd on-time reorder (test 2 vs. 3). Never on the order confirmation, where it would compete with the transactional message. | Email. | "A subscription does the remembering for me, at my pace." | Their own on-time streak and observed cadence; the subscription terms (skip, pause, cancel) stated plainly. | Start a subscription at their observed cadence, prefilled. The one-tap reorder stays as a secondary. | Never pitch subscription to first-time reorderers. Never set the subscription cadence to the label cycle. |

### Splits and personalization

- **Default path:** touch 1, then 2, then 3, then exit to `winback-series`
  eligibility at ~2x C.
- **Holdout (random, at customer level):** 10% of customers get nothing from
  this program across every cycle. See Measurement.
- **Graduation branch:** 2+ on-time reorders (threshold under test) swaps touch
  1 for touch G. This split changes the ask, so it earns its place.
- **Quantity bucket:** sets C. Not a content split; a timing input.
- **Channel split on touch 2:** SMS/push consent decides the channel. No consent
  means email or skip.
- **Multi-SKU consolidation:** if a customer has several SKUs due within ~7
  days `[Assumption]` of each other, send one reminder anchored to the earliest
  depletion date, with every due SKU in the prefilled cart. Three reminders in a
  week is a program bug, not personalization.
- **Personal cycle:** after two reorders, their own median replaces the SKU
  median. The "not yet" snooze feeds this too.

Cut anything else. Name-in-subject and weather blocks don't change a decision.

### Exits and suppression

This is where the expensive bugs live. The most common: a customer reorders and
still gets "running low?" three days later.

- **Reorder of the SKU, any channel** (site, app, phone, marketplace or retail if
  the signal exists): exit immediately; the new order starts a new episode.
- **Reorder of a larger size or a higher quantity:** exit, and suppress until
  the recomputed depletion date of the new order.
- **Subscription start for that SKU:** exit permanently to subscription
  onboarding. Graduation is a handoff, not another loop.
- **Return, refund, or cancellation of the original order:** exit. They never
  had the product to run out of.
- **SKU discontinued or out of stock at send time:** hold the send, or swap in
  the approved substitute if one is mapped. Never send a reorder link to an
  empty shelf.
- **Past ~2x C with no reorder:** exit to `winback-series` eligibility.
- **Unsubscribe, SMS STOP, or complaint:** exit that channel immediately.
- **Suppressed while in this program:** generic promotional cross-sell for the
  same category. `journey-architecture` owns the priority rules if
  `post-purchase` review asks or campaigns collide with touch 1.
- **Gift orders** (ship-to differs from bill-to): excluded at entry. The buyer
  isn't the user.

### Content blocks

- **One-tap reorder block:** SKU, variant, quantity, current price, and a signed
  deep link to a prefilled cart that works logged out. Needs: order-line data and
  a cart-link service.
- **Last-order block:** product image, size, order date, estimated run-out date.
  Needs: the depletion date computed per episode.
- **Delivery-by strip:** "order today, arrives by" date. Needs: shipping
  estimate by region.
- **Snooze / "I'm set" control:** writes a snooze date or a size change back to
  the profile. Needs: a writable profile field and a link handler.
- **Due-items block** (consolidation only): the other SKUs due within the window.
- **Subscription block** (touch G only): observed cadence, terms, prefilled
  subscription link.

## Platform build mapping

In primitives. ESP specifics for Braze, Klaviyo, Iterable, and SFMC live in
`references/platform-build.md`.

- **Trigger:** a purchase event containing a replenishable SKU, or a daily
  entry from a table of customer-SKU episodes where `reminder_date = today`.
  The second is more robust; the depletion math belongs in the data layer, not
  in a wait step.
- **Filter:** consent; not a subscriber to the SKU; not a gift order; not in the
  holdout; SKU has a cycle (observed, category fallback, or label-based and marked `[Assumption]`).
- **Split:** holdout (random, customer-level, sticky); graduation (on-time
  reorder count); touch 2 channel (consent).
- **Wait:** wait until the reminder date (75% of C); wait until ~95% of C; wait
  until ~120% of C. Each wait re-checks exits before the send.
- **Exit:** reorder (any channel, same SKU or larger size); subscription start;
  return or refund; past ~2x C to `winback-series`; unsubscribe.

## QA

This skill never sends. It tells a human what to verify before they do. In order
of cost:

1. **Reorder exit works.** A test profile that reorders between touches 1 and 2
   gets nothing more. Test a larger-size reorder and a subscription start too.
2. **The one-tap link works logged out** on mobile, lands on a prefilled cart
   with the right SKU, size, and quantity, and shows the current price.
3. **Timing matches the cycle table.** Spot-check three SKUs at different
   quantity buckets: is the reminder date 75% of the observed cycle, not the
   label?
4. **Holdout is live, sticky, and silent.** The same customer lands in the same
   arm next cycle and receives nothing from the program.
5. **Subscribers and gift orders never enter,** and one customer with three
   SKUs due in the same week gets one message, not three.

Full list in `references/qa-checklist.md`.

## Measurement

- **Primary KPI: on-time repeat rate.** The share of customers whose first
  eligible episode after assignment ends in a reorder of the same SKU (or an
  approved substitute or larger size) by expected depletion date + 25% of C.
  Measured per arm; lift is treated minus holdout.
- **Guardrails:** unsubscribe rate per send (email and SMS, separately); spam
  complaints; repeat rate at 2x C (reminders that only shift timing without
  preventing lapse show up here); orders per customer over two cycles; discount
  spend per reorder, which should be near zero. Thresholds are in
  `references/measurement.md`.
- **Holdout recipe:** 10% of customers, randomized at the customer level on
  first entry, sticky across every cycle and SKU. The control gets transactional
  messages and business-as-usual campaigns, nothing from this program. Run until
  the entering cohort reaches the sample size in `references/measurement.md`,
  then wait one full cycle plus the grace window before reading. That's roughly
  2,100 holdout customers for a 3-point lift on a 30% baseline `[Assumption]`.
- **Kill condition:** if, at the read date (two median cycles of the top SKU
  after the last cohort enters, or 12 weeks after launch, whichever is later), treated
  on-time repeat rate doesn't beat holdout by at least 3 percentage points
  `[Assumption: reset from your baseline]` with the 90% interval excluding zero,
  **and** orders per customer over two cycles isn't higher in treated, we stop
  touches 2 and 3, keep touch 1 only if it's net-positive on orders, and send
  the question back to `retention-diagnosis`. Maybe the leak isn't timing; maybe
  it's price, product, or a marketplace undercutting you.

## Field notes

I haven't got a replenishment-specific record to share here, so I'll keep this
to the two lessons that carry over from rebuilding a full lifecycle program
suite.

- Skill-driven pre-send QA caught about three errors a week before send
  `[Fact — author's record]`. The most common catch on the welcome program was
  the purchaser-exit bug `[Fact — author's record]`. That was welcome, not
  replenishment, but it's the same class of bug as a reorder that doesn't exit
  this flow. That's why QA check #1 is first.
- Campaign output went from 7 to 21 a week with the same team
  `[Fact — author's record]`. The lesson I took: a shippable v1 in week 1 beats a
  perfect program in quarter 2. For replenishment, v1 is touch 1 and a holdout,
  timed to the best cycle you have today.

## Worked example

`examples/example-brief.md` walks through Tidewell Coffee, an invented
whole-bean coffee brand. The team wants a reminder at 14 days for every 12oz bag
because "that's two weeks of coffee," with 15% off in every send, and wants
subscribers included. Their own order data puts the median repeat interval for a
single 12oz bag near 23 days `[Assumption: fictional data]`, so the label-timed
reminder would land about a week early for most customers. The decision it
illustrates best: time touch 1 to 75% of the observed cycle (day 17), drop the
default discount, exclude subscribers, and let the holdout decide whether touches
2 and 3 earn their keep.

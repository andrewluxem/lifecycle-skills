---
name: cart-abandon
description: >-
  Blueprint a timing-first cart abandonment program: first touch inside the
  hour, incentive held back as the last lever and fenced to shoppers who are
  actually persuadable, measured on margin per recovered order and against a
  holdout because many abandoners come back on their own. Use when someone says
  "build me a cart abandon flow," "our abandoned cart emails aren't recovering
  anything," "should we put a discount in the cart email," or "our cart flow
  looks great in the dashboard but margin is down."
license: MIT
---

# Cart Abandon

Most cart abandonment programs are a discount with a delay in front of it. I
think that's backwards. The biggest lever in cart recovery is speed, not money,
and the money is where most programs quietly lose it back. This skill builds
the program in the order that protects margin: fast and plain first, useful
second, incentive last and only for people who need it.

I don't send anything. I produce a build spec, a QA list, and a measurement plan
a human runs.

## When to use this skill

Trigger phrases I listen for:

- "Build me a cart abandon program" / "set up abandoned cart."
- "Our cart flow isn't recovering anything."
- "Should the first cart email have a discount?"
- "Cart recovery revenue is up but margin is down."
- "People are gaming our cart discount."
- "Add SMS to our cart abandonment."

**Leak zones this program treats:** activation (the first purchase that never
happens) and early/mid-life for repeat buyers whose carts stall. If the leak is
somewhere else, a cart program is the wrong tool.

**What it is NOT for, and who owns that:**

- The leak is unknown, or nobody has checked that abandonment is where revenue
  leaves. I route to `retention-diagnosis` first and I won't design in the dark.
- Viewed-product or category-browse recovery. That's the browse-abandon
  program. This program suppresses it; I don't build both at once.
- Who counts as a habitual abandoner or discount-seeker, cut properly. I use a
  working fence here; `segmentation-model` owns the real definition.
- Collisions with welcome, post-purchase, promo calendars, and frequency caps.
  `journey-architecture` owns the traffic rules.
- The finished subject lines and body copy. That's `lifecycle-messaging`.
- Experiment design beyond this one program. `retention-metrics`.

## What I need before I start

**Required.** Without these the program is a guess.

- **A detectable cart event** with a timestamp, the cart contents, and a known
  identity (email or phone captured before the abandon). Anonymous carts can't
  be recovered by message, and I'll say so.
- **A purchase event from every channel that takes orders**: web, app, phone,
  store, marketplace. The purchase exit is only as good as this feed.
- **Consent status per channel.** Email marketing consent, and explicit SMS
  consent if SMS is on the table.
- **AOV and gross margin**, at least as ranges. If an incentive is on the
  table, I won't design it without margin.
- **Where the leak is**, from `.claude/retention-snapshot.md` or a
  `retention-diagnosis` run. If neither exists, I stop and route.

**Optional, and what they buy.**

- Historical abandon and recovery rates: replace my `[Assumption]` benchmarks.
- Discount-code usage per customer: sharpens the incentive fence.
- Cart-level margin (not just site average): lets the incentive scale with cart
  value instead of eating thin carts.
- Inventory and price feeds at send time: stops me emailing a sold-out cart.

With partial inputs I still produce the full blueprint, the QA list, and the
holdout recipe. Every missing number becomes `[Assumption]`, and I'll mark the
incentive branch "do not activate" until margin is known.

## The thesis

Most teams get two things wrong. They wait too long, because "24 hours" sounds
polite, and the intent is gone by then. And they lead with a discount, which
trains the list to abandon on purpose and pays people who were coming back
anyway. The dashboard shows recovered revenue climbing. The P&L shows the same
orders at a lower margin.

I think a cart program should be judged on margin per recovered order next to
recovered revenue, and measured against a holdout, because a large share of
abandoners return without any message `[Assumption]`. So this program goes
first touch inside the hour, uses the middle of the sequence to answer the
objection that stalled the cart, and treats the incentive as the last lever:
late, small, and fenced away from habitual abandoners, discount-seekers, and
segments that recover well on their own.

**The sacrifice.** No discount in touches 1–3. No incentive at all for fenced
shoppers. No cart touch while browse-abandon is also talking to the same
person. No urgency theater ("only 2 left!") unless the inventory feed says it's
true. I'd rather recover fewer orders at full margin than more orders at none.

## Program blueprint

### Objective and audience

- **Outcome:** incremental recovered orders at positive incremental margin,
  measured against a holdout.
- **Entry audience:** known shoppers with consent who added to cart, didn't
  purchase, and went inactive for the abandon threshold (default 30 minutes
  `[Assumption]`).
- **Leak zones:** activation (no prior order) and early/mid-life (repeat buyer
  whose cart stalls). Both paths run the same spine; they differ at the
  incentive.

### Message architecture

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Catch intent while it's warm | 30–60 min after abandon. Intent decays fast; this is the highest-value touch in the program `[Assumption]` | Email | "My cart is saved and one click away" | The actual cart: item image, name, variant, live price | Return to restored cart | No discount, no urgency, no cross-sell ahead of the cart |
| 2 | Second nudge for SMS-consented shoppers | 3–6 h after abandon, only inside local send hours; else next permitted window. Skipped for anyone without explicit SMS consent | SMS | "Oh right, I meant to finish that" | Item name plus the cart link; nothing more fits | Return to restored cart | No second SMS, no incentive, no send in quiet hours |
| 3 | Remove the objection that stalled the cart | ~24 h after abandon. Enough time to show the shopper wasn't just distracted | Email | "The thing I was unsure about is handled" | Shipping cost and speed, returns policy, reviews on the carted item | Return to restored cart | No discount; don't re-send touch 1 with a new subject |
| 4 | Last lever, persuadable only | 48–72 h after abandon, only for the incentive-eligible branch. Late on purpose so full-price recoveries happen first | Email | "This is the one reason I needed" | Incentive terms, expiry, scoped to this cart | Checkout with incentive applied | Never to fenced shoppers; never stacked with a sitewide promo; never an open-ended code |

Touches 1 and 3 are the program. Touch 2 is an SMS option. Touch 4 is a bet
that has to earn its keep in the incentive test below.

### Splits and personalization

- **Default path:** 1 → (2 if SMS-consented) → 3 → exit. No incentive.
- **Split A, holdout (random, at entry):** 10–20% of entrants get nothing from
  this program. This is how we know anything.
- **Split B, incentive eligibility (attribute):** a shopper reaches touch 4
  only if all are true: not a habitual abandoner (working fence: 3+ abandons in
  90 days `[Assumption]`), not a discount-seeker (working fence: most recent
  orders placed with a code `[Assumption]`), not in a segment whose holdout
  recovery is already high, and cart margin clears the incentive cost.
- **Split C, incentive test (random, inside the eligible branch):** half get
  touch 4, half don't. Without this I can't tell whether the incentive bought
  orders or just discounted them.
- **Split D, first-time vs. repeat (attribute):** first-time shoppers get
  reassurance (returns, shipping) in touch 3; repeat buyers get the order-history
  proof (their own past purchase, reviews). Repeat buyers are incentive-eligible
  only by exception, because I worry they're the most likely to return anyway.

Personalization that changes a decision: the cart contents, live price and
stock, first-time vs. repeat. Anything else (name in the subject, weather) is
decoration and I'd cut it.

### Exits and suppression

- **Purchase, any channel.** Checked before every send, not just at entry. An
  order placed by phone or in store must exit the shopper. This is the most
  expensive bug in the program.
- **Cart emptied.** Exit. If items are removed but the cart isn't empty, stay
  and re-render from the live cart at send time.
- **Consent.** Unsubscribe exits email; SMS opt-out exits SMS. Re-checked
  before each send.
- **Re-entry:** one cart-abandon run per person per 14 days `[Assumption]`, so
  habitual abandoners can't farm the sequence.
- **Suppressed while in this program:** browse-abandon. One abandonment
  program per person at a time; a cart event pulls someone out of browse-abandon
  and into this one, never the reverse.
- **On exit by purchase:** hand to post-purchase. On natural completion: back to
  BAU campaigns, no further abandonment messaging until re-entry opens.

### Content blocks

- **Dynamic cart block:** item image, name, variant, quantity, live price, stock
  status. Needs the cart payload plus a send-time catalog lookup; fallback is a
  plain "return to your cart" link, never a broken image.
- **Restore-cart link:** a deep link that rebuilds the cart on any device. Needs
  a cart token that survives session expiry.
- **Objection strip:** shipping threshold and speed, returns window. Needs
  current policy values, not hardcoded ones.
- **Review snippet:** rating and one review for the carted item or its
  category. Needs a review feed; hide the block if the item has none.
- **Incentive block (touch 4 only):** single-use code or auto-applied offer,
  scoped to the cart, with expiry. Needs a code generator and margin check.

## Platform build mapping

In primitives:

- **Trigger:** cart-updated event followed by no purchase and no activity for the
  abandon threshold.
- **Filter:** known identity; email consent (and SMS consent for touch 2); not
  purchased in the last 24 h; not in cart-abandon in the last 14 days; entering
  exits browse-abandon.
- **Split:** random holdout at entry (A); incentive eligibility (B); random
  incentive test (C); first-time vs. repeat (D).
- **Wait:** 30–60 min → touch 1; to local send window → touch 2; ~24 h → touch
  3; 48–72 h → touch 4. Each wait re-checks exits on wake.
- **Exit:** purchase from any channel, cart emptied, consent revoked, sequence
  complete.

Braze Canvas, Klaviyo Flows, Iterable Journeys, and SFMC Journey Builder specifics
are in `references/platform-build.md`.

## QA

This skill never sends. Before a human activates, check these five, in this
order:

1. **Purchase exit, every channel.** Put a test profile in, place an order
   through a non-web channel, and confirm it leaves before the next send.
2. **Holdout receives nothing.** Confirm the control branch has no message
   steps, and that browse-abandon is also suppressed for control.
3. **Incentive fence.** Push a fenced profile (habitual abandoner) through and
   confirm it never reaches touch 4.
4. **SMS consent and quiet hours.** A profile without SMS consent gets no SMS;
   an abandon at 11 p.m. local waits for the morning window.
5. **Live cart render.** Change the cart mid-sequence and confirm the next touch
   shows the new contents, the current price, and hides sold-out items.

Full list in `references/qa-checklist.md`.

## Measurement

- **Primary KPI (co-primary):** incremental recovered revenue per entrant and
  incremental margin per entrant, treated vs. holdout, 7-day window after entry.
  I report margin per recovered order next to revenue every time. A program
  that buys revenue at negative margin is a loss, whatever the dashboard says.
- **Guardrails:** unsubscribe and complaint rate per send; SMS opt-out rate;
  share of recovered orders using a code; repeat-abandon rate among entrants
  (the training effect); full-price order rate in the incentive test.
- **Holdout recipe:** 10–20% random holdout, randomized per person at entry
  and sticky for the test period, so a re-entering shopper stays in the same
  arm. Control gets nothing from this program or from browse-abandon; it still
  gets BAU campaigns. Run until the sample in `references/measurement.md` is
  reached, minimum 4 full weeks to cover weekly cycles. Inside the eligible
  branch, a 50/50 incentive-vs-no-incentive split at touch 4.
- **Kill condition:** if incremental margin per entrant (treated minus holdout,
  net of incentive cost) is not positive at the 6-week read, I strip touch 4
  first and re-read after 4 more weeks. If the no-incentive program still
  doesn't beat holdout on incremental margin, we stop the program and go back
  to `retention-diagnosis`; the leak isn't where we thought. Separately, if
  touch 4's incremental margin against its own no-incentive arm is not positive
  at the 6-week read, touch 4 comes out regardless of the rest. The burden of
  proof sits on the incentive, not on its absence.

Detail, sample-size math, and the readout template are in
`references/measurement.md`.

## Field notes

None of these are cart-abandon results. They're the operating habits I bring to
this program.

- I've rebuilt a full lifecycle program suite before, and welcome shipped first
  because it had the cleanest holdout and the fastest read `[Fact — author's
  record]`. If welcome isn't live and measured yet, I'd ask whether cart should
  wait.
- Skill-driven pre-send QA caught around three errors a week before send, and
  the most common welcome catch was the purchaser-exit bug `[Fact — author's
  record]`. Cart abandon has the same exit, with more channels feeding it. That's
  why QA check 1 is first.
- Campaign output went from 7 to 21 a week with the same team `[Fact — author's
  record]`. The lesson I took: a shippable v1 in week 1 beats a perfect program
  in quarter 2. Ship touches 1 and 3 with the holdout, then earn touch 4.

## Worked example

Tidewater Tackle Co., an invented fishing-gear shop, asks for "15% off in the
first cart email." Inputs are all `[Assumption]`: AOV $96, gross margin 42%, a
9% holdout recovery rate. Per 1,000 entrants, a blanket 15% code that lifts
recovery to 14% produces about $3,629 of margin, exactly what the 90 no-program
recoveries already earned. Recovered revenue rises about 32%; incremental
margin is zero. The timing-first build without a code, at 12%, earns about
$1,210 more margin per 1,000 entrants. The walkthrough is in
`examples/example-brief.md`.

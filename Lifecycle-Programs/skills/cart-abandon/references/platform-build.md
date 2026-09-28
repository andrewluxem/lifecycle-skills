# Platform build: Cart Abandon

Structural translation of the five primitives. Component names and settings, not
screenshots. Platform UIs move; if a setting has been renamed, the primitive is
still what matters. Verify every setting in your own account before launch.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Action-based entry on the cart event (custom event or ecommerce cart event), with a Delay equal to the abandon threshold before the first step | Metric-triggered flow on the cart or checkout-started metric | Journey entry on the cart event (custom event or cart-update API call) | API Event or Data Extension entry source fed by cart events |
| Filter | Entry audience: known user, subscribed; Audience Paths for re-checks | Flow filters (re-evaluated before each step), e.g. "placed order zero times since starting this flow" | Filter tiles / entry segment conditions | Entry criteria on the event; Decision Split to re-check consent |
| Split | Experiment Paths (random), Audience Paths (attribute), Action Paths (behavior) | Conditional split (attribute or random sample), trigger split (event property) | Randomized Split tile, Filter/Split tiles on attributes | Random Split, Decision Split, Engagement Split |
| Wait | Delay step; Action Paths with a time window as wait-until-event | Time delay; delay until a time of day | Delay tile; Wait-for-event | Wait by Duration, Wait Until Date, Wait Until Event |
| Exit | Exit criteria on purchase and cart-emptied events; subscription state | Flow filters plus "remove from flow" behavior on order | Journey exit rules on purchase / cart-cleared events | Exit criteria and Goal on the order Data Extension |
| Holdout | Experiment Paths with a no-message control path, or a Canvas control variant | Random-sample conditional split to an empty branch | Randomized Split to an end tile, or journey holdout group | Random Split to an empty path ending the journey |

## Braze

- **Entry:** action-based on the cart event. Put a Delay equal to the abandon
  threshold first, and use exception events so a purchase during the delay
  prevents the first send.
- **Entry/exit criteria:** exit criteria on purchase (all channels, through
  whatever event your order system sends) and on a cart-emptied event. Add
  re-entry settings: allow re-entry only after 14 days.
- **Steps:** Delay → Message (touch 1) → Audience Path on SMS subscription
  group → Message (touch 2) → Delay → Message (touch 3) → Audience Path
  (incentive eligibility) → Experiment Path (incentive test) → Message (touch 4).
- **Holdout:** Experiment Paths at the top of the Canvas with a control path
  that has no message steps. Don't rely only on the Global Control Group: it
  measures all of messaging, not this program.
- **SMS:** send only to the SMS subscription group; turn on Canvas quiet hours
  and choose "send at next available time," not "cancel," so touch 2 lands in
  the morning.
- **Frequency capping:** decide with `journey-architecture` whether cart
  messages count toward the global cap. I'd exempt touch 1 and cap the rest.

## Klaviyo

- **Trigger:** the cart or checkout-started metric, depending on what your
  storefront sends. Checkout-started only catches people who reached checkout;
  a cart-level metric catches more. Know which one you're on.
- **Flow filters:** "placed order zero times since starting this flow" and
  "has not been in this flow in the last 14 days." Flow filters are checked
  before each step, which is what makes the purchase exit work.
- **Splits:** conditional split with a random-sample condition at the top for
  the holdout, routed to an empty branch. Conditional splits on profile
  properties for incentive eligibility and first-time vs. repeat.
- **Smart Sending:** turn it off for touch 1 (it can suppress the highest-value
  touch because someone got a campaign that morning). Leave it on for touches
  3 and 4.
- **SMS:** SMS consent is separate from email consent; filter on it. Use the
  flow's quiet-hours setting for SMS.
- **Browse suppression:** add a flow filter to browse-abandon excluding anyone
  who triggered the cart metric in the relevant window.

## Iterable

- **Entry:** journey triggered by the cart event. Set journey entry limits so a
  person can be in the journey once at a time and re-enter after 14 days.
- **Filters:** Filter tiles re-check consent and "no purchase since entry" at
  each step. Iterable's channel subscription settings govern SMS consent.
- **Splits:** Randomized Split tile at the top for the holdout (control branch
  goes straight to an end tile). Attribute splits for eligibility and customer
  type; a second Randomized Split for the incentive test.
- **Exit rules:** configure journey exit rules on the purchase event and the
  cart-cleared event so people leave mid-delay, not just at the next tile.
- **Holdout:** if you use a journey-level holdout group instead of a split,
  confirm the holdout members are also excluded from browse-abandon.

## SFMC

- **Entry source:** API Event from the commerce platform is best; a Data
  Extension on a schedule works but adds lag that can blow the 30–60 minute
  window. Check the schedule before you promise touch 1 timing.
- **Splits:** Random Split first (holdout path ends immediately). Decision
  Splits on consent, eligibility, and first-time vs. repeat.
- **Waits:** Wait by Duration for each gap. Exit criteria are evaluated as
  contacts leave wait activities, so keep waits between every send.
- **Goals and exits:** set the order Data Extension as the exit criteria source;
  a Goal on purchase is useful for reporting but doesn't replace exit criteria.
- **SMS:** MobileConnect with its own opt-in keyword and subscription; enforce
  send windows with a Wait Until time-of-day step.

## Gotchas

- **The order feed only covers the web.** Phone, store, and marketplace orders
  don't reach the ESP, so buyers keep getting "you left something behind."
  This is the most expensive bug in the program.
- **Scheduled data imports.** A batch that runs every 6 hours makes a
  "within the hour" program impossible. Fix the feed before the timing.
- **Cart content captured at entry, not at send.** The email shows a price that
  changed or an item that sold out. Pull live catalog data at send time.
- **Holdout by send instead of by person.** A shopper who abandons twice lands
  in control once and treatment once, and the read is mush. Randomize per
  person and keep it sticky.
- **Two flows on one trigger.** Legacy "abandoned checkout" flows left live
  next to the new one double-send. Audit for any other flow on the same metric.
- **Discount codes that aren't single-use.** A shared code ends up on coupon
  sites within days `[Inference]`, and then the fence is meaningless.

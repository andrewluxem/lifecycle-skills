# Platform build: post-purchase

Structural mapping only: component names and settings, not screenshots. Menu
labels drift between releases, so verify each named feature in your account
before you build around it. Where a platform can't do something natively, the
workaround is listed.

One architectural decision comes first on every platform: **transactional
touches 1–2 usually live outside the marketing journey** (a transactional API
send, a store-platform notification, or a transactional-classified message).
The marketing journey (touches 3–6) runs alongside, keyed to the same order and
delivery events. The holdout flag has to be visible to both.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Action-based entry on a custom event (e.g. `order_placed`) with an order-count property; or API-triggered entry | Metric-triggered flow on the store's placed-order metric | Journey entry on a custom event or API trigger | Entry source: API event or data extension row from the order system |
| Filter | Entry audience filters + event property filter (order_count = 1); subscription state per step | Flow filters (e.g. "placed order zero times before this event"); profile consent | Entry filters + list/segment filter; message type consent | Entry criteria on the data extension; filter/decision split on consent fields |
| Split | Decision Split (attribute/behavior); Experiment Path for random | Conditional split; trigger split on event properties; random-sample condition if available | Attribute split; Randomized Split tile | Decision Split; Random Split activity |
| Wait | Delay step; Action Paths to wait for `order_delivered` with a max window | Time delay; wait-for-event isn't native in all setups — see Klaviyo notes | Delay tile; wait-for-event tile with timeout | Wait by Duration; Wait by Attribute / Wait Until Event |
| Exit | Canvas exit criteria on events (`order_placed` again, `order_returned`) | Flow filters re-evaluated before each send; separate "exit" via profile property | Journey exit rules on events | Goal (second purchase) + Exit Criteria |
| Holdout | Random bucket attribute set at entry, or Canvas control variant; mirror the flag into transactional templates | Random split to an empty branch; store the assignment as a profile property | Randomized Split to an empty path, flag stored on the user profile | Random Split to a path with no sends; write the flag back to the contact record |

## Braze

- **Entry:** action-based Canvas on `order_placed` where `order_count = 1`. If
  your events don't carry order count, filter on a customer attribute like
  `lifetime_orders` updated before the event fires. Verify the race.
- **Holdout:** set a random bucket attribute at entry (e.g. first step writes a
  0–99 value, or use Canvas variant distribution with a control variant). The
  transactional templates read the same attribute via Liquid to drop the added
  modules for control.
- **Transactional touches:** if order and shipping emails come from Braze,
  send them from an API-triggered campaign using a transactional subscription
  state so marketing unsubscribes don't block them. If they come from the store
  platform, the module logic has to live there.
- **Delivery wait:** Action Paths listening for `order_delivered`, with a
  maximum window (e.g. 10 days) that falls back to ship + median transit.
- **Exits:** exit criteria on `order_placed` (second order) and
  `order_returned` / `order_cancelled`.
- **Frequency:** Canvas steps respect global frequency caps unless you override;
  keep 3–6 inside the caps, and keep 1–2 out of them.

## Klaviyo

- **Trigger:** metric-triggered flow on the store's placed-order metric, with a
  flow filter for first-time purchasers.
- **Transactional:** Klaviyo lets you mark specific flow messages transactional,
  which typically requires approval and restricts promotional content. Use it
  for touches 1–2 only if the store platform isn't already sending them; don't
  send two order confirmations.
- **Delivery wait:** delivery events depend on your shipping integration. If
  you have a delivered metric, run a second flow triggered by it for touches
  3–6. If not, time delay from fulfillment + transit estimate, labeled as an
  estimate.
- **Holdout:** random-sample condition in a conditional split if your account
  has it; otherwise write a random bucket property at entry and split on it.
  The control branch goes to an empty path. The property must persist so the
  delivery-triggered flow honors it.
- **Smart Sending:** off for transactional; on or deliberately set for 3–6.
- **Exits:** flow filters are re-checked before each send: "placed order zero
  times since starting this flow" removes second-order buyers; a returned or
  refunded metric removes returners.

## Iterable

- **Entry:** journey on a custom `orderPlaced` event with an order-count filter,
  or API-triggered.
- **Message types:** put touches 1–2 in a transactional message type (bypasses
  marketing unsubscribes); 3–6 in a marketing type.
- **Holdout:** Randomized Split tile at entry to an empty path, and write the
  assignment to a user field so the transactional templates can read it.
  Iterable also offers journey-level holdout options in some plans; check yours.
- **Wait:** wait-for-event tile on `orderDelivered` with a timeout fallback.
- **Exits:** journey exit rules on second `orderPlaced` and on
  `orderReturned` / `orderCancelled`.

## SFMC

- **Entry source:** API event from the order system, or a data extension that
  receives first-order rows.
- **Transactional:** Transactional Messaging API or triggered sends with a
  transactional send classification for 1–2. Marketing touches use a commercial
  send classification.
- **Holdout:** Random Split activity at the start; the control path goes to a
  join with no sends. Write the flag back to the contact data extension so
  transactional content can reference it with AMPscript.
- **Wait:** Wait by Duration for spacing; Wait Until Event / Wait by Attribute
  for delivered status, with a maximum wait.
- **Exits:** Journey Goal on second purchase; Exit Criteria on returned or
  cancelled status.

## Gotchas

- **Order-count race.** The order event fires before the order count updates,
  so every buyer looks like a first-timer (or none do). Test with a repeat buyer.
- **Double confirmations.** The store platform and the ESP both send an order
  confirmation. Decide who owns 1–2 before you build.
- **Holdout doesn't reach transactional templates.** The journey holds out
  control, but the order email still shows the modules to everyone. Either
  mirror the flag or document that the holdout measures touches 3–6 only.
- **No delivered event.** Touch 4 silently falls back to ship date and you've
  rebuilt the thing this program exists to fix.
- **Split shipments.** One order, three deliveries. Key the clock to the
  delivery of the primary item, or the last one; decide and document it.
- **Welcome not exiting.** Welcome keeps sending "first order" offers after
  purchase. That's a welcome bug, but it breaks this program.

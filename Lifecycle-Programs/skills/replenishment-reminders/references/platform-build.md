# Platform build: Replenishment Reminders

Structural guidance, not screenshots. Platform features change; confirm current
component names in your account before building. One principle holds on every
platform: **compute the depletion and reminder dates in the data layer** (CDP,
warehouse, or a nightly job), write them to the profile or a table, and let the
ESP read them. Date math inside a chain of wait steps is where these programs
break.

The data layer produces one row per active customer-SKU episode:
`customer_id, sku, qty_bucket, purchase_date, cycle_days, reminder_date,
nudge_date, checkin_date, lapse_date, on_time_reorder_count, holdout_flag`.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Action-based entry on a purchase custom event with SKU properties, or API/scheduled entry from the episode table on `reminder_date` | Date-property-triggered flow on a profile date (e.g. `next_reminder_date`), or "Placed Order" metric trigger | Event-triggered entry on purchase, or scheduled entry from a list/segment on `reminder_date = today` | Data extension entry source fed daily by an Automation Studio SQL query on the episode table |
| Filter | Entry audience filters: consent, not subscribed to SKU, not gift, `holdout_flag = false` | Flow filters: consent, not subscriber, "Placed Order zero times since starting this flow" | Entry and journey filters on user fields and events | Entry criteria on the data extension; decision split for consent |
| Split | Audience Paths (attributes: graduation count, SMS consent); Experiment Paths for random splits | Conditional split on profile properties; holdout via a random bucket property (see below) | Randomized Split tile; attribute/event splits | Random Split activity; Decision Split on attributes |
| Wait | Delay step: "until a specific day" or personalized from an attribute/context variable | Time delay; or separate date-property flows per touch | Delay tile; wait-for-event tile with timeout | Wait by Attribute (on `nudge_date`, `checkin_date`); Wait by Duration |
| Exit | Exit criteria: performs purchase of SKU; subscription started event; attribute change | Flow filter re-evaluated before each send; profile property updates | Journey exit rules on purchase and subscription events | Goal and Exit Criteria on the data extension (reorder flag, subscriber flag) |
| Holdout | Canvas control group variant (sticky per user), or a sticky attribute-based holdout filtered at entry | Random bucket profile property (0–99) assigned once; conditional split sends bucket < 10 to an empty path | Randomized Split to an empty path keyed on a sticky field, or journey holdout if your plan has it | Random Split to an empty path, but make it sticky: assign `holdout_flag` in the data extension once, filter on it |

## Braze

- **Entry:** prefer scheduled or API-triggered entry from the episode table on
  `reminder_date`. If you use action-based entry on purchase, allow re-entry
  (every purchase is a new episode) and pass SKU, quantity, and cycle as
  properties.
- **Steps:** Audience Paths (graduated vs. default) → Message (touch 1 or G) →
  Delay until `nudge_date` → Audience Paths on SMS/push consent → Message
  (touch 2) → Delay until `checkin_date` → Message (touch 3) → end.
- **Exit criteria:** purchase event containing the episode SKU (or a larger
  size of it); subscription started for that SKU; refund event.
- **Holdout:** a Canvas control variant works, but check that assignment is
  sticky for the same user across re-entries. If not, assign `holdout_flag`
  once in the data layer and filter on it. Leave the global control group on;
  it's a separate, company-wide measure.
- **Frequency capping:** decide with `journey-architecture` whether this Canvas
  is exempt. I'd exempt touch 1 only; a capped reminder that never lands is a
  lost reorder.

## Klaviyo

- **Trigger:** a date-property-triggered flow on `next_reminder_date` is the
  cleanest. Your data layer rewrites the property after each order. A
  "Placed Order" trigger with a fixed time delay works for a single-SKU catalog
  and breaks for anything with multiple cycles.
- **Filters:** "Placed Order zero times since starting this flow" (or a
  SKU-specific equivalent via a profile property) is the exit. Klaviyo re-checks
  flow filters before each send, which is what you want.
- **Holdout:** assign a random 0–99 bucket to each profile once, never
  overwrite it, and conditional-split bucket < 10 into a path with no messages.
  Flow A/B tests are for content variants, not for a no-send control.
- **Smart Sending:** it can silently skip touch 1 if the customer got a campaign
  that day. Consider turning it off for touch 1 and leaving it on for 2 and 3.
- **SMS:** separate consent; put touch 2's SMS behind a conditional split on SMS
  consent, email fallback on the other branch.

## Iterable

- **Entry:** event-triggered on purchase with re-entry allowed, or a scheduled
  journey entering users where `reminder_date` is today.
- **Tiles:** Randomized Split (holdout) → attribute split (graduated) → Send →
  Delay / Wait-for-event (purchase of SKU, timeout = until nudge date) → Send →
  Wait-for-event (timeout = until check-in) → Send.
- **Exit rules:** journey-level exit on purchase and subscription events.
  Wait-for-event tiles double as early exits between touches.
- **Holdout:** make it sticky. A Randomized Split re-rolls on every re-entry
  unless you key it on a persistent field.

## SFMC

- **Entry source:** a data extension refreshed daily by an Automation Studio
  SQL query that selects episodes where `reminder_date = today`.
- **Activities:** Decision Split (holdout flag, graduation) → Email → Wait by
  Attribute (`nudge_date`) → Decision Split (SMS consent) → MobileConnect SMS
  or Email → Wait by Attribute (`checkin_date`) → Email.
- **Goals and exit criteria:** exit when the data extension's `reordered_flag`
  or `subscriber_flag` is true. Exit criteria are evaluated on a schedule, so
  refresh those flags before the journey's evaluation runs.
- **Holdout:** assign `holdout_flag` in the source data extension once. A Random
  Split activity alone is not sticky across re-entries.

## Gotchas

- **Re-entry:** every purchase is a new episode. If re-entry is off, the second
  cycle never starts. If it's on without a customer-SKU key, a reorder spawns a
  duplicate episode while the old one is still running.
- **Multi-SKU baskets:** one order with three replenishable SKUs becomes three
  episodes. Consolidate in the data layer, not in the ESP.
- **Off-site reorders:** marketplace and retail purchases are invisible unless
  you ingest them. Without that signal, touch 2 and 3 will hit people who
  already reordered elsewhere. The snooze and "I'm set" links are your backstop.
- **Out of stock:** check inventory at send time, not at entry. A reorder link
  to an empty product page is worse than no email.
- **Price changes:** the prefilled cart must show the current price, not the
  price from the last order.
- **Time zones:** date-based waits resolve in the platform's zone unless told
  otherwise. Set send time in the customer's local zone.

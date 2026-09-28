# Platform build: Winback Series

Structural translation of the five primitives. Component names and settings,
not screenshots. The hard part of winback in every ESP is the same: lapse is
the absence of an event, so entry is a scheduled audience evaluation, not a
real-time trigger.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Scheduled daily entry; audience = segment with "last purchased" between L and L+1 day (custom attribute or purchase filter) | Segment-triggered flow on a "days since last order ≥ L" segment, or date-property trigger on a computed next-lapse date | Scheduled journey entry from a list/segment refreshed daily with the lapse condition | Scheduled Data Extension entry; DE rebuilt daily by a SQL query activity computing days since last order |
| Filter | Entry audience filters + Audience Paths; subscription group and consent checks | Flow filters (re-evaluated before each step) + profile filters on consent | Entry filters + "Filter" tiles before sends | Entry criteria on the DE + Decision Split on consent fields |
| Split | Audience Paths (tier, flags); Experiment Paths for random arms | Conditional split (tier, flags); Random sample split for arms | Attribute split; Randomized split tile | Decision Split (tier, flags); Random Split activity |
| Wait | Delay step; Action Paths with "made purchase" and a timeout | Time delay; "wait until" via conditional split after delay on "Placed Order since starting this flow" | Delay tile; Wait for event with timeout | Wait by Duration; Wait Until Event (with custom event from orders) |
| Exit | Exit criteria: "performs Purchase"; exception events; unsubscribe | Flow filter "Placed Order zero times since starting this flow" (removes on next evaluation) | Exit rule on purchase event; global unsubscribe | Goal (purchase) with exit on goal met; exit criteria on consent fields |
| Holdout | Canvas-level control group (sticky per user within the Canvas) or Experiment Path with a no-message branch | Random sample split to an empty branch; tag profiles in that branch with a property so re-entry stays in control | Journey holdout group, or randomized split to an exit tile with a user-field flag | Random Split to an empty path that updates a DE flag; filter re-entrants on that flag |

## Braze

- **Entry:** scheduled daily at a fixed time. Entry audience: "Last purchased
  more than L days ago" and "less than L+1 days ago," plus the at-risk entry
  for touch 1 as a separate short Canvas or an early path. Allow re-entry only
  after a purchase; use the "re-eligibility" window set to at least L.
- **Exit criteria:** Purchase (any product) plus your custom offline-order
  event. Put the same check in an Action Path before touches 4 and 5 so a late
  offline order still removes them.
- **Tiers:** Audience Paths on a value-tier custom attribute written by your
  model or warehouse sync. Offer eligibility as a boolean attribute computed
  upstream; don't compute break-even inside Canvas.
- **Control:** Canvas control group keeps assignment sticky within the Canvas.
  If you rebuild the Canvas, assignment resets; write the arm to a custom
  attribute on first entry to survive rebuilds. Decide whether the global
  control group also applies, and exclude it from the read if it does.
- **Frequency:** respect global frequency capping; set Canvas priority below
  cart and browse abandon.

## Klaviyo

- **Trigger:** segment-triggered flow on a segment defined as "Placed Order
  zero times in the last L days" and "at least once over all time." Segment
  triggers fire when a profile joins, so backfill needs a one-time decision.
  Alternative: a date-property trigger on a computed `next_lapse_date` synced
  from your warehouse, which gives cleaner timing.
- **Flow filters:** "Placed Order zero times since starting this flow" and
  consent filters. Klaviyo re-checks flow filters before each step, which is
  your purchaser exit.
- **Splits:** conditional split on value tier and offer eligibility properties;
  random sample split for the holdout, sending the control branch to an
  "Update profile property" action (arm = control) and nothing else.
- **Smart sending:** leave it on for touches 1–3; consider off for touch 4 only
  if the code has a hard expiry, and check against your frequency policy.
- **Codes:** use unique coupon codes from the coupon library, single-use,
  with an expiry matching the offer strip.

## Iterable

- **Entry:** scheduled journey from a dynamic list refreshed daily with the
  lapse condition. Journey "entry limit" set to once per lapse cycle.
- **Filters:** Filter tiles before each send on consent and offer eligibility.
- **Holdout:** journey holdout group for program-level lift, or a Randomized
  Split with a control branch that sets a user field and exits.
- **Exit rules:** exit on purchase event and on your custom offline-order
  event. Verify exit rules apply to users sitting in a Delay tile.

## SFMC

- **Entry source:** a Data Extension rebuilt daily by a SQL Query Activity in
  Automation Studio (days since last order, tier, offer eligibility, arm).
  Journey entry schedule matches the automation.
- **Splits:** Decision Split on tier and eligibility; Random Split for the
  holdout, with the control path writing the arm to a DE and ending.
- **Waits:** Wait by Duration between touches; Wait Until Event if you publish
  an order event.
- **Goal and exit:** Goal = purchase in the orders DE, "exit on goal met."
  Exit criteria on consent fields, evaluated at each wait.

## Gotchas

- **Order data lag.** If orders sync nightly, a morning send can reach someone
  who bought last night. Schedule sends after the sync lands, and re-check
  before offer touches.
- **Backfill blast.** Turning the program on for the whole existing lapsed pool
  sends touch 2 to tens of thousands on day one. Stagger backfill over a week
  and warm deep-lapsed addresses carefully, or leave them to the sunset policy.
- **Holdout reset on rebuild.** Cloning or rebuilding a journey resets
  platform-native control groups. Persist the arm on the profile.
- **Stacking.** A sitewide promo code plus the winback code on the same order
  doubles the incentive cost. Block stacking at checkout, not in the email.
- **Marketplace and store orders.** If they don't reach the ESP, your purchaser
  exit is blind to them. Say so in the readout.

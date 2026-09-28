# Platform build: loyalty program

Structural translation of the five primitives. Component names and settings,
not screenshots. Check your platform's current docs; names shift.

## Where the ledger lives

The points ledger almost never lives in the ESP. It lives in a loyalty platform
or the commerce backend, which owns earn rules, balances, tiers, and expiry. The
ESP consumes what the ledger emits:

- **Events:** `enrolled`, `points_posted`, `points_redeemed`, `tier_changed`,
  `balance_threshold_crossed`, `order_placed`.
- **Attributes:** `points_balance`, `points_pending`, `next_reward_threshold`,
  `tier`, `tier_progress`, `points_expiring`, `points_expiry_date`,
  `accelerator_bucket`, `accelerator_window_end`.

The accelerator holdout is the one place this matters most. The random bucket
must be assigned upstream, where the earn rule runs, and synced to the ESP as an
attribute. If the ESP assigns the bucket and the ledger doesn't know, holdout
members still earn accelerated points on their own, and your control is
contaminated.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Action-based entry on custom event (`points_posted`, `tier_changed`) or scheduled entry for statements | Metric-triggered flow on API event; date-property trigger for expiry | Journey entry on custom event; scheduled or list entry for statements | API Event entry source; Data Extension entry for scheduled sends |
| Filter | Entry audience filters on custom attributes and subscription state | Flow filters plus trigger filters on event properties | Entry rules and filter tiles on user fields | Entry criteria on the Data Extension; Decision Split for re-checks |
| Split | Audience Paths (attribute); Decision Split | Conditional split on profile property | Attribute split tile | Decision Split |
| Wait | Delay step; Action Paths for wait-until-event | Time delay; conditional split after delay to check for purchase | Delay tile; wait-for-event tile | Wait by Duration; Wait by Attribute; Wait Until Date |
| Exit | Exit criteria on `order_placed` / `points_redeemed` | Flow filter re-evaluated per step ("has placed order zero times since starting this flow") | Exit rules on event | Goal or Exit Criteria on the journey |
| Holdout | Audience Paths on upstream `accelerator_bucket`; Canvas control group only if bucket is also honored in the ledger | Conditional split on upstream `accelerator_bucket` to an empty branch | Attribute split on `accelerator_bucket` to an exit | Decision Split on `accelerator_bucket` to an exit |

For every platform: the holdout split reads the upstream bucket. Platform-native
random splits and control groups are fine for comms-only tests, but not for the
accelerator, because the ESP can't stop the ledger from awarding bonus points.

## Braze

- **Entry:** one action-based Canvas per event touch (enrollment, first earn,
  near-reward, reward available, tier-up); one scheduled Canvas for statements
  and expiry, evaluated daily on `points_expiry_date`.
- **Accelerator Canvas:** enter on `order_placed` where order count = 2 and
  `accelerator_bucket` = treated. Delay, then Action Path waiting for
  `order_placed` until `accelerator_window_end`.
- **Exit criteria:** `order_placed` exits near-reward and accelerator Canvases;
  `points_redeemed` exits reward-available and expiry.
- **Frequency capping:** respect global caps; mark the expiry warning as exempt
  only if program terms require the notice (confirm with the terms owner).
- **Liquid:** every balance and date field needs a `default` fallback, and the
  send is aborted if balance is missing on a balance-gated touch.

## Klaviyo

- **Triggers:** metric-triggered flows on the loyalty platform's API events;
  date-property flow on `points_expiry_date` for touch 9.
- **Filters:** flow filters re-evaluate at each step; use "has placed order
  zero times since starting this flow" for purchase exit.
- **Holdout:** conditional split on the upstream `accelerator_bucket` profile
  property, with the holdout branch ending immediately. Flow A/B tests are for
  content, not for this holdout.
- **Smart Sending:** on for promotional touches (3, 4, 10); consider off for
  expiry if terms treat it as a required notice.
- **Balance freshness:** profile properties are only as current as the last
  sync. Confirm sync cadence before trusting balance-gated sends.

## Iterable

- **Entry:** journeys triggered by custom events; a scheduled journey or list
  refresh for statements and expiry.
- **Split:** attribute split on `accelerator_bucket` and `tier`.
- **Waits:** wait-for-event on `order_placed` with a timeout at
  `accelerator_window_end`.
- **Exit rules:** journey-level exit on `order_placed` and `points_redeemed`.
- **Data freshness:** user fields updated by API; confirm the loyalty platform
  updates balance before the event that triggers a send, or add a short delay.

## SFMC

- **Entry source:** API Event from the loyalty platform for event touches; a
  daily-refreshed Data Extension for expiry and statements.
- **Splits:** Decision Split on `accelerator_bucket`, `tier`, and balance band.
- **Waits:** Wait by Duration for cooldowns; Wait Until Date on
  `accelerator_window_end` and expiry dates.
- **Goals and exit criteria:** goal = `order_placed` in the accelerator
  journey; exit criteria on redemption and unenroll.
- **Contact re-entry:** configure re-entry for near-reward and reward-available
  so members can enter again after each reward, with cooldowns.

## Gotchas

- **Pending vs. posted points.** Showing pending points as spendable is the
  fastest way to a support-ticket spike.
- **Event before attribute.** A `balance_threshold_crossed` event that arrives
  before the balance attribute updates renders the old balance.
- **Returns.** Points reversed by a return must re-gate touches 4, 5, and 9.
- **Timezones on expiry.** "Expires in 7 days" computed in UTC can be off by a
  day for some members.
- **Double sends.** Near-reward and reward-available can fire within hours for
  one large order. Suppress 4 when 5 fires within 48h.
- **Holdout drift.** Anyone added to the bucket logic later (a new market, a new
  app) must be randomized the same way, or the arms stop being comparable.

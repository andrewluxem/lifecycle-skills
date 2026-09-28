# Platform build: Welcome Series

Structural only: component names and settings, not screenshots. Platform menus
move. If a component name here doesn't match your account, the primitive is
what matters; find the equivalent and say so in the build notes.

## Primitive map

| Primitive | Braze (Canvas) | Klaviyo (Flows) | Iterable (Journeys) | SFMC (Journey Builder) |
|---|---|---|---|---|
| Trigger | Action-based entry on the opt-in custom event or subscription-state change | List-triggered or metric-triggered flow on the opt-in | Journey entry on list subscription or a custom opt-in event | API Event or Data Extension entry source written by the signup form |
| Filter | Entry audience filters; message-level audience re-checks | Flow filters (re-evaluated before every step) | Entry filters plus Filter or Yes/No Split tiles before sends | Entry filter criteria; Decision Split before each send |
| Split | Audience Paths / Decision Split | Conditional split | Yes/No Split, Attribute Split | Decision Split |
| Wait | Delay step; Action Paths to wait-until-order | Time delay | Delay tile; wait-for-event where available | Wait by Duration; Wait Until Event where licensed |
| Exit | Canvas exit criteria on the order event | Flow filter "placed order zero times since starting this flow" | Journey exit rules on the order event | Exit Criteria and Goal on the order DE |
| Holdout | Canvas-level control variant (not the global control group) | Random-sample conditional split to an empty branch, or a hashed profile property | Randomized Split tile to an empty path, or a journey holdout if your account has one | Random Split to an empty path, logged to a DE |

## Braze

- **Entry:** action-based on the opt-in event. Carry signup source and category
  of interest as event or custom attributes. Entry window: each user once
  (re-eligibility off).
- **Entry audience:** email subscription opted-in; not in the global suppression
  segment; a "has ordered" attribute false for the five-touch path.
- **Structure:** Audience Paths at the top for prior-order (variant) versus new.
  Delays between messages. Before touch 4, a Decision Split on "no purchase since
  entry" even though exit criteria also cover it. Belt and braces.
- **Exit criteria:** exit on the purchase event (or your order custom event).
  Hand off by having `post-purchase` enter on the same event.
- **Holdout:** add a control variant at the Canvas level, sized per
  `measurement.md`. Don't use the global control group for this; it removes
  people from every program and answers a different question.
- **Frequency capping:** decide whether welcome is exempt from global caps.
  I'd exempt touch 1 and cap the rest. `journey-architecture` has the final say.

## Klaviyo

- **Trigger:** list-triggered on the newsletter list, or metric-triggered on the
  opt-in event if you capture source there. Metric triggers carry event
  properties into the flow, which helps the source split.
- **Flow filters:** "Placed Order zero times since starting this flow" is the
  purchaser exit. Flow filters re-evaluate before every step, which is why this
  works. Add "has not been in this flow before" if re-subscribers could re-enter.
- **Splits:** conditional split on "Placed Order at least once over all time" at
  the top for the variant; conditional split on signup source for the promised-
  incentive path.
- **Holdout:** a conditional split on a random-sample condition, if your account
  offers it, with an empty "yes" branch. If not, assign a random bucket property
  at signup (for example a hash of the profile ID mod 10) and split on it.
- **Smart Sending:** off for touch 1. Leave it on for 2–5 unless it's
  suppressing so much the holdout comparison gets muddy; record the choice.

## Iterable

- **Entry:** list subscription or a custom opt-in event. Set entry to once per
  user.
- **Filters:** entry filter on email opt-in; a Yes/No Split before touch 4 on
  "no purchase since entry."
- **Exit rules:** journey-level exit on the purchase event. Confirm the rule
  applies to users sitting in a Delay tile, not only between tiles.
- **Holdout:** Randomized Split tile at the very top with an empty path, or a
  journey holdout if your account has one. Log the assignment as a user field.
- **Variant:** Attribute Split on order history directly after the holdout.

## SFMC

- **Entry source:** API Event from the signup form, or a Data Extension the form
  writes to. Set contact re-entry to "no re-entry."
- **Splits:** Random Split first for the holdout (empty path writes to a logging
  DE). Decision Split on order history for the variant.
- **Waits:** Wait by Duration between touches.
- **Exit Criteria and Goal:** set the Goal to "placed an order" and Exit
  Criteria on the same order DE. Exit criteria are evaluated as contacts leave
  wait activities, so the order DE must refresh before each wait ends. A nightly
  refresh with a morning send is the classic welcome bug on this platform.

## Gotchas

- **Order data latency beats every exit rule.** If orders reach the ESP in a
  nightly batch, every platform above will mail the offer to a same-day buyer.
  Stream the order event, or schedule touches 4 and 5 after the batch lands.
- **Marketplace and in-store orders.** If a subscriber buys through a channel
  that doesn't reach the ESP, they're still a purchaser. Match what you can;
  document what you can't.
- **Holdout assigned at send, not entry.** Some A/B features split per message.
  That's not a holdout. Assignment must happen once, at entry.
- **Promised-incentive codes in touch 1.** If the code comes from a shared pool,
  touch 4 must reference the same code, not generate a new one.
- **Re-subscriber detection.** A new email address for an old customer looks
  new. Match on customer ID where you can; accept some leakage where you can't.

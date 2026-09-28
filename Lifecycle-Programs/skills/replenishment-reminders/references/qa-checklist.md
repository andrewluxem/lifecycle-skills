# QA checklist: Replenishment Reminders

Pre-send checks a human runs before activation. This skill is read-only: it
never sends. Checks are ordered by cost of failure, most expensive first. Each is
a yes/no a reviewer can verify in the platform or the data layer.

## Blocking (do not activate until every box is checked)

- [ ] Exit on reorder verified with a live test profile: reorder the SKU after
      touch 1 and confirm touches 2, 3, and G never send.
- [ ] Exit on a larger size or higher quantity verified, and the next reminder
      date recomputed from the new order.
- [ ] Exit on subscription start verified; the profile lands in subscription
      onboarding and nowhere else.
- [ ] Exit on return or refund of the original order verified.
- [ ] Holdout split present, randomized at the customer level, sticky across
      re-entries and SKUs, and receiving nothing from this program.
- [ ] Active subscribers to the SKU cannot enter. Test with a subscriber profile.
- [ ] Gift orders (ship-to differs from bill-to) excluded at entry.
- [ ] Consent and suppression filters applied on entry and re-checked before
      each send, per channel.

## Timing and cycle data

- [ ] Reminder date for three sample SKUs (short, medium, long cycle) equals 75%
      of the observed cycle for the right quantity bucket, not the label.
- [ ] SKUs below the repeat-pair floor show their fallback source (category or
      label) and are flagged `[Assumption]` in the cycle table.
- [ ] Delivery lead time subtracted where it exceeds the threshold.
- [ ] Personal cycle replaces the SKU cycle for customers with 2+ reorders.
- [ ] A customer with three SKUs due within the consolidation window receives
      one message listing all three.
- [ ] Send time resolves to the customer's local zone.

## Content

- [ ] One-tap reorder link opens a prefilled cart with the correct SKU, size,
      and quantity, on mobile, while logged out.
- [ ] Cart shows the current price, not the historical one.
- [ ] Out-of-stock and discontinued SKUs hold the send or show the mapped
      substitute. Test with a flagged SKU.
- [ ] No discount appears in touches 1 or 2 unless an approved incentive test is
      running with its own holdout.
- [ ] Touch G appears only for profiles at or above the graduation threshold,
      and its subscription link prefills the observed cadence, not the label.
- [ ] Snooze and "I'm set / switched size" links write back to the profile and
      move the next date.

## Data and personalization

- [ ] Every dynamic field has a fallback (product image, size, order date,
      run-out date, delivery-by date).
- [ ] Run-out date and delivery-by date render as dates, in the customer's
      locale, and the delivery date is never after the run-out date in touch 1.
- [ ] Multi-quantity orders show the right quantity in the last-order block.

## Deliverability and compliance

- [ ] SMS sends only to profiles with SMS consent, inside quiet hours rules for
      the customer's zone, with STOP handling tested.
- [ ] Unsubscribe link present and working in every email.
- [ ] Touch 2 never goes by SMS and email on the same day.
- [ ] `journey-architecture` has confirmed priority against `post-purchase` and
      campaigns, and the frequency cap decision for touch 1 is recorded.

## After launch (first 72 hours)

- [ ] Entry volume matches the episode table's count for those days (within a
      few percent).
- [ ] Holdout share is ~10% of entrants.
- [ ] No profile received a touch after placing a qualifying order. Spot-check
      ten reorderers.
- [ ] Unsubscribe and complaint rates per send are inside the guardrails in
      `measurement.md`.
- [ ] Reorder link click-to-order rate isn't near zero. If it is, the link is
      broken before the program is.

# QA checklist: post-purchase

Pre-send checks a human runs before activation. This skill is read-only: it
never sends. Checks are ordered by cost of failure, most expensive first. Every
item is a yes/no a reviewer can verify in the platform with a test profile.

## Blocking (do not activate until every box is checked)

- [ ] Exit condition verified with a live test profile: a second order removes
      the profile from touches 3–6 and skips the cross-sell.
- [ ] Welcome → post-purchase handoff: a test profile that purchases mid-welcome
      exits welcome and enters this program exactly once.
- [ ] Return/refund/cancel exit: a test order marked returned stops the review
      ask and cross-sell.
- [ ] Holdout split present, randomized at entry, stored on the profile, and
      receiving nothing from touches 3–6.
- [ ] Control profiles receive touches 1–2 without the added modules (or it's
      documented that the modules go to everyone and the holdout measures 3–6
      only).
- [ ] Consent and suppression filters applied on entry and re-checked before
      each marketing send; transactional sends are not blocked by marketing
      unsubscribes.
- [ ] Repeat buyers do not enter (test with a profile that has prior orders,
      checking for the order-count race).
- [ ] Only one order confirmation and one shipping confirmation send per order.

## Content

- [ ] Touches 1–2 are primarily transactional: order/shipping information comes
      first and any module is secondary, non-promotional, and signed off by
      whoever owns compliance.
- [ ] No discount code in touches 1–2.
- [ ] The review ask does not offer an incentive conditional on a positive
      rating and does not route unhappy customers away from the public review
      form. Your legal or compliance owner confirms the review policy.
- [ ] Every touch has one CTA, and it lands on the right page (order status,
      tracking, guide, review form, single product).
- [ ] Cross-sell recommends one complementary item, never the item just bought.
- [ ] How-to content matches the product category the customer bought.

## Data and personalization

- [ ] Every dynamic field has a fallback (product name, image, guide URL).
- [ ] Touch 4 timing reads from the delivered event; the fallback when no
      delivery event arrives is ship date + median transit, and it's documented.
- [ ] Split shipments: the clock keys to the documented item (primary or last).
- [ ] TTFU class maps every product category; unmapped categories default to
      the slowest class, not the fastest.
- [ ] "Reviewed yet?" flag updates before touch 5 evaluates it.
- [ ] Cross-sell block excludes out-of-stock items and already-purchased SKUs.
- [ ] Consumable vs. durable flag is set for every SKU, so the handoff routes.

## Deliverability and compliance

- [ ] Transactional and marketing streams use the correct message type / send
      classification on each touch.
- [ ] Marketing touches 3–6 carry an unsubscribe link and physical address.
- [ ] SMS touches only go to profiles with the right SMS consent, within quiet
      hours for the recipient's time zone.
- [ ] Marketing touches sit inside global frequency caps; transactional touches
      sit outside them.

## After launch (first 72 hours)

- [ ] Entry count matches first-order count from the store for the same window
      (within a small tolerance).
- [ ] Holdout share of entrants is within a point of the configured split.
- [ ] No profile has received a touch after a second order or return.
- [ ] Unsubscribe and complaint rates on touches 3–6 are within guardrails.
- [ ] "Where is my order" contacts haven't moved against the pre-launch baseline.
- [ ] Append launch date, split, and read date to `.claude/decisions.md`.

# QA checklist: Winback Series

Pre-send checks a human runs before activation. This skill is read-only: it
never sends. Checks are ordered by cost of failure, most expensive first. Each
item is a yes/no a reviewer can verify in the platform with a test profile.

## Blocking (do not activate until every box is checked)

- [ ] Exit condition verified with a live test profile that meets it: a
      profile that places an order mid-wait leaves before the next send.
- [ ] Purchaser exit also fires on late-arriving orders (store, marketplace,
      phone) if those channels are in scope; if they aren't visible, the gap is
      written in the build notes.
- [ ] Holdout split present, randomized at entry, and receiving nothing from
      this program.
- [ ] Holdout assignment is sticky: a test profile that exits, buys, lapses
      again, and re-enters lands in the same arm.
- [ ] Consent and suppression filters applied on entry and re-checked before
      each send, per channel (SMS consent is separate from email).
- [ ] Offer gating: a Standard-tier profile reaches touch 4's position and sees
      no offer block.
- [ ] Offer gating: a serial-redeemer profile (code-driven reactivation in the
      last 12 months, no full-price order since) sees no offer block.
- [ ] Offer codes are unique, single-use, expire on the date the email states,
      and cannot stack with sitewide promo codes at checkout.
- [ ] Entry uses the brand's computed lapse line (L), not a default 90 or 180
      days, and the value is recorded in the build notes.

## Content

- [ ] No touch before 4 mentions or implies a discount.
- [ ] Touch 1 does not tell an at-risk customer they're lapsed.
- [ ] Every CTA lands on a live page; the offer CTA lands with the code applied.
- [ ] Expiry dates in copy match the code configuration.
- [ ] Touch 6 offers a real "less often" option that the preference center
      honors.
- [ ] No urgency claim that isn't true (no rolling "last chance").

## Data and personalization

- [ ] Every dynamic field has a fallback.
- [ ] Last-purchase block handles discontinued SKUs (fallback to category).
- [ ] What's-new block shows items launched after the customer's last order
      date, and falls back to brand-level if none.
- [ ] Category review block falls back to brand-level when a category has too
      few reviews.
- [ ] Value tier and offer eligibility attributes are populated for the whole
      entry audience; blank values default to Standard and no offer.

## Deliverability and compliance

- [ ] Deep-lapsed addresses (past 2L) checked against the sunset policy before
      any send; addresses past G are excluded.
- [ ] Backfill of the existing lapsed pool is staggered, not sent in one day.
- [ ] Unsubscribe link and physical address present; SMS carries opt-out
      language and respects quiet hours.
- [ ] Frequency caps and program priority confirmed with the owner of
      `journey-architecture` decisions (cart and browse abandon outrank this).

## After launch (first 72 hours)

- [ ] Entrant count per day matches pool sizing within tolerance.
- [ ] Holdout share of entrants is within a point of the configured split.
- [ ] No test or holdout profile received a send.
- [ ] Hard bounce and complaint rates on the first sends are inside the
      guardrails in `measurement.md`; if not, pause and review the deep-lapsed
      cut.
- [ ] At least one real purchaser exited correctly (check exit logs).
- [ ] Code redemptions come only from offer-eligible profiles.

# QA checklist: Cart Abandon

Pre-send checks a human runs before activation. This skill is read-only: it
never sends. Ordered by cost of failure, most expensive first. Every item is a
yes/no a reviewer can verify in the platform with a test profile.

## Blocking (do not activate until every box is checked)

- [ ] Purchase exit verified with a live test profile for **every** order
      channel (web, app, phone, store, marketplace). The profile leaves before
      the next send.
- [ ] Purchase during the first delay (before touch 1) prevents touch 1.
- [ ] Cart-emptied exit verified: empty the cart mid-sequence, no further sends.
- [ ] Holdout split present, randomized per person, sticky across re-entries,
      and the control branch contains no message steps.
- [ ] Holdout members are also suppressed from browse-abandon.
- [ ] Consent and suppression filters applied on entry and re-checked before
      each send (email unsubscribe, SMS opt-out, global suppression).
- [ ] SMS goes only to profiles with explicit SMS consent. A profile with email
      consent only receives zero SMS.
- [ ] SMS quiet hours enforced in recipient-local time: an abandon at 11 p.m.
      local sends touch 2 no earlier than the morning window.
- [ ] Incentive fence verified: a habitual-abandoner test profile and a
      discount-seeker test profile never reach touch 4.
- [ ] Incentive test split present inside the eligible branch, 50/50, with the
      no-incentive arm receiving nothing at touch 4.
- [ ] Re-entry lockout set (default 14 days) and tested with a second abandon.
- [ ] No other live flow triggers on the same cart or checkout event.

## Content

- [ ] Touches 1–3 contain no discount, code, or price-off language.
- [ ] Every touch has one CTA, and it lands on the restored cart (or checkout
      with the incentive applied, touch 4 only).
- [ ] Scarcity or low-stock language appears only when driven by live
      inventory data.
- [ ] Touch 3's proof element matches current policy (shipping threshold,
      returns window).
- [ ] Touch 4 states incentive terms and expiry, and does not stack with a
      running sitewide promotion.
- [ ] Legal footer, physical address, and unsubscribe link present on every
      email.

## Data and personalization

- [ ] Every dynamic field has a fallback.
- [ ] Cart block renders live price and stock at send time, not at entry.
- [ ] Sold-out items are hidden or labeled; a fully sold-out cart exits or
      falls back to a category link.
- [ ] Restore-cart link rebuilds the cart on a different device and after
      session expiry.
- [ ] Multi-item carts render correctly (1, 3, and 10+ items).
- [ ] Incentive codes are single-use, scoped to the cart or customer, and
      expire.
- [ ] First-time vs. repeat split reads a reliable order-count field.

## Deliverability and compliance

- [ ] Sending domain authenticated (SPF, DKIM, DMARC) for the stream the flow
      uses.
- [ ] Frequency-cap treatment agreed with `journey-architecture`.
- [ ] SMS program registration, opt-out keyword handling, and sender ID set up
      with the SMS provider.
- [ ] Regional consent rules checked for every market the flow reaches (some
      jurisdictions don't allow abandonment email without prior marketing
      consent; confirm with counsel, not with this skill).

## After launch (first 72 hours)

- [ ] Entry volume matches expected abandon volume (a big gap means a broken
      trigger or identity match).
- [ ] Holdout share of entrants is within a point of the configured split.
- [ ] Zero sends to profiles with a purchase after entry (spot-check 20).
- [ ] Unsubscribe, complaint, and SMS opt-out rates within guardrails.
- [ ] Touch 1 median send delay is inside the 30–60 minute target.
- [ ] No browse-abandon sends to anyone currently in cart-abandon.

# QA checklist: Welcome Series

A human runs these before activation. This skill is read-only: it never sends
email or SMS. Checks are ordered by cost of failure, most expensive first. Each
one is a yes/no a reviewer can verify in the platform.

## Blocking (do not activate until every box is checked)

- [ ] **Purchaser exit, live.** A test profile that orders between touch 2 and
      touch 4 exits the program and never receives touch 4 or 5.
- [ ] **Order latency measured.** You know how long an order takes to reach the
      ESP, and touches 4 and 5 are scheduled after that lag, not inside it.
- [ ] **Hand-off works.** The same test order enters the profile into
      `post-purchase`, once.
- [ ] **Offer fenced.** Touch 4 and 5 filters exclude purchasers, re-subscribers
      with prior orders, and anyone already holding a cart-abandon incentive.
- [ ] **Holdout present.** Randomized at entry, sized per `measurement.md`,
      receiving nothing from this program, and the assignment is logged where
      the analyst can query it.
- [ ] **Re-subscriber routing.** A test profile with a past order lands in the
      two-touch variant, not touch 1.
- [ ] **Consent and suppression** applied on entry and re-checked before each
      send, for email and, on touch 5, for SMS.
- [ ] **Re-entry off.** A profile that unsubscribes and re-subscribes does not
      restart the five-touch series.

## Content

- [ ] Touch 1 does not lead with a discount. If the form promised a code, the
      code is present and delivered plainly.
- [ ] No incentive appears in touches 1–3 (except a promised signup code).
- [ ] The offer's expiry in the copy matches the code's expiry in the system,
      including time zone.
- [ ] Touch 5 doesn't extend the offer or introduce a second one.
- [ ] Every proof element is real: reviews are genuine and current, claims are
      ones the brand can support.
- [ ] Each touch has one CTA, and it lands on a live, in-stock page.

## Data and personalization

- [ ] Every dynamic field has a fallback.
- [ ] Category blocks render for a profile with no category of interest.
- [ ] Product blocks exclude out-of-stock items.
- [ ] Re-subscriber blocks render for a customer whose last order was over a
      year ago.
- [ ] The offer block doesn't render, and the touch doesn't send, if the code
      pool is empty.

## Deliverability and compliance

- [ ] Sending domain authenticated (SPF, DKIM, DMARC aligned).
- [ ] One-click unsubscribe header present and the footer link works.
- [ ] Physical address and sender identity present.
- [ ] SMS touch honors quiet hours and carries opt-out language.
- [ ] Offer terms are stated and match what checkout will honor.

## After launch (first 72 hours)

- [ ] Pull every profile that received touch 4 and join to orders. Zero should
      have an order dated before the send.
- [ ] Holdout share of entrants is within a point of the target.
- [ ] Unsubscribe and complaint rates per send are inside the guardrails in
      `measurement.md`.
- [ ] Entry volume matches signup volume from the form, within the known
      consent drop-off.
- [ ] Nobody has entered twice.

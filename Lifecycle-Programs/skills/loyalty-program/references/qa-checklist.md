# QA checklist: loyalty program

Pre-send checks a human runs before activation. This skill is read-only: it
never sends. Most expensive failures first. Each item is a yes/no you can verify
in the platform or the ledger.

## Blocking (do not activate until every box is checked)

- [ ] Earn/burn table is filled, full-redemption cost is known, and the program
      breaks even without breakage.
- [ ] Finance has seen the points liability flag and sizing. (Not a sign-off on
      accounting from me; a confirmation that they know.)
- [ ] Accelerator holdout bucket is assigned upstream and honored by the ledger:
      a holdout test profile places order 3 and earns base points only.
- [ ] Holdout arm receives no touch 3 in any channel.
- [ ] Purchase exit verified: a test member who orders drops out of touches 3,
      4, 6, and 8 before the next scheduled send.
- [ ] Redemption exit verified: a test member who redeems stops getting touch 5
      and touch 9 for those points.
- [ ] Consent and suppression filters applied on entry and re-checked before
      each send.
- [ ] Lapsed members exit to `winback-series` and don't also receive loyalty
      promos.

## Content

- [ ] Every touch matches its spec: one job, one CTA, anti-goal respected.
- [ ] No touch presents pending points as spendable.
- [ ] Expiry warning states balance, date, and value, with no threatening
      framing.
- [ ] Accelerator touch doesn't read as a discount and doesn't stack with a
      same-day replenishment reminder.
- [ ] Tier touches only exist if the structure decision was tiers.
- [ ] Reward terms referenced in comms match the published program terms (the
      terms owner confirms; I don't).

## Data and personalization

- [ ] Every dynamic field has a fallback; balance-gated sends abort if balance is
      missing.
- [ ] Balance attribute refreshes before the triggering event is processed, or a
      delay covers the gap.
- [ ] Expiry dates render correctly in the member's timezone.
- [ ] Returns that reverse points re-gate touches 4, 5, and 9.
- [ ] Touch 4 doesn't fire when touch 5 fires within 48h.
- [ ] Category-aware product block falls back to bestsellers without order
      history.

## Deliverability and compliance

- [ ] SMS expiry warnings only go to members with explicit SMS consent.
- [ ] Promotional touches respect global frequency caps from
      `journey-architecture`.
- [ ] Unsubscribe links present on every promotional email; transactional
      notices classified as the terms owner has determined.
- [ ] Sending domain and IP warmed for the expected statement volume.

## After launch (first 72 hours)

- [ ] Holdout share in the first entrants is within ±1 point of the target.
- [ ] No holdout profile has an accelerated earn in the ledger.
- [ ] Unsubscribe and complaint rates per send at or below baseline.
- [ ] Support tickets mentioning points or balances checked daily.
- [ ] Reward cost as % of member sales tracking at or below the modeled rate.

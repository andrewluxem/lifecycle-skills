# Benchmarks: Welcome Series

Every number in this file is `[Assumption]`. None of it is cited, and none of it
is a measured result. These are starting points for a test, never targets. Once
you have one cycle of your own data, this file should stop mattering.

## Timing defaults

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| 1 Promise | Day 0, within 5 minutes of opt-in | Immediate only; don't test a delay here | `[Assumption]` |
| 2 Proof | Day 2 | Day 1–3 | `[Assumption]` |
| 3 Guide | Day 4 | Day 3–5 | `[Assumption]` |
| 4 Offer | Day 7, non-purchasers only | Day 5–9 | `[Assumption]` |
| 5 Last call | Day 10, 24–48h before expiry | Day 9–12 | `[Assumption]` |
| Program end | Day 14 | Day 12–21 | `[Assumption]` |
| R1 Welcome back | Day 0 | Immediate only | `[Assumption]` |
| R2 Next step | Day 3 | Day 2–5 | `[Assumption]` |

Why touch 1 isn't tested: I think opt-in intent decays in hours, and delaying the
first touch mostly measures how fast people forget they signed up `[Inference]`.
If you want to test something on touch 1, test the argument, not the clock.

Send time within a day: default to the subscriber's local mid-morning for
touches 2–5 `[Assumption]`. Touch 1 ignores this and fires on opt-in.

## Split defaults

- **Holdout:** 10% of entrants at entry `[Assumption]`. Raise to 20% for the
  first read when 12 days of signups can't reach the sample size in
  `measurement.md`. Drop back to 10% after a proven read, and keep a permanent
  5% after that `[Assumption]` so drift shows up.
- **A/B allocation inside treated:** 50/50 `[Assumption]`. One test at a time.
- **Minimum cell before a content A/B is worth running:** enough entrants that
  each arm reaches the sample size for the metric you're testing. For a
  first-purchase rate test at a 3% baseline `[Assumption]`, that's roughly 2,500
  per arm to detect a move to 4.5% `[Assumption]`. Smaller lifts need far more.
  Below that, don't split; ship the default and read the holdout.
- **Category split threshold:** only when at least a third of entrants carry the
  attribute `[Assumption]`.

## Content defaults

What each touch typically carries:

| Touch | Carries | First test worth running |
|---|---|---|
| 1 Promise | One brand idea, bestsellers block, preference link | The argument: origin vs. method vs. customer outcome |
| 2 Proof | Review strip, most-reviewed products | Reviews vs. UGC photos |
| 3 Guide | Starter guide or quiz, category bestsellers | Quiz vs. static "start here" pick |
| 4 Offer | Offer block, expiry, terms, bestsellers | Offer type (percent, fixed amount, free shipping, gift) |
| 5 Last call | Expiry, guarantee strip, one product | Email only vs. email + SMS for SMS-consented |

Tests ranked by expected value `[Inference]`:

1. **Offer type and size on touch 4.** It's where margin is spent and where the
   kill condition points first. Free shipping versus a percent-off often costs
   very differently at the same perceived value `[Assumption]`.
2. **Offer timing: day 7 versus day 5.** Earlier catches more people before they
   drift; later protects more full-price buyers. Only the holdout-adjusted
   revenue tells you which wins.
3. **Touch 1 argument.** Highest reach of any touch.
4. **Guide format on touch 3.** Matters most for catalogs where "which one?" is
   the real stall.

Discount sizing rule of thumb: the offer should cost less than the gross margin
on the incremental first orders it creates. Worked in `measurement.md`.

## How to replace these numbers

- **Baseline 30-day purchase rate for new subscribers:** new opt-ins in a past
  month, joined to orders within 30 days of opt-in, divided by opt-ins. Use a
  month before any welcome existed if you have one; otherwise use the holdout
  after cycle one.
- **Timing:** time from opt-in to first order for subscribers who bought
  unprompted (holdout). The median and 75th percentile tell you when the natural
  buyers show up; the offer should come after most of them.
- **Offer response:** redemption rate among treated non-purchasers on touch 4,
  and the full-price first-purchase rate in treated versus holdout.
- **Unsubscribe and complaint baselines:** per-send rates from your own BAU
  program over the last 90 days.

After one full cycle, replace every row above with your own number and relabel
it `[Evidence]`.

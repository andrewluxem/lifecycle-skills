# Measurement: loyalty program

The primary KPI, guardrails, holdout recipe, and kill condition also appear in
SKILL.md. This file carries the detail.

## Primary KPI

**Incremental share of wallet** on the earn accelerator.

True share of wallet is member spend ÷ member's total category spend. The
denominator is unobservable for most brands. So the read is:

**Incremental net spend per member after reward cost** =
(treated net spend per member − holdout net spend per member)
− (treated reward cost per member − holdout reward cost per member)

- **Net spend:** revenue net of discounts and returns.
- **Reward cost:** points burned × cost per point, plus expected cost of
  outstanding accelerated points at the modeled redemption rate.
- **Window:** 180 days from accelerator eligibility (after order 2).
- **Why not opens, clicks, or member revenue:** members who'd have bought anyway
  inflate every one of those. Only the holdout comparison removes them.

If you do have a category-spend estimate (survey, panel, or third-party data),
divide by it and report true share of wallet alongside. Label that denominator
`[Assumption]` unless it's measured for your members.

**Secondary (powered) metric:** third-purchase rate within 90 days of order 2.
It's binary, so it needs a smaller sample, and it's the early-life leak itself.

## Guardrails

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Reward cost as % of member sales | ≤ modeled full-redemption rate (5.0% default `[Assumption]`) | Pause accelerator; review earn rate with finance |
| Gross margin rate on member orders | Falls ≤ 1 point vs. pre-launch `[Assumption]` | Investigate stacking with promos; cap stacking |
| Unsubscribe rate per promotional send | ≤ brand baseline | Cut touch 4 or 10 frequency first |
| Complaint rate per send | ≤ brand baseline and platform limits | Pause the offending touch |
| Points liability growth | Reported to finance monthly; no threshold of mine | Finance decides |
| Redemption rate vs. model | Within ±10 points of modeled rate | If higher, rerun economics; if much lower, check reward usability, not a win |
| Cannibalization of replenishment | Replenishment conversion rate not down vs. pre-launch | Tighten suppression between programs |

A low redemption rate is not good news. It usually means the reward is hard to
use or members don't know they have it. Treat it as a bug to investigate.

## Attribution

- **Window:** 180 days from eligibility.
- **Program-influenced:** any member in the treated arm, whether or not they
  opened anything. Intent-to-treat, always.
- **Last-touch attribution is ignored for the lift claim.** It credits the
  loyalty email with orders the member was placing anyway. The holdout
  comparison overrides it every time.
- The overall program (base earn) usually can't be held out once public. Say so
  in every readout. We measure the accelerator and the comms, not "loyalty."

## Holdout recipe

- **What's held out:** the earn accelerator and touch 3. Holdout members keep
  base earn, transactional notices, touch 9 expiry warnings, and statements.
- **Size:** 10% default; up to 30% when eligible volume is low.
- **Randomization unit:** the member.
- **Assignment point:** at eligibility (order 2 placed), upstream in the loyalty
  platform, before any send. Never at send.
- **Duration:** until each arm reaches the sample size below, then 180 days for
  the spend read.
- **Terms check:** confirm with whoever owns program terms that bonus offers can
  be withheld from a random group. That's their call, not mine.

### Sample-size reasoning (for the powered third-purchase metric)

Two-proportion test, α = 0.05 two-sided, power 80% (z-sum ≈ 2.80, squared
≈ 7.84).

n per arm ≈ 7.84 × [p₁(1 − p₁) + p₂(1 − p₂)] ÷ (p₂ − p₁)²

| Input | Value | Label |
|---|---|---|
| Baseline third-purchase rate (p₁) | 25% | `[Assumption]` |
| Minimum detectable effect | +2 points (p₂ = 27%) | `[Assumption]` |
| n per arm | 7.84 × (0.1875 + 0.1971) ÷ 0.0004 ≈ **7,540** | `[Inference]` |
| Holdout share | 10% | `[Assumption]` |
| Eligible members needed | 7,540 ÷ 0.10 ≈ **75,400** | `[Inference]` |

At 10% holdout, that's a lot of second-time buyers. If you won't reach it in a
quarter, raise the holdout toward 30% (≈25,100 eligible) or accept a larger MDE.
Say which you chose and why in the readout.

Net spend per member is continuous and noisy. Read it with a confidence interval,
not a single delta, and expect it to need more members than the binary metric.

## Kill condition

If at the 26-week read (180 days after both arms reach sample size) the treated
group doesn't beat the holdout on net spend
per member after reward cost, with the 90% confidence interval's lower bound
above $0, we turn the accelerator off, keep base earn, and take the next bet to
the mid-life statement or back to `retention-diagnosis`. Separately: if observed
redemption runs above the modeled rate for two straight quarters and the P&L
only clears on breakage, we freeze new creative and redesign the earn rate with
finance.

**What I'd try next if it triggers:** a shorter accelerator window (the leak may
be earlier than the median interval), a smaller multiplier with a different
reward, or checking whether the leak is really a product or replenishment-timing
problem that `replenishment-reminders` or `retention-diagnosis` should own.

## Readout template

| Line | Treated | Holdout | Delta | 90% CI | Label |
|---|---|---|---|---|---|
| Members in arm | | | — | — | `[Evidence]` |
| Third-purchase rate (90d) | | | | | `[Evidence]` |
| Net spend per member (180d) | | | | | `[Evidence]` |
| Reward cost per member (180d) | | | | | `[Evidence]` |
| **Net spend after reward cost** | | | | | `[Evidence]` |
| Unsubscribe rate per send | | | | — | `[Evidence]` |
| Gross margin rate | | | | — | `[Evidence]` |
| Observed redemption rate | | — | vs. model | — | `[Evidence]` |
| Base program held out? | No — measured accelerator and comms only | | | | `[Fact]` |
| Decision | Continue / kill / modify | | | | |

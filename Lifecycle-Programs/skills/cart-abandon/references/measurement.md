# Measurement: Cart Abandon

The full plan. The primary KPI, guardrails, holdout recipe, and kill condition
also live in SKILL.md; this file carries the definitions and the math.

## Primary KPI

Co-primary, and always reported together:

- **Incremental recovered revenue per entrant** =
  (net revenue from orders placed within 7 days of entry, treated ÷ treated
  entrants) − (same, holdout ÷ holdout entrants).
- **Incremental margin per entrant** =
  (gross margin on those orders, net of incentive cost and message cost,
  treated ÷ treated entrants) − (same, holdout ÷ holdout entrants).

Report **margin per recovered order** (treated and holdout) next to them. If
revenue per entrant goes up and margin per recovered order goes down, the
program is buying orders, and the second number tells you how much it's paying.

**Window:** 7 days from entry `[Assumption]`. Long enough to capture the
considered buyer, short enough that the next cart doesn't blur the read.

**Why not opens, clicks, or "recovered revenue" from the ESP dashboard:** those
count every order from anyone who got a message, including the ones who were
coming back anyway. They measure attribution, not recovery.

**Unit:** per entrant, not per recipient of a specific touch. Touch-level
denominators hide the people who got nothing because they already bought.

## Guardrails

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Email unsubscribe rate per send | > 0.5% on any touch `[Assumption]` | Review that touch's timing and relevance; pause it if it persists for 2 weeks |
| Spam complaint rate | > 0.1% `[Assumption]` | Pause the program; check frequency collisions with `journey-architecture` |
| SMS opt-out rate per send | > 2% `[Assumption]` | Pause touch 2; review timing and consent source |
| Share of recovered orders using a program code | > 30% of treated recoveries `[Assumption]` | Tighten the fence; check for code leakage |
| Margin per recovered order, treated vs. holdout | Treated more than 10% below holdout `[Assumption]` | Incentive is eating margin; go to the kill-condition sequence early |
| Repeat-abandon rate among entrants | Rising for 3 straight weeks vs. the holdout | Training effect; remove touch 4 and re-read |
| Full-price order rate in the incentive test | Incentive arm below no-incentive arm | Incentive is cannibalizing; remove touch 4 |

## Attribution

- **What counts:** any order from the entrant, any channel, within 7 days of
  entry, whether or not they opened or clicked. Same rule for holdout.
- **What doesn't:** ESP last-touch attribution. It's fine for diagnosing which
  touch people were near when they bought. It never answers whether the program
  caused the order.
- **The holdout comparison overrides last-touch every time.** If the ESP says
  the flow drove $X and the holdout says incremental revenue was a third of
  that, the holdout is right. The difference is the organic return rate, and
  it's usually most of the "recovered" number `[Inference]`.

## Holdout recipe

- **Size:** 20% for the first read, 10% ongoing once proven.
- **Randomization unit:** person, not cart and not send. Assignment is sticky
  for the test period, so a shopper who abandons three times stays in one arm.
- **Assignment point:** at entry, before any wait. Assigning at send time
  leaves out people who purchased during the first wait and inflates the treated
  arm's apparent lift.
- **What control receives:** nothing from this program and nothing from
  browse-abandon. BAU campaigns continue for both arms.
- **Duration:** until the sample below is reached, with a floor of 4 full weeks
  to cover weekly cycles. Don't read early because the dashboard looks good.
- **Incentive test:** inside the eligible branch, 50/50 at touch 4, same
  person-level sticky assignment.

### Sample-size reasoning

Powering on recovery rate first, because it's the simplest:

| Input | Value | Label |
|---|---|---|
| Holdout 7-day recovery rate (p1) | 10% | `[Assumption]` |
| Treated 7-day recovery rate worth detecting (p2) | 13% (a 3-point lift) | `[Assumption]` |
| Significance (two-sided) | 0.05 (z = 1.96) | `[Assumption]` |
| Power | 80% (z = 0.84) | `[Assumption]` |
| Eligible entrants per week | 2,500 | `[Assumption]` |
| Coefficient of variation of margin per order | 0.8 | `[Assumption]` |

n per arm ≈ (1.96 + 0.84)² × [p1(1−p1) + p2(1−p2)] ÷ (p2 − p1)²
= 7.84 × (0.090 + 0.113) ÷ 0.0009 ≈ **1,770 per arm** `[Inference]`.

The control arm is the constraint. At a 20% holdout, 1,770 in control needs
about 8,850 entrants, roughly 3.5 weeks at 2,500 a week. At 10%, about 17,700
entrants, roughly 7 weeks.

Margin per entrant is noisier than a yes/no recovery, because order values
vary. With a margin CV of 0.8, variance inflates by about (1 + CV² − p) ÷ (1 − p)
≈ 1.7×, so plan on roughly **3,000 per arm**: about 15,000 entrants at a 20%
holdout, which is about **6 weeks** at the assumed volume `[Inference]`. That's
where the 6-week read date in the kill condition comes from. Recompute with
your own volume and recovery rate; if your volume is a quarter of this, the read
date moves out, not the rule.

**The incentive test is smaller and slower.** Only eligible shoppers who
haven't recovered by touch 4 are in it. Detecting 3% → 5% recovery at touch 4
needs about 1,500 per arm before the margin inflation `[Inference]`. At an
assumed 700 people reaching touch 4 a week `[Assumption]`, that's 4–5 weeks for
recovery and longer for margin. At the 6-week read the incentive test may be
underpowered. That's why the rule is "not positive → it comes out": an
incentive that can't show a positive point estimate in 6 weeks doesn't get to
stay on credit.

## Kill condition

Stated exactly as in SKILL.md:

> If incremental margin per entrant (treated minus holdout, net of incentive
> cost) is not positive at the 6-week read, I strip touch 4 first and re-read
> after 4 more weeks. If the no-incentive program still doesn't beat holdout on
> incremental margin, we stop the program and go back to `retention-diagnosis`;
> the leak isn't where we thought. Separately, if touch 4's incremental margin
> against its own no-incentive arm is not positive at the 6-week read, touch 4
> comes out regardless of the rest.

"Positive" means the point estimate is above zero with the planned sample
reached. If the sample isn't reached by week 6, extend once, by no more than 4
weeks, and say so in the readout.

**If it triggers, what I'd try next, in order:**

1. Strip the incentive entirely (already step one of the rule).
2. Move touch 1 earlier. If organic returns cluster in the first hour, the
   program may be competing with them instead of catching the ones who leave.
3. Narrow entry to first-time shoppers only. Repeat buyers often come back on
   their own `[Inference]`.
4. If none of that produces positive incremental margin, stop. Keep the
   holdout data; it's the most honest read of organic return you'll get, and
   `retention-diagnosis` should use it.

## Readout template

Fill at the read date. Every number here is `[Evidence]` once it's from your
data.

| Metric | Treated | Holdout | Difference | Label |
|---|---|---|---|---|
| Entrants | | | | |
| 7-day recovery rate | | | | |
| Revenue per entrant | | | | |
| Margin per entrant (net of incentive, message cost) | | | | |
| Margin per recovered order | | | | |
| Share of recoveries using a program code | | n/a | | |
| Unsubscribe rate per send | | n/a | | |
| SMS opt-out rate per send | | n/a | | |
| Repeat-abandon rate (next 30 days) | | | | |

| Incentive test (eligible branch, touch 4) | Incentive | No incentive | Difference |
|---|---|---|---|
| Reached touch 4 | | | |
| 7-day recovery rate from touch 4 | | | |
| Margin per person reaching touch 4 | | | |
| Full-price order rate | | | |

**Decision:** keep / strip touch 4 / narrow entry / stop.
**Why, in one sentence:**
**Logged to `.claude/decisions.md` on:**

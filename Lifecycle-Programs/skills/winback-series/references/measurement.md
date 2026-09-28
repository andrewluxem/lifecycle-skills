# Measurement: Winback Series

The full measurement plan. The primary KPI, guardrails, holdout recipe, and
kill condition also appear in `SKILL.md`; this file carries the detail.

## Primary KPI

**Incremental net reactivated margin per entrant.**

```
per arm:  (reactivation-order margin + follow-on margin in window
           − incentive cost) / entrants
KPI:      treated per-entrant value − holdout per-entrant value
```

- **Entrant:** anyone assigned to an arm at series entry (crossing L). Touch-1
  at-risk sends are measured separately (see below).
- **Reactivation order:** first order after entry.
- **Window:** from entry to L days after entry, capped at 120 days
  `[Assumption]`. Follow-on orders count if they land inside the same window.
- **Incentive cost:** discount dollars plus any shipping or gift cost on
  program-coded orders. Holdout orders that used a broadcast promo code carry
  their discount too, so both arms are net of what they actually cost.

**Why this and not reactivation rate.** I considered reactivation rate vs.
holdout with a margin guardrail. I chose margin as primary because reactivation
rate is the number a bigger code always wins. If the KPI can be bought, the
program will drift toward buying it. Reactivation rate is still reported; it's
the secondary read and the one the no-incentive fallback is judged on.

**Why not opens or clicks.** Lapsed customers open out of curiosity and don't
buy. Engagement tells you deliverability is alive, nothing more.

**At-risk touch (touch 1):** measured as the lapse rate (share crossing L)
among at-risk entrants, treated vs. a holdout of the same 10%. It's a
late-mid-life read, not a winback read, so it doesn't pool into the primary KPI.

## Guardrails

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Full-price follow-on orders per entrant, treated vs. holdout | Treated lower than holdout at the read | Turn off touches 4–5; this is the discount-training signal |
| Discount share of reactivation orders (treated) | Rises two reads in a row with flat or falling KPI `[Assumption]` | Lower the ladder step or switch to a non-price form |
| Unsubscribe rate per send | Above 2× the brand's broadcast average `[Assumption]` | Review cadence and the at-risk touch |
| Spam complaint rate per send | Above 0.1% `[Assumption]` | Pause the touch; check deep-lapsed targeting |
| Hard bounce rate on deep-lapsed sends | Above 2% `[Assumption]` | Stop sends past 2L; hand to sunset policy |
| Broadcast revenue from winback entrants | Holdout reactivators via broadcast promos exceed treated | The program isn't beating what BAU already does; review offer gating |

Note on the full-price guardrail: compare **per entrant**, which is
randomized. Comparing per reactivator is descriptive only, because who
reactivates is not random between arms.

## Attribution

- **Program-influenced:** any entrant in the treated arm who orders inside the
  window, regardless of last touch.
- **What counts as lift:** treated minus holdout, per entrant. Nothing else.
- The ESP's last-click revenue report will credit this program with every
  treated reactivation, including the ones that would have happened anyway. The
  holdout comparison overrides last-touch attribution every time, and I won't
  report last-click revenue as program impact.
- If store or marketplace orders aren't visible, both arms are equally blind,
  so the comparison is still fair, but the absolute numbers are understated. Say
  so in the readout.

## Holdout recipe

- **Size:** 10% of entrants `[Assumption]`; 20% if volume is thin.
- **Randomization unit:** customer ID, not email address (one person, several
  addresses).
- **Assignment point:** at entry, not at send. Assigning at send lets exits and
  filters bias the arms.
- **Stickiness:** arm persists on the profile across re-entries.
- **What control receives:** nothing from this program. Business-as-usual
  broadcasts continue for both arms, so the read is "program vs. BAU," which is
  the decision you're actually making.
- **Duration:** until the holdout reaches its sample size, plus one full
  window.

**Sample-size math** (two-proportion test on reactivation rate, 80% power,
alpha 0.05 two-sided, 90/10 allocation):

| Input | Value | Label |
|---|---|---|
| Holdout reactivation within window | 3% | `[Assumption]` |
| Treated reactivation within window | 4% | `[Assumption]` |
| Minimum detectable lift | 1 point absolute | `[Assumption]` |
| z for alpha 0.05 two-sided + z for 80% power | 1.96 + 0.84 | Standard |

```
holdout n = (1.96 + 0.84)² × [p_c(1−p_c) + p_t(1−p_t)/9] / (p_t − p_c)²
          = 7.84 × [0.0291 + 0.0043] / 0.0001
          ≈ 2,620 holdout entrants  →  ≈ 26,200 total entrants
```

That's `[Inference]` from `[Assumption]` inputs. Three things change it:

- **Higher base rate, bigger lift:** a High-tier read at 8% vs. 12% needs only
  ~420 holdout entrants. Tiers with higher base rates read faster.
- **The margin KPI is noisier than the rate.** Margin per entrant has a fat
  tail (a few big orders). Treat the rate calculation as the floor; plan for
  roughly 1.5–2× the entrants for a confident margin read `[Assumption]`, or
  trim order values at the 99th percentile before comparing.
- **An offer vs. no-offer test in the High tier** needs its own sample in each
  arm. If the tier won't reach it in a quarter, skip the test and run the
  program-level holdout only.

## Kill condition

Stated exactly as in `SKILL.md`. At the read date (one full window after the
holdout reaches its sample size, and no later than 16 weeks after launch):

- If incremental net reactivated margin per entrant is at or below $0 vs.
  holdout, **or** full-price follow-on orders per entrant are lower in treated
  than holdout, turn off touches 4 and 5 and run the no-incentive series for one
  more window.
- If the no-incentive series then fails to beat holdout on reactivation rate,
  stop the program, send the lapsed pool to the sunset policy, and route back to
  `retention-diagnosis`.

**What to try next if it triggers:**

1. Check the early-life tell again. If one-time buyers dominate entrants, the
   leak is upstream and a second-purchase program is the better bet.
2. Test a non-price offer form before any bigger percent.
3. Move the lapse line earlier (P70) and lean on the at-risk touch; saving
   people before they lapse is often cheaper than winning them back.
4. If none of that moves the curve, accept it. Some leaks are product or
   pricing problems, and a cadence won't fix them.

## Readout template

| Metric | Treated | Holdout | Difference | Label |
|---|---|---|---|---|
| Entrants | | | | `[Evidence]` |
| Reactivation rate in window | | | | `[Evidence]` |
| Gross margin per entrant (reactivation + follow-on) | | | | `[Evidence]` |
| Incentive cost per entrant | | | | `[Evidence]` |
| **Net reactivated margin per entrant (primary)** | | | | `[Evidence]` |
| Full-price follow-on orders per entrant | | | | `[Evidence]` |
| Discount share of reactivation orders | | | | `[Evidence]` |
| Unsubscribe / complaint / hard bounce per send | | n/a | | `[Evidence]` |

Plus, per tier (High, Standard, one-time buyers): entrants, net margin per
entrant difference, and the confidence interval. Close the readout with one of
three decisions: keep, turn off the offer ladder, or kill. Append it to
`.claude/decisions.md`.

# Measurement: Replenishment Reminders

The primary KPI, guardrails, holdout recipe, and kill condition also appear in
SKILL.md. This file carries the detail. The one idea to hold onto: many of these
customers would reorder with no reminder at all. The program earns credit only
for the reorders it pulls earlier and the lapses it prevents, and only a holdout
can show that.

## Primary KPI

**On-time repeat rate.**

- **Definition:** of customers entering the program (treated or holdout), the
  share whose first eligible episode after assignment ends in a qualifying
  reorder by the expected depletion date + 25% of C.
- **Qualifying reorder:** same SKU, an approved substitute, or a larger size or
  quantity of it, through any channel you can observe. A subscription start for
  that SKU also counts.
- **Formula:** on-time reorders ÷ customers entering, per arm. Lift = treated
  rate − holdout rate, in percentage points, with a confidence interval.
- **Window:** from purchase date to depletion date + 0.25 × C. Reorders placed
  before touch 1 would have fired count in both arms equally, which is correct:
  the holdout comparison nets them out.
- **Why this and not opens or clicks:** a reminder can get a high click rate
  from people who were reordering anyway. Clicks measure attention. The
  on-time repeat rate, against a holdout, measures whether the business got an
  order it wouldn't have got, or got it before a competitor did.

**Why customer level, first episode:** a customer with four SKUs and three
cycles would otherwise count a dozen times, and their episodes aren't
independent. Use the first eligible episode per customer for the primary read.
Report all-episode rates as a secondary, with standard errors clustered by
customer.

**Secondary metrics:**

- Median days from purchase to reorder, per arm (did reminders pull it earlier?).
- Repeat rate at 2x C, per arm (did reminders prevent lapse, or just shift
  timing?).
- Orders per customer over two cycles, per arm (the money).
- Graduation rate: share of eligible customers who start a subscription from
  touch G, and their 90-day subscription retention.

## Guardrails

Thresholds are `[Assumption]`. Replace them with your own program-level baselines
after the first read.

| Guardrail | Threshold | Action if breached |
|---|---|---|
| Email unsubscribe rate per send | Above 0.5% on any touch `[Assumption]` | Pause that touch; check timing (too early?) and whether exits are firing |
| SMS opt-out rate per send | Above 2% on touch 2 `[Assumption]` | Move touch 2 to push or email; check quiet hours |
| Spam complaint rate | Above 0.1% `[Assumption]` | Pause the program; check that reorderers are exiting |
| Repeat rate at 2x C | Treated not above holdout | Reminders are only shifting timing; review touches 2 and 3 |
| Orders per customer over two cycles | Treated not above holdout | The program isn't adding orders; see kill condition |
| Discount spend per reorder | Above zero outside an approved incentive test | Remove the discount; it's margin given to people who'd have paid |
| Subscription 90-day retention for graduates | Well below the brand's subscription baseline | Graduation threshold is too early; move from 2 to 3 on-time reorders |
| Messages to customers who already reordered | Any, in the post-launch spot-check | Treat as a blocking bug; fix exits before the next send |

## Attribution

- **Window:** purchase date to depletion + 0.25 × C for the primary KPI; to
  2 × C for the lapse guardrail.
- **Program-influenced:** any qualifying reorder by a treated customer inside
  the window. That's a reporting convenience, not a claim of causation.
- **What overrides it:** the holdout comparison, every time. Last-touch
  attribution will credit the reminder with nearly every reorder that happens
  after a send, including the ones that were already coming. If the ESP
  dashboard says the program drove a large share of repeat revenue and the
  holdout says lift is 2 points, the holdout is right.

## Holdout recipe

- **Size:** 10% of customers `[Assumption]`. 5% only if volume forces it.
- **Randomization unit:** the customer, not the episode or the send.
- **Assignment point:** at first entry to the program, once. Written to a
  persistent profile field (`holdout_flag`) and never re-rolled. The same
  customer stays in the same arm for every SKU and every cycle.
- **What the control receives:** transactional messages (order confirmation,
  shipping) and business-as-usual campaigns. Nothing from this program: no
  reminder, no nudge, no check-in, no graduation offer.
- **Duration:** keep entering customers until the holdout arm reaches the sample
  size below, then wait one full cycle plus the 25% grace window (per SKU) before
  reading. For the lapse guardrail, wait to 2x C.
- **Sticky holdout, long term:** keep a small holdout (5%) running after the
  first read. Replenishment lift can decay as customers form their own habit,
  and you'll want to know when.

**Sample-size reasoning, inputs labeled:**

| Input | Value | Label |
|---|---|---|
| Baseline on-time repeat rate (holdout) | 30% | `[Assumption]`: replace with last year's rate from `benchmarks.md` step 2 |
| Minimum detectable lift | 3 percentage points (30% → 33%) | `[Assumption]`: the smallest lift worth the build and send cost |
| Significance | 5%, two-sided | `[Assumption]`: conventional |
| Power | 80% | `[Assumption]`: conventional |
| Allocation | 90% treated / 10% holdout | `[Assumption]` |

Working it through: for a two-proportion comparison, the standard error of the
difference must be about 3 points ÷ (1.96 + 0.84) ≈ 1.07 points. The average
variance p(1−p) across 30% and 33% is about 0.216. With a 9:1 split, the
variance of the difference is 0.216 × (1/n_treated + 1/n_holdout) = 0.216 ×
(10/9) / n_holdout. Solving gives **about 2,100 holdout customers and about
18,800 treated, roughly 20,900 entering customers in total** `[Inference]`. A
50/50 split would need about 3,760 per arm; the 10% holdout costs you total
volume, not holdout volume.

The kill condition reads a 90% interval, which is a looser bar than the 95%
used here. That's deliberate: the sample is sized conservatively, and the
decision rule leans toward giving the program a fair chance.

**What this means for timing:** at 5,000 new entering customers a month
`[Assumption]`, you reach ~20,900 in a little over four months, then wait one
cycle plus grace to read. If that's too slow, don't shrink the holdout below 5%;
raise the minimum detectable lift instead, and say plainly that you can only see
big effects.

## Kill condition

Stated exactly as in SKILL.md:

> If, at the read date (two median cycles of the top SKU after the last cohort
> enters, or 12 weeks after launch, whichever is later), treated on-time repeat rate doesn't
> beat holdout by at least 3 percentage points `[Assumption: reset from your
> baseline]` with the 90% interval excluding zero, **and** orders per customer
> over two cycles isn't higher in treated, we stop touches 2 and 3, keep touch 1
> only if it's net-positive on orders, and send the question back to
> `retention-diagnosis`.

**What to try next if it triggers:**

1. Check the cycle data first. A reminder at the wrong time looks like a
   reminder that doesn't work. Re-derive the cycle and compare the reorder
   distribution to the reminder date.
2. Check whether the reorder link is actually one tap. Click-to-order rate near
   zero means the mechanism failed, not the idea.
3. Look for off-site reorders. If a marketplace sells your SKU cheaper, the
   leak is price or channel, not memory. That's `retention-diagnosis` and
   `lifecycle-context`, not more reminders.
4. If none of those explain it, accept the answer: this customer base reorders
   on its own, and the program's budget belongs elsewhere.

## Readout template

Fill this in at the read date. Every number labeled `[Evidence]` once it's from
your data.

| Metric | Treated | Holdout | Lift (pts or %) | 90% interval | Read |
|---|---|---|---|---|---|
| Customers entered | | | — | — | |
| On-time repeat rate (primary) | | | | | |
| Median days to reorder | | | | | |
| Repeat rate at 2x C | | | | | |
| Orders per customer, two cycles | | | | | |
| Revenue per customer, two cycles | | | | | |
| Email unsubscribe rate per send | | — | — | — | |
| SMS opt-out rate per send | | — | — | — | |
| Discount spend per reorder | | | | | |
| Graduation rate (eligible customers) | | — | — | — | |

**Decision:** keep / cut touches / kill. **Why, in one sentence:** ___.
**What we'll test next:** ___. Append the decision to `.claude/decisions.md`.

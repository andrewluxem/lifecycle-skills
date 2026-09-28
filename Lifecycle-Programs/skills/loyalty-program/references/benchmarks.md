# Benchmarks: loyalty program

Every number here is `[Assumption]` unless it's arithmetic on those assumptions,
which I label `[Inference]`. None of it is a measured result. These are starting
points for a model and a test, never targets. Replace them with your own numbers
after one cycle.

## Earn/burn economics, worked out

### Inputs

| Input | Value | Label | Notes |
|---|---|---|---|
| Earn rate | 1 point per $1 net spend | `[Assumption]` | Net of discounts and returns |
| Burn rate | 100 points = $5 off | `[Assumption]` | Face value $0.05/point |
| Face reward rate | 5% of spend | `[Inference]` | 1 × $0.05 |
| Cost-to-face ratio | 1.0 for dollars-off | `[Assumption]` | A merchandise reward costs roughly COGS, so the ratio drops to (1 − margin) on that item |
| Cost per point burned | $0.05 | `[Inference]` | Face × cost-to-face |
| Expected redemption rate | 70% | `[Assumption]` | Of points issued, eventually burned |
| Breakage | 30% | `[Inference]` | 1 − 70%. Stated out loud, never banked |
| Gross margin on member orders | 45% | `[Assumption]` | Before reward cost |
| Program ops cost | excluded here | — | Platform fees, staff; add as a fixed line |

### Reward cost

- Expected: 5% × 70% = **3.5% of member sales** `[Inference]`.
- Full redemption (breakage = 0): **5.0% of member sales** `[Inference]`.

### Break-even incremental lift

Let S be baseline member spend, ΔS the incremental spend the program causes, m
gross margin, c reward cost as a share of all member spend. The program pays
when incremental margin covers reward cost on *all* member spend, including
spend that would have happened anyway:

ΔS × m ≥ c × (S + ΔS) → ΔS / S ≥ c / (m − c)

| Scenario | c | Break-even ΔS/S | Label |
|---|---|---|---|
| Full redemption | 5.0% | 0.05 ÷ 0.40 = **12.5%** | `[Inference]` |
| 70% redemption | 3.5% | 0.035 ÷ 0.415 = **8.4%** | `[Inference]` |

The gap between 8.4% and 12.5% is the breakage-dependent zone. If your plan
needs lift in that range to break even, you're counting on 30% of members
forgetting. Redesign the earn rate or the reward before anything else.

The most common mistake here: forgetting that reward cost falls on baseline
spend too. Members who'd have bought anyway still earn. That subsidy is the real
cost of the program, and it's why incremental lift, not member revenue, is the
only honest read.

### Liability, sized for context only

Illustration: 50,000 members × 600 unredeemed points = 30M points `[Assumption]`.
Face value 30M × $0.05 = $1.5M; at 70% expected redemption, about $1.05M
`[Inference]`. How that's booked, when, and how breakage is treated is a finance
and accounting decision. I size it so finance isn't surprised. I don't advise on
it.

### Accelerator cost

A 2× accelerator on one order adds another 5% face on that order. At $40 AOV
`[Assumption]` that's $2.00 face, $1.40 expected at 70% redemption
`[Inference]`. It's paid on every accelerated order, including ones that would
have happened anyway, which is exactly why it gets a holdout.

## Tiers vs. points: decision defaults

| Signal | Leans tiers | Leans points | Label |
|---|---|---|---|
| Purchase frequency | < 4 orders/year | ≥ 6 orders/year | `[Assumption]` |
| AOV | High | Low | `[Assumption]` |
| Category | Identity, status, visible use | Routine, consumable | `[Inference]` |
| Member motive | Recognition, access | Next small reward | `[Inference]` |

Between the lines, start with points. It's simpler to explain, cheaper to
change, and tiers can be layered on once the base mechanic proves out.

## Timing defaults

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| 1 Enrollment | Immediate; +24h if joined at checkout | 0–48h | `[Assumption]` |
| 2 First earn | On posted points | — (event-bound) | `[Assumption]` |
| 3 Accelerator | After order 2; window ~0.8× median reorder interval | 0.6–1.0× | `[Assumption]` |
| 4 Near-reward | At 80% of threshold; 7-day cooldown | 70–90% | `[Assumption]` |
| 5 Reward available | On threshold crossed | — | `[Assumption]` |
| 6 Near-tier | Within 20% of tier, ≥30 days left | 15–30%; 30–60 days | `[Assumption]` |
| 7 Tier-up | On tier change | — | `[Assumption]` |
| 8 Tier-at-risk | 60 days before period end | 45–90 days | `[Assumption]` |
| 9 Expiry | 30 and 7 days before | 45/14/3 | `[Assumption]` |
| 10 Statement | Monthly for high-frequency; quarterly otherwise | — | `[Assumption]` |
| Lapse line | ~2× median reorder interval | 1.5–3× | `[Assumption]` |

## Split defaults

- **Accelerator holdout:** 10% default, up to 30% when eligible volume is low.
  The accelerator is a bonus, so a larger holdout costs little goodwill
  `[Inference]`.
- **Content A/B inside the treated arm:** only once each cell has at least ~2,000
  eligible members `[Assumption]`. Below that, don't split; you won't read it.
- **Never** A/B the expiry warning's presence. Everyone with a meaningful
  balance gets it.

## Content defaults

What each touch typically carries: the balance module, the progress bar, and one
CTA. Tests ranked by expected value, not ease:

1. Accelerator window length (changes the economics and the leak).
2. Accelerator multiplier, 1.5× vs. 2× (changes cost per incremental order).
3. Near-reward threshold, 70% vs. 80% vs. 90%.
4. Channel for touch 4 (push vs. email) among app users.
5. Statement cadence.

Subject-line tests are last. They move opens, not wallet share.

## How to replace these numbers

- **Redemption rate and breakage:** from the ledger, points burned ÷ points
  issued for cohorts old enough that their points have fully expired.
- **Margin:** finance's gross margin on member orders, net of returns.
- **Median reorder interval:** days between order 1→2 and 2→3, by cohort.
- **Second-to-third purchase rate:** share of 2-order customers who place a 3rd
  within 90 days.
- **Liability:** from finance, not from this file.

After one cycle, this file should be irrelevant for your brand.

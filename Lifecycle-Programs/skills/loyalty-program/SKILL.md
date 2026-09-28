---
name: loyalty-program
description: >-
  Design a loyalty program's economics and its lifecycle comms, in that order:
  earn/burn model, breakage stated out loud, tiers vs. points, then the
  enrollment, first-earn, near-reward, tier-up, and points-expiry touches, with
  an earn-accelerator holdout and a kill condition. Use when someone says "we
  want a loyalty program," "our points program isn't moving frequency," "should
  we do tiers or points," "members plateau after year one," or "build the
  loyalty emails," and the leak is known to be early-life (second-to-third
  purchase) or mid-life plateau erosion.
license: MIT
---

# Loyalty Program

Most loyalty programs are designed backwards. Someone picks a tier name, a
metal color, and a launch email, and the economics get worked out after the
creative is approved. Then finance asks what it costs, and the answer is "it
depends on breakage." That's the moment I get worried. This skill does the math
first, says the breakage number out loud, and only then designs the comms that
run on top of it.

I work in stages and stop between them: economics, then structure, then touches,
then measurement. If the economics don't clear, I stop there and tell you.

## When to use this skill

Trigger phrases I listen for:

- "We want to launch a loyalty program" or "a rewards program."
- "Our points program exists but frequency hasn't moved."
- "Should we do tiers or points?"
- "Members stall after their first reward" or "year-two members plateau."
- "Build the loyalty lifecycle emails: welcome to the program, tier-up, expiry."
- "Can breakage pay for this?" (Short answer: it shouldn't. See the thesis.)

**Leak zones treated:** early-life (the second-to-third purchase, where a habit
either forms or doesn't) and mid-life (plateau erosion, members who stay but
buy less). Loyalty is a weak activation tool and a poor resurrection tool.

**What this is NOT for, and who owns it:**

- Unknown leak. If you can't tell me where customers are leaving, I route you to
  `retention-diagnosis` first. I won't design a program in the dark. A points
  scheme bolted onto an activation problem is an expensive discount.
- The first purchase-to-second journey. `post-purchase` owns onboarding after an
  order and hands members in to me.
- Consumable reorder timing. `replenishment-reminders` owns "you're about to run
  out" and hands in; I don't duplicate its cadence.
- Lapsed members. Once someone crosses the lapse line, they go to
  `winback-series`. A points reminder is not a winback.
- Who qualifies for what. `segmentation-model` owns the member cuts; I consume
  them.
- The finished words. `lifecycle-messaging` writes copy; I hand it touch specs.
- Points liability accounting, revenue recognition, tax, and program terms. I
  flag them and tell you to bring in finance and whoever owns your terms. I give
  no accounting, tax, or legal advice.

## What I need before I start

**Required** (without these the program is a guess):

- The leak zone, from `.claude/retention-snapshot.md` or a
  `retention-diagnosis` read.
- Gross margin on member orders, and AOV. Every earn rate is a margin decision.
- Purchase frequency: median days between orders, and the second-to-third
  purchase rate.
- Where the points ledger lives (loyalty platform, commerce backend, or nothing
  yet) and which events it can emit to the ESP: enrolled, points posted, balance,
  tier change, expiry date.
- Consent status by channel.

**Optional** (makes it sharper):

- Category purchase behavior: is this high-consideration and identity-driven, or
  high-frequency and low-AOV? This decides tiers vs. points.
- Current redemption and breakage history if a program already exists.
- App presence (push and in-app change the channel plan).
- Finance's view on reward cost and liability tolerance.

**With partial inputs** I can still produce the economics model with every
missing number labeled `[Assumption]`, a tiers-vs-points recommendation stated
as conditional, and the full touch architecture. What I won't produce without
margin data is an earn rate I'd call safe.

## The thesis

Economics before creative. I think most loyalty programs fail quietly because
nobody modeled them at 100% redemption. The plan assumes 30–40% of points will
never be redeemed, the P&L only clears because of that, and the program is now a
promise the business hopes members forget. I won't design that. Breakage gets
stated out loud, as a number, and the program has to break even without it.
Breakage is upside, never the plan.

Second position: tiers beat points where status matters. High-consideration,
identity-driven categories (travel, apparel with a point of view, premium beauty)
reward recognition, and a tier gives members something to protect. Points win on
frequency: high-frequency, low-AOV categories (coffee, pet food, grocery-adjacent
DTC) where the next small reward is the pull. Hybrid programs are fine once the
base mechanic is proven. I'd rather ship one clean mechanic than a hybrid nobody
can explain in a sentence.

Third: you usually can't hold out the whole program once it's public, so the
measurable bet is the earn accelerator and the lifecycle comms. That's where the
holdout goes.

**The sacrifice.** This program does not acquire members through paid media, does
not fix activation, does not win back lapsed customers, and does not run
discount campaigns dressed as loyalty. It also doesn't pick reward merchandise or
negotiate partner rewards. Those are merchandising and partnership calls.

## Program blueprint

### Objective and audience

**Objective:** raise incremental share of wallet among enrolled members, read as
net spend per member after reward cost vs. a holdout on the earn accelerator.

**Entry audience:** enrolled members with at least one purchase, consented on at
least one channel, not in an active winback. Handed in from `post-purchase`
(after first order) and `replenishment-reminders` (consumables buyers).

**Leak zones:** early-life (second-to-third purchase) and mid-life (plateau).

### Earn/burn economics (before any comms)

I fill this table before touch 1 is specced. Defaults below are placeholders;
the full worked math is in `references/benchmarks.md`.

| Line | Default | Label | How it's used |
|---|---|---|---|
| Earn rate | 1 point per $1 net spend | `[Assumption]` | Points issued per order |
| Redemption value | 100 points = $5 off | `[Assumption]` | Face value $0.05/point; 5% face reward rate |
| Cost per point | $0.05 for dollars-off rewards; COGS share for merchandise rewards | `[Assumption]` | Real cost when a point is burned |
| Expected redemption rate | 70% | `[Assumption]` | Share of issued points eventually burned |
| Breakage (stated out loud) | 30% | `[Assumption]` | 1 − redemption rate. Upside only |
| Gross margin | 45% | `[Assumption]` | Pays for the reward |
| Expected reward cost | 3.5% of member sales | `[Inference]` | 5% × 70% |
| Full-redemption reward cost | 5.0% of member sales | `[Inference]` | The number the design must survive |
| Break-even lift at full redemption | 12.5% incremental member spend | `[Inference]` | 0.05 ÷ (0.45 − 0.05) |
| Break-even lift at 70% redemption | 8.4% | `[Inference]` | 0.035 ÷ (0.45 − 0.035) |
| Liability | outstanding points × $0.05 × expected redemption | `[Inference]` | Flag to finance; not my call |

**The rule:** if the program only clears between 8.4% and 12.5% lift, it's
living on breakage. I redesign the earn rate or reward before writing a touch.
Platform fees and ops cost come on top; add them.

**Liability:** outstanding points are a real obligation on someone's books. How
it's recognized is a finance and accounting matter. I flag it, size it roughly
for context, and tell you to involve finance before launch. That's where my help
ends.

### Message architecture

Frameworks, not copy. `lifecycle-messaging` writes the words.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Enrollment | On `enrolled` event; if enrolled at checkout, fold into the order confirmation or wait 24h so it doesn't compete | Email; in-app if app | Member knows how to earn and how far the first reward is | Live balance and points-to-first-reward | View account | Don't sell a second purchase; `post-purchase` is still onboarding |
| 2 | First earn | On first `points_posted` (often after ship or return window), not at order, so the balance is real | Email or push | Points are real and already count toward something | Posted balance, reward threshold | See how close you are | Don't show pending points as spendable |
| 3 | Earn accelerator (the bet) | After order 2, bonus earn on order 3 within ~0.8× median reorder interval; early-life leak | Email; push if app | A third order now earns faster | Accelerated points on their own next order | Shop, lands on their last category | Not a discount; not sent to holdout; not stacked with a replenishment reminder the same day |
| 4 | Near-reward | Balance crosses ~80% of next reward threshold; 7-day cooldown | Push or email | The gap is small and specific | Exact points and dollar gap | Shop | Don't fire on a balance that one order can't close |
| 5 | Reward available | Balance crosses threshold | Email; in-app badge | A reward is waiting | Reward value and how to apply it | Redeem | No false urgency; the reward isn't going anywhere yet |
| 6 | Near-tier (tier programs only) | Within ~20% of next tier with ≥30 days left in the qualifying window | Email | Status is within reach | Qualifying spend so far vs. threshold | See tier benefits | Don't fire with too little time to qualify |
| 7 | Tier-up | On `tier_changed` up | Email; in-app | What changed for them, concretely | Benefits list for the new tier | Explore benefits | Don't sell in the same message |
| 8 | Tier-at-risk | 60 days before qualifying period ends, if short; mid-life plateau | Email | What it takes to keep status | Spend gap and date | See what's left | No guilt, no threat; skip if the gap is unrealistic |
| 9 | Points-expiry warning | 30 and 7 days before expiry, balance ≥ one reward's worth | Email; SMS only with explicit consent | Points expire on a date and can be used | Balance, expiry date, what it's worth | Redeem | Never fire on trivial balances; never read as a threat |
| 10 | Periodic statement | Monthly or quarterly for active mid-life members | Email | They see the value they've already gotten | Rewards redeemed YTD, balance, tier progress | View account | Not a promo blast with a balance stapled on |

Touch 9 exists on purpose. If we don't warn before expiry, we're banking on
forgetting, and that's the breakage-as-plan trap wearing a different coat.

### Splits and personalization

- **Default path:** points program, email, touches 1–5, 9, 10.
- **Tiers vs. points:** tier touches (6, 7, 8) only run if the structure decision
  was tiers. Decided once, at design time, not per member.
- **App vs. no app:** push and in-app replace email for 2, 4, 5 when the member
  has the app and push consent. Changes the channel, not the job.
- **Accelerator holdout (random):** at eligibility for touch 3, a random bucket
  (10–30%) gets base earn only, no accelerator, and no touch 3. The bucket must
  be honored by the loyalty platform's earn rules, not just the ESP.
- **Balance band:** touches 4 and 9 gate on balance. Below one reward's worth,
  they don't fire.
- **Segment cuts** from `segmentation-model` (e.g., consumables vs. one-off
  buyers) change the accelerator window, not the program. Anything else is
  decoration and I cut it.

### Exits and suppression

- **Purchase** exits touches 3, 4, 6, and 8 immediately. The bug I worry about
  most: a member buys and still gets "you're so close" the next morning.
- **Redemption** exits touches 5 and 9 for the redeemed points.
- **Lapse** (no order in ~2× median reorder interval `[Assumption]`) exits all
  promotional loyalty comms and hands to `winback-series`. Only touch 9 still
  fires, on meaningful balances.
- **Unenroll or unsubscribe** exits everything; transactional balance notices
  follow program terms.
- **Returns** that reverse points re-evaluate balance-gated touches before send.
- **Suppression while in this program:** during the `post-purchase` onboarding
  window, touch 3 waits. On days `replenishment-reminders` fires, touches 3 and
  4 hold. Cross-program priority and caps belong to `journey-architecture`.

### Content blocks

- **Balance module:** points balance, pending vs. posted, dollar equivalent.
  Needs a real-time or daily balance attribute; fallback hides the block.
- **Progress bar:** points or spend to next reward or tier. Needs threshold and
  current value.
- **Expiry strip:** points expiring and date. Needs per-member expiry date.
- **Tier benefits card:** current and next tier benefits. Static per tier.
- **Accelerator badge:** bonus earn rate and window end. Needs holdout bucket
  and window end date.
- **Category-aware product block:** last purchased category. Needs order
  history; fallback is bestsellers.

## Platform build mapping

In primitives. ESP specifics live in `references/platform-build.md`. The points
ledger usually lives in a loyalty platform or commerce backend, not the ESP; the
ESP consumes its events and attributes.

- **Trigger:** `enrolled`, `points_posted`, `order_placed` (count = 2),
  `balance_threshold_crossed`, `tier_changed`, scheduled expiry date.
- **Filter:** enrolled, channel consent, not in winback, balance band.
- **Split:** random accelerator holdout at eligibility; tier vs. points; app vs.
  no app.
- **Wait:** until next order or accelerator window end; days-before-expiry;
  cooldowns on touch 4.
- **Exit:** purchase, redemption, lapse to `winback-series`, unenroll.

## QA

This skill never sends. It tells a human what to verify first. Full list in
`references/qa-checklist.md`.

1. **Holdout honored in the ledger.** A holdout test profile places order 3 and
   earns base points, not accelerated ones.
2. **Purchase exit works.** A test member who buys drops out of touches 3 and 4
   before the next send.
3. **Balances are posted, not pending.** Touch 2 and the balance module read
   posted points only.
4. **Expiry math is right.** Touch 9 shows the correct date and balance and
   doesn't fire on trivial balances.
5. **Economics sign-off exists.** The earn/burn table is filled, full-redemption
   cost is known, and finance has seen the liability flag.

## Measurement

Detail in `references/measurement.md`. The four that must live here:

- **Primary KPI:** incremental share of wallet, read as net spend per member
  after reward cost, accelerator-treated vs. holdout, over 180 days from
  eligibility. True share of wallet needs an outside category-spend estimate;
  without one, spend per member vs. holdout is the honest proxy.
- **Guardrails:** reward cost as % of member sales stays at or below the modeled
  full-redemption rate; gross margin rate on member orders doesn't fall more than
  1 point `[Assumption]`; unsubscribe and complaint rates per send at or below
  the brand's baseline; points liability growth reported to finance monthly.
  Each guardrail's threshold and breach action is in `references/measurement.md`.
- **Holdout recipe:** 10–30% of members, randomized per member at the moment
  they become eligible for the accelerator (after order 2), not at send. Control
  gets base earn, transactional notices, and touch 9 (expiry is a fairness line
  I won't cross), and nothing from touch 3. Run until each arm hits the sample
  size in `references/measurement.md`, then 180 days.
- **Kill condition:** if at the 26-week read (180 days after both arms reach
  sample size) the treated group doesn't beat the
  holdout on net spend per member after reward cost, with the 90% confidence
  interval's lower bound above $0, we turn the accelerator off, keep base earn,
  and take the next bet to the mid-life statement or back to
  `retention-diagnosis`. Separately: if observed redemption runs above the
  modeled rate for two straight quarters and the P&L only clears on breakage,
  we freeze new creative and redesign the earn rate with finance.

## Field notes

None of these come from a loyalty program. They come from lifecycle program work
generally, and they carry over.

- Welcome shipped first in a lifecycle rebuild because it had the cleanest
  holdout and the fastest read `[Fact — author's record]`. For loyalty, that's
  the accelerator: it's the one piece you can hold out cleanly.
- Skill-driven pre-send QA caught about 3 errors per week before send, and the
  most common welcome catch was the purchaser-exit bug `[Fact — author's
  record]`. That's why purchase exit is QA check 2 here.
- Campaign output went from 7 to 21 per week with the same team `[Fact —
  author's record]`. The lesson I take: a shippable v1 in week 1 beats a perfect
  program in quarter 2. Ship touches 1, 2, 3, and 9 first.

## Worked example

Fernhollow Coffee Co. (invented) sells beans and pods DTC, AOV $32 and reorder
every ~5 weeks `[Assumption]`. The team wanted three metal tiers at 10% back and
planned to fund it on 50% breakage. At 55% margin `[Assumption]`, 10% back needs
22% incremental spend at full redemption to break even `[Inference]`. I
recommended points, not tiers (high frequency, low AOV), at 5% back with a 2×
accelerator on order 3, and a 30% accelerator holdout. Full walkthrough in
`examples/example-brief.md`.

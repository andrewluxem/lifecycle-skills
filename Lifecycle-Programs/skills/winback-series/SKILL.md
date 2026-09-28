---
name: winback-series
description: >-
  Blueprint a winback series that tiers lapsed customers by recency and
  predicted value before spending a dollar of incentive, escalates the offer
  only where the expected margin covers it, and hands the truly gone to the
  sunset policy instead of discounting them forever. Use when someone says
  "build a winback flow," "our lapsed customers aren't coming back," "send
  everyone who hasn't bought in 90 days a code," or "our winback isn't
  working" — after confirming the leak is actually in resurrection or late
  mid-life, not early-life.
license: MIT
---

# Winback Series

Most winback programs are a discount with a timer on it. They light up a
dashboard, because some of the people who got the code were coming back anyway,
and they quietly teach the rest of the file that waiting pays. I won't design
one of those. This skill tiers the lapsed file first, spends incentive only
where the math says it earns its keep, measures against a holdout, and lets the
truly gone go.

I'm read-only: I produce a build spec, a QA list, and a measurement plan. I
never send email or SMS.

## When to use this skill

- "Build me a winback / re-engagement / lapsed-customer program."
- "Our winback isn't working," or "it only works with 30% off."
- "Everyone who hasn't bought in 90 days should get a code."
- "How much should the winback offer be, and who gets it?"

**Leak zone:** resurrection first, and late mid-life for the at-risk band just
before lapse. That's it.

**The routing rule.** `retention-diagnosis` warns that teams build winback when
the leak is really early-life. I check that before I design anything:

- If there's no `.claude/retention-snapshot.md` and you can't tell me where the
  retention curve drops hardest, I route you to `retention-diagnosis` and stop.
  I won't design in the dark.
- If the snapshot or the curve puts the dominant leak in activation or
  early-life, I say so and route back. A winback aimed at one-time buyers who
  never formed a habit is an early-life fix wearing a winback costume.
- Quick tell I run myself: the share of the lapsed pool with exactly one order.
  If it's the majority, I flag it and ask whether the real program is a
  second-purchase journey, not this one.

**What this is NOT for, and who owns it:**

| Adjacent problem | Owner |
|---|---|
| Where is the leak? Is winback even the right fix? | `retention-diagnosis` |
| Business model, active metric, margin, stack | `lifecycle-context` |
| Defining the value tiers and validating them | `segmentation-model` |
| Priority vs. cart abandon, promos, frequency caps | `journey-architecture` |
| The finished subject lines and body copy | `lifecycle-messaging` |
| Experiment design beyond this one program | `retention-metrics` |
| Reorder timing for consumables before lapse | `replenishment-reminders` (hands off to me past ~2× the usage cycle) |
| Points and status comms for members | `loyalty-program` (pauses promo comms while someone is in winback) |
| Removing the truly gone from the mailable file | The team's deliverability / sunset policy. There is no sunset skill in this plugin yet; it's a candidate future program. |

## What I need before I start

**Required.** Without these the program is a guess:

1. **Order history with dates**, enough to compute the inter-purchase interval
   distribution for repeat buyers. "Lapsed" is defined from your own purchase
   cycle, never a generic 90 or 180 days.
2. **Gross margin per order** (or AOV plus a margin rate). Incentive decisions
   are margin decisions. Revenue alone hides the cost of the code.
3. **Consent status by channel** and the current suppression list.
4. **Where the leak is**: a retention snapshot, a curve, or a cohort table.
5. **What a "return" is**: a purchase, and in which channels you can see it
   (site, app, store, marketplace).

**Optional:** a predicted-value score from `segmentation-model` (without it I
proxy value with trailing 12-month margin, labeled `[Inference]`); past winback
results with a holdout; per-customer incentive history, to spot serial
redeemers; your sunset threshold.

**With partial inputs** I still produce the tiering logic, the touch
architecture, the incentive break-even formula, and the holdout recipe. Every
missing number becomes `[Assumption]`, and the incentive touches stay off until
margin is `[Fact]`.

## The thesis

I think most winback programs fail twice. First, they define "lapsed" as a round
number that has nothing to do with the brand, so a coffee buyer on a 30-day
cycle and a mattress buyer on a 7-year cycle get the same 90-day email. Second,
they lead with the discount for everyone. The code gets redeemed by people who
would have come back at full price, and the ones it actually wins learn to wait
for the next one. A winback that trains discount-only return is a margin
transfer with a dashboard.

So this program does three things in order. It defines lapse from the brand's
own inter-purchase interval. It tiers the lapsed file by recency and predicted
value and opens with no incentive at all. And it escalates the offer only for
tiers where the incremental margin covers the code, remembering that the code
is paid to every redeemer, not just the incremental ones.

**The sacrifice.** This program deliberately does not try to win back everyone.
Low-value lapsed customers get relevance, not money. Serial redeemers get no
escalation. The truly gone leave the program for the sunset policy. I'd rather
hand back a smaller, profitable reactivation number than a big one that costs
more than it returns.

## Program blueprint

### Objective and audience

**Objective:** incremental reactivated gross margin, net of incentive cost,
from customers who have passed the brand's own lapse line.

**Defining the bands** (all from your order data, `[Evidence]` once computed):

- **M:** median days between consecutive orders for repeat buyers.
- **L (lapse line):** P80 of that interval, so past L a customer is later than
  80% of real repeat gaps. Test P75 to P90 `[Assumption]`.
- **G (gone line):** where the untreated return rate flattens near zero. Start
  at 3×L `[Assumption]`; replace it with your curve.

| Band | Days since last order | Leak zone | In this program? |
|---|---|---|---|
| At-risk | Between ~1.25×M and L | Late mid-life | One no-incentive touch only |
| Lapsed | L to 2L | Resurrection | Full series |
| Deep-lapsed | 2L to G | Resurrection | Stay-or-go touch only |
| Gone | Past G | None this program can fix | Exit to sunset policy |

**Value tiers:** High and Standard, from predicted value, or trailing 12-month
margin as a proxy. One-time buyers get their own flag because they drive the
early-life check.

### Message architecture

Timing is expressed in the brand's own cycle so it scales from a 30-day
consumable to a 2-year durable. Words belong to `lifecycle-messaging`.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | At-risk nudge (late mid-life) | At ~1.25×M: late but not lapsed; the cheapest save is before the habit breaks | Email; push if app-active | "It's about time for your usual" | Last-purchase or replenishment block | Reorder / shop last category | No discount. Don't tell them they're lapsed |
| 2 | Recognition | At L: the first moment they're later than most repeat buyers | Email | "We noticed, and here's what's relevant to you" | What's-new-since-your-last-order block | Browse personalized category | No incentive. No guilt framing |
| 3 | Reason to return | L + ~0.25×M: gives touch 2 time to work before adding anything | Email | "The thing you liked is still worth coming back for" | Reviews or rating for their category | Shop category | No incentive yet; no generic bestseller dump |
| 4 | First offer (gated) | L + ~0.5×M, only for tiers where break-even holds | Email; SMS for consented High tier only | "There's a concrete reason to come back this week" | Single-use code with a clear expiry | Redeem on a landing page with the code applied | Never shown to Standard tier or serial redeemers. Never sitewide-stackable |
| 5 | Escalation (High tier only) | Touch 4 + ~7 days, only if the higher step still breaks even | Email; SMS if consented | "This is the best reason we'll give" | Bigger step, or a different form (shipping, gift) | Redeem before expiry | No escalation past the ladder cap. No fake urgency |
| 6 | Stay or go | At 2L, for anyone still in: before they hit the gone line | Email | "Tell us how often you want to hear from us" | Preference options, including less often | Choose frequency or opt down | No offer. Non-response is an answer; don't chase it |

### Splits and personalization

Every split below changes a decision. If it didn't, I cut it.

- **Holdout (random, at entry):** 10% of entrants, sticky by customer ID across
  re-entries. They receive nothing from this program. See Measurement.
- **Recency band:** set by the waits, not a separate split. Band determines
  which touches a person is eligible for.
- **Value tier:** High vs. Standard. Standard never sees touches 4 or 5 unless
  the break-even check below passes for Standard specifically.
- **Incentive eligibility filter:** offer only if (a) the tier's break-even is
  positive, (b) the customer didn't reactivate on a code in the last 12 months
  without a later full-price order, and (c) they aren't in another discount
  program right now.
- **One-time buyers:** default path through touches 2, 3, and 6 only. Their
  share of entrants is the early-life tell; if it dominates, route to
  `retention-diagnosis`.
- **Optional incentive test (High tier, volume permitting):** randomize the
  High tier into offer vs. no-offer arms. It's the only clean way to learn
  whether the code itself is incremental.

**The incentive break-even, per entrant in a tier:**

`incremental reactivation × (order margin + expected follow-on margin)` minus
`reactivation with offer × incentive cost per redeemed order`

The second term is the one teams forget: you pay the code to everyone who
redeems, including the people who were coming back anyway. If the result is not
positive with your numbers, that tier doesn't get an offer.

Personalization that earns its place: last category purchased (it changes the
product block). Cut: first name in the subject, "we miss you" countdowns.

### Exits and suppression

- **Purchase, any visible channel → exit immediately**, before the next send is
  evaluated. This is where winbacks break: a customer buys at full price and
  gets a code two days later. Include store and marketplace orders if the data
  arrives; if it arrives late, add a re-check before touches 4 and 5.
- **Unsubscribe, complaint, hard bounce, consent revoked → exit**, and honor it
  across channels per your policy.
- **Crosses G, or finishes touch 6 with no response → exit to the sunset
  policy.** The team's deliverability owner decides suppression; this program
  just hands off.
- **Enters a higher-priority program** (cart or browse abandon, service
  recovery) → pause winback, don't exit. `journey-architecture` owns the
  priority order.
- **Re-entry:** allowed after a new purchase and a new lapse. Incentive
  eligibility is capped at once per 12 months per customer `[Assumption]`.
- **Suppressed while in the program:** broadcast promo codes for offer-tier
  customers (no stacking), other re-engagement campaigns, and touch 1 for anyone
  still inside `replenishment-reminders`, which owns pre-lapse reorder timing.

### Content blocks

| Block | Used in | Data it needs |
|---|---|---|
| Last purchase / replenishment | 1, 2 | Last order SKUs, category, days since order |
| What's new since your last order | 2, 3 | Catalog feed with launch dates; last order date |
| Category proof | 3 | Review rating and count by category; fallback to brand-level |
| Offer strip | 4, 5 | Eligibility flag, unique single-use code, expiry date, ladder step |
| Preference center | 6 | Frequency options, channel consent state |

## Platform build mapping

In primitives. ESP-specific builds live in `references/platform-build.md`
(Braze Canvas, Klaviyo Flows, Iterable Journeys, SFMC Journey Builder).

- **Trigger:** daily evaluation of days since last order crossing ~1.25×M
  (touch 1) or L (series entry). A scheduled audience entry, not a real-time
  event: lapse is the absence of an event.
- **Filter:** consent by channel, suppression list, not in gone band, not
  currently in a higher-priority program, incentive eligibility for offer
  touches.
- **Split:** random 10% holdout at entry; value tier; one-time buyer flag;
  optional offer vs. no-offer arm in High tier.
- **Wait:** fractions of M between touches, each a wait-until-purchase with a
  timeout.
- **Exit:** purchase, consent loss, crossing G, or silence after touch 6 →
  sunset handoff. Pause, not exit, on higher-priority program entry.

## QA

The five checks that catch the most expensive errors, in order. Full list in
`references/qa-checklist.md`. I tell a human what to verify; I never send.

1. **Purchaser exit works.** A test profile that orders mid-wait leaves before
   the next send, including a late-arriving store or marketplace order.
2. **Offer gating holds.** A Standard-tier profile and a serial-redeemer profile
   both reach touch 4's position and see no offer block.
3. **Holdout is real.** Randomized at entry, sticky on re-entry, receives
   nothing from this program, and isn't getting a code from a parallel
   campaign.
4. **Lapse line is the brand's.** The entry query uses the computed L, and the
   entrant count matches the pool sizing within a reasonable tolerance.
5. **Deep-lapsed deliverability.** Addresses dormant past 2L are checked
   against the sunset policy before touch 6 goes to them; a sudden bounce spike
   is a stop signal.

## Measurement

**Primary KPI: incremental net reactivated margin per entrant.** Treated minus
holdout, measured on gross margin from reactivation orders plus follow-on orders
inside the window, minus incentive cost. Window: from entry to L days after
entry (one lapse-length), capped at 120 days `[Assumption]`.

I chose this over reactivation rate because reactivation rate can be bought: a
bigger code moves it every time. Net margin per entrant is the only number that
says the program made money after paying the people who were coming back anyway.

**Guardrails:**

- **Full-price repeat after reactivation:** full-price follow-on orders per
  entrant inside the window, treated vs. holdout. If treated is lower, the code
  is training discount-only return.
- **Discount share of reactivation orders**, per tier: rising share with flat
  margin is the same signal, earlier.
- **Unsubscribe, complaint, and deep-lapsed hard bounce rates.** Thresholds in
  `references/measurement.md`.

**Holdout recipe:** 10% of entrants, randomized by customer ID at entry (not
at send), sticky across re-entries. Control gets nothing from this program but
stays in business-as-usual broadcasts. Run until the holdout holds enough
entrants for the lift you care about. Sample-size math with labeled inputs is in
`references/measurement.md`; at a 3% untreated return rate, detecting a 1-point
lift needs roughly 2,600 holdout entrants `[Inference]` from `[Assumption]`
inputs.

**Kill condition.** At the read date (one full window after the holdout reaches
its sample size, and no later than 16 weeks after launch):

- If incremental net reactivated margin per entrant is at or below $0 vs.
  holdout, **or** full-price follow-on orders per entrant are lower in treated
  than holdout, I turn off touches 4 and 5 and run the no-incentive series for
  one more window.
- If the no-incentive series then fails to beat holdout on reactivation rate,
  I stop the program, send the lapsed pool to the sunset policy, and route back
  to `retention-diagnosis`: the leak is probably not where we thought.

## Field notes

Operator experience, not measured here, and none of it about winback itself.

- The most common catch in pre-send QA on a welcome program was the
  purchaser-exit bug `[Fact — author's record]`. Winback has the same failure
  mode with a worse cost: a code sent to someone who just paid full price. It's
  QA check #1 for a reason.
- On a program-suite rebuild, welcome shipped first because it had the cleanest
  holdout and the fastest read `[Fact — author's record]`. Winback reads slower
  because the window is a full lapse-length, so I wouldn't put it first in the
  queue.
- A shippable v1 in week one beat a perfect program in quarter two
  `[Fact — author's record]`. For winback, v1 is touches 2, 3, and 6 with a
  holdout and no incentive. Add the offer ladder once margin is `[Fact]`.

## Worked example

`examples/example-brief.md` walks Tallgrass Pantry, an invented DTC spice and
pantry brand. The team asked for "25% off to everyone who hasn't bought in 90
days." Their median reorder interval is 38 days and the lapse line is 64
`[Evidence]`, so 90 days was already a month late. The decision it illustrates
best: the break-even math gives the High tier an offer and the Standard tier
none (about +$0.41 vs. -$0.03 net margin per entrant `[Inference]` from
`[Assumption]` lift inputs), and the holdout decides whether that was right.

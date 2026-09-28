---
name: welcome-series
description: >-
  Blueprint for a day-0-to-14 welcome series that turns new subscribers into
  first purchasers and hands them straight to post-purchase for the second:
  five touches (promise, proof, guide, offer, last call), purchasers exit the
  moment they buy, the incentive is fenced to non-purchasers on day 7, returning
  customers get a two-touch variant, and the whole thing ships with a holdout.
  Use when someone says "our welcome flow isn't converting," "build me a welcome
  series," "new subscribers never buy," "should we lead with a discount," or
  "buyers keep getting our first-order emails."
license: MIT
---

# Welcome Series

Most welcome series are a coupon with four reminders stapled to it. They open
with 15% off, repeat it four times, and keep mailing "make your first purchase"
to people who already did. Then the team reads last-touch revenue off the flow
report and calls it the best program they have. Some of that revenue was coming
anyway. This skill builds the version you can defend: a sequence that earns the
first purchase, gets out of the way the moment it happens, and proves its lift
against people who got nothing.

## When to use this skill

Use it when someone says:

- "Our welcome flow isn't converting."
- "Build me a welcome series for new email subscribers."
- "New subscribers sign up and never buy."
- "Should the welcome email lead with a discount?"
- "Customers who already ordered keep getting 'your first order' emails."
- "We want a welcome for people who re-subscribe."

**Leak zone:** activation (subscriber to first purchase) and the front edge of
early-life (first purchase to second). This program owns the first. It hands the
second to `post-purchase` the moment an order lands.

**What it is not for:**

- Post-order onboarding, cross-sell, and the second-purchase push. That's
  `post-purchase` in this plugin. Welcome's job ends at the order.
- Cart abandonment. That's `cart-abandon` in this plugin; I only define how
  welcome yields to it.
- Deciding whether activation is actually your leak. That's
  `retention-diagnosis`. **If you don't know where the leak is, I route you
  there first and I won't design in the dark.** A beautiful welcome series on a
  business whose real leak is day-60 lapse is a nice-looking waste of a quarter.
- The words. I give you the frame for each touch; `lifecycle-messaging` or your
  writers turn it into copy.
- Priority and frequency rules across every program. That's
  `journey-architecture`. I state welcome's defaults and flag the collisions.

## What I need before I start

**Required**

- **The subscribe event you can actually detect,** with a timestamp and the
  signup source (pop-up, footer, checkout opt-in, SMS keyword). No reliable
  trigger, no program.
- **Order data joinable to the subscriber, and how fast it lands.** Real-time
  order events or a nightly batch? This decides whether the purchaser exit works.
  It's the most important question on this list.
- **Consent status per channel.** Email, and SMS if you want the last-call touch
  on SMS.
- **AOV and gross margin,** if an incentive is on the table. I won't size a
  discount without them.
- **Whether the signup form promises an incentive.** If it does, touch 1 owes
  that code. That changes the architecture.

**Optional, and what each buys you**

- Monthly new-subscriber volume. Without it I can't tell you whether a 6-week
  read is possible; I'll say so rather than pretend.
- Category of interest (from the form or first browse). Unlocks the guide split.
- Current 30-day purchase rate for new subscribers. Replaces my baseline
  `[Assumption]` in the sample-size math.
- Review volume and rating. Feeds the proof touch.
- `.claude/lifecycle-context.md` and `.claude/retention-snapshot.md` if they
  exist. I read them first and don't re-ask.

With partial inputs I still produce the full blueprint. Every missing number
becomes `[Assumption]`, and I list which ones to replace before launch. What I
won't do with partial inputs is claim the program will work.

## The thesis

I think the discount-first welcome is the most expensive habit in lifecycle
marketing. It trains a brand-new subscriber, on day zero, that the list is where
the markdowns live. Then it pays that markdown to a slice of people who were
going to buy at full price anyway. Many new subscribers sign up mid-purchase.
They didn't need 15% off. They needed a receipt.

So this program argues before it bribes. Touch 1 makes the brand's promise.
Touch 2 proves it. Touch 3 removes the reason people stall. Only on day 7, and
only to people who still haven't bought, does an incentive appear. It expires on
a real date, and touch 5 is the last call on it. Anyone who buys at any point
leaves immediately for `post-purchase`. I worry more about that exit than about
any subject line. Letting buyers keep getting "buy your first" emails is the
most common welcome bug I know. It leaks margin. It also tells a new customer
you don't know who they are.

**The sacrifice.** This program does not chase the second purchase itself. It
does not re-engage subscribers who went quiet after day 14; that's BAU and,
later, `winback-series`. It does not win back lapsed customers who happen to
re-subscribe with a full promo stack. And it does not run without a holdout,
because a retained customer is not a saved customer. That applies here too.

## Program blueprint

### Objective and audience

- **Objective:** maximize incremental revenue per new subscriber in the 30 days
  after signup. The first purchase happens inside welcome. The second happens
  inside `post-purchase`, and both count toward the KPI.
- **Entry audience:** anyone who newly opts in to email marketing with no prior
  order on record. Returning customers who re-subscribe enter the two-touch
  variant instead.
- **Leak zone:** activation, with early-life handed off at the order.

### Message architecture

Default path: new subscriber, no prior order, no purchase yet.

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Promise | Day 0, within minutes of signup. Intent peaks at the moment of opt-in and decays within hours. | Email | Believe what this brand is for and why it's different, in one idea | The brand's single most defensible claim (origin, material, method) | Shop the core range or bestsellers | Leading with a discount. If the form promised a code, deliver it plainly and don't make it the argument. |
| 2 | Proof | Day 2. Long enough to not stack on touch 1, short enough that the brand is still remembered. | Email | Believe other people like them bought and were glad | Review snippets with rating and count; UGC | Shop the most-reviewed items | Stacking claims with no proof; inventing or cherry-picking reviews |
| 3 | Guide | Day 4. By now the stall is usually "which one?" or "will it fit / work for me?" | Email | Know which product to start with | Fit, sizing, or starter guide; category bestsellers from their stated interest | Take the quiz or go to the starter pick | Dumping the whole catalog; any incentive |
| 4 | Offer | Day 7, non-purchasers only. The first three touches have done their job for anyone they were going to convert at full price. | Email | Have a concrete, time-limited reason to act now | The offer itself, with a real expiry and plain terms | Redeem the first-order offer | Appearing before day 7; reaching anyone who already bought; a bigger discount than margin allows |
| 5 | Last call | Day 10, 24–48 hours before the offer expires. Deadlines work when they're real. | Email; SMS only if SMS-consented | Act before the offer ends, or decide not to | Expiry date and time; the guarantee or return policy that de-risks the order | Redeem before expiry | Fake urgency; extending the offer; a second, bigger offer |

Day 14 is the program's end. Non-purchasers leave for BAU on day 14.

**Re-subscriber variant (known customer, 2 touches).**

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| R1 | Welcome back | Day 0. Acknowledge the relationship at the moment they opted back in. | Email | Feel recognized, and know what's changed since they last bought | What's new since their last order date (range, policy, service) | Set preferences or shop what's new | Any first-order incentive; pretending they're new |
| R2 | Relevant next step | Day 3. Gives R1 room to breathe before a product ask. | Email | See the one product that fits their history | Replenishment timing or a complement to their past order | Shop the recommended item | Discounting; re-running the five-touch series |

### Splits and personalization

- **Entry split: prior order or not.** Order history on the email or the matched
  customer ID decides five-touch versus the re-subscriber variant. This is the
  one split that is never optional.
- **Holdout split: random, at entry.** 10% default, 20% if volume is thin (see
  Measurement). Holdout gets nothing from this program.
- **Signup-source split: promised-incentive forms versus everything else.** If
  the pop-up promised a code, touch 1 delivers it and touch 4 becomes a reminder
  of that same code, not a second offer. I'd push to test the form without the
  promise, but that's an acquisition decision, not a welcome one.
- **Category-of-interest split** on touches 2 and 3, only when the attribute
  exists for at least a third of entrants `[Assumption]`. Below that, the
  fallback block does the work and the split is decoration.
- **Cut:** first-name tokens in subject lines, weather, and send-time
  personalization on touch 1. None of them change a decision this program makes.

### Exits and suppression

- **Purchase, any channel, any time: exit immediately to `post-purchase`.** This
  is the bug. Check it three ways: as a program-level exit on the order event, as
  a filter re-evaluated before every send, and as a data-latency check. If
  orders land in a nightly batch, a buyer at 9 a.m. still gets the 7 p.m. offer.
  Fix the feed or move the send, then verify with a live test profile.
- **Unsubscribe, hard bounce, or spam complaint:** exit, no destination.
- **Day 14 without purchase:** exit to BAU newsletter. No extension, no "one
  more" offer.
- **Cart or browse abandon while in welcome:** cart abandon takes priority and
  welcome pauses. The day-7 offer is skipped if cart abandon already sent an
  incentive, so no one holds two. `journey-architecture` owns the final rule.
- **Suppressed while in welcome:** BAU promotional campaigns with a discount,
  days 0–10, so nothing undercuts the fenced offer. Transactional messages are
  never suppressed.
- **Re-entry:** once per person, ever. Re-subscribers who already completed
  welcome get the variant, not a second run.

### Content blocks

| Block | Used in | Data it needs | Fallback |
|---|---|---|---|
| Brand promise | 1, R1 | Static, owned by the brand team | None needed |
| Review strip | 2, 5 | Reviews feed: rating, count, snippet, product ID | Aggregate rating only |
| Category bestsellers | 2, 3 | Catalog feed with in-stock flag; category of interest | Sitewide bestsellers, in stock |
| Starter guide | 3 | Fit/size/quiz content per category | The general starter guide |
| Offer | 4, 5 | Unique or shared code, expiry timestamp, purchaser suppression | None; if the code pool is empty, the touch doesn't send |
| Guarantee strip | 5 | Return and shipping policy | Required; no fallback |
| What's new | R1 | Last order date; changelog of range and policy | Top new arrivals |
| Recommended next | R2 | Order history; replenishment or complement mapping | Bestseller in their past category |

## Platform build mapping

In primitives. ESP specifics for Braze, Klaviyo, Iterable, and SFMC are in
`references/platform-build.md`.

- **Trigger:** email marketing opt-in event, with signup source and timestamp.
- **Filter:** email consent true; not on global suppression; never entered
  welcome before. Re-checked before every send, including "no order since
  entry."
- **Split:** random holdout at entry; prior order (variant) versus none;
  signup source; category of interest on 2–3.
- **Wait:** fixed delays of 2, 2, 3, and 3 days, each as a wait that also
  listens for the order event, not a blind timer.
- **Exit:** order event (to `post-purchase`); unsubscribe, bounce, or complaint;
  day 14 (to BAU).

## QA

This skill is read-only. It never sends. It tells a human what to verify before
they activate. The five checks that catch the most expensive errors, in order:

1. **Purchaser exit, tested live.** Enter a test profile, place a real or test
   order between touches 2 and 4, and confirm touch 4 never sends. Then check
   when that order reached the platform. Most failures here are data latency.
2. **Offer fence.** Confirm touch 4 and 5 filters exclude purchasers and the
   re-subscriber variant, and that the code expires when the copy says it does.
3. **Holdout.** Random, assigned at entry, receiving nothing, and logged so the
   analyst can find it.
4. **Re-subscriber routing.** A test profile with a past order lands in the
   two-touch variant, not touch 1.
5. **Fallbacks.** Every dynamic block renders for a profile with no category,
   no name, and no browse history.

Full list: `references/qa-checklist.md`.

## Measurement

Detail lives in `references/measurement.md`. The four decisions live here.

- **Primary KPI: revenue per new subscriber, 30 days from entry,** treated
  versus holdout. Total revenue from all orders by that person in the window,
  divided by everyone who entered, buyers and non-buyers. Not attributed
  revenue, not opens, not clicks.
- **Guardrails:**
  - Unsubscribe rate per send under 0.5% `[Assumption]`.
  - Spam complaint rate under 0.1% `[Assumption]`.
  - Discount cost per treated subscriber below the incremental gross margin the
    program produces.
  - Full-price first-purchase rate in treated no lower than in holdout. If it
    is, the offer is cannibalizing.
  - 60-day second-purchase rate, as a lagging check that welcome buyers aren't
    discount-only buyers.
- **Holdout recipe:** 10% of entrants, randomized per subscriber at entry (not
  at send), receiving nothing from this program but the same BAU and
  transactional mail as everyone else. The read cohort is everyone who entered
  in the first 12 days, so each has a complete 30-day window by the week-6 read.
  At a 3% baseline 30-day purchase rate `[Assumption]` and a target of 4.5%
  `[Assumption]`, that's about 11,800 entrants at 10% holdout, or about 6,950 at
  20% (80% power, 5% two-sided alpha). If 12 days of signups can't reach 6,950,
  I'll tell you the 6-week read is not possible and we set an honest date instead.
  Welcome needs this too: many new subscribers would buy anyway.
- **Kill condition:** if, at the week-6 read, treated revenue per new subscriber
  doesn't beat holdout with a lift whose confidence interval excludes zero, we
  stop and redesign the offer touch first: size, fence, timing, then expiry. One
  redesign, one more 6-week read. If that fails too, the problem is upstream of
  the offer, and it goes back to `retention-diagnosis`.

I append the holdout plan, the read date, and the kill condition to
`.claude/decisions.md` so the next skill can hold us to it.

## Field notes

- I rebuilt the lifecycle program suite at a home-furnishings retailer; revenue
  per email rose 4x in 7 months `[Fact — author's record]`. Welcome shipped
  first because it had the cleanest holdout and the fastest read `[Fact —
  author's record]`.
- Skill-driven pre-send QA caught about 3 errors a week before send. The most
  common welcome catch was the purchaser-exit bug `[Fact — author's record]`.
  That's why it is QA check #1 and not a footnote.
- Campaign output went from 7 to 21 a week with the same team `[Fact — author's
  record]`. The lesson I took: a shippable v1 in week 1 beats a perfect program
  in quarter 2. Ship the five touches with the holdout. Tune later.

## Worked example

`examples/example-brief.md` walks Tidewell Coffee Co., an invented DTC coffee
brand, from brief to build spec. The team wants 15% off in the first email and
the same five emails for everyone. We move the incentive to a fenced day-7
touch, route past buyers to the two-touch variant, and add the purchaser exit
they didn't know was missing. Their volume is about 5,000 new subscribers a week
`[Assumption]`. That's too thin for a 10% holdout to read in 6 weeks, so the
first read runs a 20% holdout and drops to 10% once the program has proven lift.

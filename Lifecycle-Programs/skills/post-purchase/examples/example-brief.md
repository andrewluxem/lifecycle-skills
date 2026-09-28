# Example brief: Tallgrass Kitchen Co.

Tallgrass Kitchen Co. is an invented brand. Every number below is invented and
labeled. No employer or client data.

## The brief

Tallgrass sells cast-iron skillets, Dutch ovens, and care products direct to
consumer. Their CRM lead writes:

> "Our shipping emails get great opens. Let's use them. Put a 15%-off-your-next-
> order code in the shipping confirmation, and ask for a review in the same
> email so we catch people while they're paying attention. Then send a
> bestsellers email a week after ship."

Two things in there are wrong. The shipping confirmation is a transactional
message; turning it into a promo spends trust and creates compliance risk. And
a review ask at ship date reaches someone who hasn't touched the skillet. The
instinct — use the attention — is right. The placement is wrong.

## Inputs

| Input | Value | Label |
|---|---|---|
| First orders per month | 4,500 | `[Assumption]` |
| AOV, first order | $92 | `[Assumption]` |
| Baseline 60-day first→second purchase rate | 18% | `[Assumption]` |
| Median days between orders 1 and 2 | 41 | `[Assumption]` |
| Median ship → delivered | 4 days | `[Assumption]` |
| Delivered event available | Yes, from their shipping integration | `[Assumption]` |
| TTFU, skillets and Dutch ovens | 3–5 days (first weekend cook) | `[Assumption]` |
| TTFU, care products (oil, scrubbers) | 0–2 days | `[Assumption]` |
| Share of first orders that are cookware vs. care-only | 85% / 15% | `[Assumption]` |
| Shipping email open rate vs. promotional | ~2.5x | `[Assumption]` |
| Transactional templates | Sent by the store platform, support conditional blocks | `[Assumption]` |

## Diagnosis check

Tallgrass had already run `retention-diagnosis`. Their snapshot put the dominant
leak in early-life: strong first orders, and most customers never placed a
second one `[Assumption — invented snapshot]`. That's this program's zone. If
the snapshot hadn't existed, I'd have stopped here and routed them to
`retention-diagnosis` before designing anything.

## Build spec

**Entry:** first order (order count = 1). Welcome-series purchasers exit
welcome on the same event and land here.

**Holdout:** 20% random at entry, customer-level, stored as a profile flag.

**Message architecture (cookware path):**

| # | Purpose | Timing + rationale | Channel | Job | Proof element | CTA | Anti-goal |
|---|---|---|---|---|---|---|---|
| 1 | Order confirmation + "what happens next" | On order | Email | Trust the order | Order summary, ship window | Order status | Any offer |
| 2 | Shipping confirmation + "season before first use" module | On ship | Email; SMS tracking if opted in | Be ready to cook on day one | Tracking, a 3-step care summary | Track package | The 15%-off code; the review ask |
| 3 | First-cook guide | Delivery + 1 day — the box is open that evening | Email | Cook something that sticks less than they feared | Short video, care FAQ | Watch the guide | Selling |
| 4 | Review / photo ask | Delivery + 10 days — two weekends of cooking `[Assumption]` | Email | "My first cook helps the next buyer" | Count of existing reviews | Rate it (one click) | Incentive tied to a good rating |
| 5 | Review reminder | Touch 4 + 6 days, non-reviewers only | Email | Same, lower friction | Same | Same | A third ask |
| 6 | Cross-sell: seasoning oil | Delivery + 17 days, no second order yet | Email | "This keeps the skillet working" | Share of skillet buyers who also buy the oil `[Assumption]` | Shop the oil | A discount; a bestseller grid; another skillet |

**Care-only path:** skip touch 3 (the guide is for cookware), review ask at
delivery + 5 days, cross-sell a skillet only if affinity data supports it,
otherwise skip 6.

**Splits:** TTFU class (cookware vs. care-only); reviewed-yet before 5; random
holdout at entry. No first-name or location personalization.

**Exits:** second order → exit; oil or scrubber buyers go to
`replenishment-reminders`, cookware-only second-order buyers go to
`loyalty-program`. Return/cancel → exit the marketing layer. Delivery exception
→ pause and restart from actual delivery. Program end (touch 6 + 7 days) →
hand off by product type.

**Primitives:**

- Trigger: `order_placed`, order count = 1.
- Filter: marketing consent for 3–6; no returns/cancels; no test accounts.
- Split: 20% holdout; cookware vs. care-only; reviewed yet.
- Wait: until delivered (max 10 days, fallback ship + 4); fixed delays after.
- Exit: second order, return/cancel, unsubscribe, program end → handoff.

## Measurement plan

- **Primary KPI:** 60-day first→second purchase rate, treated vs. holdout.
  Window ≈ 1.5 × 41 days.
- **Sample:** baseline 18% `[Assumption]`, 80/20 split, α 0.05, power 0.80. To
  detect a 2.5-point lift needs ~12,200 entrants (~2,400 control)
  `[Inference]`. At 4,500 first orders a month that's about 12 weeks of
  enrollment.
- **Dates:** launch week 1; enrollment closes end of week 12; final read end of
  week 21 (last cohort's 60-day window closes). Directional check at week 8,
  no decision on it.
- **Guardrails:** marketing unsubscribes on 3–6, complaints, first-order return
  rate, discount rate on second orders, "where is my order" contacts.
- **Kill condition:** if treated doesn't beat holdout by at least 2.5 points
  absolute on 60-day second-purchase rate at the week-21 read (matching the
  MDE — a smaller kill threshold couldn't be detected), or a guardrail breaches
  two weeks running, Tallgrass cuts the cross-sell, keeps the review ask only if
  it's not raising unsubscribes or returns, and goes back to
  `retention-diagnosis`.

## What we deliberately didn't do

- **No 15%-off code** in the shipping email or anywhere in the program. If a
  second-order incentive is ever on the table, it's a separate test with a
  margin guardrail, and the conversation starts in `retention-metrics`.
- **No bestsellers grid.** One complementary item, because a grid tests nothing
  and teaches the customer to wait for a sale.
- **No reorder clock for oil.** That's `replenishment-reminders`.
- **No points or tiers.** That's `loyalty-program`.
- **No finished copy.** The touch specs go to `lifecycle-messaging` or
  Tallgrass's writers.
- **No collision rules with their weekly promo.** That's `journey-architecture`;
  for now, promo sends that would cross-sell a different item are suppressed
  while a customer is in touches 3–6.

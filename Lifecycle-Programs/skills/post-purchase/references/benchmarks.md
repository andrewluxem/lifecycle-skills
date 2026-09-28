# Benchmarks: post-purchase

Every number in this file is `[Assumption]`. None of it is cited, and none of it
is a measured result. It's a starting point for a test, never a target. The goal
is to replace each row with your own data after one cycle.

## Timing defaults

The marketing clock starts at **delivery**, not ship date. If you have no
delivery event, estimate it as ship date + your median transit time and label
every downstream timing `[Assumption]`.

| Touch | Default timing | Range worth testing | Label |
|---|---|---|---|
| 1. Order confirmation | Immediately on order | None — it's transactional, send it now | `[Assumption]` |
| 2. Shipping confirmation | On ship event | None — send on the event | `[Assumption]` |
| 3. How-to / first use | Delivery + 1 day | Delivery day (setup-heavy) to delivery + 3 days | `[Assumption]` |
| 4. Review / UGC ask | Delivery + TTFU + 3–5 days | See TTFU table below | `[Assumption]` |
| 5. Review reminder | Touch 4 + 5–7 days | 4–10 days; never a second reminder | `[Assumption]` |
| 6. Cross-sell | Delivery + TTFU + 7–14 days | Before touch 4 vs. after touch 5 — test it | `[Assumption]` |
| Handoff | Touch 6 + 7 days, or on second order | Up to day 45–60 post-delivery | `[Assumption]` |

### Time-to-first-use (TTFU) by category

This is the number most teams never measure and the one this program is built
around. These are placeholders.

| Category shape | Example | TTFU default | Review ask lands | Label |
|---|---|---|---|---|
| Instant | Apparel, accessories, books | 0–2 days | Delivery + 4–7 days | `[Assumption]` |
| Days | Cookware, small appliances, supplements | 3–7 days | Delivery + 8–14 days | `[Assumption]` |
| Weeks | Skincare, furniture, fitness gear | 14–28 days | Delivery + 18–35 days | `[Assumption]` |
| Assembly/install | Large furniture, electronics setup | Varies by install date | After install event if you have one | `[Assumption]` |

## Attention benchmarks

| Metric | Placeholder | Label |
|---|---|---|
| Order/shipping open rate vs. promotional | 2–3x | `[Assumption]` |
| Review submission per 100 review asks | 3–8 | `[Assumption]` |
| Cross-sell click-to-order on a single-item recommendation | 1–4% | `[Assumption]` |
| First→second purchase within 60 days, no program | 15–25% (DTC retail) | `[Assumption]` |

Don't set a target from these. Pull your own baselines first.

## Split defaults

- **Holdout:** 10–20% at entry, customer-level. Smaller only if your volume is
  large enough to hit the minimum detectable lift (see `measurement.md`).
- **A/B tests inside the treated arm:** 50/50, and only after the holdout read
  is running. One test at a time; the holdout is the first question.
- **Minimum audience per cell before an A/B test is worth running:** enough to
  detect the effect you care about on the metric you care about. For
  review-submission tests that's usually a few thousand asks per cell
  `[Assumption]`; for second-purchase tests, far more.
- **TTFU split:** only if at least two TTFU classes each carry a meaningful
  share of first orders. One dominant category → one path.

## Content defaults

What each touch typically carries, and the tests worth running first, ranked by
expected value:

1. **Review ask timing** (touch 4: delivery + TTFU vs. ship + 7). Highest value
   because it tests the thesis, and it moves both review volume and the
   likelihood the customer hears from you after a good experience.
2. **Cross-sell presence and timing** (touch 6 on vs. off, then early vs. late).
   Tells you whether the program's revenue comes from this touch or from the
   experience touches.
3. **How-to format** (guide vs. short video). Moderate value; affects returns as
   much as repurchase.
4. **Review ask channel** (email vs. SMS for consented customers). Only if SMS
   consent is widespread.
5. **Transactional module content** (what goes in the "get ready" module).
   Lowest priority: small audience effect, and every change needs compliance
   review.

Tests I would not run: discount vs. no discount in the shipping email (don't
put it there), incentive-for-review variants that depend on the rating given.

## How to replace these numbers

| Benchmark | Query or report |
|---|---|
| Delivery lag | Delivered timestamp minus ship timestamp, median and p90 by carrier and region |
| TTFU | Survey a sample ("when did you first use it?") or proxy with first app/registration/support event after delivery |
| Transactional vs. promo open rate | Your ESP's open rate by message type, last 90 days; treat Apple Mail Privacy Protection–inflated opens with suspicion |
| Baseline first→second rate | Share of first-order customers from a pre-program cohort with a second order within the window |
| Days between orders 1 and 2 | Median across customers with 2+ orders, last 12 months |
| Review submission rate | Reviews submitted / review asks sent, by category |

After one full cycle, this file should be irrelevant to you.

# "Boring levels" IB strategy check (Nov 2 2026, updated with all her levels)

Results sheet: artifact **"IB Strategy Check"**. Research only, not advice.

## Her claims
- "$62,000 in prop payouts in August, $42,000 in September."
- "My best setup wins about 70% of the time."

## Her rules, as coded
- **Initial balance (IB):** the high and low of 9:30–10:29 ET. IB mid = halfway between them.
  - She trades 10:30–15:00 and skips the last hour.
- **Failed auction:**
  - Price goes outside the IB, then a candle closes back inside.
  - Enter at that close. Stop beyond the swing of the move outside.
  - Target: IB mid.
- **Trend continuation:**
  - The IB trend is set by the IB close against the 9:30 open.
  - Price pulls back to IB mid, then a candle closes back on the trend side.
  - Stop beyond the pullback. Target: the IB high (in an uptrend) or IB low (in a downtrend).
  - Confluence: the anchored VWAP from 9:30 sits near IB mid.
- **Tokyo session:** the 18:00–20:00 range.
  - From 20:00, trade a sweep and fade of the range, or a breakout and retest.
- **Risk:** $200 per trade. Stop for the day after 2 losses.
- **Also tested:**
  - a close outside the IB (instead of a wick) for the failed auction;
  - a 10:30–12:00 window;
  - targets of 1R, 2R, 3R, 4R and the far side of the range;
  - a fixed 50-pt stop at 1:2;
  - random-time entries with the same stop and target.

## Her levels, now all coded
- **Previous day high / low:** the 18:00–17:00 session.
- **London high / low:** 02:00–08:00 ET.
- **Previous session volume profile** (POC = busiest price, VAH / VAL = top and bottom of the 70% value area):
  - NQ / ES: the NY 9:30–16:00 session. Gold: the full 18:00–17:00 session, as she says.
- **Previous week volume profile:** Sun 18:00 to Fri 17:00.
- **Supply / demand zones on 30m and 60m:**
  - An aggressive displacement candle: body ≥ 1 ATR and a close beyond the prior candle's high / low.
  - "Strict" = body ≥ 1.5 ATR, coming out of a tight 3-candle range.
  - The zone = the candle to the left, body high to body low. It dies on a close beyond its far side.
- **VWAPs:** NY anchored (9:30), weekly, Asia (18:00).
- **Level trade:**
  - Price comes to a level, then within 12 candles a candle closes back past it in its color.
  - "Aggressive" = it also closes beyond the prior candle's high / low.
  - Stop beyond the swing. Target: the next level at least 1R away (her "look left"), 1R–4R, or a fixed 1:2.
- **A+** = 2 or more levels stacked within 0.2 × the stop (NQ 10 pts).
- **Confluence on her IB and Tokyo setups:**
  - Failed auction: the swing reaches a level.
  - Trend continuation: a level sits at IB mid.
  - Asia: if Asia opens inside the previous value area, short VAH / long VAL.

## Levels results (NQ 2022–25, then MNQ 2026)
| Setup | Chart | Trades | WR | avg RR | t-score | 2026 avg RR |
|---|---|---|---|---|---|---|
| All her levels, aggressive, next-level target | 5m | 6,776 | 42% | −0.04 | −2.9 | −0.10 |
| All her levels, aggressive, next-level target | 1m | 8,544 | 37% | −0.08 | −5.3 | −0.03 |
| A+ (2+ levels stacked) | 5m | 5,700 | 42% | −0.05 | −3.5 | −0.12 |
| A+ (2+ levels stacked) | 1m | 7,236 | 37% | −0.09 | −5.4 | −0.04 |
| Failed auction + swing into a level (her A+) | 5m | 539 | 37% | −0.05 | −0.7 | +0.26 (58 trades) |
| Failed auction + swing into a level (her A+) | 1m | 531 | 27% | −0.11 | −1.2 | +0.81 (31 trades) |
| Trend continuation + VWAP + level | 5m | 262 | 45% | −0.01 | −0.2 | +0.41 (27 trades) |

- **546 level combos** had 30+ trades in both periods. **0 passed.** Random entries: 0 passed.
- **No single level family works on its own:**
  - previous day, London, session VP, week VP, 30m zones, 60m zones;
  - strict zones on first touch only.
- **Asia levels and the Asia VP rule lose.** The Asia VWAP retest is about 0.
- **ES and gold:** nothing holds in both halves.

## Dollars after the fix
- **The fix:** one trade at a time, and the 2-loss stop is counted only when the losses close.
- **Why:** an earlier draft counted losses at entry. That looked ahead and made the playbook look profitable.

| Setup | Chart | 2022–25 per month | 2026 per month |
|---|---|---|---|
| Her full playbook (IB + A+ levels + Tokyo sweep) | 5m | −$444 | −$27 |
| Her full playbook | 1m | −$1,427 | −$603 |
| IB setups only | 5m | −$255 | +$1,053 |
| IB setups only | 1m | −$662 | +$704 |

## Results
**NQ 2022–25 (3 years, 430–735 trades per setup), her exact rules:**

| Setup | Chart | WR | avg RR | PF | t-score |
|---|---|---|---|---|---|
| Failed auction → IB mid | 5m | 36% | −0.04 | 0.93 | −0.7 |
| Failed auction → IB mid | 1m | 25% | −0.15 | 0.81 | −2.0 |
| Trend continuation → IB edge | 5m | 44% | −0.04 | 0.94 | −0.6 |
| Trend continuation → IB edge | 1m | 29% | −0.02 | 0.97 | −0.2 |
| Trend continuation + VWAP at IB mid | 5m | 44% | −0.03 | 0.94 | −0.4 |
| Tokyo sweep-fade, 3R | 5m | 30% | −0.15 | 0.79 | −2.6 |
| Tokyo breakout-retest, 3R | 5m | 31% | −0.11 | 0.85 | −1.6 |

**MNQ 2026 (5m, small sample):**
- Trend continuation: 65 trades, WR 46%, avg RR +0.25, PF 1.45, t-score 1.2.
- Failed auction: 103 trades, WR 44%, avg RR +0.19, PF 1.33, t-score 0.8.
- These are positive, but below the t-score 2 bar.

**ES and gold (2026):**
- 20–60 trades per test, mostly about 0 or negative.
- Nothing passes t 2 in both halves.

## The claims vs the data
- **No 70% win rate.**
  - With her targets: 25–46%.
  - Even with a 1R target: about 48–51%.
- **Dollars on one NQ account** ($200 risk, max 2 losses a day, both IB setups):

| Period | $ per month | Best month | 50k eval pass rate |
|---|---|---|---|
| 2022–25 | −$256 (5m) / −$662 (1m) | +$5,800 | 17% |
| 2026 | +$1,050 (5m) / +$700 (1m) | +$3,700 | 60–71% (only 5–7 tries) |

- **The $62k month:**
  - It would need about 10 accounts in a best-ever month, or about 60 accounts at the 2026 average, all copying the same trades.
  - Big payout totals across many accounts don't prove an edge. Losing stretches only burn cheap evaluations, and the winners get shown.

## Verdict
- **Her IB rules are about breakeven to losing over 3 years of NQ.** 2026 was a good stretch, but it is not enough to call it an edge.
- **The claimed 70% win rate does not show up** with any target.
- **Her risk rules are sound:** fixed dollar risk, 2-loss daily stop, no news, skip the last hour. Use them.
- **The entries themselves show no edge in this data, with or without her levels.** Adding her levels does not help; the full playbook loses more than the IB setups alone.

## Files
- ibtest.py: IB / Tokyo rules and grader.
- lvtest.py: her levels (volume profile, zones, PDH / PDL, London, VWAPs) and the level trades.
- lvagg.py, lvagg2.py, mksum7.py: level summaries and dollars.
- lvtest.parquet: every trade, with entry and exit times.
- ibagg.py, ibagg2.py, mksum6.py: summaries.
- ibtest.parquet: every trade.

# Chart Fanatics strategies vs their claims (Nov 2 2026)

Results sheet: artifact **"Chart Fanatics Strategy Check"**. Research only, not advice.

## What was tested
- **Strategies:** six futures strategies, coded from each trader's own rules:
  - Fabio Valentini's rules come from the full 3.5-hour episode;
  - the other five come from their TradeZella pages.
- **Data:**
  - NQ Dec 2022 – Nov 2025 (P1) against MNQ 2026 (P2);
  - MES and MGC: the first half of 2026 against the second half.
- **Grid:** every entry × stop × target × exit, plus the fixed 1:2 test (NQ 50 / ES 20 / gold 12).
- **Random twin:** every trade gets one.
- **PASS** = t-score 2+ in both periods.
- **Not tested:** JLaw, Clement Ang and Marios Stamatoudis trade stocks, and there is no stock data here.
- **Data warning:** MNQ 1m covers only about 2 months of 2026, so the 1m strategies have few P2 trades.

## Short answer
- **None of the six pass.** The combos with 30+ trades in both periods gave 0 passes, and the random entries passed 2 of Marci's combos.
- **The traders' own exact rules lose or sit near 0 on NQ 2022–25 for four of them:** JJ Simon, Candace Lau, Dhesi, and Okala's main rule.
- **The claimed results can't come from these rules on one account.** Those claims are 500% and 320% returns, plus $1.8M and $5M+ in prop payouts.

## Claims vs test
| Trader | Their claim | The test |
|---|---|---|
| **Fabio Valentini** (Auction Market) | Top 3 in the Robbins World Cup, "over 500%" in 12 months. 1:2.5 minimum, 1:5 common. Risk 0.25–0.5% per trade. | **Trend model, NQ 1m:** 115 trades in 3 years, WR 39%, avg RR +0.29 at 1:2.5 (t 1.8). That is about +6% a year at 0.5% risk; 500% would need about +360R a year. **Mean reversion:** −0.13. |
| **JJ Simon** (Fair Pricing) | Over $1.8M in payouts on up to 45 accounts. About 20% WR at 1:4. Evaluations always 25 pt stop / 38 pt target, 25–33% pass rate. | **His evaluation rule:** WR 37%, avg RR −0.10 on 4,729 trades (t −5.6), and −0.10 again in 2026. **50k pass rate:** 17%, then 0 of 5. **The 1:4 continuation** does hit his ~20% WR (22%), but avg RR is only +0.03. |
| **Okala** (80/20) | More than $5M in payouts (his own website). 10 pt stop, half off at +15. | **Full rule on 1m:** −0.12. On 3m / 5m it is positive in 2022–25 but negative in 2026. **The H short alone:** +0.65 (146 trades). **The Fork long:** −0.38. |
| **Candace Lau** (Sweep + IFVG) | At least 1:2. | **1:2:** WR 35%, avg RR −0.06 (1,174 trades). **London only:** −0.16. |
| **Dhesi** (Liquidity Inversion) | No stats. | **Half off + runner:** −0.03. **1:2:** +0.12, but that comes mostly from 2023; 2026 is −0.23. |
| **Marci Silfrain** (Measured Move) | 320% in the Robbins World Cup. | **NQ:** 5m −0.07, 15m +0.12 then −0.05. **ES 15m:** +0.28 / +0.27 (small sample). **Gold 15m:** +0.10 / +0.10. **Her favourite 1st and 2nd structures** are no better. |

## Worth watching (not proven)
- **Fabio's NY trend model**
  - **The setup:** price is out of the previous session's value area. It pulls back to the low-volume price of the move (the low-volume node), then a big full-body candle on high volume closes back in the trend direction. The stop goes 2 ticks past that candle.
  - **Results by year, half off at 1:2 with the runner to the previous day high / low:** +0.30, +0.55, +0.23 and +0.45 in 2023, 2024, 2025 and 2026. The random twins lose in most years.
  - **Weak spots:**
    - only about 38 trades a year;
    - t-score about 2.1 in 2022–25;
    - just 19 trades in 2026;
    - it loses on 5m.
- **Okala's H short**
  - **The setup:** a bounce into an 80 level fails. Enter with a limit at the 80, a 10 pt stop, half off at +15, and the runner to the close.
  - **Results by year:** +0.44, +0.76, +0.80 and +0.94 in 2023, 2024, 2025 and 2026.
  - **Weak spots:**
    - only 14 trades in 2026;
    - t-score 1.9;
    - taking everything off at +15 instead turns it negative in 2025–26.

## Why the claims and the test differ
- **Payout totals across many prop accounts don't prove an edge.** Losing evaluations are cheap, and only the wins get shown. JJ himself spent about $400k on evaluations and fees.
- **Contest returns come from one hot stretch** at high risk, not from the average expectancy.
- **Fabio's real trigger can't be seen in candle data.** He enters on big-order bubbles (20–40 contracts) and CVD (a running total of buying minus selling). Candles can't show those, so a volume spike stands in for them. Any edge he has may live in that order flow, which this test can't check.

## Files
- `cfstrat.py`: every strategy's signal rules.
- `cfrun.py`: the grid runner.
- `cfagg.py`: the summaries.
- `cf_trades*.parquet`: every trade.
- The same scripts are saved in the MMM-TEST-LAB repo under `python/archive/cf/`.

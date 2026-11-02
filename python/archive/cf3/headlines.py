"""Each trader's own rule(s) to headline (label, market, chart minutes, filters, $ risk per trade, losses-per-day stop) and their claims."""
F = lambda **k: k
HEAD = {
 'Fabio Valentini': [
  ('Trend model: half at 1:2, runner to prev day H/L', 'NQ', 1, F(tagstart='TREND', stop='col wk', target='col tp', exit='half 2'), 500, 4),
  ('Trend model: 1:2.5 (his minimum)', 'NQ', 1, F(tagstart='TREND', stop='col wk', target='2.5', exit='stop/target'), 500, 4),
  ('Mean reversion London: target previous POC', 'NQ', 1, F(tagstart='MEAN REV London', stop='col wk', target='col tp', exit='stop/target'), 500, 4),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'JJ Simon': [
  ('Eval rule: 25 pt stop, 1:1.5', 'NQ', 1, F(stop='pts 25.0', target='1.52', exit='stop/target'), 500, 3),
  ('Reversion to fair price', 'NQ', 1, F(tagstart='REV', stop='pts 25.0', target='col tp', exit='stop/target'), 500, 3),
  ('Continuation 1:4 (his "20% WR at 1:4")', 'NQ', 1, F(tagstart='CONT', stop='pts 25.0', target='4', exit='stop/target'), 500, 3),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Okala': [
  ('10 pt stop, half at +15, break-even runner (1m)', 'NQ', 1, F(entry='market', stop='pts 10.0', target='none', exit='half 1.5'), 200, 3),
  ('H short, limit at the 80, 10 pt stop, half at +15 (1m)', 'NQ', 1, F(tag='H short', entry='limit lim', stop='pts 10.0', target='none', exit='half 1.5'), 200, 3),
  ('Fork long, 10 pt stop, half at +15 (1m)', 'NQ', 1, F(tag='Fork long', entry='market', stop='pts 10.0', target='none', exit='half 1.5'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Candace Lau': [
  ('Limit in the IFVG, sweep stop, 1:2', 'NQ', 1, F(entry='limit lim', stop='col wk', target='2', exit='stop/target'), 200, 3),
  ('London only, limit, sweep stop, 1:2', 'NQ', 1, F(tagstart='London', entry='limit lim', stop='col wk', target='2', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Dhesi': [
  ('Structure stop, half at 1:1.5, runner to opposing level', 'NQ', 1, F(stop='col wk', target='col tp', exit='half 1.5'), 500, 2),
  ('Structure stop, 1:2', 'NQ', 1, F(stop='col wk', target='2', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Marci Silfrain': [
  ('Measured move, NQ 15m', 'NQ', 15, F(stop='col wk', target='col tp', exit='stop/target'), 200, None),
  ('Measured move, NQ 5m', 'NQ', 5, F(stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Measured move, ES 15m', 'ES', 15, F(stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts), NQ 15m', 'NQ', 15, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'TG Capital': [
  ('Trident, FVG stop, ride until the EMA stack breaks (NQ 30m)', 'NQ', 30, F(entry='market', stop='col wk', target='none', exit='EMA stack breaks'), 500, None),
  ('Trident, FVG stop, 1:20 (his claim)', 'NQ', 30, F(entry='market', stop='col wk', target='20', exit='stop/target'), None, None),
  ('Trident, gold 30m, ride the EMA stack', 'GC', 30, F(entry='market', stop='col wk', target='none', exit='EMA stack breaks'), None, None),
  ('Max fixed 1:2 (50 pts), NQ 30m', 'NQ', 30, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Tori Trades': [
  ('Trendline bounce, out on a close through the line (NQ 4H)', 'NQ', 240, F(tagstart='Bounce', stop='col wk', target='none', exit='stop/target'), 500, None),
  ('Trendline break, out on a close back through the Safety Line (NQ 4H)', 'NQ', 240, F(tagstart='Break', stop='col wk', target='none', exit='stop/target'), None, None),
  ('Trendline bounce, gold 4H', 'GC', 240, F(tagstart='Bounce', stop='col wk', target='none', exit='stop/target'), None, None),
  ('Trendline bounce, NQ 1H', 'NQ', 60, F(tagstart='Bounce', stop='col wk', target='none', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts), NQ 4H', 'NQ', 240, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Jade Cap': [
  ('Raid + FVG, limit at the FVG, stop above the raid, target opposite liquidity (5m)', 'NQ', 5, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), 500, 2),
  ('Same on 1m', 'NQ', 1, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts), 5m', 'NQ', 5, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Trader Kane': [
  ('SMT + FVG break, stop above the SMT high, target 50% of the impulse (3m)', 'NQ', 3, F(entry='market', stop='col wk', target='col tp', exit='stop/target'), 500, 2),
  ('SMT, 25 pt stop, 1:1 (his 100-tick base hit)', 'NQ', 3, F(entry='market', stop='pts 25.0', target='1', exit='stop/target'), None, None),
  ('SMT, structure stop, half at 1:1, break-even runner to 1:4 (3m)', 'NQ', 3, F(entry='market', stop='col wk', target='4', exit='half 1'), None, None),
  ('Max fixed 1:2 (50 pts), 3m', 'NQ', 3, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Tanja Trades': [
  ('AMD: limit in the FVG, stop past the sweep, target range opposite (5m)', 'NQ', 5, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), 500, 2),
  ('AMD on NFP Fridays only (her news days, partial)', 'NQ', 5, F(tag='news day', entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Same on 1m', 'NQ', 1, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts), 5m', 'NQ', 5, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Andrea Cimitan': [
  ('Failed auction at VAL / VAH, target POC', 'NQ', 5, F(tagstart='Failed auction', stop='col wk', target='col tp', exit='stop/target'), 500, 3),
  ('Failed auction with absorption (volume + wick)', 'NQ', 5, F(tag='Failed auction absorbed', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Breakout with acceptance, OR stop, 1:2', 'NQ', 5, F(tag='Breakout acceptance', stop='col wk', target='2', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 5, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Carmine Rosato': [
  ('LVN pullback, stop past the zone, target high / low of day', 'NQ', 1, F(tag='LVN pullback', stop='col wk', target='col tp', exit='stop/target'), 500, 3),
  ('Stop-run reclaim of the previous NY low / high, 1:2', 'NQ', 1, F(tag='Stop-run reclaim', stop='col wk', target='2', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Forrest Knight': [
  ('Profile edge + level + signal candle, wick stop, opposite level (1H)', 'NQ', 60, F(stop='col wk', target='col tp', exit='stop/target'), 500, None),
  ('Same, 1:2', 'NQ', 60, F(stop='col wk', target='2', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 60, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Rajan Dhall': [
  ('Auction zone retest, candle stop, 1:2', 'NQ', 5, F(stop='col wk', target='2', exit='stop/target'), 500, 2),
  ('Max fixed 1:2 (50 pts)', 'NQ', 5, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Anthony Crudele': [
  ('Beacon mean reversion: close through 30%, target 50% (daily)', 'NQ', 1440, F(tag='Mean reversion', stop='col wk', target='col tp', exit='stop/target'), 500, None),
  ('Expansion breakout, 2 ATR stop, 5-day hold', 'NQ', 1440, F(tag='Expansion', stop='col wk', target='none', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts), daily', 'NQ', 1440, F(stop='fixed', target='2', exit='stop/target'), None, None)],
'Trader Mayne': [
  ('OTE breaker: limit, stop below the swept low, target the range high (H4 -> M15)', 'NQ', 15, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), 500, None),
  ('Same on gold', 'GC', 15, F(entry='limit lim', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 15, F(entry='market', stop='fixed', target='2', exit='stop/target'), None, None)],
 'Marco Trades': [
  ('Liquidity trap, stop past the sweep, target opposing liquidity (5m)', 'NQ', 5, F(stop='col wk', target='col tp', exit='stop/target'), 500, None),
  ('Liquidity trap, 1:3 (his minimum)', 'NQ', 5, F(stop='col wk', target='3', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 5, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Vincent Desiano': [
  ('Break & retest, retest stop, TP1 = next level (2m)', 'NQ', 2, F(stop='col wk', target='col tp', exit='stop/target'), 500, None),
  ('Break & retest, half at 1:1, break-even runner to 15:55', 'NQ', 2, F(stop='col wk', target='none', exit='half 1'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 2, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Abraham Perez': [
  ('IFVG after a sweep (proxy: no Bookmap), sweep stop, 1:2', 'NQ', 1, F(stop='col wk', target='2', exit='stop/target'), 500, None),
  ('Same, target the next session level', 'NQ', 1, F(stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 1, F(stop='fixed', target='2', exit='stop/target'), None, None)],
 'Trader Yush': [
  ('Failed breakout at VAH / VAL (proxy: no delta / big lots), target the other side of value', 'NQ', 5, F(stop='col wk', target='col tp', exit='stop/target'), 500, 2),
  ('Same, target the middle of value (his T1)', 'NQ', 5, F(stop='col wk', target='col tp2', exit='stop/target'), None, None),
  ('Range days only', 'NQ', 5, F(tag='Range day', stop='col wk', target='col tp', exit='stop/target'), None, None),
  ('Max fixed 1:2 (50 pts)', 'NQ', 5, F(stop='fixed', target='2', exit='stop/target'), None, None)],
}
CLAIMS = {}

# ---------------------------------------------------------------- claims (quoted, with source) and the verdict line
def C(headline, quotes, insight): return dict(headline=headline, quotes=quotes, insight=insight)
CLAIMS = {
 'Fabio Valentini': C('Top 3 Robbins World Cup, "over 500%" in 12 months', [
   ('"top three in the world rankings of the Robins Club ... over 500% return ... in the futures division" (host, 1:40)', 'https://www.tradezella.com/strategies/auction-market-strategy'),
   ('Another episode description says "audited returns as high as 218% in a single competition year" — not the same as 500%', 'https://podscan.fm/podcasts/words-of-rizdom-trading-podcast/episodes/trading-live-with-the-best-scalper-in-the-world-perfect-accuracy'),
   ('Risk "0.25% ... 0.5%" per trade; 1:2.5 minimum, "1 to five is common"; POC target "reverses 70% of the time"', 'https://www.tradezella.com/strategies/auction-market-strategy')],
   'Re-check with his newer rules (IQ Capital episode): NO partials, full exit at the prior day high / low = +0.52 (t 1.9) and +0.72 on 19 trades in 2026; his new "machine gun" 1:1 value-migration model loses every year (−0.29, 23,124 trades). First test: his NY trend model is positive every year 2023–2026 (half at 1:2 + runner: +0.36 avg RR in 2022–25, t 2.1) while random twins lose. But ~38 trades a year at 0.5% risk is about +7% a year, not 500%; 2026 has only 19 trades; it loses on 5m. His real trigger (20–40 lot bubbles) is invisible in candles. Mean reversion loses.'),
 'JJ Simon': C('"Over $1.8M" / $1.93M in prop payouts', [
   ('$550,000 spent on about 2,200 evaluations, about 483 payouts, $1,931,000 total payouts', 'https://sozai.app/transcript/spent-550000-prop-firm-evaluations-lessons/'),
   ('Evals always 1:1.5 (25 pt stop, 38 target); about 20% win rate at 1:4', 'https://sozai.app/transcript/steal-1-minute-strategy-1-8m/index.md')],
   'His own eval rule loses: 4,729 trades, WR 37%, avg RR −0.10, t −5.6, and −0.10 again in 2026. Yet the account machine turns it into money: 20 copied accounts at a $25–100 eval net about +$15k to +$92k over 3 years. That matches his own story — the payouts come from buying thousands of cheap evaluations (his 2,200 evals ≈ 22 payouts per 100), not from a per-trade edge.'),
 'Okala': C('"Over $5 million in payouts"; "70% win rate"', [('Host: "over $5 million in payouts ... 3 million of which was just last year"; "this trader has a 70% win rate"; Okala: "mid to low 70s" (full episode transcript)', 'https://www.chartfanatics.com/strategies'),('"more than $5 million in prop-firm payouts" (business claim, not audited)', 'https://blog.pickmytrade.io/okala-80-20-strategy-pine-script/')],
   'Re-coded from the full episode on his 200-second chart (see Transcript re-check): his full model loses (−0.12 avg RR, 1,458 trades; 2026 −0.16) with a 39% win rate, not 70%+. The H short at an 80 held to 16:00 is still positive (+0.65; 2026 +1.12 on 14 trades) but it disappears at 20 levels and on his own 200 s chart — a lucky slice, not his model.'),
 'Candace Lau': C('"At least 1:2"; 40–50 NQ pts in ~9 minutes (example)', [('"generally structured around at least 1:2 risk-to-reward"', 'https://www.tradezella.com/strategies/nq-liquidity-sweep-reversal-scalping-strategy')],
   'Sweep + IFVG with a limit in the gap: 1,174 trades, WR 35%, avg RR −0.06; 2026 −0.15. London only −0.16. No payouts even across 20 copied accounts.'),
 'Dhesi': C('No stats published', [('Two losses end the day; half at the first target, then break-even and runner', 'https://www.tradezella.com/strategies/liquidity-inversion-model')],
   'Half off + runner: −0.03 (2022–25), −0.13 (2026). The plain 1:2 version was +0.12 but almost all of it in 2023.'),
 'Marci Silfrain': C('"320% return" in the Robbins World Cup; "World\'s #2 futures trader"', [('"STEAL This SIMPLE Trading Strategy from The WORLD\'s #2 Futures Trader - Marci Silfrain" (772K views)', 'https://outlierkit.com/channel/chart-fanatics'), ('320% Robbins World Cup return (summary)', 'https://lilys.ai/hi/notes/grok-ai-20260119/marci-silfrain-futures-world-champion')],
   'Measured move on NQ 15m: +0.12 in 2022–25, −0.05 in 2026; NQ 5m and 1H lose. Random entries passed more grid combos (1) than her rule (0). A contest return is one hot stretch at big risk, not an average.'),
 'TG Capital': C('"90% win rate", "1:20+ RR"', [('"Around 90% when all rules are followed"; setups "a handful of times per year"', 'https://www.chartfanatics.com/strategies/unique-high-rr'), ('Video title: "STEAL This INSANE Simple 90% Win Rate Trading Strategy (1:20+ RR)"', 'https://youtube.com/watch?v=ADnslyKOwFE')],
   'A 90% win rate AND 1:20 would be +17R per trade — nothing like that exists. Coded on NQ 30m (his window 03:00–06:30), 16 setups in 3 years: WR 19% riding the EMA stack, 6% at 1:20. Gold (his main market) has only 2026 data: 2 setups.'),
 'Tori Trades': C('"Approaching nearly $500,000 in profits"', [('"approaching nearly $500,000 in profits" verified via broker statements (summary)', 'https://youtubesummary.com/summary/VTEQ2fhGLqE'), ('"turned a $5,000 account into over half a million" (own video)', 'https://videohighlight.com/v/PnIkSLm2yRk')],
   'Trendline bounce on NQ 4H with her line-trailing exit: −0.08 (2022–25), −0.13 (2026); NQ 1H −0.15. Gold 4H 2026 +0.31 on 37 trades. Her markets are mostly platinum / crude / copper, which are not in this data.'),
 'Jade Cap': C('"Roughly $4.5 million" payouts; "world record" largest prop payout', [('"roughly $4.5 million in total" payouts; "the world record for the largest prop firm payouts"', 'https://chatwithtraders.com/episode/304-kyle-ng')],
   'Raid + FVG (09:30–11:30): 252 trades, WR 49%, avg RR −0.03 (2022–25), +0.18 on 31 trades in 2026. No payouts on 20 copied accounts in 2022–25.'),
 'Trader Kane': C('Record $2.3M prop payout; "$130,000 to over $1.4 million in about a month"', [('Host intro: "the record for the largest payout in prop firm history ... over $2.3 million"; "in December he took $130,000 to over $1.4 million in roughly about a month" (0:17)', 'https://www.youtube.com/watch?v=HNuRp9Z1bMs'),('"$1,926,240" across about 40 payouts on 20 copy-traded accounts; "bought probably 500 prop accounts over my lifetime"; model "loses just as much as it wins"', 'https://blog.pickmytrade.trade/trader-kane-strategy-the-lab-model-nq-trading-system-explained/')],
   'Re-coded from the full episode (see Transcript re-check): with SMT, 15 trades in 2026 at +0.74 on 5m and 6 losers on 3m — too few to judge. Without SMT, 3 years of NQ: −0.09 avg RR on 334 trades. His own live week showed a 50% win rate. The money story is accounts: 20 copy-traded Apex accounts, ~500 bought.'),
 'Tanja Trades': C('No stats; CPI example "around 100 points"', [('CPI short "around 100 points" in minutes (example only)', 'https://www.chartfanatics.com/strategies/amd-model')],
   'AMD (06:00–08:30 range, sweep, displacement FVG): 218 trades, WR 50%, avg RR −0.03; 2026 −0.10. Her news-day filter could only be approximated (NFP Fridays: 6 trades).'),
 'Andrea Cimitan': C('"Six-figure trading profits"', [('"with seven years of experience and six-figure trading profits"', 'https://www.chartacademy.com/instructors/andrea-cimitan')],
   'Failed auction at VAL / VAH back to POC: −0.06 (2022–25), −0.36 (2026). With the absorption proxy: −0.06. His opening-range breakout with body acceptance: +0.07 then −0.01.'),
 'Carmine Rosato': C('"7-figure trader", "$203K month in May 2025"', [('"breaking down the techniques behind his $203K month in May 2025"', 'https://www.youtube.com/watch?v=UhkRRqO1gQM')],
   'LVN pullback: only 11 setups (+0.53) — too few. The prior-day-low stop-run reclaim loses (−0.22, t −2.3). His real confirmation is footprint / heatmap, which candles can\'t show.'),
 'Forrest Knight': C('"7-figure futures trader"', [('"Forrest is a 7-figure trader"', 'https://tradingwithforrest.com')],
   'Profile edge + ON / PD level + 1H signal candle: 36 setups in 3 years, −0.10 to the opposite level, +0.15 at 1:2. Too rare to prove anything.'),
 'Rajan Dhall': C('"Running a multi-million fund"', [('"a full-time trader running a multi-million fund"', 'https://www.desiretotrade.com/504')],
   'Auction-zone retest in the daily trend: 36 setups, −0.05 at his 2:1.'),
 'Anthony Crudele': C('25-year veteran, CME member (no P&L claimed)', [('25-year trading veteran, CME member, former pit trader (episode description)', 'https://www.youtube.com/watch?v=EZ_L7zovyrw')],
   'Daily Bollinger "Beacon" mean reversion: 45 trades, −0.23 (2022–25), −0.03 (2026). Expansion breakouts: 7 trades.'),
 'Trader Mayne': C('"$10M+ in profits"; wins "about a third of the time" at 2:1', [('"$10M+ in Profits"; wins "about a third of the time" at "2-to-1 reward-to-risk"', 'https://www.chartacademy.com/instructors/trader-mayne')],
   'His own stats (33% at 2:1) are breakeven before costs. Coded on NQ H4 → M15: 50 setups, WR 14%, avg RR −0.46. Built for crypto swing trading, which isn\'t in this data.'),
 'Marco Trades': C('"$500K+" (host); ">$100,000 in payouts last year" (himself)', [('"Last year I did over $100,000 in payouts whilst doing this."', 'https://2outube.com/watch?v=T_djSNBmV00'), ('Video title: "STEAL This EASY Liquidity TRAP Trading Strategy - $500K+"', 'https://youtube.com/watch?v=DAnXM7C16h0')],
   'Liquidity trap at the NY open: 667 trades, WR 51%, avg RR −0.19 (t −4.9) to opposing liquidity; 1:3 −0.09 then +0.02. Zero payouts on 20 copied accounts. Note his own $100k vs the host\'s $500k.'),
 'Vincent Desiano': C('"$1M+ verified P&L" (mostly options)', [('"over $1 million in verified lifetime profit and loss"; unprofitable his first five years', 'https://www.chartacademy.com/instructors/vincent-desiano')],
   'Break & retest on NQ 2m (10:00–12:00): 274 trades, −0.09 to TP1; half + runner −0.09 (2026 +0.44 on 19). His P&L is mostly options, so not comparable to NQ.'),
 'Abraham Perez': C('"$600K+ in prop firm payouts"', [('"$600k+ In Payouts"', 'https://www.chartacademy.com/instructors/abraham-perez')],
   'Proxy only (his Bookmap / tape confirmation can\'t be seen): 23 IFVG setups, −0.25 at 1:2.'),
 'Trader Yush': C('"$2+ million in payouts"; "$300,000 in January" on ~$5,000 of evals', [('"over $2 million in prop firm payouts"; "$300,000 in January alone with only around $5,000 in eval spend"', 'https://podcasts.apple.com/si/podcast/the-ict-trader-who-made-%242-million-after-switching-to/id1780241706?i=1000759854537&l=sl')],
   'Proxy only (big-lot prints and delta can\'t be seen): failed breakout at VAH / VAL with a level nearby: 105 trades, −0.14. Still, 20 copied cheap accounts would have netted ~+$11–17k — the account machine again.'),
}

INDUSTRY = [
 ('Topstep 2025: 16.8% of Combines passed', 'And only <b>33.3% of funded traders ever got a payout</b>. That is about 6 attempts per pass and ~18 attempts per account that ever pays.', 'https://www.topstep.com/our-program'),
 ('Only 4–7% of buyers ever get paid', 'FPFX: 7% of 300,000 accounts reached a payout. Goat Funded Trader: 22,279 paid of 594,997 buyers (3.7%). The Funded Trader: about 1–2%.', 'https://www.financemagnates.com/forex/only-1-in-20-traders-pass-prop-firm-challenges-reports-the-funded-trader/'),
 ('Average payout ≈ $1,200–$2,000', 'FTMO ≈ $2,030 per payout (Sept 2026). Tradeify ≈ $1,536, MyFundedFutures ≈ $1,215 from public payment records.', 'https://www.financemagnates.com/forex/ftmo-adds-200-million-to-lifetime-payouts-in-one-year-as-monthly-rewards-near-15-million/'),
 ('One person can run 40+ funded accounts', 'Apex allows 20 accounts and trade copiers; Topstep 5; Lucid 5 funded; Tradeify 5; Take Profit Trader 5. Copy one trade to all of them.', 'https://blog.pickmytrade.io/apex-copy-trading-rules-account-failed/'),
 ('Evaluations cost $20–$60 with codes', 'Apex 50k at $24.90 with a 90% code (+$79 activation). Chart Fanatics promotes Apex with code "CF" (80% off).', 'https://www.eltraderfinanciado.com/en/news/apex-trader-funding/apex-trader-funding-price-cuts-zero-activation-fee-2026'),
 ('JJ Simon\'s own math', '$550,000 on ~2,200 evaluations → ~483 payouts → $1.93M. About 22 payouts per 100 evaluations. He advises against copy trading because the accounts all win or lose together.', 'https://sozai.app/transcript/spent-550000-prop-firm-evaluations-lessons/'),
]

UNTESTED = [
 ('JLaw', 'Multiple Edge Trading System (stocks)', 'Stocks: no stock data in this library.'),
 ('Clement Ang', 'Price Cycle Continuation & Failed Base (stocks)', 'Stocks: no stock data.'),
 ('Marios Stamatoudis', 'Parabolic Short (stocks)', 'Stocks: no stock data.'),
 ('Connor Bates', 'Super Stock Momentum (stocks)', 'Stocks: no stock data.'),
 ('Naoufel Taief', '"$1M+ profits" algorithmic framework', 'A system-building framework (StrategyQuant), not one strategy: nothing faithful to test.'),
 ('Dylan O\'Neil', 'VIX futures strategy', 'No VIX futures data.'),
 ('Fredy Sarmiento', '"75% win rate" gamma-wall reversal on NQ/ES', 'Every entry level comes from options data (gamma walls, open interest). No sample size given for the 75%.'),
 ('NBB Trader (Omor)', '"$1M+ in prop payouts", PO3 + OTE + ADR', 'His playbook is tagged Forex, and the X post credits the $1.1M to his community, not to him. Rules are codeable — a good next test. Note: the playbook\'s R numbers are off by one level (a 0.62 entry is 1.63R, not 2.38R).'),
 ('Matteo Conti', '"€15B bank trader", opening range / VWAP / overnight hold', 'No performance claim, only an illustrative 70%. Simple ORB ideas like this are already covered by the MMM opening-range tests.'),
]

INSIGHTS = [
 ('How can they be paid millions with no edge in the rules?', 'Four things, all said in their own episodes: (1) <b>many accounts</b> — Apex allows 20, copied with one click; Kane bought ~500, JJ Simon ~2,200 evaluations; (2) <b>tiny, strict losses</b> — Okala\'s 10 pt stop, Kane\'s fast break-even, Fabio\'s daily max — which keep the cost per trade close to zero; (3) <b>size up when hot</b> — Okala "step on the gas", Kane trails news days, Fabio adds 3–4 positions on trend days; (4) <b>discretion and data the video does not show</b> — Kane: "the discretion is my edge"; Fabio uses order-book (MBO) data and says his model is not a standalone strategy.'),
 ('The prop deal itself pays a disciplined coin flip', 'Simulation: 1,000 make-believe traders with NO edge (1:2 trades, avg RR −0.05 after costs), each copying 1 trade a day onto 20 Apex-like accounts for 2 years ($25 eval + $79 activation, $2,000 payout cap, 6 payouts per account, rebuy when blown). Median payouts $96,000; the luckiest 1% got $392,000; 80% ended net positive. Why: a loss costs at most ~$104 per account, a funded account can pay up to $12,000. The edge is in the account rules, not the chart.'),
 ('Discipline is the real line, not the setup', 'The same simulation at avg RR −0.15 per trade (sloppy stops, overtrading): median net −$2,310 and only 48% positive. At −0.30 (typical losing retail): 90% lose. That is why only 4–7% of prop buyers ever get paid while these guests get paid a lot: they keep every loss small and never break the account rules. Real firms also add consistency rules and payout reviews, so real numbers are lower than this simplified model.'),
 ('A 10x month can be pure variance', 'Kane\'s host says he took $130,000 to $1.4 million in about a month. With NO edge and 15% of the balance risked per trade at 1:2 (2 trades a day), about 1 trader in 200 does that in a month — and 62% lose half. With thousands of traders trying, a few always will; those are the ones invited on the show.'),
 ('"Verified" means the payouts are real — not that the rules make money', 'Chart Fanatics says it only features "traders with verified results" but does not publish how results are checked. A payout is real money, but it is gross across many accounts, it is not net of evaluations bought, and it does not test the setup they teach. The same site carries an Apex 90%-off code "CF" through an affiliate link.'),
 ('Payout totals measure accounts, not edge', 'A payout certificate adds up every payout across every account and firm. It never subtracts the failed evaluations, resets and activation fees. JJ Simon\'s own numbers: $550k spent to collect $1.93M. Kane: ~500 accounts bought, 20 copy-traded at once.'),
 ('A losing rule can still pay out on many cheap accounts', 'Copy JJ Simon\'s losing eval rule (avg RR −0.10) onto 20 accounts and rebuy every one that blows up: in 2022–25 that is ~$158–160k of payouts and a best month of $80–93k to screenshot — net +$15k at a $100 eval, +$92k at Apex\'s $25 + $79, −$274k at $300. The eval price, not the strategy, decides the result.'),
 ('Random trades post payouts too', 'With 20 copied accounts, random entries (no edge at all) produced up to $87,000 of payouts in our simulation (Marci\'s random twins), and $50–65k for Tori, Desiano and Fabio. Some people trading coin flips on enough accounts will always have a great month to show.'),
 ('Copy trading multiplies the screenshot, not the edge', 'All copied accounts win and lose together. 20 accounts turn a $4k month into an $80k month — and a bad week into 20 blown accounts. That is why the totals look huge and the per-account math looks ordinary.'),
 ('The firm pays winners with everyone\'s fees', 'Only 4–7% of buyers ever get paid (FPFX, Goat Funded Trader). The payouts on the videos are funded by the other 93–96%. A sponsor discount code (e.g. Apex "CF") makes the lottery cheaper for the guest and the audience.'),
 ('Contest returns are one hot stretch', 'Robbins World Cup results (Fabio 500%, Marci 320%) come from big size over one year. Fabio\'s best rule here earns ~+15R a year; at his 0.5% risk that is ~7%. 500% would need ~360R a year.'),
 ('Survivorship: you only meet the winners', 'Thousands of traders run these same setups on prop accounts. The ones invited on a channel are the ones whose accounts happened to pay. The rules they share should therefore be tested before being trusted — and here none passed.'),
 ('What they really sell', 'The common thread is not a pattern: it is risk control (small fixed risk, a daily loss stop, few trades) plus account volume. Those risk rules are worth copying. The entries, coded from their own pages, show no edge in this data.'),
]

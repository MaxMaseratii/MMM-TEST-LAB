s = open('MMM_FVA_Break_4.0.pine').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
def span(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

rep('indicator("MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.0", "FVA Break 4.0",', 'indicator("MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.1", "FVA Break 4.1",')
span('// MMM FAIR VALUE AREA BREAK 4.0', '//  The old entries', '''// MMM FAIR VALUE AREA BREAK 4.1
//  FVA        = the body range of the neutral candles (NBC) before a body close (BC).
//  FLIP ZONE  = the body of the last opposite BC before a flip:
//               PEL+ (bull) after a bearish run, PES+ (bear) after a bullish run.
//  STRATEGIES = the only setups that passed the honest test (1h chart):
//   FVA.M1 · Flip Zone Fail · LONG       a 1h close ABOVE a PES+ zone -> buy · daily ATR stop · 1:4
//   FVA.M2 · Asia Flip Zone Fail · BOTH  in Asia (18:00-02:00 NY) a 1h close through a flip zone
//                                        -> trade the break · zone stop · 1:1.5 · WR 56%
''')
rep('const color T_WARN = #FFB300\n', 'const color T_WARN = #FFB300\nconst color T_SEC2 = #262626\n')
span('grp_st   = "2. Strategy · FVA.M1 (tested)"', 'grp_tr    = "3. Trades on Chart"', '''grp_st   = "2. Strategies (tested · 1h)"
sM1      = input.bool(true, "FVA.M1 · Flip Zone Fail · LONG · 1:4", group=grp_st, tooltip="RULE\\nA bearish flip zone (PES+ box) = the body of the last bullish BC before sellers flipped the trend.\\nWhen a 1h candle CLOSES ABOVE the top of that box, the sellers failed → BUY at that close.\\nStop = yesterday's daily ATR(14) × 0.15 (≈ 46 pts in 2023–25, ≈ 82 pts in 2026).\\nTarget = 1:4.\\nEarly exit = at the close of the 2nd neutral candle (NBC) in a row when both close in their upper half (the push stalls).\\nTime limit = 100 candles. One trade per candle.\\n\\nTESTED (1h · market at the close · stop first on 1m data · 1 pt cost)\\nNQ 2023–25: 402 trades · WR 36% · PF 1.47 · avg RR +0.30 · t-score 3.1 (2023 +0.25 · 2024 +0.40 · 2025 +0.23)\\nMNQ 2026: 51 trades · WR 45% · PF 2.22 · avg RR +0.63 · t-score 2.2\\nBoth: 453 trades · WR 37% · PF 1.54 · avg RR +0.33 · t-score 3.7\\nRandom 1h longs with the same stop / target / exit: about 0.")
sM2      = input.bool(true, "FVA.M2 · Asia Flip Zone Fail · BOTH · 1:1.5 · WR 56%", group=grp_st, tooltip="RULE (Asia only: the 1h candle that opens 18:00 – 01:00 New York)\\nA 1h candle CLOSES THROUGH a flip zone:\\n• close ABOVE a PES+ zone = sellers failed → BUY at that close\\n• close BELOW a PEL+ zone = buyers failed → SELL at that close\\nStop = the far side of the zone ± 4 ticks (Zone stop), or a fixed stop.\\nTarget = 1:1.5. Time limit = 100 candles. One trade per candle per side.\\n\\nTESTED (1h · market at the close · stop first on 1m data · 1 pt cost)\\nZone stop, no early exit:\\nNQ 2023–25: 119 trades · WR 55% · PF 1.73 · avg RR +0.34 · t 3.0 (2023 +0.18 · 2024 +0.23 · 2025 +0.50)\\nMNQ 2026: 34 trades · WR 59% · PF 2.08 · avg RR +0.45 · t 2.1\\nBoth: 153 trades · WR 56% · PF 1.81 · avg RR +0.37 · t 3.6\\nFixed 50 pt stop + stall exit (2 NBC both leaning with the trade):\\nBoth: 153 trades · WR 56% · PF 1.86 · avg RR +0.34 · t 3.6 (2026: WR 65%, +0.56)\\nLongs and shorts both made money in both periods. Outside Asia the short side does NOT work.")
m2Stop   = input.string("Zone (tested best)", "M2 Stop", options=["Zone (tested best)", "Fixed 50 NQ / 20 ES"], group=grp_st, tooltip="Zone = the far side of the broken zone ± 4 ticks (≈ 46 pts 2023–25, ≈ 99 pts 2026), no early exit.\\nFixed = 50 pts NQ / MNQ (20 pts ES / MES, untested) with the 2-NBC stall exit, as tested.")
m1AnyTF  = input.bool(false, "Run on Any Timeframe (untested)", group=grp_st, tooltip="OFF = the strategies only trade on a 1h chart (how they were tested). The zones still draw on every chart.")
m1Lines  = input.bool(true, "Trigger Lines on Flip Zones", group=grp_st, tooltip="PES+ zones: a line at the top = a 1h CLOSE above it is the buy (M1 always, M2 in Asia).\\nPEL+ zones: a line at the bottom = a 1h CLOSE below it in Asia is the M2 sell.")

''')
rep('fzBear    = input.bool(true, "PES+ (Bear Flip Zones · M1 trigger)"', 'fzBear    = input.bool(true, "PES+ (Bear Flip Zones · M1 / M2 buy trigger)"')
rep('fzBull    = input.bool(true, "PEL+ (Bull Flip Zones · context)"', 'fzBull    = input.bool(true, "PEL+ (Bull Flip Zones · M2 sell trigger)"')
rep('tooltip="Shows FVA.M1 only when it is ARMED (a live PES+ zone above price), IN A TRADE, or TRADED TODAY.")', 'tooltip="Shows a strategy only when it is ARMED (a live trigger, M2 only in Asia), IN A TRADE, or TRADED TODAY.")')
rep('tooltip="The full numbers of FVA.M1: tested (2023–26) and this chart.")', 'tooltip="The full numbers of FVA.M1 and FVA.M2: tested (2023–26) and this chart.")')
rep('bool   m1Run = sM1 and (tf1h or m1AnyTF)\n', '''bool   tfOk  = tf1h or m1AnyTF
bool   m1Run = sM1 and tfOk
bool   m2Run = sM2 and tfOk
bool   m2Fix = m2Stop != "Zone (tested best)"
float  FIXP  = isES ? 20.0 : 50.0
int    nyMin = hour(time, "America/New_York") * 60 + minute(time, "America/New_York")
bool   inAsia = nyMin >= 1080 or nyMin < 120
''')
span('type Trd\n', 'var array<FS>  bulls', '''type Trd
    int   k
    int   side
    int   xm
    int   eBar
    int   eT
    float e
    float stp
    float tp
    float d
    int   xBar = na
    int   xT = na
    float xPx = na
    float R = na
    int   res = 0
    int   xDay = na

// stats per strategy (this chart)
type St
    int   n = 0
    int   w = 0
    float sR = 0.0
    float sR2 = 0.0
    float gW = 0.0
    float gL = 0.0
    float wUsd = 0.0
    float lUsd = 0.0
    float cum = 0.0
    float pk = 0.0
    float dd = 0.0
    int   curW = 0
    int   curL = 0
    int   maxW = 0
    int   maxL = 0
    int   t0 = na

''')
span('// stats (this chart)\nvar int   stN', '// ═══════════════════════════════════════════════════════════════════════\n// TRADE ENGINE', '''var array<St> ST = array.from(St.new(), St.new())
var array<string> SN = array.from("FVA.M1", "FVA.M2")
bool  sigL     = false
float sigLStop = na
bool  sigS     = false
float sigSStop = na

f_book(St s, float R, float usd) =>
    s.n   += 1
    s.sR  += R
    s.sR2 += R * R
    if R > 0
        s.w    += 1
        s.gW   += R
        s.wUsd += usd
        s.curW += 1
        s.curL := 0
    else
        s.gL   -= R
        s.lUsd += usd
        s.curL += 1
        s.curW := 0
    s.maxW := math.max(s.maxW, s.curW)
    s.maxL := math.max(s.maxL, s.curL)
    s.cum  += usd
    s.pk   := math.max(s.pk, s.cum)
    s.dd   := math.max(s.dd, s.pk - s.cum)
    true

''')
span('// TRADE ENGINE (FVA.M1)', '// ═══════════════════════════════════════════════════════════════════════\n// STRUCTURE ENGINE', open('engine41.txt').read())
rep('''                if not z.isBull and c > z.top
                    m1Signal := true
''', '''                if not z.isBull and c > z.top and not sigL
                    sigL     := true
                    sigLStop := z.bot - 4 * syminfo.mintick
                if z.isBull and c < z.bot and not sigS
                    sigS     := true
                    sigSStop := z.top + 4 * syminfo.mintick
''')
span('    // FVA.M1 entry (one trade per candle)', '// ═══════════════════════════════════════════════════════════════════════\n// RENDER', open('entries41.txt').read())
rep('''            bool  arm = not z.isBull and (not z.isSig or z.sigState == -1)
            string nm = z.isBull ? "PEL+" : "PES+" + (arm and sM1 ? " · M1" : "")
''', '''            bool  armL = not z.isBull and (not z.isSig or z.sigState == -1)
            bool  armS = z.isBull and (not z.isSig or z.sigState == 1)
            string tg  = armL ? ((sM1 ? " · M1" : "") + (sM2 ? (sM1 ? "·M2" : " · M2") : "")) : armS and sM2 ? " · M2" : ""
            string nm  = (z.isBull ? "PEL+" : "PES+") + tg
''')
rep('''            if not z.isBull and arm and sM1 and m1Lines
                f_lvl(z.tBox, futT, z.top, zc, 1, line.style_dashed, "M1 ▲ close > " + str.tostring(z.top, format.mintick), f_lsz(lvl_size), "FVA.M1 trigger: a 1h candle CLOSING above this line = BUY at that close.\\nStop = yesterday's daily ATR × 0.15 · Target 1:4 · stall exit after 2 NBC.")
''', '''            if armL and (sM1 or sM2) and m1Lines
                f_lvl(z.tBox, futT, z.top, zc, 1, line.style_dashed, (sM1 ? "M1" : "") + (sM1 and sM2 ? "·" : "") + (sM2 ? "M2" : "") + " ▲ close > " + str.tostring(z.top, format.mintick), f_lsz(lvl_size), "BUY trigger: a 1h candle CLOSING above this line.\\nFVA.M1 (any session): stop daily ATR × 0.15 · 1:4 · stall exit.\\nFVA.M2 (Asia 18:00–02:00 only): stop = zone bottom − 4 ticks (or fixed) · 1:1.5.")
            if armS and sM2 and m1Lines
                f_lvl(z.tBox, futT, z.bot, zc, 1, line.style_dashed, "M2 ▼ close < " + str.tostring(z.bot, format.mintick) + " (Asia)", f_lsz(lvl_size), "SELL trigger (FVA.M2, Asia 18:00–02:00 only): a 1h candle CLOSING below this line.\\nStop = zone top + 4 ticks (or fixed) · Target 1:1.5.")
''')
rep('''                    float live = open_ ? (close - t.e) / t.d : t.R
                    string tx  = "M1 ▲ " + (open_ ? "live " : "") + f_sgn(live, "0.0") + " avg RR"
''', '''                    float live = open_ ? t.side * (close - t.e) / t.d : t.R
                    string tx  = (t.k == 0 ? "M1" : "M2") + (t.side == 1 ? " ▲ " : " ▼ ") + (open_ ? "live " : "") + f_sgn(live, "0.0") + " avg RR"
''')
rep('''                    string tip = "FVA.M1 · Flip Zone Fail · LONG\\nEntry " + str.tostring(t.e, format.mintick) + " · Stop " + str.tostring(t.stp, format.mintick) + " (−" + str.tostring(t.d, "#.##") + " pts) · Target " + str.tostring(t.tp, format.mintick) + " (1:4)" + (open_ ? "\\nOPEN" : "\\nExit " + str.tostring(t.xPx, format.mintick) + " · " + f_resTxt(t.res) + " · " + f_usd((t.xPx - t.e - COST) * PV * contracts))
''', '''                    string tip = (t.k == 0 ? "FVA.M1 · Flip Zone Fail · LONG" : "FVA.M2 · Asia Flip Zone Fail · " + (t.side == 1 ? "LONG" : "SHORT")) + "\\nEntry " + str.tostring(t.e, format.mintick) + " · Stop " + str.tostring(t.stp, format.mintick) + " (−" + str.tostring(t.d, "#.##") + " pts) · Target " + str.tostring(t.tp, format.mintick) + (t.k == 0 ? " (1:4)" : " (1:1.5)") + (open_ ? "\\nOPEN" : "\\nExit " + str.tostring(t.xPx, format.mintick) + " · " + f_resTxt(t.res) + " · " + f_usd((t.side * (t.xPx - t.e) - COST) * PV * contracts))
''')
rep('''dLabels.push(label.new(t.eT, t.stp, tx, xloc=xloc.bar_time, style=label.style_label_up,''', '''dLabels.push(label.new(t.eT, t.stp, tx, xloc=xloc.bar_time, style=t.side == 1 ? label.style_label_up : label.style_label_down,''')
i = s.index('// TABLES — LIVE')
s = s[:i] + open('tables41.txt').read()
open('MMM_FVA_Break_4.1.pine', 'w').write(s)
print('ok', len(s.splitlines()))

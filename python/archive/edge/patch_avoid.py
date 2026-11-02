"""EDGE PRO: two 'avoid' rules from the XB filter test (Oct 30 2026), NQ / MNQ only (where they were tested).
X.M4: skip when the 15m close is already outside the live DAILY XB on the break side (long above its high / short below its low).
C.M1: skip when the 15m close is inside a live 1h, 4h or daily FVA of its own side (BuFVA for longs, BeFVA for shorts).
The HTF candles are built from the 15m candles inside the 15m core (same as the 1h trend and the 4H filter)."""
src = open('MMM_EDGE_PRO.pine').read()
def rep(a, b):
    global src
    assert src.count(a) == 1, (src.count(a), a[:80]); src = src.replace(a, b)

# inputs
rep('mkChk = input.bool(true, "Market Check',
    'avX4  = input.bool(true, "X.M4 · skip when already outside the daily XB", group=g1, tooltip="NQ / MNQ (Oct 30 2026 test): no X.M4 trade when the 15m close is already OUTSIDE the live daily Xpander Block on the break side (long above its high, short below its low). Those trades chased a move that had left: avg RR −0.22 (2022–25) and −0.50 (2026) with the tested exit, and the ½-out trades made +0.00 / −0.09.\\nSkipping them: ½ out avg RR +0.15 → +0.18 (2022–25) and +0.26 → +0.33 (2026), WR 70% → 71% and 77% → 81%.\\nThe daily XB is built from the 15m candles (session 18:00 → 17:00), opposite-side engine (MMM PRO x 4.0).")\n'
    'avC1  = input.bool(true, "C.M1 · skip inside a live 1h / 4h / daily FVA", group=g1, tooltip="NQ / MNQ (Oct 30 2026 test): no C.M1 trade when the 15m close is INSIDE a live 1h, 4h or daily FVA of its own side (BuFVA for longs, BeFVA for shorts). Those trades lost on all three timeframes (50 pt 1:2: −0.07 to −0.32 avg RR).\\nSkipping them: avg RR +0.13 → +0.17 (2022–25) and +0.26 → +0.35 (2026), PF 1.26 → 1.34, t 4.6 → 5.0.\\nFVA (MMM PRO x 4.0): after a bearish XB break = first NBC body bottom → XB high; after a bullish break = XB low → first NBC body top. It dies on a close through it. Built from the 15m candles.")\n'
    'mkChk = input.bool(true, "Market Check')

# HTF XB engine (before f_core)
rep('f_core() =>\n    var float dOpen = na',
'''// ─── HTF Xpander Block (opposite-side engine, MMM PRO x 4.0) built from the 15m candles · its live FVAs ───
// cls = this 15m candle closes the HTF candle. Returns [XB live, XB high, XB low, FVA sides, FVA tops, FVA bottoms].
f_htfXB(bool cls) =>
    var float cO   = na
    var float cH   = na
    var float cL   = na
    var bool  newC = true
    var float pH   = na
    var float pL   = na
    var int   last = 0
    var bool  wait = false
    var bool  live = false
    var float exH  = na
    var float exL  = na
    var float xH   = na
    var float xL   = na
    var float fO   = na
    var float fC   = na
    var array<int>   fS = array.new<int>()
    var array<float> fT = array.new<float>()
    var array<float> fB = array.new<float>()
    if newC or na(cO)
        cO := open
        cH := high
        cL := low
    else
        cH := math.max(cH, high)
        cL := math.min(cL, low)
    newC := cls
    if cls
        float c = close
        if not na(pH)
            bool bu = c > pH
            bool be = c < pL
            bool bc = bu or be
            int  dr = bu ? 1 : -1
            bool xo = bc and (last == 0 or dr != last)
            if fS.size() > 0
                for i = fS.size() - 1 to 0
                    if (fS.get(i) == 1 and c < fB.get(i)) or (fS.get(i) == -1 and c > fT.get(i))
                        fS.remove(i)
                        fT.remove(i)
                        fB.remove(i)
            if live
                if c > xH or c < xL
                    int   bd  = c > xH ? 1 : -1
                    float top = bd == -1 ? xH : math.max(fO, fC)
                    float bot = bd == -1 ? math.min(fO, fC) : xL
                    if top > bot
                        fS.push(bd)
                        fT.push(top)
                        fB.push(bot)
                        if fS.size() > 12
                            fS.shift()
                            fT.shift()
                            fB.shift()
                    live := false
                    wait := xo
                    if xo
                        exH := cH
                        exL := cL
                else
                    xH := math.max(xH, cH)
                    xL := math.min(xL, cL)
            else if wait
                if bc
                    exH := cH
                    exL := cL
                else
                    live := true
                    wait := false
                    xH := math.max(exH, cH)
                    xL := math.min(exL, cL)
                    fO := cO
                    fC := c
            else if xo
                wait := true
                exH := cH
                exL := cL
            if bc
                last := dr
        pH := cH
        pL := cL
    [live, xH, xL, fS, fT, fB]

// is price p inside a live FVA of side s
f_inFva(array<int> fS, array<float> fT, array<float> fB, int s, float p) =>
    bool r = false
    if fS.size() > 0
        for i = 0 to fS.size() - 1
            if fS.get(i) == s and p >= fB.get(i) and p <= fT.get(i)
                r := true
    r

f_core() =>
    var float dOpen = na''')

# HTF states inside f_core (every 15m candle, right after the 1h candle block)
rep('''    bool h1Close = mnt == 45
''', '''    bool h1Close = mnt == 45
    // HTF XB (1h · 4h 18:00 anchor · daily 18:00 → 17:00) closed on this 15m candle
    int  mEnd = (md + 15) % 1440
    bool c4h  = mEnd == 1320 or mEnd == 120 or mEnd == 360 or mEnd == 600 or mEnd == 840 or mEnd == 1020
    [x1L, x1H, x1Lo, f1S, f1T, f1B] = f_htfXB(h1Close)
    [x4L, x4H, x4Lo, f4S, f4T, f4B] = f_htfXB(c4h)
    [xDL, xDH, xDLo, fDS, fDT, fDB] = f_htfXB(mEnd == 1020)
''')

# X.M4 skip
rep('        if on1 and okX and zEv == 2 and zNum >= 2 and (not fltOn or dDir == zDir) and (zDir == 1 ? mpL : mpS)',
    '        bool x4Out = avX4 and NEWR and xDL and (zDir == 1 ? close > xDH : close < xDLo)\n'
    '        if on1 and okX and zEv == 2 and zNum >= 2 and (not fltOn or dDir == zDir) and (zDir == 1 ? mpL : mpS) and not x4Out')
# C.M1 skip
rep('''        if on8 and ((gL and afL) or (gS and afS))
            int s8 = gL and afL ? 1 : -1
            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 7, s8, close, close - s8 * (FX50 ? FIXPT : atr), true, 6.0, 0, na, 0.0)''',
'''        if on8 and ((gL and afL) or (gS and afS))
            int s8 = gL and afL ? 1 : -1
            bool c1In = avC1 and NEWR and (f_inFva(f1S, f1T, f1B, s8, close) or f_inFva(f4S, f4T, f4B, s8, close) or f_inFva(fDS, fDT, fDB, s8, close))
            if not c1In
                f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 7, s8, close, close - s8 * (FX50 ? FIXPT : atr), true, 6.0, 0, na, 0.0)''')

# tooltips
rep("Tested (no gate, skip 00–02) · 2022–25 → 2026 · Blended: WR 70% → 77% · 72% · avg RR +0.15 → +0.26 · +0.18 · PF 1.56 → 2.25 · 1.71 · t 3.9 / 4.0 / 5.4 · max 4 losses / 15 wins in a row.\\nBest time: 18:00–20:00 and Sunday open.",
    "NQ / MNQ: skip it when the close is already outside the live daily XB on the break side (switch below).\\nTested (no gate, skip 00–02, with the skip) · 2022–25 → 2026 · Blended: WR 71% → 81% · 73% · avg RR +0.18 → +0.33 · +0.22 · PF 1.70 → 2.86 · 1.91 · t 4.3 / 4.5 / 5.9 · max 4 losses / 14 wins in a row · 642 trades.\\nWithout the skip: WR 72% · avg RR +0.15 → +0.26 · +0.18 · PF 1.71.\\nBest time: 18:00–20:00 and Sunday open.")
rep("Asia + NY AM only. No MMPD (tested without).\\nFull: WR 33% · avg RR +0.16 · PF 1.26 · t-score 4.6 · max 17 losses / 8 wins in a row · 3,012 trades.",
    "Asia + NY AM only. No MMPD (tested without).\\nNQ / MNQ: skip it when the close is inside a live 1h, 4h or daily FVA of its own side (switch below).\\nFull, with the skip: WR 34% · avg RR +0.17 → +0.35 · +0.21 · PF 1.34 · t-score 3.6 / 4.0 / 5.0 · max 16 losses / 8 wins in a row · 2,247 trades.\\nWithout the skip: WR 33% · avg RR +0.13 → +0.26 · +0.16 · PF 1.26 · 3,012 trades.")

# tested numbers (NQ blended) · worst run in R
rep('0 => "X.M4|½ out|756,72,0.18,1.71,5.4,4,15,19972,10176,57|', '0 => "X.M4|½ out|642,73,0.22,1.91,5.9,4,14,17693,7416,56|')
rep('8 => "C.M1|1:6|3012,33,0.16,1.26,4.6,17,8,83339,65239,35|', '8 => "C.M1|1:6|2247,34,0.21,1.34,5.0,16,8,66444,47711,35|')
rep('        "X.M4" => 16.4\n', '        "X.M4" => 9.9\n')
rep('        "C.M1" => 66.2\n', '        "C.M1" => 56.3\n')
# header
rep("//   The new rules run on NQ / MNQ. On ES, gold and crude they did NOT hold, so there the old rules stay.",
    "//   The new rules run on NQ / MNQ. On ES, gold and crude they did NOT hold, so there the old rules stay.\n"
    "//   · AVOID (XB filter test, NQ / MNQ): X.M4 skips a close already outside the daily XB on the break side ·\n"
    "//     C.M1 skips a close inside a live 1h / 4h / daily FVA of its own side. Both switches are in ④ Edges.")
open('MMM_EDGE_PRO.pine', 'w').write(src)
print('ok', len(src))

TYPES = r'''// TYPES & STATE
// ═══════════════════════════════════════════════════════════════
// A break, married to the PO4 swing that made it.
type Cause
    string kind
    float  price
    int    t1
    int    t2
    bool   isBull
    bool   pass
    bool   against
    int    score
    bool   ax
    string tip

type Swing
    float        price
    int          t
    int          bIdx
    bool         isHigh
    int          tier
    bool         official
    int          seq
    bool         swept
    float        oH
    float        oL
    int          oT
    array<Cause> causes
    bool         conf
    int          cIdx

type GapBox
    box   b
    line  l
    label lbl
    float top
    float bot
    bool  isBull
    bool  isLine
    bool  isTouched
    bool  stoppedExtending
    color origBg
    color origBorder
    color origLine
    int   creationBar
    int   t

type AxData
    label lbl
    label tri
    float trigger
    bool  isBull
    int   t

var Swing[]  swingHighs  = array.new<Swing>()
var Swing[]  swingLows   = array.new<Swing>()
var GapBox[] visual_gaps = array.new<GapBox>()
var AxData[] active_axs  = array.new<AxData>()
var label[]  sweep_lbls  = array.new<label>()
var float[]  sweep_lvls  = array.new<float>()
var float[]  sweep_px    = array.new<float>()
var int[]    sweep_t     = array.new<int>()
var bool[]   sweep_isLow = array.new<bool>()

var int   blkIdx        = 0
var int   signalState   = 0
var int   trendState    = 0
var int   lastCdlBar    = -1
var int   lastCdsBar    = -1
var int   ldCount       = 0
var int   sdCount       = 0
var int   po4Seq        = 0
var float trackHigh     = na
var int   trackHighTime = na
var float trackHighL    = na
var float trackLow      = na
var int   trackLowTime  = na
var float trackLowH     = na

bool cdl_event      = false
bool cds_event      = false
bool ld_event       = false
bool sd_event       = false
bool swp_low_event  = false
bool swp_high_event = false

// ═══════════════════════════════════════════════════════════════
// STRUCTURE HELPERS (they read the STRUCTURE candle's volume and delta)
// ═══════════════════════════════════════════════════════════════
f_breakScore(bool isBull, float rv, float dl, bool ax) =>
    int  volPts = rv >= strong_vol_factor ? 2 : rv >= 1.0 ? 1 : 0
    bool agree  = isBull ? dl > 0 : dl < 0
    volPts + (agree ? 1 : 0) + (ax ? 1 : 0)

f_breakTip(string kind, bool isBull, bool pass, float rv, float dl, bool ax, bool bcOk) =>
    bool   agree = isBull ? dl > 0 : dl < 0
    string ctag  = ax ? (isBull ? "BuAx (accelerator)" : "BeAx (accelerator)") : bcOk ? (isBull ? "BuBC" : "BeBC") : "NBC (soft break)"
    string src   = blockSameTF ? (using_real_fp ? "FOOTPRINT" : "SYNTHETIC") : "SYNTHETIC (structure TF " + f_tfName(blockTF) + ")"
    TFP + kind + (pass ? "" : " (failed " + gate_mode + ")") + " | Candle: " + ctag + "\nVolume: " + str.tostring(rv, "#.##") + "x avg" + (rv >= strong_vol_factor ? " (STRONG)" : "") + "\nDelta: " + f_fmt_delta(dl) + (agree ? " (agrees)" : " (against)") + "\nSource: " + src

f_newSwing(bool isHigh, float price, int t, float oOther, int idx) =>
    Swing.new(price, t, idx, isHigh, 0, true, 0, false, isHigh ? price : oOther, isHigh ? oOther : price, t, array.new<Cause>(), false, 0)

// GATE (MMM Pro Edge): a new leg / a continuation needs a fresh confirmation.
f_clearConf() =>
    if swingHighs.size() > 0
        for s in swingHighs
            s.conf := false
    if swingLows.size() > 0
        for s in swingLows
            s.conf := false

// Memory guard: plain swings go first, then the oldest PO4s.
f_guard(Swing[] arr) =>
    while arr.size() > maxKeep
        int idx = 0
        for j = 0 to arr.size() - 1
            if arr.get(j).tier == 0
                idx := j
                break
        arr.remove(idx)

// Only STRONG sweeps get a label. Returns true when it is a strong rejection.
f_sweep(float price, bool isLowSweep, float rv, float dl, float ext, int t) =>
    bool rej       = isLowSweep ? dl > 0 : dl < 0
    bool strongRej = rej and rv >= strong_vol_factor
    if strongRej and showSweeps
        string tip = (isLowSweep ? "Sell-side" : "Buy-side") + " liquidity swept, close back inside\nVolume: " + str.tostring(rv, "#.##") + "x avg (STRONG)\nDelta: " + f_fmt_delta(dl) + " (pushing back)\nDeleted on a close " + (isLowSweep ? "below this candle low" : "above this candle high")
        label lb = label.new(t, price, TFP + "SWP+", xloc=xloc.bar_time, color=color(na), textcolor=isLowSweep ? LINE_BULL : LINE_BEAR, style=isLowSweep ? label.style_label_up : label.style_label_down, size=size.tiny, tooltip=tip)
        sweep_lbls.push(lb)
        sweep_lvls.push(ext)
        sweep_px.push(price)
        sweep_t.push(t)
        sweep_isLow.push(isLowSweep)
        if sweep_lbls.size() > MAX_MARKS
            label.delete(sweep_lbls.shift())
            sweep_lvls.shift()
            sweep_px.shift()
            sweep_t.shift()
            sweep_isLow.shift()
    strongRej

f_addGap(int left, int right, float top, float bot, bool isBull, bool isLine, string txt, color bg, color border, color lnCol, bool fixedStop) =>
    float mid = math.avg(top, bot)
    box bx = isLine ? box.new(left, top, right, bot, border_color=border, bgcolor=color(na), border_style=line.style_dotted) : box.new(left, top, right, bot, border_color=color(na), bgcolor=bg)
    line ln = line.new(left, mid, right, mid, color=lnCol, style=isLine ? line.style_dotted : line.style_solid)
    label lb = show_gap_labels ? label.new(gap_lbl_side == "Right" ? right : left, mid, txt, color=color.new(color.white, 100), textcolor=gap_lbl_col, style=label.style_none, size=size.tiny) : na
    visual_gaps.push(GapBox.new(bx, ln, lb, top, bot, isBull, isLine, false, fixedStop, bg, border, lnCol, bar_index, time))

'''

STEP2 = r'''// STEP 2 — STRUCTURE (one closed STRUCTURE candle per step: HTF in LTF)
// ═══════════════════════════════════════════════════════════════
if stepNow
    blkIdx += 1
    // Order flow of the structure candle: real footprint only on the chart TF
    float sDl   = blockSameTF ? current_delta : bDl
    bool  sAxBu = blockSameTF and bull_accel
    bool  sAxBe = blockSameTF and bear_accel
    bool  bBu   = bC > bH1
    bool  bBe   = bC < bL1

    // 2a. GATE (MMM Pro Edge): the leg reached its OWN extreme (bull >= 80 / bear <= 20)
    if gateOn and not na(gHi) and not na(gLo)
        if gHi >= 80 and signalState == 1
            bullImp := true
        if gLo <= 20 and signalState == -1
            bearImp := true

    // 2b. Track the running extreme of the current leg (and its candle)
    if trendState == 0
        if na(trackHigh) or bH > trackHigh
            trackHigh     := bH
            trackHighTime := bT
            trackHighL    := bL
        if na(trackLow) or bL < trackLow
            trackLow     := bL
            trackLowTime := bT
            trackLowH    := bH
    if trendState == 1 and bH >= trackHigh
        trackHigh     := bH
        trackHighTime := bT
        trackHighL    := bL
    if trendState == -1 and bL <= trackLow
        trackLow     := bL
        trackLowTime := bT
        trackLowH    := bH

    // 2c. The first opposite break candle locks the swing
    if bBe and trendState >= 0
        swingHighs.push(f_newSwing(true, trackHigh, trackHighTime, trackHighL, blkIdx))
        f_guard(swingHighs)
        trendState   := -1
        trackLow     := bL
        trackLowTime := bT
        trackLowH    := bH
    else if bBu and trendState <= 0
        swingLows.push(f_newSwing(false, trackLow, trackLowTime, trackLowH, blkIdx))
        f_guard(swingLows)
        trendState    := 1
        trackHigh     := bH
        trackHighTime := bT
        trackHighL    := bL

    // 2d. Swing lows: a CLOSE below = break (CDSs / SDs#, or a silent delete
    //     for an old-trend swing). A wick only = sweep, the swing stays.
    bool lowBroken = false
    bool lowSwept  = false
    if swingLows.size() > 0
        for i = swingLows.size() - 1 to 0
            Swing s = swingLows.get(i)
            if s.bIdx < blkIdx and bL <= s.price
                if bC < s.price
                    bool isFlip = signalState != -1
                    bool newLeg = s.bIdx > lastCdsBar
                    // GATE: a small p (not confirmed) closed through = deleted, no SD
                    bool gKill  = gateOn and not isFlip and newLeg and not s.conf
                    if not lowBroken and (isFlip or newLeg) and not gKill
                        lowBroken := true
                        int    num  = isFlip ? 0 : sdCount + 1
                        bool   pass = true
                        string kind = isFlip ? "CDS" + ENG : "SD" + ENG + (showNumbers ? str.tostring(num) : "")
                        if swingHighs.size() > 0
                            Swing po = swingHighs.last()
                            po.tier     := isFlip ? 1 : num + 1
                            po.official := pass
                            po4Seq      += 1
                            po.seq      := po4Seq
                            po.causes.push(Cause.new(kind, s.price, s.t, bT, false, pass, f_againstHtf(-1), f_breakScore(false, bRv, sDl, sAxBe), sAxBe, f_breakTip(kind, false, pass, bRv, sDl, sAxBe, bBe)))
                        signalState := -1
                        f_clearConf()
                        if isFlip
                            lastCdsBar := blkIdx
                            sdCount    := 0
                            hitXD      := false
                            hitXP      := false
                            bullImp    := false
                            bullPb     := false
                            bearImp    := false
                            bearPb     := false
                            cds_event  := pass
                        else
                            sdCount  := num
                            bearImp  := false
                            bearPb   := false
                            sd_event := pass
                    swingLows.remove(i)
                else if not s.swept
                    s.swept := true
                    if not lowSwept
                        lowSwept := true
                        if f_sweep(s.price, true, bRv, sDl, bL, bT)
                            swp_low_event := true

    // 2e. Swing highs: a CLOSE above = break (CDLs / LDs#). A wick only = sweep.
    bool highBroken = false
    bool highSwept  = false
    if swingHighs.size() > 0
        for i = swingHighs.size() - 1 to 0
            Swing s = swingHighs.get(i)
            if s.bIdx < blkIdx and bH >= s.price
                if bC > s.price
                    bool isFlip = signalState != 1
                    bool newLeg = s.bIdx > lastCdlBar
                    // GATE: a small p (not confirmed) closed through = deleted, no LD
                    bool gKill  = gateOn and not isFlip and newLeg and not s.conf
                    if not highBroken and (isFlip or newLeg) and not gKill
                        highBroken := true
                        int    num  = isFlip ? 0 : ldCount + 1
                        bool   pass = true
                        string kind = isFlip ? "CDL" + ENG : "LD" + ENG + (showNumbers ? str.tostring(num) : "")
                        if swingLows.size() > 0
                            Swing po = swingLows.last()
                            po.tier     := isFlip ? 1 : num + 1
                            po.official := pass
                            po4Seq      += 1
                            po.seq      := po4Seq
                            po.causes.push(Cause.new(kind, s.price, s.t, bT, true, pass, f_againstHtf(1), f_breakScore(true, bRv, sDl, sAxBu), sAxBu, f_breakTip(kind, true, pass, bRv, sDl, sAxBu, bBu)))
                        signalState := 1
                        f_clearConf()
                        if isFlip
                            lastCdlBar := blkIdx
                            ldCount    := 0
                            hitXD      := false
                            hitXP      := false
                            bullImp    := false
                            bullPb     := false
                            bearImp    := false
                            bearPb     := false
                            cdl_event  := pass
                        else
                            ldCount  := num
                            bullImp  := false
                            bullPb   := false
                            ld_event := pass
                    swingHighs.remove(i)
                else if not s.swept
                    s.swept := true
                    if not highSwept
                        highSwept := true
                        if f_sweep(s.price, false, bRv, sDl, bH, bT)
                            swp_high_event := true

    // 2f. GATE: p -> P# once the pullback reached the OPPOSITE extreme after the leg's own extreme
    if gateOn and not na(gHi) and not na(gLo)
        if signalState == 1 and bullImp and gLo <= 20 and swingHighs.size() > 0
            for s in swingHighs
                if s.bIdx > lastCdlBar and not s.conf
                    s.conf := true
                    s.cIdx := blkIdx
        if signalState == -1 and bearImp and gHi >= 80 and swingLows.size() > 0
            for s in swingLows
                if s.bIdx > lastCdsBar and not s.conf
                    s.conf := true
                    s.cIdx := blkIdx

// ═══════════════════════════════════════════════════════════════
// STEP 2b — SWEEP CLEAN-UP + STRUCTURAL VOIDS (chart timeframe, closed candles)
// ═══════════════════════════════════════════════════════════════
if barstate.isconfirmed
    // Sweep labels die on a close beyond their sweep candle
    if sweep_lbls.size() > 0
        for i = sweep_lbls.size() - 1 to 0
            bool  isLowSw = sweep_isLow.get(i)
            float lvl     = sweep_lvls.get(i)
            if time > sweep_t.get(i) and ((isLowSw and close < lvl) or (not isLowSw and close > lvl))
                label.delete(sweep_lbls.get(i))
                sweep_lbls.remove(i)
                sweep_lvls.remove(i)
                sweep_px.remove(i)
                sweep_t.remove(i)
                sweep_isLow.remove(i)

    // Structural voids (⚡ = made with strong volume)
'''

RENDER = r'''// RENDER — on the last bar everything structural is deleted and redrawn from
// state, so a PO4 removed above takes its breaks and zone with it. Overlays
// (UH$ / UL$, voids, SWP+, AX) are shown or hidden by the same range rule.
// ═══════════════════════════════════════════════════════════════
f_breakColor(Cause c) =>
    not c.pass ? FAIL_COL : htf_dim and c.against ? color.new(FAIL_COL, 30) : c.isBull ? LINE_BULL : LINE_BEAR

f_drawCause(Cause c) =>
    if showBreaks and (c.pass or show_failed)
        color  col = f_breakColor(c)
        string txt = TFP + (c.pass ? c.kind + (showStars and c.score > 0 ? " " + str.tostring(c.score) + "⭐" : "") + (c.ax ? " ⚡" : "") : str.lower(c.kind))
        drawn_lines.push(line.new(c.t1, c.price, c.t2, c.price, xloc=xloc.bar_time, color=col, width=1, style=c.pass ? line.style_solid : line.style_dotted))
        drawn_labels.push(label.new(int(math.avg(c.t1, c.t2)), c.price, txt, xloc=xloc.bar_time, color=color(na), textcolor=col, style=c.isBull ? label.style_label_down : label.style_label_up, size=f_szs(brk_size), tooltip=c.tip + (c.against ? "\nAgainst the HTF bias" : "")))

f_gapPaint(GapBox u, bool vis) =>
    color bgC = u.isTouched ? color.new(u.origBg, 85) : u.origBg
    color bdC = u.isTouched ? color.new(u.origBorder, 80) : u.origBorder
    color lnC = u.isTouched ? color.new(u.origLine, 80) : u.origLine
    color lbC = u.isTouched ? color.new(gap_lbl_col, 70) : gap_lbl_col
    if u.isLine
        u.b.set_border_color(vis ? bdC : color.new(#000000, 100))
    else
        u.b.set_bgcolor(vis ? bgC : color.new(#000000, 100))
    u.l.set_color(vis ? lnC : color.new(#000000, 100))
    if not na(u.lbl)
        u.lbl.set_textcolor(vis ? lbC : color.new(#000000, 100))

if barstate.islast
    f_clear_drawn()
    int futureT = f_future_time(line_ext)
    int spanMs  = timeframe.in_seconds(blockTF) * 1000

    // Trend markers: newest PO4 per side + the newest T1 of that side.
    Swing lastBull = na
    Swing starBull = na
    Swing lastBear = na
    Swing starBear = na
    if swingLows.size() > 0
        for s in swingLows
            if s.tier > 0
                if na(lastBull) or s.seq > lastBull.seq
                    lastBull := s
                if s.tier == 1 and (na(starBull) or s.seq > starBull.seq)
                    starBull := s
    if swingHighs.size() > 0
        for s in swingHighs
            if s.tier > 0
                if na(lastBear) or s.seq > lastBear.seq
                    lastBear := s
                if s.tier == 1 and (na(starBear) or s.seq > starBear.seq)
                    starBear := s

    // The always-drawn range = highest to lowest marker, and their candles.
    float rHi = na
    float rLo = na
    int   hiT = na
    int   loT = na
    for m in array.from(lastBull, starBull, lastBear, starBear)
        if not na(m)
            if na(rHi) or m.price > rHi
                rHi := m.price
                hiT := m.t
            if na(rLo) or m.price < rLo
                rLo := m.price
                loT := m.t

    // Live range: P# = the newest swing of the current leg that a close past
    // would turn into the next LD / SD; R# = the newest opposite swing after it.
    Swing pSw = na
    Swing rSw = na
    if signalState == 1
        for s in swingHighs
            if s.bIdx > lastCdlBar and (na(pSw) or s.bIdx > pSw.bIdx)
                pSw := s
        if not na(pSw)
            for s in swingLows
                if s.bIdx > pSw.bIdx and (na(rSw) or s.bIdx > rSw.bIdx)
                    rSw := s
    else if signalState == -1
        for s in swingLows
            if s.bIdx > lastCdsBar and (na(pSw) or s.bIdx > pSw.bIdx)
                pSw := s
        if not na(pSw)
            for s in swingHighs
                if s.bIdx > pSw.bIdx and (na(rSw) or s.bIdx > rSw.bIdx)
                    rSw := s
    int nRng = (signalState == 1 ? ldCount : sdCount) + 1
    // GATE: P# is a small p until confirmed; the R# only counts after it
    bool pCf = not na(pSw) and (not gateOn or pSw.conf)
    if gateOn and not na(rSw) and (not pCf or rSw.bIdx <= pSw.cIdx)
        rSw := na

    array<int> q = f_quota()

    // 1. PO4s (a PO4 + its breaks + its zone = ONE item), newest first
    array<Swing> po4L = array.new<Swing>()
    array<int>   po4S = array.new<int>()
    array<Swing> plnL = array.new<Swing>()
    array<int>   plnT = array.new<int>()
    for side = 0 to 1
        Swing[] arr = side == 0 ? swingHighs : swingLows
        if arr.size() > 0
            for s in arr
                if s.tier > 0
                    po4L.push(s)
                    po4S.push(s.seq)
                else
                    plnL.push(s)
                    plnT.push(s.t)
    array<Swing> vis = array.new<Swing>()
    if po4L.size() > 0
        array<int> o1 = po4S.sort_indices(order.descending)
        for k = 0 to o1.size() - 1
            Swing s = po4L.get(o1.get(k))
            if f_take(q, f_inR(s.price, rHi, rLo) or f_onMarker(s.t, hiT, loT, spanMs), not s.isHigh)
                vis.push(s)
    // 2. plain swings (the live P# / R# can always show)
    if plnL.size() > 0
        array<int> o2 = plnT.sort_indices(order.descending)
        for k = 0 to o2.size() - 1
            Swing s = plnL.get(o2.get(k))
            bool live = showLiveAlways and ((not na(pSw) and s.bIdx == pSw.bIdx and s.isHigh == pSw.isHigh) or (not na(rSw) and s.bIdx == rSw.bIdx and s.isHigh == rSw.isHigh))
            if live or f_take(q, f_inR(s.price, rHi, rLo) or f_onMarker(s.t, hiT, loT, spanMs), not s.isHigh)
                vis.push(s)

    if showSwings and vis.size() > 0
        for s in vis
            bool isPO4 = s.tier > 0
            bool isP   = not na(pSw) and s.bIdx == pSw.bIdx and s.isHigh == pSw.isHigh
            bool isR   = not na(rSw) and s.bIdx == rSw.bIdx and s.isHigh == rSw.isHigh
            bool isPL  = (signalState == 1 and not na(lastBull) and s.seq == lastBull.seq and not s.isHigh) or (signalState == -1 and not na(lastBear) and s.seq == lastBear.seq and s.isHigh)
            color  c   = isPO4 ? (s.official ? (s.isHigh ? LINE_BEAR : LINE_BULL) : FAIL_COL) : isP ? color.new(s.isHigh ? LINE_BEAR : LINE_BULL, pCf ? 0 : 40) : isR ? (s.isHigh ? LINE_BEAR : LINE_BULL) : s.isHigh ? (signalState == 1 ? BULL_TGT : color.new(LINE_BEAR, 30)) : (signalState == -1 ? BEAR_TGT : color.new(LINE_BULL, 30))
            string nm  = isPO4 ? (s.isHigh ? "BePO4" : "BuPO4") + ENG + " T" + str.tostring(s.tier) + (s.official ? "" : " ✗") : isP ? (pCf ? (s.isHigh ? "BeP" : "BuP") + str.tostring(nRng) + ENG : (s.isHigh ? "bep" : "bup") + str.tostring(nRng) + ENG + " · p") : isR ? (s.isHigh ? "BeR" : "BuR") + str.tostring(nRng) + ENG : s.isHigh ? "sh" : "sl"
            string txt = TFP + nm
            string tip = isPO4 ? (isPL ? "Protected Level (PL): the swing that made the last break. A body close through it flips the structure." : "PO4 = the swing that made this break. A body close through it deletes it with its break and zone.") : isP ? (pCf ? "P# = the newest swing of this leg. A body close past it = the next " + (signalState == 1 ? "LD" : "SD") + str.tostring(nRng) + ENG + "." : "small p: the " + gate_mode + " gate has not confirmed this pullback yet (leg's own extreme, then the opposite extreme). A close through it deletes it: no LD / SD.") : isR ? "R# = the newest swing after P#. It becomes PO4 T" + str.tostring(nRng + 1) + " on the next " + (signalState == 1 ? "LD" : "SD") + "." : (s.isHigh ? "Swing high" : "Swing low") + (s.swept ? " (swept)" : "") + " — deleted on a body close through it"
            string sty = isPO4 ? line.style_solid : isP ? line.style_dashed : line.style_dotted
            f_add_level(s.price, txt, c, isPL ? 2 : 1, sty, s.t, futureT, isPO4 ? (isPL ? 6 : 5) : isP or isR ? 4 : 2, lvl_size, tip)
            if isPO4
                if s.causes.size() > 0
                    for cz in s.causes
                        f_drawCause(cz)
                bool showZ = s.tier == 1 ? show_eblk : show_iblk
                if showZ and s.official and not na(s.oH) and not na(s.oL) and s.oH > s.oL
                    [zT, zB] = f_zoneSlice(s.oH, s.oL, not s.isHigh)
                    color zc = s.isHigh ? LINE_BEAR : LINE_BULL
                    drawn_boxes.push(box.new(s.oT, zT, futureT, zB, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(zc, zone_transp), text=zone_show_name ? TFP + f_zoneName(s.tier == 1, not s.isHigh, ENG) : "", text_color=color.new(zc, 20), text_size=size.tiny, text_halign=text.align_right, text_valign=text.align_center))

    // 3. UH$ / UL$
    if uh_lbls.size() > 0
        for i = uh_lbls.size() - 1 to 0
            bool v = f_take(q, f_inR(uh_prices.get(i), rHi, rLo) or f_onMarker(uh_t.get(i), hiT, loT, spanMs), false)
            label.set_textcolor(uh_lbls.get(i), v ? uh_col : color.new(uh_col, 100))
    if ul_lbls.size() > 0
        for i = ul_lbls.size() - 1 to 0
            bool v = f_take(q, f_inR(ul_prices.get(i), rHi, rLo) or f_onMarker(ul_t.get(i), hiT, loT, spanMs), true)
            label.set_textcolor(ul_lbls.get(i), v ? ul_col : color.new(ul_col, 100))
    // 4. voids
    if visual_gaps.size() > 0
        for i = visual_gaps.size() - 1 to 0
            GapBox u = visual_gaps.get(i)
            f_gapPaint(u, f_take(q, f_boxInR(u.top, u.bot, rHi, rLo) or f_onMarker(u.t, hiT, loT, spanMs), u.isBull))
    // 5. SWP+
    if sweep_lbls.size() > 0
        for i = sweep_lbls.size() - 1 to 0
            bool isLowSw = sweep_isLow.get(i)
            bool v = f_take(q, f_inR(sweep_px.get(i), rHi, rLo) or f_onMarker(sweep_t.get(i), hiT, loT, spanMs), isLowSw)
            color sc = isLowSw ? LINE_BULL : LINE_BEAR
            label.set_textcolor(sweep_lbls.get(i), v ? sc : color.new(sc, 100))
    // 6. AX
    if active_axs.size() > 0
        for i = active_axs.size() - 1 to 0
            AxData ax = active_axs.get(i)
            bool  v  = f_take(q, f_inR(ax.trigger, rHi, rLo) or f_onMarker(ax.t, hiT, loT, spanMs), ax.isBull)
            color ac = ax.isBull ? DEEP_GREEN : DEEP_RED
            label.set_textcolor(ax.lbl, v ? ac : color.new(ac, 100))
            if not na(ax.tri)
                label.set_color(ax.tri, v ? ac : color.new(ac, 100))

    if show_tn_step
        bool bullSame = not na(starBull) and not na(lastBull) and starBull.seq == lastBull.seq
        bool bearSame = not na(starBear) and not na(lastBear) and starBear.seq == lastBear.seq
        if not na(starBull)
            drawn_labels.push(label.new(futureT, starBull.price, bullSame ? "🟢🟩" : "🟢", xloc=xloc.bar_time, style=label.style_label_right, color=color(na), textcolor=LINE_BULL, size=size.small))
        if not na(lastBull) and not bullSame
            drawn_labels.push(label.new(futureT, lastBull.price, "🟩", xloc=xloc.bar_time, style=label.style_label_right, color=color(na), textcolor=LINE_BULL, size=size.small))
        if not na(starBear)
            drawn_labels.push(label.new(futureT, starBear.price, bearSame ? "🔴🟥" : "🔴", xloc=xloc.bar_time, style=label.style_label_right, color=color(na), textcolor=LINE_BEAR, size=size.small))
        if not na(lastBear) and not bearSame
            drawn_labels.push(label.new(futureT, lastBear.price, "🟥", xloc=xloc.bar_time, style=label.style_label_right, color=color(na), textcolor=LINE_BEAR, size=size.small))

    f_draw_groups()
    f_xdxpDraw()

'''

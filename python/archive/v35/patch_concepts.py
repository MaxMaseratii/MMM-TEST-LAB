import sys
src = open('concepts_orig.pine').read()
n_edits = 0

def rep(old, new, count=1):
    global src, n_edits
    c = src.count(old)
    if c != count:
        print("FAIL count=%d for:\n%s" % (c, old[:300]))
        sys.exit(1)
    src = src.replace(old, new)
    n_edits += 1

# ---------------------------------------------------------------- header
rep('''//@version=6
indicator("MMM Concepts Pro+ @MaxMaserati", overlay=true, max_lines_count=500, max_labels_count=500, max_boxes_count=500)
''', '''//@version=6
indicator("MMM Concepts Pro+ @MaxMaserati", overlay=true, max_lines_count=500, max_labels_count=500, max_boxes_count=500)

// =====================================================
// MMM CONCEPTS PRO+ — the ZONE engine "x" of the MMM foundation
//   Zone (box) = expander BC + the candles that close back inside it.
//   Flip         = CDLx / CDSx  (box closed through AGAINST the trend)
//   Continuation = LDx1, LDx2… / SDx1, SDx2… (count runs until the next flip)
//   Gate (NO GATE / MMPD 27 / MMPD fast / MMPD Delta) decides which breaks
//   are OFFICIAL. Only official breaks get entries, alerts and HTF bias.
//   Block TF data = last CLOSED block candle only. No repaint.
// =====================================================
''')

# ---------------------------------------------------------------- new inputs
rep('''showOnlyCDLxCDSx = input.bool(false, "Show Only CDLx/CDSx", inline='univ2', group='⚡ PRIMARY CONTROLS')
''', '''showOnlyCDLxCDSx = input.bool(false, "Show Only CDLx/CDSx", inline='univ2', group='⚡ PRIMARY CONTROLS')

// =====================================================
// 🧱 BOX GROWTH (G1 vs G0)
// =====================================================
boxGrowMode = input.string("Grow with wicks (G1)", "Box Growth", options=["Grow with wicks (G1)", "Fixed range (G0)"], group="🧱 Box Growth", tooltip="G1 GROW: the box keeps the MMM definition. Inside candles whose wicks go past the edge (and close back inside) push the edge out to the new last high / last low. The protected level sits past the liquidity already taken = fewer fake breaks, wider stop.\\n\\nG0 FIXED: like B&C. The box is frozen at the range it had when it was born (the expander candle range). It breaks earlier and gives a tighter stop, but fakes out more.\\n\\nTest both. Let the data decide.")
bool boxGrow = boxGrowMode == "Grow with wicks (G1)"

// =====================================================
// 🚦 GATE (which breaks are official)
// =====================================================
grp_gate    = "🚦 Gate (Official Breaks)"
gate_mode   = input.string("NO GATE", "Gate", options=["NO GATE", "MMPD 27", "MMPD fast", "MMPD Delta"], group=grp_gate, tooltip="NO GATE = every break is official (normal break, no filter).\\n\\nMMPD 27 / MMPD fast / MMPD Delta = the MMM Pro Edge rhythm, read on the BLOCK timeframe:\\n• Flip (CDLx / CDSx) is official only if the old leg reached its extreme first: oscillator ≤ 20 before a CDLx, ≥ 80 before a CDSx.\\n• Continuation (LDx / SDx) is official only if the leg reached its OWN extreme (bull ≥ 80) and THEN the pullback reached the OPPOSITE extreme (≤ 20) before the break.\\n\\nMMPD Delta = the natural order-flow version (built on candle delta).\\nThe structure never changes with the gate. Only official breaks get entries and alerts.")
gate_fast   = input.int(9, "MMPD fast Length", minval=5, maxval=50, group=grp_gate)
show_failed = input.bool(false, "Show Failed Breaks (small grey)", group=grp_gate, tooltip="OFF = only official breaks are drawn.\\nON = breaks that failed the gate are drawn in grey, lowercase (cdlx, ldx3...).")
showNextLvl = input.bool(true, "Show Next LDx / SDx Level", group=grp_gate, tooltip="Draws the level that makes the NEXT continuation, with its number (▸ LDx3). A body close through it = LDx3.")

// =====================================================
// 🧭 HTF BIAS (HTF in LTF)
// =====================================================
grp_htfb   = "🧭 HTF Bias"
htf_mode   = input.string("Off", "HTF Bias From", options=["Off", "Last Flip (CDLx/CDSx)", "Last Continuation (LDx/SDx)", "Last BC"], group=grp_htfb, tooltip="The zone engine runs on the HTF (last CLOSED HTF candle only, no repaint).\\n\\nLast Flip = direction of the last HTF CDLx / CDSx (the trend).\\nLast Continuation = direction of the last HTF LDx / SDx made AFTER the last flip. No continuation yet = no bias.\\nLast BC = direction of the last HTF body close candle.\\n\\nOff = no HTF filter.")
htf_bias_tf = input.timeframe("240", "HTF Bias Timeframe", group=grp_htfb)
htf_filter = input.bool(true, "Entries With HTF Bias Only", group=grp_htfb)
htf_table  = input.bool(true, "Show HTF Bias Box", inline="hb", group=grp_htfb)
htf_tbl_pos = input.string("Bottom Center", "", options=["Top Left","Top Center","Top Right","Bottom Left","Bottom Center","Bottom Right"], inline="hb", group=grp_htfb)

// =====================================================
// 📰 NEWS BLOCK (no trades)
// =====================================================
grp_news   = "📰 News Block"
news_on    = input.bool(true, "Block Entries Around News", group=grp_news, tooltip="No new trade, and every NOT-YET-FILLED trade is cancelled, on a candle that touches a news window (New York time). Intraday charts only.\\nCPI / NFP: 08:30. FOMC: 14:00 statement + 14:30 press conference.")
news_nfp   = input.bool(true, "NFP = First Friday of the Month", group=grp_news, tooltip="BLS sometimes moves NFP (holidays, shutdowns). Add those dates to the CPI list if needed.")
news_pre   = input.int(5, "Minutes Before", minval=0, maxval=120, inline="nw", group=grp_news)
news_post  = input.int(15, "Minutes After", minval=0, maxval=240, inline="nw", group=grp_news)
cpi_dates  = input.text_area("2026-01-13,2026-02-13,2026-03-11,2026-04-10,2026-05-12,2026-06-10,2026-07-14,2026-08-12,2026-09-11,2026-10-14,2026-11-10,2026-12-10,2027-01-13,2027-02-11,2027-03-10,2027-04-13,2027-05-12,2027-06-10,2027-07-14,2027-08-11,2027-09-14,2027-10-14,2027-11-10,2027-12-10", "CPI Dates (YYYY-MM-DD)", group=grp_news, tooltip="Comma separated, New York date. Source: BLS release schedule. Add older dates to block them in backtests.")
fomc_dates = input.text_area("2025-01-29,2025-03-19,2025-05-07,2025-06-18,2025-07-30,2025-09-17,2025-10-29,2025-12-10,2026-01-28,2026-03-18,2026-04-29,2026-06-17,2026-07-29,2026-09-16,2026-10-28,2026-12-09,2027-01-27,2027-03-17,2027-04-28,2027-06-09,2027-07-28,2027-09-15,2027-10-27,2027-12-08", "FOMC Decision Dates (YYYY-MM-DD)", group=grp_news, tooltip="Comma separated, decision day only. 2027 dates are tentative — check federalreserve.gov.")
news_bg    = input.bool(true, "Shade News Windows", group=grp_news)
''')

# exact-point stops by default
rep('''slTicksCandle = input.int(2, "SL Ticks Beyond Candle/Block"''', '''slTicksCandle = input.int(0, "SL Ticks Beyond Candle/Block"''')
rep('''slTicksBox = input.int(2, "SL Ticks Beyond Block"''', '''slTicksBox = input.int(0, "SL Ticks Beyond Block"''')

# ---------------------------------------------------------------- HTF data (no repaint)
rep('''[htf_time, htf_time_close, htf_high, htf_low, htf_close, htf_volume, htf_open] =
     request.security(syminfo.tickerid, blockTF, [time, time_close, high, low, close, volume, open], lookahead=barmerge.lookahead_off)

var prev_htf_block_time = 0
newHTFBlockCandle = htf_time != prev_htf_block_time
prev_htf_block_time := htf_time

htf_prev_high = request.security(syminfo.tickerid, blockTF, high[1], lookahead=barmerge.lookahead_off)
htf_prev_low  = request.security(syminfo.tickerid, blockTF, low[1],  lookahead=barmerge.lookahead_off)
htf_prev_time = request.security(syminfo.tickerid, blockTF, time[1], lookahead=barmerge.lookahead_off)
''', '''// NO REPAINT: on a higher block TF we read the LAST CLOSED block candle
// ([1] + lookahead_on). History and live behave the same: a block candle is
// processed on the first chart candle after it closed. On the chart TF the
// candle is read directly (no delay).
bool blockSameTF = timeframe.in_seconds(blockTF) <= timeframe.in_seconds(timeframe.period)

f_blockNow() =>
    bool bAff = high <= high[1] and low <= low[1] and close <= high[1] and close >= low[1] and high >= low[1]
    bool sAff = low >= low[1] and high >= high[1] and close <= high[1] and close >= low[1] and low <= high[1]
    [time, time_close, high, low, close, nz(volume), open, high[1], low[1], time[1], bAff, sAff]

f_blockPrev() =>
    [t0, tc0, h0, l0, c0, v0, o0, ph0, pl0, pt0, ba0, sa0] = f_blockNow()
    [t0[1], tc0[1], h0[1], l0[1], c0[1], v0[1], o0[1], ph0[1], pl0[1], pt0[1], ba0[1], sa0[1]]

[n_time, n_tclose, n_high, n_low, n_close, n_vol, n_open, n_phigh, n_plow, n_ptime, n_bAff, n_sAff] = f_blockNow()
[s_time, s_tclose, s_high, s_low, s_close, s_vol, s_open, s_phigh, s_plow, s_ptime, s_bAff, s_sAff] = request.security(syminfo.tickerid, blockTF, f_blockPrev(), lookahead=barmerge.lookahead_on)

htf_time       = blockSameTF ? n_time   : s_time
htf_time_close = blockSameTF ? n_tclose : s_tclose
htf_high       = blockSameTF ? n_high   : s_high
htf_low        = blockSameTF ? n_low    : s_low
htf_close      = blockSameTF ? n_close  : s_close
htf_volume     = blockSameTF ? n_vol    : s_vol
htf_open       = blockSameTF ? n_open   : s_open
htf_prev_high  = blockSameTF ? n_phigh  : s_phigh
htf_prev_low   = blockSameTF ? n_plow   : s_plow
htf_prev_time  = blockSameTF ? n_ptime  : s_ptime
htf_bullAff    = blockSameTF ? n_bAff   : s_bAff
htf_bearAff    = blockSameTF ? n_sAff   : s_sAff

var prev_htf_block_time = 0
newHTFBlockCandle = not na(htf_time) and htf_time != prev_htf_block_time
prev_htf_block_time := nz(htf_time, prev_htf_block_time)
''')

rep('''htf_isNeutralCandle    = not htf_isBullishBodyClose and not htf_isBearishBodyClose
''', '''htf_isNeutralCandle    = not htf_isBullishBodyClose and not htf_isBearishBodyClose

// =====================================================
// GATE OSCILLATORS (same math as Super MMPD / MMM Pro Edge)
// =====================================================
const color FAIL_COL = #9e9e9e
const string NY = "America/New_York"
bool gateOn = gate_mode != "NO GATE"

f_xsa(float src, int len) =>
    var float out = na
    float ma = ta.sma(src, len)
    out := na(out) ? ma : (src + out * (len - 1)) / len
    out

f_mmpd(int len) =>
    float cl = (close - ta.lowest(low, len)) / (ta.highest(high, len) - ta.lowest(low, len)) * 100
    float s1 = f_xsa(cl, 5)
    float s2 = f_xsa(s1, 3)
    float c  = (3 * s1 - 2 * s2 - 50) * 1.032 + 50
    float o  = ta.ema(((2 * close + high + low + open) / 5 - ta.lowest(low, len + 7)) / (ta.highest(high, len + 7) - ta.lowest(low, len + 7)) * 100, 13)
    [c, o]

f_dma() =>
    float v  = na(volume) or volume == 0 ? 1.0 : volume
    float dl = close > open and close > close[1] ? v : close < open and close < close[1] ? -v : close > close[1] ? v * 0.5 : close < close[1] ? -v * 0.5 : 0.0
    float ds = ta.ema(dl, 3)
    float lo = ta.lowest(ds, 14)
    float dr = ta.highest(ds, 14) - lo
    float c  = ta.ema(dr > 0 ? (ds - lo) / dr * 100 : 50, 3)
    float o  = ta.ema(c, 13)
    [c, o]

f_gateNow() =>
    [c1, o1] = f_mmpd(27)
    [c2, o2] = f_mmpd(gate_fast)
    [c3, o3] = f_dma()
    float hi = gate_mode == "MMPD 27" ? math.max(c1, o1) : gate_mode == "MMPD fast" ? math.max(c2, o2) : math.max(c3, o3)
    float lo = gate_mode == "MMPD 27" ? math.min(c1, o1) : gate_mode == "MMPD fast" ? math.min(c2, o2) : math.min(c3, o3)
    [hi, lo]

f_gatePrev() =>
    [hi, lo] = f_gateNow()
    [hi[1], lo[1]]

[g_hi_now, g_lo_now] = f_gateNow()
[g_hi_htf, g_lo_htf] = request.security(syminfo.tickerid, blockTF, f_gatePrev(), lookahead=barmerge.lookahead_on)
float gHi = blockSameTF ? g_hi_now : g_hi_htf
float gLo = blockSameTF ? g_lo_now : g_lo_htf

// Gate memory (impulse -> pullback -> continuation), block TF candles
var bool hitXD   = false   // oscillator <= 20 since the last flip
var bool hitXP   = false   // oscillator >= 80 since the last flip
var bool bullImp = false   // bull leg reached its own extreme (>= 80)
var bool bullPb  = false   // then the pullback reached <= 20
var bool bearImp = false
var bool bearPb  = false

// =====================================================
// HTF BIAS — compact copy of the zone engine on the HTF (closed candle only)
// =====================================================
f_htfZone() =>
    var float exH   = na
    var float exL   = na
    var int   exDir = 0
    var bool  waiting = false
    var bool  live  = false
    var float bH    = na
    var float bL    = na
    var int   bType = 0      // 1 = Supply (after BuBC), -1 = Demand (after BeBC)
    var int   bias  = 0
    var int   lastC = 0
    var int   lastBC = 0
    var float revH  = na
    var float revL  = na
    bool bu = close > high[1]
    bool be = close < low[1]
    bool bc = bu or be
    bool flipped = false
    if live
        if bc and (close > bH or close < bL)
            bool up = close > bH
            if up and bType == -1 and bias != 1
                bias    := 1
                lastC   := 0
                revH    := bH
                revL    := bL
                flipped := true
            else if not up and bType == 1 and bias != -1
                bias    := -1
                lastC   := 0
                revH    := bH
                revL    := bL
                flipped := true
            live    := false
            exH     := high
            exL     := low
            exDir   := up ? 1 : -1
            waiting := true
        else if boxGrow
            bH := math.max(bH, high)
            bL := math.min(bL, low)
    else if waiting
        if bc
            exH   := high
            exL   := low
            exDir := bu ? 1 : -1
        else if close <= exH and close >= exL
            live    := true
            bH      := exH
            bL      := exL
            bType   := exDir
            waiting := false
        else
            waiting := false
    else if bc
        exH     := high
        exL     := low
        exDir   := bu ? 1 : -1
        waiting := true
    if not flipped
        if bu and be[1] and bias != 1
            bias    := 1
            lastC   := 0
            revH    := high
            revL    := low[1]
            flipped := true
        else if be and bu[1] and bias != -1
            bias    := -1
            lastC   := 0
            revH    := high[1]
            revL    := low
            flipped := true
    if not flipped
        if bias == 1 and bu and not na(revH) and close > revH
            lastC := 1
            revH  := high
        else if bias == -1 and be and not na(revL) and close < revL
            lastC := -1
            revL  := low
    if bu
        lastBC := 1
    if be
        lastBC := -1
    [nz(bias[1]), nz(lastC[1]), nz(lastBC[1])]

[htfSig, htfCont, htfBC] = request.security(syminfo.tickerid, htf_bias_tf, f_htfZone(), lookahead=barmerge.lookahead_on)
int  htfBias  = htf_mode == "Last Flip (CDLx/CDSx)" ? htfSig : htf_mode == "Last Continuation (LDx/SDx)" ? htfCont : htf_mode == "Last BC" ? htfBC : 0
bool htfLong  = htf_mode == "Off" or not htf_filter or htfBias == 1
bool htfShort = htf_mode == "Off" or not htf_filter or htfBias == -1

// =====================================================
// NEWS BLOCK (light: date lists + first-Friday NFP, no external data)
// =====================================================
f_inWin(int startMin, int endMin) =>
    int bS = hour(time, NY) * 60 + minute(time, NY)
    int bE = hour(time_close, NY) * 60 + minute(time_close, NY)
    if bE <= bS
        bE += 1440
    bS < endMin and bE > startMin

string dStr      = str.format_time(time, "yyyy-MM-dd", NY)
bool   isNFP     = news_nfp and dayofweek(time, NY) == dayofweek.friday and dayofmonth(time, NY) <= 7
bool   isCPI     = str.contains(cpi_dates, dStr)
bool   isFOMC    = str.contains(fomc_dates, dStr)
bool   newsBlock = news_on and timeframe.isintraday and (((isCPI or isNFP) and f_inWin(510 - news_pre, 510 + news_post)) or (isFOMC and f_inWin(840 - news_pre, 900 + news_post)))

bgcolor(news_bg and newsBlock ? color.new(color.orange, 85) : na, title="News Window")

// Official-event flags (for alertcondition)
bool ev_cdl = false
bool ev_cds = false
bool ev_ld  = false
bool ev_sd  = false
''')

# ---------------------------------------------------------------- types
rep('''    float  entryZonePrice
    label  ldsdLabel

var NeutralBox[] neutralBoxes''', '''    float  entryZonePrice
    label  ldsdLabel
    bool   isRev    = false   // the break was a flip (CDLx / CDSx)
    bool   official = true    // the break passed the gate (and, for continuations, the trend)

var NeutralBox[] neutralBoxes''')

rep('''    float  midlinePrice
    bool   zoneTouched

var CDLPlusBlock[] cdlPlusBlocks''', '''    float  midlinePrice
    bool   zoneTouched
    bool   official = true

var CDLPlusBlock[] cdlPlusBlocks''')

rep('''    string sweepType
    bool   isBullish

var SweepLine lastBullishSweep''', '''    string sweepType
    bool   isBullish
    float  candleExt = na   // the sweep candle's low (low sweep) / high (high sweep)

var SweepLine lastBullishSweep''')

# ---------------------------------------------------------------- CDLx+ block label: middle right at line end
rep('''createCDLPlusBlock(string pType, int barIdx, int barTime, float priceH, float priceL, float openP, float closeP, string tfString) =>
    blk = CDLPlusBlock.new()''', '''createCDLPlusBlock(string pType, int barIdx, int barTime, float priceH, float priceL, float openP, float closeP, string tfString, bool isOfficial) =>
    blk = CDLPlusBlock.new()
    blk.official      := isOfficial''')
rep('''    labelText = cdlPlusLblFmt != 'None' ? getCDLPlusLabelText(pType == "CDLx+", tfString, cdlPlusLblFmt) : ""
    if labelText != "" and in_calc_range
        labelYPos  = pType == "CDLx+" ? priceH : priceL
        labelStyle = pType == "CDLx+" ? label.style_label_up : label.style_label_down
        blk.theLabel := label.new(x=f_future_time(offsetGap), y=labelYPos, text=labelText, color=color.new(color.white, 100), textcolor=lineColor, style=labelStyle, size=getSizeFromString(cdlPlusLblSize), xloc=xloc.bar_time)
''', '''    labelText = cdlPlusLblFmt != 'None' ? getCDLPlusLabelText(pType == "CDLx+", tfString, cdlPlusLblFmt) : ""
    labelText := isOfficial ? labelText : str.lower(labelText)
    if labelText != "" and in_calc_range
        blk.theLabel := label.new(x=extTime, y=blk.price, text=labelText, color=color.new(color.white, 100), textcolor=isOfficial ? lineColor : FAIL_COL, style=label.style_label_left, size=getSizeFromString(cdlPlusLblSize), xloc=xloc.bar_time)
''')
rep('''    line.set_x2(blk.theLine, extTime)
    if not na(blk.theLabel)
        label.set_x(blk.theLabel, f_future_time(offsetGap))''', '''    line.set_x2(blk.theLine, extTime)
    if not na(blk.theLabel)
        label.set_x(blk.theLabel, extTime)''')

# ---------------------------------------------------------------- trade filter (news + HTF bias)
rep('''addTradeToCategory(Trade t, string category) =>
    targetArray = switch category
        "BlockCDLPlus"   => trades_BlockCDLPlus
        "BlockCDL"       => trades_BlockCDL
        "BlockLD"        => trades_BlockLD
        "CandleCDLPlus"  => trades_CandleCDLPlus
        "CandleCDL"      => trades_CandleCDL
        "CandleLD"       => trades_CandleLD
        => trades_BlockCDL
    maxLimit = switch category
        "BlockCDLPlus"   => maxEntries_BlockCDLPlus
        "BlockCDL"       => maxEntries_BlockCDL
        "BlockLD"        => maxEntries_BlockLD
        "CandleCDLPlus"  => maxEntries_CandleCDLPlus
        "CandleCDL"      => maxEntries_CandleCDL
        "CandleLD"       => maxEntries_CandleLD
        => 1
    while array.size(targetArray) >= maxLimit
        oldTrade = array.shift(targetArray)
        deleteTrade(oldTrade)
    array.push(targetArray, t)
    array.set(manualExitWarningFlag, 0, false)
    true
''', '''// Every new trade passes the same two filters: no news window, and the HTF
// bias (when enabled) points the same way. A rejected trade is erased.
addTradeToCategory(Trade t, string category) =>
    bool ok = not newsBlock and (t.isLong ? htfLong : htfShort)
    if not ok
        deleteTrade(t)
    else
        targetArray = switch category
            "BlockCDLPlus"   => trades_BlockCDLPlus
            "BlockCDL"       => trades_BlockCDL
            "BlockLD"        => trades_BlockLD
            "CandleCDLPlus"  => trades_CandleCDLPlus
            "CandleCDL"      => trades_CandleCDL
            "CandleLD"       => trades_CandleLD
            => trades_BlockCDL
        maxLimit = switch category
            "BlockCDLPlus"   => maxEntries_BlockCDLPlus
            "BlockCDL"       => maxEntries_BlockCDL
            "BlockLD"        => maxEntries_BlockLD
            "CandleCDLPlus"  => maxEntries_CandleCDLPlus
            "CandleCDL"      => maxEntries_CandleCDL
            "CandleLD"       => maxEntries_CandleLD
            => 1
        while array.size(targetArray) >= maxLimit
            oldTrade = array.shift(targetArray)
            deleteTrade(oldTrade)
        array.push(targetArray, t)
        array.set(manualExitWarningFlag, 0, false)
    ok
''')

# ---------------------------------------------------------------- box logic start: gate memory + affinity globals
rep('''if enableNeutralCandleBoxes and barstate.isconfirmed and newHTFBlockCandle and in_calc_range
    isCurrentNonBodyClose   = htf_isNeutralCandle
    isCurrentBodyClose      = htf_isBullishBodyClose or htf_isBearishBodyClose
    isCurrentBullishAffinity = request.security(syminfo.tickerid, blockTF, high <= high[1] and low <= low[1] and close <= high[1] and close >= low[1] and high >= low[1], lookahead=barmerge.lookahead_off)
    isCurrentBearishAffinity = request.security(syminfo.tickerid, blockTF, low >= low[1] and high >= high[1] and close <= high[1] and close >= low[1] and low <= high[1], lookahead=barmerge.lookahead_off)
''', '''bool flipThisBar = false   // a CDLx / CDSx happened on this block candle
bool flipPass    = true    // ...and it passed the gate
bool contThisBar = false   // an LDx / SDx happened on this block candle
bool contPass    = true

if enableNeutralCandleBoxes and barstate.isconfirmed and newHTFBlockCandle and in_calc_range
    isCurrentNonBodyClose   = htf_isNeutralCandle
    isCurrentBodyClose      = htf_isBullishBodyClose or htf_isBearishBodyClose
    isCurrentBullishAffinity = htf_bullAff
    isCurrentBearishAffinity = htf_bearAff

    // GATE MEMORY — this block candle's oscillator (only matters when a gate is on)
    if gateOn and not na(gHi) and not na(gLo)
        if gHi >= 80
            hitXP := true
            if currentBias == "CDLx"
                bullImp := true
            if currentBias == "CDSx" and bearImp
                bearPb := true
        if gLo <= 20
            hitXD := true
            if currentBias == "CDSx"
                bearImp := true
            if currentBias == "CDLx" and bullImp
                bullPb := true
''')

# ---------------------------------------------------------------- G0 fixed box on inside candles
rep('''    if (isCurrentNonBodyClose or isCurrentBullishAffinity or isCurrentBearishAffinity) and minNeutralCandles == 1 and not na(currentLiveBox) and trackingNeutral
        neutralCount += 1
        if currentLiveBox.boxType == "Demand" and isCurrentBullishAffinity''', '''    if (isCurrentNonBodyClose or isCurrentBullishAffinity or isCurrentBearishAffinity) and minNeutralCandles == 1 and not na(currentLiveBox) and trackingNeutral
        neutralCount += 1
        if not boxGrow
            na
        else if currentLiveBox.boxType == "Demand" and isCurrentBullishAffinity''')
rep('''        float boxHigh = neutralHigh
        float boxLow  = neutralLow
        if useExpanderBoundaries and not na(lastExpanderHigh) and not na(lastExpanderLow)
            if currentLiveBox.boxType == "Demand"
                boxLow  := displayBoxBoundary
                if lastExpanderHigh >= neutralHigh
                    boxHigh := lastExpanderHigh
            else
                boxHigh := displayBoxBoundary
                if lastExpanderLow <= neutralLow
                    boxLow := lastExpanderLow
''', '''        float boxHigh = neutralHigh
        float boxLow  = neutralLow
        if not boxGrow
            // G0 FIXED: the box keeps the range it was born with.
            boxHigh := currentLiveBox.originalHigh
            boxLow  := currentLiveBox.originalLow
        else if useExpanderBoundaries and not na(lastExpanderHigh) and not na(lastExpanderLow)
            if currentLiveBox.boxType == "Demand"
                boxLow  := displayBoxBoundary
                if lastExpanderHigh >= neutralHigh
                    boxHigh := lastExpanderHigh
            else
                boxHigh := displayBoxBoundary
                if lastExpanderLow <= neutralLow
                    boxLow := lastExpanderLow
''')
rep('''            bodyCloseSwept   = false
            if not closeBreaksAbove and not closeBreaksBelow''', '''            bodyCloseSwept   = false
            if not closeBreaksAbove and not closeBreaksBelow and boxGrow''')

# ---------------------------------------------------------------- flip block (always computed, gate, middle-right labels, short SL fix)
old_flip_start = '''                CDLabel      = label(na)
                isReversal   = false
                if showCDLabels or showOnlyCDLxCDSx
                    cdexText  = ""
                    cdexColor = color(na)
                    cdexY     = 0.0
                    CDStyle   = label.style_label_up
                    if currentLiveBox.boxType == "Supply" and closeBreaksBelow
                        isReversal := true
                        cdexText   := "CDSx"
                        cdexColor  := CDShortColor
                        cdexY      := currentLiveBox.low
                        CDStyle    := label.style_label_down
                    else if currentLiveBox.boxType == "Demand" and closeBreaksAbove
                        isReversal := true
                        cdexText   := "CDLx"
                        cdexColor  := CDLongColor
                        cdexY      := currentLiveBox.high
                        CDStyle    := label.style_label_up
                    if isReversal and showCDLabels
                        middleTime = int(currentLiveBox.startTime + (htf_time - currentLiveBox.startTime) / 2)
                        CDLabel := label.new(x=f_future_time(offsetGap), y=cdexY, text=cdexText, style=CDStyle, size=getSizeFromString(CDLabelSize), color=color.new(color.white, 100), textcolor=cdexColor, xloc=xloc.bar_time)
                        if cdexText == "CDSx"
                            dotLabel = label.new(x=f_future_time(offsetGap), y=currentLiveBox.high, text="•", style=label.style_none, size=size.tiny, color=color.new(CDLongColor, 0), textcolor=CDLongColor, xloc=xloc.bar_time)
                            array.push(cdexDots, CDExDot.new(currentLiveBox.high, currentLiveBox.startBar, int(htf_time), "CDSx", dotLabel))
                        else if cdexText == "CDLx"
                            dotLabel = label.new(x=f_future_time(offsetGap), y=currentLiveBox.low, text="•", style=label.style_none, size=size.tiny, color=color.new(CDShortColor, 0), textcolor=CDShortColor, xloc=xloc.bar_time)
                            array.push(cdexDots, CDExDot.new(currentLiveBox.low, currentLiveBox.startBar, int(htf_time), "CDLx", dotLabel))
                        if isReversal
                            if cdexText == "CDLx"'''
i0 = src.find(old_flip_start)
assert i0 >= 0, "flip start"
end_marker = '''                                    marketDirection := "SHORT"
                currentLiveBox.CDLabel    := CDLabel
                currentLiveBox.hasCDLabel := isReversal
'''
i1 = src.find(end_marker, i0)
assert i1 > i0, "flip end"
new_flip = '''                CDLabel      = label(na)
                // FLIP: the box is closed through AGAINST the trend. A Demand box
                // broken up while the trend is already CDLx is NOT a new CDLx
                // (no "CDL after CDL") — the continuation rule handles it.
                bool   isReversal = false
                bool   revPass    = true
                string cdexText   = ""
                color  cdexColor  = color(na)
                float  cdexY      = 0.0
                if currentLiveBox.boxType == "Supply" and closeBreaksBelow and currentBias != "CDSx"
                    isReversal := true
                    cdexText   := "CDSx"
                    cdexColor  := CDShortColor
                    cdexY      := currentLiveBox.low
                else if currentLiveBox.boxType == "Demand" and closeBreaksAbove and currentBias != "CDLx"
                    isReversal := true
                    cdexText   := "CDLx"
                    cdexColor  := CDLongColor
                    cdexY      := currentLiveBox.high
                if isReversal
                    revPass     := not gateOn or (cdexText == "CDLx" ? hitXD : hitXP)
                    flipThisBar := true
                    flipPass    := revPass
                    if showCDLabels and (revPass or show_failed)
                        string cdTip = cdexText + (revPass ? " (official)" : " (failed " + gate_mode + ")") + " | box " + str.tostring(currentLiveBox.low, format.mintick) + " - " + str.tostring(currentLiveBox.high, format.mintick)
                        CDLabel := label.new(x=f_future_time(offsetGap), y=cdexY, text=revPass ? cdexText : str.lower(cdexText), style=label.style_label_left, size=getSizeFromString(CDLabelSize), color=color.new(color.white, 100), textcolor=revPass ? cdexColor : FAIL_COL, xloc=xloc.bar_time, tooltip=cdTip)
                        if cdexText == "CDSx"
                            dotLabel = label.new(x=f_future_time(offsetGap), y=currentLiveBox.high, text="•", style=label.style_none, size=size.tiny, color=color.new(CDLongColor, 0), textcolor=CDLongColor, xloc=xloc.bar_time)
                            array.push(cdexDots, CDExDot.new(currentLiveBox.high, currentLiveBox.startBar, int(htf_time), "CDSx", dotLabel))
                        else
                            dotLabel = label.new(x=f_future_time(offsetGap), y=currentLiveBox.low, text="•", style=label.style_none, size=size.tiny, color=color.new(CDShortColor, 0), textcolor=CDShortColor, xloc=xloc.bar_time)
                            array.push(cdexDots, CDExDot.new(currentLiveBox.low, currentLiveBox.startBar, int(htf_time), "CDLx", dotLabel))
                    hitXD   := false
                    hitXP   := false
                    bullImp := false
                    bullPb  := false
                    bearImp := false
                    bearPb  := false
                    if cdexText == "CDLx"
                        lastSignalType  := revPass ? "CDLx" : "cdlx"
                        lastSignalPrice := currentLiveBox.high
                        lastWasReversal := true
                        lastRevBoxHigh  := currentLiveBox.high
                        lastRevBoxLow   := currentLiveBox.low
                        currentBias     := "CDLx"
                        ldCount := 0
                        sdCount := 0
                        ev_cdl  := revPass
                        if array.size(ldsdLabels) > 0
                            i = array.size(ldsdLabels) - 1
                            while i >= 0
                                if array.size(ldsdLabels) > i
                                    ldsdItem = array.get(ldsdLabels, i)
                                    if ldsdItem.labelType == "SDx"
                                        label.delete(ldsdItem.theLabel)
                                        array.remove(ldsdLabels, i)
                                i -= 1
                        closeOppositeTrades(true)
                        if enableCandleCDL and revPass
                            float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                            float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxLow)) ? lastRevBoxLow : htf_low
                            slP = slBase - (slTicksCandle * syminfo.mintick)
                            riskP = math.abs(e - slP)
                            tpP = e + (riskP * rrRatio)
                            newTrade = createTrade(true, e, slP, tpP, "PO4 CDLx", "CandleCDL", currentLiveBox.high, currentLiveBox.low, int(htf_time))
                            if addTradeToCategory(newTrade, "CandleCDL")
                                lastAction := "PO4 CDLx entry created"
                                if enableAlerts
                                    alert(lastAction, alert.freq_all)
                        marketDirection := "LONG"
                    else
                        lastSignalType  := revPass ? "CDSx" : "cdsx"
                        lastSignalPrice := currentLiveBox.low
                        lastWasReversal := true
                        lastRevBoxHigh  := currentLiveBox.high
                        lastRevBoxLow   := currentLiveBox.low
                        currentBias     := "CDSx"
                        sdCount := 0
                        ldCount := 0
                        ev_cds  := revPass
                        if array.size(ldsdLabels) > 0
                            i = array.size(ldsdLabels) - 1
                            while i >= 0
                                if array.size(ldsdLabels) > i
                                    ldsdItem = array.get(ldsdLabels, i)
                                    if ldsdItem.labelType == "LDx"
                                        label.delete(ldsdItem.theLabel)
                                        array.remove(ldsdLabels, i)
                                i -= 1
                        closeOppositeTrades(false)
                        if enableCandleCDL and revPass
                            // SHORT: stop above the block high / candle high, target below.
                            float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                            float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxHigh)) ? lastRevBoxHigh : htf_high
                            slP = slBase + (slTicksCandle * syminfo.mintick)
                            riskP = math.abs(e - slP)
                            tpP = e - (riskP * rrRatio)
                            newTrade = createTrade(false, e, slP, tpP, "PO4 CDSx", "CandleCDL", currentLiveBox.high, currentLiveBox.low, int(htf_time))
                            if addTradeToCategory(newTrade, "CandleCDL")
                                lastAction := "PO4 CDSx entry created"
                                if enableAlerts
                                    alert(lastAction, alert.freq_all)
                        marketDirection := "SHORT"
                // A continuation box (broken WITH the trend) is official only when
                // the trend agrees and the continuation gate is open.
                bool contBoxOk = closeBreaksAbove ? (currentBias == "CDLx" and (not gateOn or (bullImp and bullPb))) : (currentBias == "CDSx" and (not gateOn or (bearImp and bearPb)))
                currentLiveBox.isRev      := isReversal
                currentLiveBox.official   := isReversal ? revPass : contBoxOk
                currentLiveBox.breakoutDirection := closeBreaksAbove ? "up" : "down"
                currentLiveBox.CDLabel    := CDLabel
                currentLiveBox.hasCDLabel := isReversal and (revPass or show_failed)
'''
src = src[:i0] + new_flip + src[i1 + len(end_marker):]
n_edits += 1

# ---------------------------------------------------------------- LD / SD detection (always on, close-based, gate, numbered, middle right)
old_ld_start = '''    // LD/SD DETECTION
    if (enableBlockLD or enableCandleLD) and lastWasReversal and barstate.isconfirmed and newHTFBlockCandle and in_calc_range'''
i0 = src.find(old_ld_start)
assert i0 >= 0
old_ld_end = '''                lastRevBoxLow := htf_low

    // CDLx+/CDSx+ CREATION'''
i1 = src.find(old_ld_end, i0)
assert i1 > i0
new_ld = '''    // LD/SD DETECTION — runs whatever entries are switched on (the count and
    // labels are structure, not an entry setting). A continuation needs a BODY
    // CLOSE beyond the last level (a wick through it is only a sweep), and it is
    // never counted on the flip candle itself.
    if lastWasReversal and not flipThisBar and barstate.isconfirmed and newHTFBlockCandle and in_calc_range
        if currentBias == "CDLx" and htf_isBullishBodyClose and not na(lastRevBoxHigh)
            if htf_close > lastRevBoxHigh
                ldCount += 1
                contThisBar := true
                contPass    := not gateOn or (bullImp and bullPb)
                bullImp     := false
                bullPb      := false
                ev_ld       := contPass
                ldLabel  = "LDx" + str.tostring(ldCount)
                tfString = f_timeframeToString(blockTF)
                label sharedLDLabel = na
                if (showCDLabels or showOnlyCDLxCDSx) and showLDSDLabels and (contPass or show_failed)
                    ldLabelText = showTimeframeLabel ? getBlockLabelText(true, tfString, blockLabelFormat, ldLabel) : getBlockLabelText(true, "", blockLabelFormat, ldLabel)
                    sharedLDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxHigh, text=contPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_left, size=getSizeFromString(blockLabelSize), color=color.new(color.white, 100), textcolor=contPass ? CDLongColor : FAIL_COL, xloc=xloc.bar_time, tooltip=ldLabel + (contPass ? " (official)" : " (failed " + gate_mode + ")"))
                    array.push(ldsdLabels, LDSDLabel.new(sharedLDLabel, "LDx", ldCount, int(htf_time)))
                if enableCandleLD and contPass
                    float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxLow)) ? lastRevBoxLow : htf_low
                    slP = slBase - (slTicksCandle * syminfo.mintick)
                    riskP = math.abs(e - slP)
                    tpP = e + (riskP * rrRatio)
                    newTrade = createTrade(true, e, slP, tpP, "PO4 " + ldLabel, "CandleLD", htf_high, htf_low, int(htf_time))
                    newTrade.ldsdLabel := sharedLDLabel
                    newTrade.fromCDLPlus := false
                    if addTradeToCategory(newTrade, "CandleLD")
                        lastAction := "PO4 " + ldLabel + " entry created"
                        if enableAlerts
                            alert(lastAction, alert.freq_all)
                lastSignalType := contPass ? ldLabel : str.lower(ldLabel)
                lastRevBoxHigh := htf_high
        else if currentBias == "CDSx" and htf_isBearishBodyClose and not na(lastRevBoxLow)
            if htf_close < lastRevBoxLow
                sdCount += 1
                contThisBar := true
                contPass    := not gateOn or (bearImp and bearPb)
                bearImp     := false
                bearPb      := false
                ev_sd       := contPass
                sdLabel  = "SDx" + str.tostring(sdCount)
                tfString = f_timeframeToString(blockTF)
                label sharedSDLabel = na
                if (showCDLabels or showOnlyCDLxCDSx) and showLDSDLabels and (contPass or show_failed)
                    sdLabelText = showTimeframeLabel ? getBlockLabelText(false, tfString, blockLabelFormat, sdLabel) : getBlockLabelText(false, "", blockLabelFormat, sdLabel)
                    sharedSDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxLow, text=contPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_left, size=getSizeFromString(blockLabelSize), color=color.new(color.white, 100), textcolor=contPass ? CDShortColor : FAIL_COL, xloc=xloc.bar_time, tooltip=sdLabel + (contPass ? " (official)" : " (failed " + gate_mode + ")"))
                    array.push(ldsdLabels, LDSDLabel.new(sharedSDLabel, "SDx", sdCount, int(htf_time)))
                if enableCandleLD and contPass
                    float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxHigh)) ? lastRevBoxHigh : htf_high
                    slP = slBase + (slTicksCandle * syminfo.mintick)
                    riskP = math.abs(e - slP)
                    tpP = e - (riskP * rrRatio)
                    newTrade = createTrade(false, e, slP, tpP, "PO4 " + sdLabel, "CandleLD", htf_high, htf_low, int(htf_time))
                    newTrade.ldsdLabel := sharedSDLabel
                    newTrade.fromCDLPlus := false
                    if addTradeToCategory(newTrade, "CandleLD")
                        lastAction := "PO4 " + sdLabel + " entry created"
                        if enableAlerts
                            alert(lastAction, alert.freq_all)
                lastSignalType := contPass ? sdLabel : str.lower(sdLabel)
                lastRevBoxLow := htf_low
        while array.size(ldsdLabels) > 50
            LDSDLabel oldL = array.shift(ldsdLabels)
            label.delete(oldL.theLabel)

    // CDLx+/CDSx+ CREATION'''
src = src[:i0] + new_ld + src[i1 + len(old_ld_end):]
n_edits += 1

# ---------------------------------------------------------------- CDLx+ / CDSx+ (flip / continuation, gated, never double counted)
old_cp_start = '''            if prevWasBearishBC and currentIsBullBC
                if shouldShowCDLPlus and showCDLxPlus'''
i0 = src.find(old_cp_start)
assert i0 >= 0
old_cp_end = '''        prevWasBullishBC := currentIsBullBC
        prevWasBearishBC := currentIsBearBC
'''
i1 = src.find(old_cp_end, i0)
assert i1 > i0
new_cp = '''            // BuBC right after a BeBC. Three cases:
            //  - a box CDLx already fired on this candle -> same event, no recount
            //  - trend not bull yet                        -> CDLx+ FLIP
            //  - trend already bull                        -> LDx#+ CONTINUATION
            //    (unless an LDx was already counted on this candle)
            if prevWasBearishBC and currentIsBullBC
                bool   isReversalCDLPlus = false
                string cdlPlusLabel = ""
                bool   plusPass = true
                if flipThisBar
                    plusPass := flipPass
                else if currentBias != "CDLx"
                    isReversalCDLPlus := true
                    plusPass := not gateOn or hitXD
                    flipThisBar := true
                    flipPass    := plusPass
                    ev_cdl      := plusPass
                    lastSignalType := plusPass ? "CDLx+" : "cdlx+"
                    currentBias    := "CDLx"
                    ldCount        := 0
                    sdCount        := 0
                    lastRevBoxHigh := htf_high
                    lastRevBoxLow  := htf_prev_low
                    lastWasReversal := true
                    hitXD   := false
                    hitXP   := false
                    bullImp := false
                    bullPb  := false
                    bearImp := false
                    bearPb  := false
                    if array.size(ldsdLabels) > 0
                        i = array.size(ldsdLabels) - 1
                        while i >= 0
                            if array.size(ldsdLabels) > i
                                ldsdItem = array.get(ldsdLabels, i)
                                if ldsdItem.labelType == "SDx"
                                    label.delete(ldsdItem.theLabel)
                                    array.remove(ldsdLabels, i)
                            i -= 1
                    closeOppositeTrades(true)
                else if contThisBar
                    plusPass := contPass
                else
                    ldCount  += 1
                    contThisBar := true
                    plusPass := not gateOn or (bullImp and bullPb)
                    contPass := plusPass
                    bullImp  := false
                    bullPb   := false
                    ev_ld    := plusPass
                    cdlPlusLabel := "LDx" + str.tostring(ldCount) + "+"
                    lastSignalType := plusPass ? cdlPlusLabel : str.lower(cdlPlusLabel)
                    label sharedLDLabel = na
                    if shouldShowCDLPlus and (showCDLabels or showOnlyCDLxCDSx) and showLDSDLabels and (plusPass or show_failed)
                        ldLabelText = showTimeframeLabel ? getBlockLabelText(true, tfString, blockLabelFormat, cdlPlusLabel) : getBlockLabelText(true, "", blockLabelFormat, cdlPlusLabel)
                        sharedLDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxHigh, text=plusPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_left, size=getSizeFromString(blockLabelSize), color=color.new(color.white, 100), textcolor=plusPass ? CDLongColor : FAIL_COL, xloc=xloc.bar_time)
                        array.push(ldsdLabels, LDSDLabel.new(sharedLDLabel, "LDx", ldCount, int(htf_time)))
                    if enableCandleLD and plusPass
                        float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                        float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxLow)) ? lastRevBoxLow : htf_low
                        slP = slBase - (slTicksCandle * syminfo.mintick)
                        riskP = math.abs(e - slP)
                        tpP = e + (riskP * rrRatio)
                        newTrade = createTrade(true, e, slP, tpP, "PO4 " + cdlPlusLabel, "CandleLD", htf_high, htf_prev_low, int(htf_time))
                        newTrade.ldsdLabel := sharedLDLabel
                        newTrade.fromCDLPlus := true
                        if addTradeToCategory(newTrade, "CandleLD")
                            lastAction := "PO4 " + cdlPlusLabel + " entry created (CDLx+)"
                            if enableAlerts
                                alert(lastAction, alert.freq_all)
                lastRevBoxHigh := htf_high
                if shouldShowCDLPlus and showCDLxPlus and (plusPass or show_failed)
                    blk = createCDLPlusBlock("CDLx+", bar_index, int(htf_prev_time), htf_high, htf_prev_low, htf_open, htf_close, tfString, plusPass)
                    array.push(cdlPlusBlocks, blk)
                if enableCandleCDLPlus and plusPass
                    lastSignalPrice := htf_high
                    float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? htf_prev_low : htf_low
                    slP = slBase - (slTicksCandle * syminfo.mintick)
                    riskP = math.abs(e - slP)
                    tpP = e + (riskP * rrRatio)
                    newTrade = createTrade(true, e, slP, tpP, "CDLx+", "CandleCDLPlus", htf_high, htf_prev_low, int(htf_time))
                    newTrade.fromCDLPlus := true
                    if addTradeToCategory(newTrade, "CandleCDLPlus")
                        marketDirection := "LONG"
                        lastAction := "CDLx+ entry created" + (isReversalCDLPlus ? " (Reversal)" : " (Continuation)")
                        if enableAlerts
                            alert(lastAction, alert.freq_all)

            if prevWasBullishBC and currentIsBearBC
                bool   isReversalCDLPlus = false
                string cdlPlusLabel = ""
                bool   plusPass = true
                if flipThisBar
                    plusPass := flipPass
                else if currentBias != "CDSx"
                    isReversalCDLPlus := true
                    plusPass := not gateOn or hitXP
                    flipThisBar := true
                    flipPass    := plusPass
                    ev_cds      := plusPass
                    lastSignalType := plusPass ? "CDSx+" : "cdsx+"
                    currentBias    := "CDSx"
                    ldCount        := 0
                    sdCount        := 0
                    lastRevBoxHigh := htf_prev_high
                    lastRevBoxLow  := htf_low
                    lastWasReversal := true
                    hitXD   := false
                    hitXP   := false
                    bullImp := false
                    bullPb  := false
                    bearImp := false
                    bearPb  := false
                    if array.size(ldsdLabels) > 0
                        i = array.size(ldsdLabels) - 1
                        while i >= 0
                            if array.size(ldsdLabels) > i
                                ldsdItem = array.get(ldsdLabels, i)
                                if ldsdItem.labelType == "LDx"
                                    label.delete(ldsdItem.theLabel)
                                    array.remove(ldsdLabels, i)
                            i -= 1
                    closeOppositeTrades(false)
                else if contThisBar
                    plusPass := contPass
                else
                    sdCount  += 1
                    contThisBar := true
                    plusPass := not gateOn or (bearImp and bearPb)
                    contPass := plusPass
                    bearImp  := false
                    bearPb   := false
                    ev_sd    := plusPass
                    cdlPlusLabel := "SDx" + str.tostring(sdCount) + "+"
                    lastSignalType := plusPass ? cdlPlusLabel : str.lower(cdlPlusLabel)
                    label sharedSDLabel = na
                    if shouldShowCDLPlus and (showCDLabels or showOnlyCDLxCDSx) and showLDSDLabels and (plusPass or show_failed)
                        sdLabelText = showTimeframeLabel ? getBlockLabelText(false, tfString, blockLabelFormat, cdlPlusLabel) : getBlockLabelText(false, "", blockLabelFormat, cdlPlusLabel)
                        sharedSDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxLow, text=plusPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_left, size=getSizeFromString(blockLabelSize), color=color.new(color.white, 100), textcolor=plusPass ? CDShortColor : FAIL_COL, xloc=xloc.bar_time)
                        array.push(ldsdLabels, LDSDLabel.new(sharedSDLabel, "SDx", sdCount, int(htf_time)))
                    if enableCandleLD and plusPass
                        float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                        float slBase = (masterSLMode == "Block Extremes (HH/LL)" and not na(lastRevBoxHigh)) ? lastRevBoxHigh : htf_high
                        slP = slBase + (slTicksCandle * syminfo.mintick)
                        riskP = math.abs(e - slP)
                        tpP = e - (riskP * rrRatio)
                        newTrade = createTrade(false, e, slP, tpP, "PO4 " + cdlPlusLabel, "CandleLD", htf_prev_high, htf_low, int(htf_time))
                        newTrade.ldsdLabel := sharedSDLabel
                        newTrade.fromCDLPlus := true
                        if addTradeToCategory(newTrade, "CandleLD")
                            lastAction := "PO4 " + cdlPlusLabel + " entry created (CDSx+)"
                            if enableAlerts
                                alert(lastAction, alert.freq_all)
                lastRevBoxLow := htf_low
                if shouldShowCDLPlus and showCDSxPlus and (plusPass or show_failed)
                    blk = createCDLPlusBlock("CDSx+", bar_index, int(htf_prev_time), htf_prev_high, htf_low, htf_open, htf_close, tfString, plusPass)
                    array.push(cdlPlusBlocks, blk)
                if enableCandleCDLPlus and plusPass
                    lastSignalPrice := htf_low
                    float e = calculateCandleEntry(htf_high, htf_low, htf_open, htf_close)
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? htf_prev_high : htf_high
                    slP = slBase + (slTicksCandle * syminfo.mintick)
                    riskP = math.abs(e - slP)
                    tpP = e - (riskP * rrRatio)
                    newTrade = createTrade(false, e, slP, tpP, "CDSx+", "CandleCDLPlus", htf_prev_high, htf_low, int(htf_time))
                    newTrade.fromCDLPlus := true
                    if addTradeToCategory(newTrade, "CandleCDLPlus")
                        marketDirection := "SHORT"
                        lastAction := "CDSx+ entry created" + (isReversalCDLPlus ? " (Reversal)" : " (Continuation)")
                        if enableAlerts
                            alert(lastAction, alert.freq_all)

        prevWasBullishBC := currentIsBullBC
        prevWasBearishBC := currentIsBearBC
'''
src = src[:i0] + new_cp + src[i1 + len(old_cp_end):]
n_edits += 1

# ---------------------------------------------------------------- block limit entries: official + flip flag
rep('''                isReversal    = box_item.hasCDLabel
                shouldCreate  = isReversal ? enableBlockCDL : enableBlockLD
                entryCategory = isReversal ? "BlockCDL" : "BlockLD"

                if shouldCreate
                    float e = zonePrice
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? box_item.low : low''', '''                isReversal    = box_item.isRev
                shouldCreate  = (isReversal ? enableBlockCDL : enableBlockLD) and box_item.official
                entryCategory = isReversal ? "BlockCDL" : "BlockLD"

                if shouldCreate
                    float e = zonePrice
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? box_item.low : low''')
rep('''                isReversal    = box_item.hasCDLabel
                shouldCreate  = isReversal ? enableBlockCDL : enableBlockLD
                entryCategory = isReversal ? "BlockCDL" : "BlockLD"

                if shouldCreate
                    float e = zonePrice
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? box_item.high : high''', '''                isReversal    = box_item.isRev
                shouldCreate  = (isReversal ? enableBlockCDL : enableBlockLD) and box_item.official
                entryCategory = isReversal ? "BlockCDL" : "BlockLD"

                if shouldCreate
                    float e = zonePrice
                    float slBase = (masterSLMode == "Block Extremes (HH/LL)") ? box_item.high : high''')
rep('''        blk = array.get(cdlPlusBlocks, i)
        if not blk.zoneTouched
            isLongBox = blk.type == "CDLx+"''', '''        blk = array.get(cdlPlusBlocks, i)
        if not blk.zoneTouched and blk.official
            isLongBox = blk.type == "CDLx+"''')

# ---------------------------------------------------------------- sweeps: middle right, close-based on the sweep candle
rep('''        deleteSweepLine(lastBearishSweep)
        ln  = line.new(x1=swHTime, y1=swH, x2=time, y2=swH, color=sweepLineColor, width=sweepLineWidth, xloc=xloc.bar_time)
        midTime = int(swHTime + (time - swHTime) / 2)
        lbl = label.new(x=midTime, y=swH, text=lblTxt, style=label.style_label_down, color=color.new(color.white, 100), textcolor=sweepLineColor, size=getSizeFromString(sweepLabelSize), xloc=xloc.bar_time)
        lastBearishSweep := SweepLine.new(ln, lbl, swH, swHTime, time, lblTxt, false)''', '''        deleteSweepLine(lastBearishSweep)
        ln  = line.new(x1=swHTime, y1=swH, x2=time, y2=swH, color=sweepLineColor, width=sweepLineWidth, xloc=xloc.bar_time)
        lbl = label.new(x=time, y=swH, text=lblTxt, style=label.style_label_left, color=color.new(color.white, 100), textcolor=sweepLineColor, size=getSizeFromString(sweepLabelSize), xloc=xloc.bar_time, tooltip="Buy-side sweep. Deleted when a candle CLOSES above this sweep candle high.")
        lastBearishSweep := SweepLine.new(ln, lbl, swH, swHTime, time, lblTxt, false, high)''')
rep('''        deleteSweepLine(lastBullishSweep)
        ln  = line.new(x1=swLTime, y1=swL, x2=time, y2=swL, color=sweepLineColor, width=sweepLineWidth, xloc=xloc.bar_time)
        midTime = int(swLTime + (time - swLTime) / 2)
        lbl = label.new(x=midTime, y=swL, text=lblTxt, style=label.style_label_up, color=color.new(color.white, 100), textcolor=sweepLineColor, size=getSizeFromString(sweepLabelSize), xloc=xloc.bar_time)
        lastBullishSweep := SweepLine.new(ln, lbl, swL, swLTime, time, lblTxt, true)''', '''        deleteSweepLine(lastBullishSweep)
        ln  = line.new(x1=swLTime, y1=swL, x2=time, y2=swL, color=sweepLineColor, width=sweepLineWidth, xloc=xloc.bar_time)
        lbl = label.new(x=time, y=swL, text=lblTxt, style=label.style_label_left, color=color.new(color.white, 100), textcolor=sweepLineColor, size=getSizeFromString(sweepLabelSize), xloc=xloc.bar_time, tooltip="Sell-side sweep. Deleted when a candle CLOSES below this sweep candle low.")
        lastBullishSweep := SweepLine.new(ln, lbl, swL, swLTime, time, lblTxt, true, low)''')
rep('''if not na(lastBearishSweep) and close > lastBearishSweep.price
    deleteSweepLine(lastBearishSweep)
    lastBearishSweep := na

if not na(lastBullishSweep) and close < lastBullishSweep.price
    deleteSweepLine(lastBullishSweep)
    lastBullishSweep := na
''', '''// A sweep dies when a candle CLOSES beyond the sweep candle itself.
if barstate.isconfirmed and not na(lastBearishSweep) and time > lastBearishSweep.endTime and close > lastBearishSweep.candleExt
    deleteSweepLine(lastBearishSweep)
    lastBearishSweep := na

if barstate.isconfirmed and not na(lastBullishSweep) and time > lastBullishSweep.endTime and close < lastBullishSweep.candleExt
    deleteSweepLine(lastBullishSweep)
    lastBullishSweep := na
''')

# ---------------------------------------------------------------- news cancels unfilled trades
rep('''                    if not t.activated and (bar_index - t.creationBar) > 500
                        t.forceExit := true
                        t.forceExitReason := "Expired"
''', '''                    if not t.activated and (bar_index - t.creationBar) > 500
                        t.forceExit := true
                        t.forceExitReason := "Expired"

                    if not t.activated and not t.forceExit and newsBlock
                        t.forceExit := true
                        t.forceExitReason := "News Window"
''')

# ---------------------------------------------------------------- CDLx+ block: close-based deletion
rep('''        shouldDelete = blk.creationBar != bar_index and ((blk.type == "CDLx+" and low <= blk.price) or (blk.type == "CDSx+" and high >= blk.price))''', '''        shouldDelete = barstate.isconfirmed and blk.creationBar != bar_index and ((blk.type == "CDLx+" and close < blk.price) or (blk.type == "CDSx+" and close > blk.price))''')

# ---------------------------------------------------------------- box routing by the real break direction
rep('''            neutralBox = array.get(neutralBoxes, i)
            if high > neutralBox.high
                if showOnlyCDLxCDSx and not neutralBox.hasCDLabel''', '''            neutralBox = array.get(neutralBoxes, i)
            // Every box in this list is already broken by a CLOSE. Route it by
            // the direction it actually broke, never by whichever wick came first.
            if neutralBox.breakoutDirection == "up"
                if showOnlyCDLxCDSx and not neutralBox.hasCDLabel''')
rep('''                array.remove(neutralBoxes, i)
            else if low < neutralBox.low
                if showOnlyCDLxCDSx and not neutralBox.hasCDLabel''', '''                array.remove(neutralBoxes, i)
            else if neutralBox.breakoutDirection == "down"
                if showOnlyCDLxCDSx and not neutralBox.hasCDLabel''')
# box invalidation: close back through the far edge
rep('''                if neutralBox.low >= low
                    if not na(neutralBox.highLine)''', '''                if barstate.isconfirmed and close < neutralBox.low
                    if not na(neutralBox.highLine)''')
rep('''                if neutralBox.high < high
                    if not na(neutralBox.highLine)''', '''                if barstate.isconfirmed and close > neutralBox.high
                    if not na(neutralBox.highLine)''')
# CDEx dots: close-based
rep('''            if (dot.dotType == "CDSx" and high > dot.price) or (dot.dotType == "CDLx" and low < dot.price)''', '''            if barstate.isconfirmed and ((dot.dotType == "CDSx" and close > dot.price) or (dot.dotType == "CDLx" and close < dot.price))''')

# ---------------------------------------------------------------- bias row + gate in the signals table
rep('''        biasText  = currentBias == "CDLx" ? "Bias: CDLx → LDx" + str.tostring(ldCount) : "Bias: CDSx → SDx" + str.tostring(sdCount)''', '''        biasText  = (currentBias == "CDLx" ? "Bias: CDLx → LDx" + str.tostring(ldCount) : "Bias: CDSx → SDx" + str.tostring(sdCount)) + " | Gate: " + gate_mode + " | Box: " + (boxGrow ? "G1" : "G0")''')

# ---------------------------------------------------------------- tail: next level, HTF box, alerts
rep('''// Execute final unified A&B overlap drawing checks on the last bar
if barstate.islast
    f_draw_groups()''', '''// =====================================================
// NEXT LDx / SDx LEVEL — the level whose body close makes the next continuation
// =====================================================
var float prevRevH = na
var float prevRevL = na
var int   revHT    = na
var int   revLT    = na
if barstate.isconfirmed
    if not na(lastRevBoxHigh) and (na(prevRevH) or lastRevBoxHigh != prevRevH)
        prevRevH := lastRevBoxHigh
        revHT    := int(nz(htf_time, time))
    if not na(lastRevBoxLow) and (na(prevRevL) or lastRevBoxLow != prevRevL)
        prevRevL := lastRevBoxLow
        revLT    := int(nz(htf_time, time))

var line  nextLn  = na
var label nextLbl = na
if barstate.islast
    line.delete(nextLn)
    label.delete(nextLbl)
    if showNextLvl and (currentBias == "CDLx" or currentBias == "CDSx")
        bool   nUp  = currentBias == "CDLx"
        float  nP   = nUp ? lastRevBoxHigh : lastRevBoxLow
        int    nT   = nUp ? revHT : revLT
        string nTx  = "▸ " + (nUp ? "LDx" + str.tostring(ldCount + 1) : "SDx" + str.tostring(sdCount + 1))
        color  nCol = color.new(nUp ? CDLongColor : CDShortColor, 30)
        if not na(nP) and not na(nT)
            int nEnd = f_future_time(offsetGap)
            nextLn  := line.new(nT, nP, nEnd, nP, xloc=xloc.bar_time, color=nCol, style=line.style_dotted, width=1)
            nextLbl := label.new(nEnd, nP, nTx, xloc=xloc.bar_time, style=label.style_label_left, color=color(na), textcolor=nCol, size=size.small, tooltip="A body close " + (nUp ? "above" : "below") + " this level = " + str.substring(nTx, 2))

// =====================================================
// HTF BIAS BOX
// =====================================================
f_htfPos(string p) =>
    switch p
        "Top Left"      => position.top_left
        "Top Center"    => position.top_center
        "Top Right"     => position.top_right
        "Bottom Left"   => position.bottom_left
        "Bottom Right"  => position.bottom_right
        => position.bottom_center

var table biasTbl = table.new(f_htfPos(htf_tbl_pos), 1, 1, bgcolor=#000000, border_width=1, frame_color=color.new(color.white, 70), frame_width=1)
if barstate.islast
    if htf_table and htf_mode != "Off"
        string bSrc = htf_mode == "Last Flip (CDLx/CDSx)" ? "Flip" : htf_mode == "Last Continuation (LDx/SDx)" ? "Cont" : "BC"
        string bDir = htfBias == 1 ? "BULL" : htfBias == -1 ? "BEAR" : "NONE"
        color  bCol = htfBias == 1 ? bullishBodyCloseColor : htfBias == -1 ? bearishBodyCloseColor : color.silver
        table.cell(biasTbl, 0, 0, "HTF " + f_timeframeToString(htf_bias_tf) + " · " + bSrc + " · " + bDir + (newsBlock ? " · NEWS" : ""), text_color=bCol, text_size=size.small)
    else
        table.clear(biasTbl, 0, 0)

alertcondition(ev_cdl, "CDLx Flip (official)", "CDLx - bullish flip (zone engine)")
alertcondition(ev_cds, "CDSx Flip (official)", "CDSx - bearish flip (zone engine)")
alertcondition(ev_ld, "LDx Continuation (official)", "LDx - bullish continuation (zone engine)")
alertcondition(ev_sd, "SDx Continuation (official)", "SDx - bearish continuation (zone engine)")

// Execute final unified A&B overlap drawing checks on the last bar
if barstate.islast
    f_draw_groups()''')

open('MMM_Concepts_Pro_Plus_3.5.pine', 'w').write(src)
print("ok edits", n_edits, "lines", src.count('\n'))

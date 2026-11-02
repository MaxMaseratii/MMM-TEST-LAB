import sys
sys.path.insert(0, '/home/claude/v35')
from news_module import NEWS_INPUTS, NEWS_ENGINE
src = open('/home/claude/v35/pro_orig.pine').read()

def rep(old, new, count=1):
    global src
    c = src.count(old)
    if c != count:
        print("FAIL count=%d for:\n%s" % (c, old[:400])); sys.exit(1)
    src = src.replace(old, new)

# ---------------------------------------------------------------- header note
rep('''// STATE MACHINE (transplanted verbatim in behaviour):''', '''// MMM FOUNDATION — this is the CANDLE engine "c":
//   Flip         = CDLc / CDSc (the T1 reversal)
//   Continuation = LDc1, LDc2… / SDc1, SDc2… (count runs until the next flip)
//   Gate (NO GATE / MMPD 27 / MMPD fast / MMPD Delta) decides which breaks
//   are OFFICIAL. Only official breaks arm with-trend entries and alerts.
//
// STATE MACHINE (transplanted verbatim in behaviour):''')

# ---------------------------------------------------------------- inputs
rep('''max_history      = input.int(40, "Memory Guard (Max Structures Kept)"''', '''eng_tag          = input.bool(true, "Engine Tag  (CDLc / CDSc / LDc / SDc)", group=grp_gen, tooltip="Adds the engine letter to every break so you always know which MMM engine made it.\\nc = Candle engine (MMM Pro) · x = Zone engine (Concepts Pro+) · s = Swing engine (Order Flow Suite).")
max_history      = input.int(40, "Memory Guard (Max Structures Kept)"''')

rep('''hvc_max_bars     = input.int(300, "Max Footprint Bars", minval=50, maxval=1000, group=grp_ccm)
''', '''hvc_max_bars     = input.int(300, "Max Footprint Bars", minval=50, maxval=1000, group=grp_ccm)

// ─── 9. GATE & HTF BIAS ───
grp_gate         = "9. Gate & HTF Bias"
gate_mode        = input.string("NO GATE", "Gate", options=["NO GATE", "MMPD 27", "MMPD fast", "MMPD Delta"], group=grp_gate, tooltip="NO GATE = every break is official (normal break, no filter).\\n\\nMMPD 27 / MMPD fast / MMPD Delta = the MMM Pro Edge rhythm:\\n• Flip (CDLc / CDSc) is official only if the old leg reached its extreme first: oscillator ≤ 20 before a CDLc, ≥ 80 before a CDSc.\\n• Continuation (LDc / SDc) is official only if the leg reached its OWN extreme (bull ≥ 80) and THEN the pullback reached the OPPOSITE extreme (≤ 20) before the break.\\n\\nMMPD Delta = the natural order-flow version (built on candle delta).\\nThe structure never changes with the gate. A failed break keeps its PO4 (marked ✗) but gets no with-trend entry, no block, no alert.")
gate_fast        = input.int(9, "MMPD fast Length", minval=5, maxval=50, group=grp_gate)
show_failed      = input.bool(false, "Show Failed Breaks (small grey)", group=grp_gate, tooltip="OFF = the cause label of a failed break is hidden.\\nON = it is drawn in grey, lowercase (cdlc, ldc2...).")
htf_mode         = input.string("Off", "HTF Bias From", options=["Off", "Last Flip (CDLc/CDSc)", "Last Continuation (LDc/SDc)", "Last BC"], group=grp_gate, tooltip="A compact copy of the PO4 engine (T# / P# / R#) runs on the HTF — last CLOSED HTF candle only, no repaint.\\n\\nLast Flip = direction of the last HTF CDLc / CDSc (the trend).\\nLast Continuation = direction of the last HTF LDc / SDc made AFTER the last flip. No continuation yet = no bias.\\nLast BC = direction of the last HTF body close candle.\\n\\nOff = no HTF filter.")
htf_tf           = input.timeframe("240", "HTF Timeframe", group=grp_gate)
htf_filter       = input.bool(true, "Entries With HTF Bias Only", group=grp_gate)
htf_table        = input.bool(true, "Show HTF Bias Box", inline="hb", group=grp_gate)
htf_tbl_pos      = input.string("Top Right", "", options=["Top Left","Top Center","Top Right","Bottom Left","Bottom Center","Bottom Right"], inline="hb", group=grp_gate)

// ─── 10. NEWS BLOCK ───
''' + NEWS_INPUTS.format(grp="10. News Block"))

# ---------------------------------------------------------------- POLine official flag
rep('''    bool   sbe_trig         = false
    int    sbe_freeze_t     = na

// ─── Standalone CDS/CDL not coupled to a Tn ───''', '''    bool   sbe_trig         = false
    int    sbe_freeze_t     = na
    bool   official         = true    // the break that made this Tn passed the gate

// ─── Standalone CDS/CDL not coupled to a Tn ───''')

# ---------------------------------------------------------------- globals: gate, HTF, news, entry filter
rep('''bool alert_sbe_bear = false
''', '''bool alert_sbe_bear = false
bool alert_cdl      = false
bool alert_cds      = false
bool alert_ld       = false
bool alert_sd       = false

// ═══════════════════════════════════════════════════════════════════════════
// GATE OSCILLATORS (same math as Super MMPD / MMM Pro Edge)
// ═══════════════════════════════════════════════════════════════════════════
const color FAIL_COL = #9e9e9e
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

[gHi, gLo] = f_gateNow()

// Gate memory (impulse -> pullback -> continuation)
var bool hitXD   = false   // oscillator <= 20 since the last flip
var bool hitXP   = false   // oscillator >= 80 since the last flip
var bool bullImp = false   // bull leg reached its own extreme (>= 80)
var bool bullPb  = false   // then the pullback reached <= 20
var bool bearImp = false
var bool bearPb  = false
var bool legOfficial = true   // the break that made the current Tn passed the gate

// ═══════════════════════════════════════════════════════════════════════════
// HTF BIAS — compact copy of the PO4 engine (T# / P# / R#) on the HTF.
// Last CLOSED HTF candle only ([1] + lookahead_on) = no repaint.
// ═══════════════════════════════════════════════════════════════════════════
f_htfPro() =>
    var int   side   = 0
    var float tn     = na
    var float pb     = na
    var float rs     = na
    var int   lastC  = 0
    var int   lastBC = 0
    bool bu   = close > high[1]
    bool be   = close < low[1]
    bool done = false
    if side == 1
        if close < tn
            side  := -1
            tn    := na(pb) ? open : pb
            pb    := na
            rs    := na
            lastC := 0
            done  := true
        else if not na(pb) and close > pb
            tn    := na(rs) ? open : rs
            pb    := na
            rs    := na
            lastC := 1
            done  := true
    else if side == -1
        if close > tn
            side  := 1
            tn    := na(pb) ? open : pb
            pb    := na
            rs    := na
            lastC := 0
            done  := true
        else if not na(pb) and close < pb
            tn    := na(rs) ? open : rs
            pb    := na
            rs    := na
            lastC := -1
            done  := true
    else
        if bu
            side := 1
            tn   := open
            done := true
        else if be
            side := -1
            tn   := open
            done := true
    if not done
        if side == 1
            if not na(rs) and close < rs
                rs := na
            if be and na(pb)
                pb := open
            else if bu and not na(pb) and na(rs)
                rs := open
        else if side == -1
            if not na(rs) and close > rs
                rs := na
            if bu and na(pb)
                pb := open
            else if be and not na(pb) and na(rs)
                rs := open
    if bu
        lastBC := 1
    if be
        lastBC := -1
    [nz(side[1]), nz(lastC[1]), nz(lastBC[1])]

[htfSig, htfCont, htfBC] = request.security(syminfo.tickerid, htf_tf, f_htfPro(), lookahead=barmerge.lookahead_on)
int  htfBias  = htf_mode == "Last Flip (CDLc/CDSc)" ? htfSig : htf_mode == "Last Continuation (LDc/SDc)" ? htfCont : htf_mode == "Last BC" ? htfBC : 0
bool htfLong  = htf_mode == "Off" or not htf_filter or htfBias == 1
bool htfShort = htf_mode == "Off" or not htf_filter or htfBias == -1

''' + NEWS_ENGINE + '''
// ENTRY FILTER — every entry line passes the same checks: no news window,
// HTF bias agrees, and (with a gate on) a WITH-TREND entry needs the current
// leg's break to be official. Counter-trend pullback entries skip the gate.
f_entOk(bool isLong) =>
    bool withTrend = (isLong and mainSide == 1) or (not isLong and mainSide == -1)
    not newsBlock and (isLong ? htfLong : htfShort) and (not gateOn or not withTrend or legOfficial)

// Engine letter on every break name (c = candle engine).
f_eng(string txt) =>
    string r = txt
    if eng_tag
        r := str.replace_all(r, "CDL", "CDLc")
        r := str.replace_all(r, "CDS", "CDSc")
        r := str.replace_all(r, "cdl", "cdlc")
        r := str.replace_all(r, "cds", "cdsc")
        r := str.replace_all(r, "LD", "LDc")
        r := str.replace_all(r, "SD", "SDc")
        r := str.replace_all(r, "ld", "ldc")
        r := str.replace_all(r, "sd", "sdc")
    r
''')

# ---------------------------------------------------------------- entry arming passes the filter
rep('''f_armSbe(float sbe, float ent, bool isLong, int t) =>
    if f_sbeValid(sbe, ent, isLong)''', '''f_armSbe(float sbe, float ent, bool isLong, int t) =>
    if f_sbeValid(sbe, ent, isLong) and f_entOk(isLong)''')
rep('''f_armEnt(Node n, float p, float tgt, float alt, bool isLong) =>
    n.ent_price         := p
    n.tgt_price         := tgt
    n.alt_price         := alt
    n.ent_str           := f_entStr(isLong)
    n.entry_triggered   := false
    n.is_swept_rejected := false
    n.ent_freeze_t      := na
    n.ent_arm_bar       := bar_index
    f_armSbe(n.sbe_price, p, isLong, n.t)''', '''f_armEnt(Node n, float p, float tgt, float alt, bool isLong) =>
    if f_entOk(isLong)
        n.ent_price         := p
        n.tgt_price         := tgt
        n.alt_price         := alt
        n.ent_str           := f_entStr(isLong)
        n.entry_triggered   := false
        n.is_swept_rejected := false
        n.ent_freeze_t      := na
        n.ent_arm_bar       := bar_index
        f_armSbe(n.sbe_price, p, isLong, n.t)''')
rep('''f_armOrg(Node n, bool isLong) =>
    n.org_price    := n.price
    n.org_str      := f_entStr(isLong)
    n.org_trig     := false
    n.org_freeze_t := na
    n.org_arm_bar  := bar_index
    f_armSbe(n.sbe_price, n.price, isLong, n.t)''', '''f_armOrg(Node n, bool isLong) =>
    if f_entOk(isLong)
        n.org_price    := n.price
        n.org_str      := f_entStr(isLong)
        n.org_trig     := false
        n.org_freeze_t := na
        n.org_arm_bar  := bar_index
        f_armSbe(n.sbe_price, n.price, isLong, n.t)''')

# news cancels untouched entries
rep('''    bool hit = false
    if not na(n)
        if not na(n.ent_price)
            if bar_index > nz(n.ent_arm_bar, -1)''', '''    bool hit = false
    if not na(n)
        if newsBlock
            if not na(n.ent_price) and not n.entry_triggered
                n.ent_price := na
                n.ent_str   := ""
            if not na(n.org_price) and not n.org_trig
                n.org_price := na
                n.org_str   := ""
        if not na(n.ent_price)
            if bar_index > nz(n.ent_arm_bar, -1)''')

# ---------------------------------------------------------------- gate memory at the top of each confirmed bar
rep('''if barstate.isconfirmed

    // TWO-WAY CANDLE''', '''if barstate.isconfirmed

    // GATE MEMORY — this candle's oscillator (only matters when a gate is on)
    if gateOn and not na(gHi) and not na(gLo)
        if gHi >= 80
            hitXP := true
            if mainSide == 1
                bullImp := true
            if mainSide == -1 and bearImp
                bearPb := true
        if gLo <= 20
            hitXD := true
            if mainSide == -1
                bearImp := true
            if mainSide == 1 and bullImp
                bullPb := true

    // TWO-WAY CANDLE''')

# ---------------------------------------------------------------- reversal (T1) gate
rep('''        bool normalShiftAlso = mainSide == 1 ? cdsFired : cdlFired
        int  newSide = -mainSide''', '''        bool normalShiftAlso = mainSide == 1 ? cdsFired : cdlFired
        int  newSide = -mainSide
        // GATE: a flip is official only if the old leg reached its extreme.
        bool flipPass = not gateOn or (newSide == 1 ? hitXD : hitXP)
        legOfficial := flipPass
        hitXD   := false
        hitXP   := false
        bullImp := false
        bullPb  := false
        bearImp := false
        bearPb  := false''')
rep('''isForced=tForced, legExt=legX, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV)
        if show_ent and eTrO
            newPl.ent_price''', '''isForced=tForced, legExt=legX, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV, official=flipPass)
        if show_ent and eTrO and f_entOk(newSide == 1)
            newPl.ent_price''')
rep('''        if newSide == 1
            alert_po4_bull := true
        else
            alert_po4_bear := true''', '''        if flipPass
            if newSide == 1
                alert_po4_bull := true
                alert_cdl      := true
            else
                alert_po4_bear := true
                alert_cds      := true''')

# ---------------------------------------------------------------- continuation (LD / SD) gate
rep('''        Node brokenPullback = mainSide == 1 ? beStatic : buStatic
        int  oldTier = curTier''', '''        Node brokenPullback = mainSide == 1 ? beStatic : buStatic
        int  oldTier = curTier
        // GATE: a continuation is official only if the leg reached its own
        // extreme and THEN the pullback reached the opposite extreme.
        bool contPass = not gateOn or (mainSide == 1 ? (bullImp and bullPb) : (bearImp and bearPb))
        legOfficial := contPass
        bullImp := false
        bullPb  := false
        bearImp := false
        bearPb  := false''')
rep('''isForced=tForced2, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV)
        if show_ent and eTrO''', '''isForced=tForced2, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV, official=contPass)
        if show_ent and eTrO and f_entOk(mainSide == 1)''')
rep('''        if mainSide == 1
            alert_po4_bull := true
        else
            alert_po4_bear := true''', '''        if contPass
            if mainSide == 1
                alert_po4_bull := true
                alert_ld       := true
            else
                alert_po4_bear := true
                alert_sd       := true''')

# ---------------------------------------------------------------- genesis gate
rep('''            int side = cdlFired ? 1 : -1
            bool   gUseCdl = side == 1''', '''            int side = cdlFired ? 1 : -1
            bool gPass = not gateOn or (side == 1 ? hitXD : hitXP)
            legOfficial := gPass
            hitXD   := false
            hitXP   := false
            bullImp := false
            bullPb  := false
            bearImp := false
            bearPb  := false
            bool   gUseCdl = side == 1''')
rep('''isForced=gForced, legExt=gLegX, c_high=high, c_low=low, c_open=open, c_close=close, c_time=time, c_volPct=curVolPct)
            if show_ent and eTrO''', '''isForced=gForced, legExt=gLegX, c_high=high, c_low=low, c_open=open, c_close=close, c_time=time, c_volPct=curVolPct, official=gPass)
            if show_ent and eTrO and f_entOk(side == 1)''')
rep('''            if side == 1
                alert_po4_bull := true
            else
                alert_po4_bear := true''', '''            if gPass
                if side == 1
                    alert_po4_bull := true
                    alert_cdl      := true
                else
                    alert_po4_bear := true
                    alert_cds      := true''')

# ---------------------------------------------------------------- news: cancel untouched PO4 + SBE entries
rep('''                bool closedThrough = (s.side == 1 and close < s.price - f_eps()) or (s.side == -1 and close > s.price + f_eps())
                if closedThrough''', '''                bool closedThrough = (s.side == 1 and close < s.price - f_eps()) or (s.side == -1 and close > s.price + f_eps())
                if closedThrough or (newsBlock and not s.trig)''')
rep('''                POLine pl = poLines.get(pi)
                if not na(pl.ent_price)
                    entSeen += 1''', '''                POLine pl = poLines.get(pi)
                if newsBlock and not na(pl.ent_price) and not pl.entry_triggered
                    pl.ent_price := na
                    pl.ent_str   := ""
                if not na(pl.ent_price)
                    entSeen += 1''')

# ---------------------------------------------------------------- render: engine letter, gate status
rep('''                string txt = (pl.side == 1 ? "BuPO4" : "BePO4") + (show_tiers ? " T" + str.tostring(pl.tier) : "") + (pl.isForced ? " Forced" : "")''', '''                string txt = (pl.side == 1 ? "BuPO4" : "BePO4") + (show_tiers ? " T" + str.tostring(pl.tier) : "") + (pl.isForced ? " Forced" : "") + (pl.official ? "" : " ✗")''')
rep('''                    color bc = isLdSd ? (pl.side == 1 ? ld_base_col : sd_base_col) : c
                    if not isLdSd or show_pb
                        drawn_lines.push(line.new(pl.causeT, pl.causePrice, causeEnd, pl.causePrice, xloc=xloc.bar_time, color=bc, width=1, style=line.style_solid))
                        drawn_labels.push(label.new(math.round(math.avg(pl.causeT, causeEnd)), pl.causePrice, pl.causeText, xloc=xloc.bar_time, style=pl.side == 1 ? label.style_label_down : label.style_label_up, textcolor=bc, color=color(na), size=f_sz(pl.causeMajor ? ld_sd_size : "tiny")))''', '''                    color bc = isLdSd ? (pl.side == 1 ? ld_base_col : sd_base_col) : c
                    color uc = pl.official ? bc : FAIL_COL
                    string ct = f_eng(pl.official ? pl.causeText : str.lower(pl.causeText))
                    // CDLc / LDc above the middle of the break line, CDSc / SDc below it.
                    if (not isLdSd or show_pb) and (pl.official or show_failed)
                        drawn_lines.push(line.new(pl.causeT, pl.causePrice, causeEnd, pl.causePrice, xloc=xloc.bar_time, color=uc, width=1, style=pl.official ? line.style_solid : line.style_dotted))
                        drawn_labels.push(label.new(math.round(math.avg(pl.causeT, causeEnd)), pl.causePrice, ct, xloc=xloc.bar_time, style=pl.side == 1 ? label.style_label_down : label.style_label_up, textcolor=uc, color=color(na), size=f_sz(pl.causeMajor ? ld_sd_size : "tiny"), tooltip=ct + (pl.official ? " (official)" : " (failed " + gate_mode + ")")))''')
rep('''                if show_ent and ent_trend and ent_best_zone and pl.tier == 1 and not na(pl.causePrice) and not na(pl.c_high)''', '''                if show_ent and ent_trend and ent_best_zone and pl.official and pl.tier == 1 and not na(pl.causePrice) and not na(pl.c_high)''')
rep('''                string plBlockName = plIsLdSd ? (pl.side == 1 ? "MMM iBlock L" : "MMM iBlock S") : (pl.side == 1 ? "eBlock CDL" : "eBlock CDS")
                if show_zones and plZoneOn and not na(pl.c_high)''', '''                string plBlockName = plIsLdSd ? (pl.side == 1 ? "MMM iBlock L" : "MMM iBlock S") : f_eng(pl.side == 1 ? "eBlock CDL" : "eBlock CDS")
                if show_zones and plZoneOn and pl.official and not na(pl.c_high)''')
rep('''            drawn_labels.push(label.new(math.round(math.avg(sm.ownerT, sm.breakT)), sm.price, sm.markerTxt, xloc=xloc.bar_time''', '''            drawn_labels.push(label.new(math.round(math.avg(sm.ownerT, sm.breakT)), sm.price, f_eng(sm.markerTxt), xloc=xloc.bar_time''')

# ---------------------------------------------------------------- HTF box + alerts
rep('''alertcondition(alert_gmc_bull, title="New BuX GMC", message="New BuX GMC (bullish momentum) confirmed on {@ticker}} at {{close}}")''', '''alertcondition(alert_gmc_bull, title="New BuX GMC", message="New BuX GMC (bullish momentum) confirmed on {{ticker}} at {{close}}")''')
src = src.rstrip('\n') + '''
alertcondition(alert_cdl, title="CDLc Flip (official)", message="CDLc - bullish flip (candle engine) on {{ticker}} at {{close}}")
alertcondition(alert_cds, title="CDSc Flip (official)", message="CDSc - bearish flip (candle engine) on {{ticker}} at {{close}}")
alertcondition(alert_ld, title="LDc Continuation (official)", message="LDc - bullish continuation (candle engine) on {{ticker}} at {{close}}")
alertcondition(alert_sd, title="SDc Continuation (official)", message="SDc - bearish continuation (candle engine) on {{ticker}} at {{close}}")

// ═══════════════════════════════════════════════════════════════════════════
// HTF BIAS BOX
// ═══════════════════════════════════════════════════════════════════════════
f_htfPos(string p) =>
    switch p
        "Top Left"      => position.top_left
        "Top Center"    => position.top_center
        "Bottom Left"   => position.bottom_left
        "Bottom Center" => position.bottom_center
        "Bottom Right"  => position.bottom_right
        => position.top_right

var table biasTbl = table.new(f_htfPos(htf_tbl_pos), 1, 1, bgcolor=#000000, border_width=1, frame_color=color.new(color.white, 70), frame_width=1)
if barstate.islast
    if htf_table and (htf_mode != "Off" or gateOn)
        string bSrc = htf_mode == "Last Flip (CDLc/CDSc)" ? "Flip" : htf_mode == "Last Continuation (LDc/SDc)" ? "Cont" : htf_mode == "Last BC" ? "BC" : "off"
        string bDir = htf_mode == "Off" ? "" : htfBias == 1 ? " · BULL" : htfBias == -1 ? " · BEAR" : " · NONE"
        color  bCol = htfBias == 1 ? bull_col : htfBias == -1 ? bear_col : color.silver
        table.cell(biasTbl, 0, 0, "HTF " + htf_tf + " · " + bSrc + bDir + " | Gate: " + gate_mode + (legOfficial ? "" : " ✗") + (newsBlock ? " · NEWS" : ""), text_color=bCol, text_size=size.small)
    else
        table.clear(biasTbl, 0, 0)
'''

open('/home/claude/v35/MMM_Pro_3.5.pine', 'w').write(src)
print("ok", src.count('\n'))

# Shared Pine v6 modules for the three MMM indicators (3.6).
# Each block is plain Pine text; {placeholders} are filled per indicator.

NEWS_DEFAULT = "\\n".join([
    # NFP (BLS Employment Situation, 08:30 NY)
    "2026-01-09 08:30 USD H NFP", "2026-02-11 08:30 USD H NFP", "2026-03-06 08:30 USD H NFP", "2026-04-03 08:30 USD H NFP",
    "2026-05-08 08:30 USD H NFP", "2026-06-05 08:30 USD H NFP", "2026-07-02 08:30 USD H NFP", "2026-08-07 08:30 USD H NFP",
    "2026-09-04 08:30 USD H NFP", "2026-10-02 08:30 USD H NFP", "2026-11-06 08:30 USD H NFP", "2026-12-04 08:30 USD H NFP",
    "2027-01-08 08:30 USD H NFP", "2027-02-05 08:30 USD H NFP", "2027-03-05 08:30 USD H NFP", "2027-04-02 08:30 USD H NFP",
    "2027-05-07 08:30 USD H NFP", "2027-06-04 08:30 USD H NFP", "2027-07-02 08:30 USD H NFP", "2027-08-06 08:30 USD H NFP",
    "2027-09-03 08:30 USD H NFP", "2027-10-08 08:30 USD H NFP", "2027-11-05 08:30 USD H NFP", "2027-12-03 08:30 USD H NFP",
    # CPI (BLS, 08:30 NY)
    "2026-01-13 08:30 USD H CPI", "2026-02-13 08:30 USD H CPI", "2026-03-11 08:30 USD H CPI", "2026-04-10 08:30 USD H CPI",
    "2026-05-12 08:30 USD H CPI", "2026-06-10 08:30 USD H CPI", "2026-07-14 08:30 USD H CPI", "2026-08-12 08:30 USD H CPI",
    "2026-09-11 08:30 USD H CPI", "2026-10-14 08:30 USD H CPI", "2026-11-10 08:30 USD H CPI", "2026-12-10 08:30 USD H CPI",
    "2027-01-13 08:30 USD H CPI", "2027-02-11 08:30 USD H CPI", "2027-03-10 08:30 USD H CPI", "2027-04-13 08:30 USD H CPI",
    "2027-05-12 08:30 USD H CPI", "2027-06-10 08:30 USD H CPI", "2027-07-14 08:30 USD H CPI", "2027-08-11 08:30 USD H CPI",
    "2027-09-14 08:30 USD H CPI", "2027-10-14 08:30 USD H CPI", "2027-11-10 08:30 USD H CPI", "2027-12-10 08:30 USD H CPI",
    # FOMC statement 14:00 + press conference 14:30 NY
    "2026-01-28 14:00 USD H FOMC", "2026-01-28 14:30 USD H FOMC PC", "2026-03-18 14:00 USD H FOMC", "2026-03-18 14:30 USD H FOMC PC",
    "2026-04-29 14:00 USD H FOMC", "2026-04-29 14:30 USD H FOMC PC", "2026-06-17 14:00 USD H FOMC", "2026-06-17 14:30 USD H FOMC PC",
    "2026-07-29 14:00 USD H FOMC", "2026-07-29 14:30 USD H FOMC PC", "2026-09-16 14:00 USD H FOMC", "2026-09-16 14:30 USD H FOMC PC",
    "2026-10-28 14:00 USD H FOMC", "2026-10-28 14:30 USD H FOMC PC", "2026-12-09 14:00 USD H FOMC", "2026-12-09 14:30 USD H FOMC PC",
    "2027-01-27 14:00 USD H FOMC", "2027-01-27 14:30 USD H FOMC PC", "2027-03-17 14:00 USD H FOMC", "2027-03-17 14:30 USD H FOMC PC",
    "2027-04-28 14:00 USD H FOMC", "2027-04-28 14:30 USD H FOMC PC", "2027-06-09 14:00 USD H FOMC", "2027-06-09 14:30 USD H FOMC PC",
    "2027-07-28 14:00 USD H FOMC", "2027-07-28 14:30 USD H FOMC PC", "2027-09-15 14:00 USD H FOMC", "2027-09-15 14:30 USD H FOMC PC",
    "2027-10-27 14:00 USD H FOMC", "2027-10-27 14:30 USD H FOMC PC", "2027-12-08 14:00 USD H FOMC", "2027-12-08 14:30 USD H FOMC PC",
])

# ─────────────────────────────────────────────────────────────── GATE · P/D
GATE_INPUTS = '''grp_gate    = "{grp}"
gate_mode   = input.string("NO GATE", "Gate", options=["NO GATE", "MMPD 27", "MMPD fast", "MMPD Delta"], group=grp_gate, tooltip="NO GATE = every break is official (normal break, no filter).\\n\\nMMPD 27 / MMPD fast / MMPD Delta = the MMM Pro Edge rhythm{gate_tf}:\\n• Flip (CDL / CDS) is official only if the old leg reached its extreme first: oscillator ≤ 20 before a CDL, ≥ 80 before a CDS.\\n• Continuation (LD / SD) is official only if the leg reached its OWN extreme (bull ≥ 80) and THEN the pullback reached the OPPOSITE extreme (≤ 20) before the break.\\n\\nMMPD Delta = the natural order-flow version (built on candle delta).\\nThe structure never changes with the gate. A failed break keeps its PO4 (marked ✗), its label turns grey or hides, and it sends no alert.")
gate_fast   = input.int(9, "MMPD fast Length", minval=5, maxval=50, group=grp_gate)
show_failed = input.bool(false, "Show Failed Breaks (small grey)", group=grp_gate, tooltip="OFF = the label of a break that failed the gate is hidden (its PO4 stays, marked ✗).\\nON = it is drawn in grey, lowercase.")
zone_side   = input.string("Long in Discount / Short in Premium", "Premium / Discount Side", options=["Long in Discount / Short in Premium", "Long in Premium / Short in Discount"], group=grp_gate, tooltip="Which part of every eBlock / iBlock is drawn.\\nStandard = long in the DISCOUNT part (lower), short in the PREMIUM part (upper).\\nOpposite (op.) = long in premium, short in discount.\\nTest both: this is the Premium vs Discount test.")
zone_tier   = input.string("50% (0-50% / 50-100%)", "Zone Depth", options=["Extreme (0-12.5% / 87.5-100%)", "Balanced (12.5-25% / 75-87.5%)", "Standard (25-50% / 50-75%)", "50% (0-50% / 50-100%)"], group=grp_gate, tooltip="How deep into the origin candle / box the zone sits, measured from the side chosen above.")
'''

GATE_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// GATE OSCILLATORS (same math as Super MMPD / MMM Pro Edge)
// ═══════════════════════════════════════════════════════════════
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

f_gatePrev() =>
    [hi, lo] = f_gateNow()
    [hi[1], lo[1]]

// Gate memory (impulse -> pullback -> continuation)
var bool hitXD   = false   // oscillator <= 20 since the last flip
var bool hitXP   = false   // oscillator >= 80 since the last flip
var bool bullImp = false   // bull leg reached its own extreme (>= 80)
var bool bullPb  = false   // then the pullback reached <= 20
var bool bearImp = false
var bool bearPb  = false

// Zone slice of an origin candle / box: which part is drawn depends on the
// Premium / Discount side and the depth.
f_zoneSlice(float top, float bot, bool isBull) =>
    bool  lowSide = zone_side == "Long in Discount / Short in Premium" ? isBull : not isBull
    float rng = top - bot
    float zT = na
    float zB = na
    if zone_tier == "Extreme (0-12.5% / 87.5-100%)"
        zT := lowSide ? bot + rng * 0.125 : top
        zB := lowSide ? bot : bot + rng * 0.875
    else if zone_tier == "Balanced (12.5-25% / 75-87.5%)"
        zT := lowSide ? bot + rng * 0.25 : bot + rng * 0.875
        zB := lowSide ? bot + rng * 0.125 : bot + rng * 0.75
    else if zone_tier == "Standard (25-50% / 50-75%)"
        zT := lowSide ? bot + rng * 0.50 : bot + rng * 0.75
        zB := lowSide ? bot + rng * 0.25 : bot + rng * 0.50
    else
        zT := lowSide ? bot + rng * 0.50 : top
        zB := lowSide ? bot : bot + rng * 0.50
    [zT, zB]
'''

# ─────────────────────────────────────────────────────────────── ZONES (eBlock / iBlock)
ZONE_INPUTS = '''grp_zone       = "{grp}"
show_eblk      = input.bool(true, "eBlock  (Flip Zone · CDL / CDS)", group=grp_zone, tooltip="The zone of every T1 PO4 — the origin of a FLIP (CDL / CDS). It lives exactly as long as its PO4 (husband & wife).")
show_iblk      = input.bool(true, "iBlock  (Continuation Zone · LD / SD)", group=grp_zone, tooltip="The zone of every T2, T3… PO4 — the origin of a CONTINUATION (LD / SD). It lives exactly as long as its PO4.")
zone_naming    = input.string("eBlock / iBlock", "Zone Naming", options=["eBlock / iBlock", "External / Internal Entry Zone", "Flip / Continuation Zone"], group=grp_zone)
zone_show_name = input.bool(true, "Name Inside Box", inline="zn", group=grp_zone)
zone_transp    = input.int(85, "Transparency", minval=0, maxval=100, inline="zn", group=grp_zone)
'''

ZONE_HELPERS = '''// Zone name from the naming scheme. isFlip = T1 (CDL / CDS), else T2+ (LD / SD).
f_zoneName(bool isFlip, bool isBull, string eng) =>
    string fl = (isBull ? "CDL" : "CDS") + eng
    string co = (isBull ? "LD" : "SD") + eng
    zone_naming == "eBlock / iBlock" ? (isFlip ? "MMM eBlock " + fl : "MMM iBlock " + co) : zone_naming == "External / Internal Entry Zone" ? (isFlip ? "External Entry Zone " + fl : "Internal Entry Zone " + co) : (isFlip ? "Flip Zone " + fl : "Continuation Zone " + co)
'''

# ─────────────────────────────────────────────────────────────── MERGED LEVELS (Pro system)
LEVELS = '''// ═══════════════════════════════════════════════════════════════
// RIGHT-EDGE LEVELS — levels sharing a price MERGE into one line whose label
// joins every name with " & " (MMM Pro system). Highest priority styles it.
// ═══════════════════════════════════════════════════════════════
type EdgeLvl
    float         price
    array<string> labels
    color         ln_col
    int           ln_width
    string        ln_style
    int           b_time
    int           e_time
    int           priority
    string        txt_sz
    string        tip

var array<EdgeLvl> render_groups = array.new<EdgeLvl>()
var array<line>    drawn_lines   = array.new<line>()
var array<label>   drawn_labels  = array.new<label>()
var array<box>     drawn_boxes   = array.new<box>()

f_eps() => math.max(syminfo.mintick * 0.51, 1e-5)

f_szs(string s) =>
    s == "large" ? size.large : s == "normal" ? size.normal : s == "small" ? size.small : size.tiny

f_add_level(float p_price, string p_text, color p_col, int p_width, string p_style, int p_start_t, int p_end_t, int p_prio, string p_txt_sz, string p_tip) =>
    bool found = false
    int b0 = math.min(nz(p_start_t, time), nz(p_end_t, time))
    int e0 = math.max(nz(p_start_t, time), nz(p_end_t, time))
    if render_groups.size() > 0
        for grp in render_groups
            if math.abs(grp.price - p_price) <= f_eps()
                found := true
                if str.length(p_text) > 0 and array.indexof(grp.labels, p_text) == -1
                    grp.labels.push(p_text)
                grp.b_time := math.min(grp.b_time, b0)
                grp.e_time := math.max(grp.e_time, e0)
                if str.length(p_tip) > 0
                    grp.tip := str.length(grp.tip) > 0 ? grp.tip + "\\n" + p_tip : p_tip
                if p_prio > grp.priority
                    grp.ln_col   := p_col
                    grp.ln_width := p_width
                    grp.ln_style := p_style
                    grp.priority := p_prio
                    grp.txt_sz   := p_txt_sz
                break
    if not found
        array<string> nl = array.new<string>()
        if str.length(p_text) > 0
            nl.push(p_text)
        render_groups.push(EdgeLvl.new(p_price, nl, p_col, p_width, p_style, b0, e0, p_prio, p_txt_sz, p_tip))

f_clear_drawn() =>
    if drawn_lines.size() > 0
        for ln in drawn_lines
            line.delete(ln)
        drawn_lines.clear()
    if drawn_labels.size() > 0
        for lb in drawn_labels
            label.delete(lb)
        drawn_labels.clear()
    if drawn_boxes.size() > 0
        for bx in drawn_boxes
            box.delete(bx)
        drawn_boxes.clear()

f_draw_groups() =>
    if render_groups.size() > 0
        for grp in render_groups
            drawn_lines.push(line.new(grp.b_time, grp.price, grp.e_time, grp.price, xloc=xloc.bar_time, color=grp.ln_col, width=grp.ln_width, style=grp.ln_style))
            drawn_labels.push(label.new(grp.e_time, grp.price, array.join(grp.labels, " & "), xloc=xloc.bar_time, textcolor=grp.ln_col, color=color(na), style=label.style_label_left, size=f_szs(grp.txt_sz), tooltip=grp.tip))
    render_groups.clear()

var int bar_time_diff = timeframe.in_seconds() * 1000
f_future_time(int ext) =>
    int diff = time - nz(time[1], time)
    if diff <= 0
        diff := bar_time_diff
    if diff <= 0
        diff := 60000
    time + math.round(diff * ext)
'''

# ─────────────────────────────────────────────────────────────── ZONE ENGINE (x) — shared
ZONE_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// MMM ZONE ENGINE (x) — box break logic inside the MMM Pro T# / P# / R# system.
// One block candle per call when doStep is true (state lives inside).
//  BOX     = expander BC + the candles that close back inside it.
//            G1 grow: an inside candle's wick past the edge pushes the edge out.
//            G0 fixed: the box keeps the range it was born with.
//  TREND   = the last PO4 x (Tn). Bull: BuPO4x below price · Bear: BePO4x above.
//  P#      = the FIRST box after Tn = the pullback start.
//            Bull: its HIGH is the level · Bear: its LOW is the level.
//  R#      = the first box formed after the P# box ended = the resumption base.
//            Bull: its LOW · Bear: its HIGH. A close back through it erases it.
//  LDx#    = a body close past P# -> R# becomes T(#+1) (no R# = the pullback extreme).
//  CDLx / CDSx = a body close past the last T# -> the P# level becomes the new T1
//            (no P# = the extreme of the leg). Every other box break is ignored.
// Returns the state + this candle's events.
// ═══════════════════════════════════════════════════════════════
f_zoneEngine(bool doStep, float o, float h, float l, float c, float v, float ph, float pl, int t, bool grow, bool expMode) =>
    var bool  zWait = false
    var float exH   = na
    var float exL   = na
    var int   exT   = na
    var int   exDir = 0
    var bool  zLive = false
    var float bxH   = na
    var float bxL   = na
    var int   bxT   = na
    var int   bxId  = 0
    var float bxD   = 0.0
    var float bxV   = 0.0
    var int   side  = 0
    var int   tier  = 0
    var float tnP   = na
    var int   tnT   = na
    var float pP    = na
    var int   pT    = na
    var int   pId   = -1
    var bool  pLive = false
    var float pOH   = na
    var float pOL   = na
    var float rP    = na
    var int   rT    = na
    var int   rId   = -1
    var bool  rLive = false
    var float rOH   = na
    var float rOL   = na
    var float legHi = na
    var float legHiL = na
    var int   legHiT = na
    var float legLo = na
    var float legLoH = na
    var int   legLoT = na
    var float pbHi  = na
    var float pbHiL = na
    var int   pbHiT = na
    var float pbLo  = na
    var float pbLoH = na
    var int   pbLoT = na
    int   evType = 0
    int   evDir  = 0
    int   evNum  = 0
    float brkP   = na
    int   brkT   = na
    float nTnP   = na
    int   nTnT   = na
    float nOH    = na
    float nOL    = na
    int   nOT    = na
    bool  endF   = false
    float endH   = na
    float endL   = na
    int   endT   = na
    int   endRole = 0
    float endNdb = 0.0
    int   formRole = -1
    if doStep and not na(c) and not na(ph) and not na(pl)
        bool  bu  = c > ph
        bool  be  = c < pl
        bool  bc  = bu or be
        float rg  = h - l
        float dlt = rg > 0 ? nz(v) * ((c - l) - (h - c)) / rg : 0.0
        bool  formed = false
        // 1. BOX DETECTOR
        if zLive
            if c > bxH or c < bxL
                endF    := true
                endH    := bxH
                endL    := bxL
                endT    := bxT
                endRole := bxId == pId ? 1 : bxId == rId ? 2 : 0
                endNdb  := bxV > 0 ? bxD / bxV : 0.0
                if bxId == pId
                    pLive := false
                if bxId == rId
                    rLive := false
                zLive := false
                zWait := bc
                if bc
                    exH   := h
                    exL   := l
                    exT   := t
                    exDir := bu ? 1 : -1
            else
                if grow
                    bxH := math.max(bxH, h)
                    bxL := math.min(bxL, l)
                bxD += dlt
                bxV += nz(v)
        else if zWait
            if bc
                exH   := h
                exL   := l
                exT   := t
                exDir := bu ? 1 : -1
            else
                zLive  := true
                zWait  := false
                formed := true
                bxId   += 1
                bxT    := exT
                bxD    := dlt
                bxV    := nz(v)
                if expMode
                    bxH := grow ? math.max(exH, h) : exH
                    bxL := grow ? math.min(exL, l) : exL
                else
                    bxH := h
                    bxL := l
        else if bc
            zWait := true
            exH   := h
            exL   := l
            exT   := t
            exDir := bu ? 1 : -1
        // live P# / R# boxes carry their level while they grow
        if zLive and bxId == pId
            pP  := side == 1 ? bxH : bxL
            pOH := bxH
            pOL := bxL
        if zLive and bxId == rId
            rP  := side == 1 ? bxL : bxH
            rOH := bxH
            rOL := bxL
        // 2. EXTREMES (leg since Tn, pullback since P#)
        if side != 0
            if na(legHi) or h > legHi
                legHi  := h
                legHiL := l
                legHiT := t
            if na(legLo) or l < legLo
                legLo  := l
                legLoH := h
                legLoT := t
        if not na(pP)
            if na(pbHi) or h > pbHi
                pbHi  := h
                pbHiL := l
                pbHiT := t
            if na(pbLo) or l < pbLo
                pbLo  := l
                pbLoH := h
                pbLoT := t
        // 3. STRUCTURE: Reversal > Continuation > R# invalidation
        if side == 1
            if c < tnP
                evType := 1
                evDir  := -1
                brkP   := tnP
                brkT   := tnT
                bool hasP = not na(pP)
                nTnP := hasP ? pP : legHi
                nTnT := hasP ? pT : legHiT
                nOH  := hasP ? pOH : legHi
                nOL  := hasP ? pOL : legHiL
                nOT  := hasP ? pT : legHiT
            else if not na(pP) and c > pP
                evType := 2
                evDir  := 1
                evNum  := tier
                brkP   := pP
                brkT   := pT
                bool hasR = not na(rP)
                nTnP := hasR ? rP : pbLo
                nTnT := hasR ? rT : pbLoT
                nOH  := hasR ? rOH : pbLoH
                nOL  := hasR ? rOL : pbLo
                nOT  := hasR ? rT : pbLoT
            else if not na(rP) and c < rP
                rP    := na
                rT    := na
                rId   := -1
                rLive := false
        else if side == -1
            if c > tnP
                evType := 1
                evDir  := 1
                brkP   := tnP
                brkT   := tnT
                bool hasP = not na(pP)
                nTnP := hasP ? pP : legLo
                nTnT := hasP ? pT : legLoT
                nOH  := hasP ? pOH : legLoH
                nOL  := hasP ? pOL : legLo
                nOT  := hasP ? pT : legLoT
            else if not na(pP) and c < pP
                evType := 2
                evDir  := -1
                evNum  := tier
                brkP   := pP
                brkT   := pT
                bool hasR = not na(rP)
                nTnP := hasR ? rP : pbHi
                nTnT := hasR ? rT : pbHiT
                nOH  := hasR ? rOH : pbHi
                nOL  := hasR ? rOL : pbHiL
                nOT  := hasR ? rT : pbHiT
            else if not na(rP) and c > rP
                rP    := na
                rT    := na
                rId   := -1
                rLive := false
        else if endF
            // GENESIS: the first box break starts the first trend
            evType := 1
            evDir  := c > endH ? 1 : -1
            brkP   := evDir == 1 ? endH : endL
            brkT   := endT
            nTnP   := evDir == 1 ? endL : endH
            nTnT   := endT
            nOH    := endH
            nOL    := endL
            nOT    := endT
        if evType != 0
            side  := evDir
            tier  := evType == 1 ? 1 : tier + 1
            tnP   := nTnP
            tnT   := nTnT
            pP    := na
            pT    := na
            pId   := -1
            pLive := false
            rP    := na
            rT    := na
            rId   := -1
            rLive := false
            legHi  := h
            legHiL := l
            legHiT := t
            legLo  := l
            legLoH := h
            legLoT := t
            pbHi  := na
            pbLo  := na
        // 4. ROLE of a box born on this candle
        if formed
            formRole := 0
            if side != 0 and na(pP)
                pId   := bxId
                pLive := true
                pP    := side == 1 ? bxH : bxL
                pT    := bxT
                pOH   := bxH
                pOL   := bxL
                pbHi  := bxH
                pbHiL := bxL
                pbHiT := bxT
                pbLo  := bxL
                pbLoH := bxH
                pbLoT := bxT
                formRole := 1
            else if side != 0 and not pLive and na(rP)
                rId   := bxId
                rLive := true
                rP    := side == 1 ? bxL : bxH
                rT    := bxT
                rOH   := bxH
                rOL   := bxL
                formRole := 2
    float liveNdb = bxV > 0 ? bxD / bxV : 0.0
    int   liveRole = zLive ? (bxId == pId ? 1 : bxId == rId ? 2 : 0) : -1
    [side, tier, tnP, tnT, pP, pT, rP, rT, evType, evDir, evNum, brkP, brkT, nTnP, nTnT, nOH, nOL, nOT, zLive, bxH, bxL, bxT, liveNdb, liveRole, endF, endH, endL, endT, endRole, endNdb]
'''

# ─────────────────────────────────────────────────────────────── HTF BIAS (all three engines)
HTF_INPUTS = '''grp_htf     = "{grp}"
htf_src     = input.string("Off", "HTF Bias From", options=["Off", "Last BC", "Last Flip (CDL / CDS)", "Last Continuation (LD / SD)"], group=grp_htf, tooltip="Read on the LAST CLOSED HTF candle only (no repaint).\\n\\nOff = no HTF bias (B0).\\nLast BC = direction of the last HTF body close candle (B1). The box also shows where that BC came from: a flip, a continuation, or a plain BC.\\nLast Flip = direction of the last HTF CDL / CDS of the engine below (the trend).\\nLast Continuation = direction of the last HTF LD / SD made AFTER the last flip. No continuation yet = no bias.")
htf_eng     = input.string("{eng_default}", "HTF Break Engine", options=["Zone x (boxes)", "Candle c (PO4)", "Swing s (swings)"], group=grp_htf, tooltip="Which MMM engine reads the HTF breaks:\\nx = boxes (Concepts Pro+) = B2 zone break\\nc = PO4 candles (MMM Pro) = B3 candle break\\ns = swings (Order Flow Suite) = B4 swing break\\nTest all three: same HTF, different engine.")
htf_tf      = input.timeframe("240", "HTF Timeframe", group=grp_htf)
htf_dim     = input.bool(true, "Dim Breaks Against HTF Bias", group=grp_htf, tooltip="A break against the HTF bias is drawn in grey. Nothing is hidden.")
htf_table   = input.bool(true, "Show HTF Bias Box", inline="hb", group=grp_htf)
htf_tbl_pos = input.string("{pos_default}", "", options=["Top Left", "Top Center", "Top Right", "Bottom Left", "Bottom Center", "Bottom Right"], inline="hb", group=grp_htf)
'''

HTF_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// HTF BIAS — compact copies of the three MMM engines, run on the HTF.
// Last CLOSED HTF candle only ([1] + lookahead_on) = no repaint.
// Each returns [flip side, continuation side, last BC, BC origin]
// origin: 2 = the last BC was a flip candle, 1 = a continuation candle, 0 = plain.
// ═══════════════════════════════════════════════════════════════
f_htfSwing() =>
    var float   tH    = high
    var float   tL    = low
    var int     tSt   = 0
    var int     sig   = 0
    var int     lastC = 0
    var int     cdlB  = -1
    var int     cdsB  = -1
    var float[] hs    = array.new<float>()
    var int[]   hsb   = array.new<int>()
    var float[] ls    = array.new<float>()
    var int[]   lsb   = array.new<int>()
    bool flipEv = false
    bool contEv = false
    bool bu = close > high[1]
    bool be = close < low[1]
    if tSt == 0
        tH := math.max(tH, high)
        tL := math.min(tL, low)
    if tSt == 1 and high >= tH
        tH := high
    if tSt == -1 and low <= tL
        tL := low
    if be and tSt >= 0
        hs.push(tH)
        hsb.push(bar_index)
        tSt := -1
        tL  := low
    else if bu and tSt <= 0
        ls.push(tL)
        lsb.push(bar_index)
        tSt := 1
        tH  := high
    bool lowDone = false
    if ls.size() > 0
        for i = ls.size() - 1 to 0
            float p = ls.get(i)
            int   b = lsb.get(i)
            if b < bar_index and close < p
                if not lowDone
                    bool flip = sig != -1
                    if flip or b > cdsB
                        lowDone := true
                        if flip
                            cdsB   := bar_index
                            lastC  := 0
                            flipEv := true
                        else
                            lastC  := -1
                            contEv := true
                        sig := -1
                ls.remove(i)
                lsb.remove(i)
    bool highDone = false
    if hs.size() > 0
        for i = hs.size() - 1 to 0
            float p = hs.get(i)
            int   b = hsb.get(i)
            if b < bar_index and close > p
                if not highDone
                    bool flip = sig != 1
                    if flip or b > cdlB
                        highDone := true
                        if flip
                            cdlB   := bar_index
                            lastC  := 0
                            flipEv := true
                        else
                            lastC  := 1
                            contEv := true
                        sig := 1
                hs.remove(i)
                hsb.remove(i)
    while ls.size() > 20
        ls.shift()
        lsb.shift()
    while hs.size() > 20
        hs.shift()
        hsb.shift()
    [sig, lastC, flipEv, contEv]

f_htfCandle() =>
    var int   side  = 0
    var float tn    = na
    var float pb    = na
    var float rs    = na
    var int   lastC = 0
    bool flipEv = false
    bool contEv = false
    bool bu   = close > high[1]
    bool be   = close < low[1]
    bool done = false
    if side == 1
        if close < tn
            side   := -1
            tn     := na(pb) ? open : pb
            pb     := na
            rs     := na
            lastC  := 0
            done   := true
            flipEv := true
        else if not na(pb) and close > pb
            tn     := na(rs) ? open : rs
            pb     := na
            rs     := na
            lastC  := 1
            done   := true
            contEv := true
    else if side == -1
        if close > tn
            side   := 1
            tn     := na(pb) ? open : pb
            pb     := na
            rs     := na
            lastC  := 0
            done   := true
            flipEv := true
        else if not na(pb) and close < pb
            tn     := na(rs) ? open : rs
            pb     := na
            rs     := na
            lastC  := -1
            done   := true
            contEv := true
    else
        if bu or be
            side   := bu ? 1 : -1
            tn     := open
            done   := true
            flipEv := true
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
    [side, lastC, flipEv, contEv]

f_htfZone() =>
    var int lastC = 0
    [zs, zt, ztn, ztt, zp, zpt, zr, zrt, zev, zdir, znum, zbp, zbt, zntp, zntt, zoh, zol, zot, zlive, zbh, zbl, zbt2, zndb, zrole, zef, zeh, zel, zet, zer, zen] = f_zoneEngine(true, open, high, low, close, volume, high[1], low[1], time, {htf_grow}, true)
    if zev == 1
        lastC := 0
    if zev == 2
        lastC := zdir
    [zs, lastC, zev == 1, zev == 2]

f_htfAll() =>
    var int lastBC = 0
    var int bcOrg  = 0
    [s1, c1, f1, n1] = f_htfSwing()
    [s2, c2, f2, n2] = f_htfCandle()
    [s3, c3, f3, n3] = f_htfZone()
    bool useX = htf_eng == "Zone x (boxes)"
    bool useC = htf_eng == "Candle c (PO4)"
    int  sd = useX ? s3 : useC ? s2 : s1
    int  cn = useX ? c3 : useC ? c2 : c1
    bool fe = useX ? f3 : useC ? f2 : f1
    bool ne = useX ? n3 : useC ? n2 : n1
    bool bu = close > high[1]
    bool be = close < low[1]
    if bu or be
        lastBC := bu ? 1 : -1
        bcOrg  := fe ? 2 : ne ? 1 : 0
    [nz(sd[1]), nz(cn[1]), nz(lastBC[1]), nz(bcOrg[1])]

[htfSig, htfCont, htfBC, htfOrg] = request.security(syminfo.tickerid, htf_tf, f_htfAll(), lookahead=barmerge.lookahead_on)
int  htfBias = htf_src == "Last BC" ? htfBC : htf_src == "Last Flip (CDL / CDS)" ? htfSig : htf_src == "Last Continuation (LD / SD)" ? htfCont : 0

// true when a break in direction dir goes AGAINST the HTF bias
f_againstHtf(int dir) =>
    htf_src != "Off" and htfBias != 0 and htfBias != dir

f_htfPos(string p) =>
    switch p
        "Top Left"      => position.top_left
        "Top Center"    => position.top_center
        "Top Right"     => position.top_right
        "Bottom Left"   => position.bottom_left
        "Bottom Right"  => position.bottom_right
        => position.bottom_center
'''

HTF_TABLE = '''// ═══════════════════════════════════════════════════════════════
// HTF BIAS BOX
// ═══════════════════════════════════════════════════════════════
var table biasTbl = table.new(f_htfPos(htf_tbl_pos), 1, 1, bgcolor=#000000, border_width=1, frame_color=color.new(color.white, 70), frame_width=1)
if barstate.islast
    if htf_table and htf_src != "Off"
        string bSrc = htf_src == "Last BC" ? "Last BC" : htf_src == "Last Flip (CDL / CDS)" ? "Flip" : "Cont"
        string bEng = htf_eng == "Zone x (boxes)" ? "x" : htf_eng == "Candle c (PO4)" ? "c" : "s"
        string bDir = htfBias == 1 ? "BULL" : htfBias == -1 ? "BEAR" : "NONE"
        string bOrg = htf_src == "Last BC" ? (htfOrg == 2 ? " (from a flip " + bEng + ")" : htfOrg == 1 ? " (from a continuation " + bEng + ")" : " (plain BC)") : " · engine " + bEng
        color  bCol = htfBias == 1 ? {bull_col} : htfBias == -1 ? {bear_col} : color.silver
        table.cell(biasTbl, 0, 0, "HTF " + htf_tf + " · " + bSrc + " · " + bDir + bOrg, text_color=bCol, text_size=size.small)
    else
        table.clear(biasTbl, 0, 0)
'''

# ─────────────────────────────────────────────────────────────── NEWS v2
NEWS_INPUTS = '''grp_news      = "{grp}"
news_paste    = input.text_area("''' + NEWS_DEFAULT + '''", "News Calendar (one box for all)", group=grp_news, tooltip="ONE box for every event. One event per line:\\nYYYY-MM-DD HH:MM CUR I Title\\nTime = New York. I = H (red) · M (orange) · L (yellow) · N (grey).\\nIt comes filled with NFP, CPI and FOMC for 2026–2027. Paste the extra weeks made by the MMM News Converter page at the end.")
news_cur      = input.string("USD", "Currencies", group=grp_news, tooltip="Comma list of currencies used. ES / NQ = USD.")
news_red      = input.bool(true,  "🔴 High", inline="imp", group=grp_news, tooltip="Which impacts are used: red = High, orange = Medium, yellow = Low, grey = holiday / non-economic.")
news_org      = input.bool(false, "🟠 Medium", inline="imp", group=grp_news)
news_yel      = input.bool(false, "🟡 Low", inline="imp", group=grp_news)
news_gry      = input.bool(false, "⚪ Grey", inline="imp", group=grp_news)
news_warn     = input.string("30", "Warning: Minutes Before", options=["15", "30"], group=grp_news, tooltip="The dot sits on the candle that holds this time (news time minus 15 or 30 minutes): a closed candle or the live one.")
news_dot      = input.bool(true, "Dot", inline="nd", group=grp_news)
news_lbl      = input.bool(true, "Label (CPI / FOMC…)", inline="nd", group=grp_news, tooltip="Tiny name next to the dot: ABOVE the dot when the candle is bearish, BELOW it when the candle is bullish.")
news_dot_at   = input.string("High", "At", options=["High", "Low"], inline="nd", group=grp_news)
news_max      = input.int(5, "Max Dots + Labels", minval=0, maxval=100, group=grp_news, tooltip="How many news dots / labels stay on the chart (newest first).")
news_bg       = input.bool(true, "Background", inline="nb", group=grp_news, tooltip="Shades the news window (minutes before → minutes after the news).")
news_bg_max   = input.int(3, "Max", minval=0, maxval=100, inline="nb", group=grp_news)
news_pre      = input.int(5, "Window: Min Before", minval=0, maxval=120, inline="nw", group=grp_news)
news_post     = input.int(15, "Min After", minval=0, maxval=240, inline="nw", group=grp_news)
news_del      = input.bool(true, "Delete When Price Takes the Dot", inline="ndl", group=grp_news, tooltip="ON: the dot, its label and its background are deleted together when a later candle CLOSES above the dot (dot at High) / below it (dot at Low), or touches it.")
news_del_mode = input.string("Close Above / Below", "", options=["Close Above / Below", "Touch"], inline="ndl", group=grp_news)
'''

NEWS_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// NEWS ENGINE (shared by every MMM indicator) — light: no library and no
// external request. Events come from the one calendar box.
// ═══════════════════════════════════════════════════════════════
const string NWS_TZ = "America/New_York"

type NewsMark
    label dot
    label txt
    box   bg
    float price
    bool  atHi
    int   bar
    int   wS
    int   wE

f_nwImpOk(string imp) =>
    imp == "H" ? news_red : imp == "M" ? news_org : imp == "L" ? news_yel : imp == "N" ? news_gry : false

f_nwCol(string imp) =>
    imp == "H" ? color.red : imp == "M" ? color.orange : imp == "L" ? color.yellow : color.gray

f_nwRank(string imp) =>
    imp == "H" ? 4 : imp == "M" ? 3 : imp == "L" ? 2 : 1

f_nwDate(string d, int hh, int mm) =>
    int t = na
    if str.length(d) == 10
        float y  = str.tonumber(str.substring(d, 0, 4))
        float m  = str.tonumber(str.substring(d, 5, 7))
        float dd = str.tonumber(str.substring(d, 8, 10))
        if not na(y) and not na(m) and not na(dd)
            t := timestamp(NWS_TZ, int(y), int(m), int(dd), hh, mm)
    t

var array<int>    nwT = array.new<int>()
var array<string> nwI = array.new<string>()
var array<string> nwN = array.new<string>()

if barstate.isfirst
    array<int>    tT = array.new<int>()
    array<string> tI = array.new<string>()
    array<string> tN = array.new<string>()
    string curList = "," + str.replace_all(str.upper(news_cur), " ", "") + ","
    for ln in str.split(str.replace_all(news_paste, ";", "\\n"), "\\n")
        array<string> tk = str.split(str.trim(ln), " ")
        if tk.size() >= 4
            string dS  = tk.get(0)
            string tS  = tk.get(1)
            string cur = str.upper(tk.get(2))
            string imp = str.upper(tk.get(3))
            if str.length(tS) == 5 and str.contains(curList, "," + cur + ",") and f_nwImpOk(imp)
                float hh = str.tonumber(str.substring(tS, 0, 2))
                float mm = str.tonumber(str.substring(tS, 3, 5))
                if not na(hh) and not na(mm)
                    int t = f_nwDate(dS, int(hh), int(mm))
                    if not na(t)
                        string ttl = ""
                        if tk.size() > 4
                            for k = 4 to tk.size() - 1
                                ttl += (k > 4 ? " " : "") + tk.get(k)
                        tT.push(t)
                        tI.push(imp)
                        tN.push(str.length(ttl) > 0 ? ttl : cur)
    if tT.size() > 0
        array<int> ord = tT.sort_indices(order.ascending)
        for k = 0 to ord.size() - 1
            nwT.push(tT.get(ord.get(k)))
            nwI.push(tI.get(ord.get(k)))
            nwN.push(tN.get(ord.get(k)))

int    nwPre    = news_pre * 60000
int    nwPost   = news_post * 60000
int    nwWarn   = (news_warn == "15" ? 15 : 30) * 60000
int    nwBarMs  = timeframe.in_seconds(timeframe.period) * 1000
int    nwEnd    = nz(time_close, time + nwBarMs)
var int nwPtr   = 0
bool   nwInWin  = false
int    nwWinS   = na
int    nwWinE   = na
string nwWarnTxt = ""
string nwWarnTip = ""
string nwWarnImp = ""
int    nwWarnS  = na
int    nwWarnE  = na
if timeframe.isintraday and nwT.size() > 0
    while nwPtr < nwT.size()
        if nwT.get(nwPtr) + nwPost < time
            nwPtr += 1
        else
            break
    if nwPtr < nwT.size()
        for j = nwPtr to nwT.size() - 1
            int et = nwT.get(j)
            if et - math.max(nwPre, nwWarn) >= nwEnd
                break
            if time < et + nwPost and nwEnd > et - nwPre
                nwInWin := true
                nwWinS  := na(nwWinS) ? et - nwPre : math.min(nwWinS, et - nwPre)
                nwWinE  := na(nwWinE) ? et + nwPost : math.max(nwWinE, et + nwPost)
            int wt = et - nwWarn
            if wt >= time and wt < nwEnd
                string nm = nwN.get(j)
                if not str.contains(nwWarnTxt, nm)
                    nwWarnTxt += (str.length(nwWarnTxt) > 0 ? "/" : "") + nm
                nwWarnTip += (str.length(nwWarnTip) > 0 ? "\\n" : "") + str.format_time(et, "HH:mm", NWS_TZ) + " NY · " + nwI.get(j) + " · " + nm
                nwWarnS := na(nwWarnS) ? et - nwPre : math.min(nwWarnS, et - nwPre)
                nwWarnE := na(nwWarnE) ? et + nwPost : math.max(nwWarnE, et + nwPost)
                if str.length(nwWarnImp) == 0 or f_nwRank(nwI.get(j)) > f_nwRank(nwWarnImp)
                    nwWarnImp := nwI.get(j)
bool newsBlock = nwInWin
bool newsWarn  = str.length(nwWarnTxt) > 0

var array<NewsMark> nwMarks = array.new<NewsMark>()
var int nwKillE = na   // end of a window whose dot was taken: no new shading before it

f_nwMake(bool keep) =>
    color dc   = f_nwCol(nwWarnImp)
    bool  atHi = news_dot_at == "High"
    float p    = atHi ? high : low
    label d    = news_dot ? label.new(bar_index, p, "", style=label.style_circle, color=dc, textcolor=dc, size=size.tiny, tooltip="News in " + news_warn + " min:\\n" + nwWarnTip) : na
    label tx   = news_lbl ? label.new(bar_index, p, nwWarnTxt, style=close < open ? label.style_label_down : label.style_label_up, color=color(na), textcolor=dc, size=size.tiny, tooltip=nwWarnTip) : na
    if keep
        nwMarks.push(NewsMark.new(d, tx, na, p, atHi, bar_index, nwWarnS, nwWarnE))
    keep

// Live candle: a temporary dot (rolled back every tick). Closed candle: kept.
if newsWarn and (news_dot or news_lbl)
    f_nwMake(barstate.isconfirmed)

if barstate.isconfirmed and timeframe.isintraday
    // Background: shade the window of the newest mark (or start one when the
    // warning candle was missed).
    if nwInWin and news_bg and (na(nwKillE) or time >= nwKillE)
        NewsMark m = na
        if nwMarks.size() > 0
            m := nwMarks.last()
        if na(m) or time >= m.wE
            m := NewsMark.new(na, na, na, na, true, bar_index, nwWinS, nwWinE)
            nwMarks.push(m)
        if na(m.bg)
            m.bg := box.new(time, high, nwEnd, low, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(color.orange, 85))
        else
            m.bg.set_right(nwEnd)
            m.bg.set_top(math.max(m.bg.get_top(), high))
            m.bg.set_bottom(math.min(m.bg.get_bottom(), low))
    // Deletion: a later candle takes the dot -> dot, label and background go together.
    if news_del and nwMarks.size() > 0
        for i = nwMarks.size() - 1 to 0
            NewsMark m = nwMarks.get(i)
            if not na(m.price) and bar_index > m.bar
                bool hit = news_del_mode == "Touch" ? (m.atHi ? high >= m.price : low <= m.price) : (m.atHi ? close > m.price : close < m.price)
                if hit
                    if not na(m.wE)
                        nwKillE := na(nwKillE) ? m.wE : math.max(nwKillE, m.wE)
                    label.delete(m.dot)
                    label.delete(m.txt)
                    box.delete(m.bg)
                    nwMarks.remove(i)
    // Caps: dots + labels share one count, backgrounds have their own.
    int nDot = 0
    int nBg  = 0
    if nwMarks.size() > 0
        for i = nwMarks.size() - 1 to 0
            NewsMark m = nwMarks.get(i)
            if not na(m.dot) or not na(m.txt)
                nDot += 1
                if nDot > news_max
                    label.delete(m.dot)
                    label.delete(m.txt)
                    m.dot := na
                    m.txt := na
            if not na(m.bg)
                nBg += 1
                if nBg > news_bg_max
                    box.delete(m.bg)
                    m.bg := na
            if na(m.dot) and na(m.txt) and na(m.bg) and time >= m.wE
                nwMarks.remove(i)
'''

# ─────────────────────────────────────────────────────────────── STRUCTURE TIMEFRAME (HTF in LTF)
TF_INPUTS = '''grp_tf          = "{grp}"
tfMode          = input.string("Manual", "Structure Timeframe Mode", options=["Manual", "Auto Combination"], group=grp_tf, tooltip="HTF in LTF: the structure (swings / boxes / PO4s, breaks, gate) is built on the STRUCTURE timeframe and drawn on your chart.\\nManual = the timeframe below (empty = chart timeframe).\\nAuto Combination = chart timeframe × 4 or × 6 (M15 chart -> H1 or H1:30).\\nOnly CLOSED structure candles are used: no repaint.")
autoMultiplier  = input.string("4x", "Auto Multiplier", options=["4x", "6x"], group=grp_tf)
structTimeframe = input.timeframe("", "Structure Timeframe", group=grp_tf, tooltip="Empty = chart timeframe.")
showTfLabel     = input.bool(true, "Structure TF in Labels (H1 CDL…)", group=grp_tf)
'''

TF_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// STRUCTURE TIMEFRAME — last CLOSED structure candle ([1] + lookahead_on).
// On the chart timeframe the candle is read directly (no delay).
// ═══════════════════════════════════════════════════════════════
f_get_auto_tf(string _tf, string _multStr) =>
    int mult = _multStr == "4x" ? 4 : 6
    int tf_sec = timeframe.in_seconds(_tf)
    string res = _tf
    if not na(tf_sec)
        int tf_mins = math.round(tf_sec / 60)
        if tf_sec < 60
            res := str.tostring(tf_sec * mult) + "S"
        else if tf_mins < 1440
            res := str.tostring(tf_mins * mult)
        else if tf_mins == 1440
            res := str.tostring(mult) + "D"
        else if tf_mins == 10080
            res := str.tostring(mult) + "W"
        else
            res := str.tostring(mult) + "M"
    res

f_tfName(string t) =>
    string s = str.length(t) == 0 ? timeframe.period : t
    switch s
        "1"   => "M1"
        "3"   => "M3"
        "5"   => "M5"
        "15"  => "M15"
        "30"  => "M30"
        "45"  => "M45"
        "60"  => "H1"
        "120" => "H2"
        "180" => "H3"
        "240" => "H4"
        "360" => "H6"
        "480" => "H8"
        "720" => "H12"
        => s

string blockTF     = tfMode == "Auto Combination" ? f_get_auto_tf(timeframe.period, autoMultiplier) : (structTimeframe == "" ? timeframe.period : structTimeframe)
bool   blockSameTF = timeframe.in_seconds(blockTF) <= timeframe.in_seconds(timeframe.period)
string TFP         = showTfLabel and not blockSameTF ? f_tfName(blockTF) + " " : ""

// Structure candle: OHLCV, its history, a close-location delta and its RVOL.
f_blockNow() =>
    float rg = high - low
    float v  = nz(volume)
    float dl = rg > 0 ? v * ((close - low) - (high - close)) / rg : 0.0
    float av = ta.sma(v, 20)[1]
    float rv = nz(av) > 0 ? v / av : 0.0
    [time, open, high, low, close, v, high[1], low[1], high[2], low[2], open[1], close[1], time[1], dl, rv]

f_blockPrev() =>
    [t0, o0, h0, l0, c0, v0, ph0, pl0, ph2, pl2, po0, pc0, pt0, dl0, rv0] = f_blockNow()
    [t0[1], o0[1], h0[1], l0[1], c0[1], v0[1], ph0[1], pl0[1], ph2[1], pl2[1], po0[1], pc0[1], pt0[1], dl0[1], rv0[1]]

[n_t, n_o, n_h, n_l, n_c, n_v, n_h1, n_l1, n_h2, n_l2, n_o1, n_c1, n_t1, n_dl, n_rv] = f_blockNow()
[s_t, s_o, s_h, s_l, s_c, s_v, s_h1, s_l1, s_h2, s_l2, s_o1, s_c1, s_t1, s_dl, s_rv] = request.security(syminfo.tickerid, blockTF, f_blockPrev(), lookahead=barmerge.lookahead_on)
[g_hi_htf, g_lo_htf] = request.security(syminfo.tickerid, blockTF, f_gatePrev(), lookahead=barmerge.lookahead_on)
[g_hi_now, g_lo_now] = f_gateNow()

int   bT  = blockSameTF ? n_t  : s_t
float bO  = blockSameTF ? n_o  : s_o
float bH  = blockSameTF ? n_h  : s_h
float bL  = blockSameTF ? n_l  : s_l
float bC  = blockSameTF ? n_c  : s_c
float bV  = blockSameTF ? n_v  : s_v
float bH1 = blockSameTF ? n_h1 : s_h1
float bL1 = blockSameTF ? n_l1 : s_l1
float bH2 = blockSameTF ? n_h2 : s_h2
float bL2 = blockSameTF ? n_l2 : s_l2
float bO1 = blockSameTF ? n_o1 : s_o1
float bC1 = blockSameTF ? n_c1 : s_c1
int   bT1 = blockSameTF ? n_t1 : s_t1
float bDl = blockSameTF ? n_dl : s_dl
float bRv = blockSameTF ? n_rv : s_rv
float bVp = bRv * 100
float gHi = blockSameTF ? g_hi_now : g_hi_htf
float gLo = blockSameTF ? g_lo_now : g_lo_htf

var int prevBlockT = 0
bool newBlock = not na(bT) and bT != prevBlockT
prevBlockT := nz(bT, prevBlockT)
bool stepNow = barstate.isconfirmed and newBlock
'''

# ─────────────────────────────────────────────────────────────── OUTSIDE-RANGE ALLOCATOR
RANGE_INPUTS = '''grp_rng      = "{grp}"
maxLines     = input.int(10, "Max Items Outside the 🟢🟩 Range", minval=0, maxval=200, group=grp_rng, tooltip="Everything between the highest and lowest 🟢🟩🔴🟥 marker is ALWAYS drawn.\\nOutside that range only this many items are drawn, split 50 / 50 between bull and bear, newest first. A PO4 with its break and its zone (husband & wife) counts as ONE.\\n0 = ZERO: nothing outside the range — no line, label or box — except what sits on the candle of the highest / lowest marker.\\nPriority outside: PO4s first, then the other structure, then the overlays.")
showLiveAlways = input.bool(true, "Always Show the Live Range (P# / R# / forming box)", group=grp_rng, tooltip="ON: the levels of the range price is trading in right now always show, even outside the marker range.\\nOFF: they follow the rule above like everything else.")
'''

RANGE_HELPERS = '''// ═══════════════════════════════════════════════════════════════
// OUTSIDE-RANGE ALLOCATOR — inside the marker range = always drawn; outside =
// a 50 / 50 bull / bear budget, newest first. q = [bull left, bear left].
// ═══════════════════════════════════════════════════════════════
f_inR(float p, float hi, float lo) =>
    not na(hi) and not na(lo) and not na(p) and p <= hi + f_eps() and p >= lo - f_eps()

f_boxInR(float top, float bot, float hi, float lo) =>
    not na(hi) and not na(lo) and top <= hi + f_eps() and bot >= lo - f_eps()

// Items born on the candle of the highest / lowest marker (one STRUCTURE candle
// = spanMs wide) are allowed even with Max = 0.
f_onMarker(int t, int hiT, int loT, int spanMs) =>
    int w = math.max(nz(spanMs), 1)
    not na(t) and ((not na(hiT) and t >= hiT and t < hiT + w) or (not na(loT) and t >= loT and t < loT + w))

f_quota() =>
    int qBull = int(math.ceil(maxLines / 2.0))
    array.from(qBull, maxLines - qBull)

f_take(array<int> q, bool inside, bool isBull) =>
    bool ok = inside
    if not ok
        int k = isBull ? 0 : 1
        if q.get(k) > 0
            q.set(k, q.get(k) - 1)
            ok := true
    ok
'''

# ─────────────────────────────────────────────────────────────── BC FLOW + VOLATILITY STOP TABLE
STATS_INPUTS = '''grp_st  = "{grp}"
st_on   = input.bool(true, "BC Flow & Volatility Table", inline="st", group=grp_st, tooltip="Counts, on the CHART timeframe, how body closes (BC) follow each other, and gives the volatility stop in points (S6) next to the fixed stop (S0).")
st_pos  = input.string("Bottom Right", "", options=["Top Left", "Top Center", "Top Right", "Middle Left", "Middle Right", "Bottom Left", "Bottom Center", "Bottom Right"], inline="st", group=grp_st)
st_sz   = input.string("Small", "", options=["Tiny", "Small", "Normal"], inline="st", group=grp_st)
st_atr  = input.int(14, "ATR Length", minval=1, group=grp_st)
st_fix  = input.float(0.0, "Fixed Stop Points (0 = Auto: NQ 50 / ES 20)", minval=0.0, step=0.25, group=grp_st)
'''

STATS_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// BC FLOW STATS (chart timeframe) + VOLATILITY STOP (S6) IN POINTS
//  run          = BCs in one direction until the first opposite BC
//  pure run     = BCs in a row with NO NBC between
//  flip         = an opposite BC · continuation = a same-side BC after an NBC pause
// Index 0 = bull runs, 1 = bear runs.
// ═══════════════════════════════════════════════════════════════
var int stDir   = 0
var int stPure  = 0
var int stRun   = 0
var int stNbc   = 0
var int stConts = 0
var array<float> stPureFlipS = array.from(0.0, 0.0)
var array<int>   stPureFlipN = array.from(0, 0)
var array<float> stPureNbcS  = array.from(0.0, 0.0)
var array<int>   stPureNbcN  = array.from(0, 0)
var array<float> stRunS      = array.from(0.0, 0.0)
var array<int>   stRunN      = array.from(0, 0)
var array<float> stNbcFlipS  = array.from(0.0, 0.0)
var array<int>   stNbcFlipN  = array.from(0, 0)
var array<float> stNbcContS  = array.from(0.0, 0.0)
var array<int>   stNbcContN  = array.from(0, 0)
var array<float> stContS     = array.from(0.0, 0.0)
var array<int>   stImmFlip   = array.from(0, 0)

f_stAdd(array<float> s, array<int> n, int k, float v) =>
    s.set(k, s.get(k) + v)
    n.set(k, n.get(k) + 1)

if barstate.isconfirmed and bar_index > 0
    int sd = close > high[1] ? 1 : close < low[1] ? -1 : 0
    int sk = stDir == 1 ? 0 : 1
    if sd == 0
        if stDir != 0
            if stNbc == 0 and stPure > 0
                f_stAdd(stPureNbcS, stPureNbcN, sk, stPure)
            stNbc  += 1
            stPure := 0
    else if stDir == 0
        stDir   := sd
        stPure  := 1
        stRun   := 1
        stNbc   := 0
        stConts := 0
    else if sd == stDir
        if stNbc > 0
            f_stAdd(stNbcContS, stNbcContN, sk, stNbc)
            stConts += 1
            stPure  := 1
        else
            stPure += 1
        stRun += 1
        stNbc := 0
    else
        if stNbc == 0
            f_stAdd(stPureFlipS, stPureFlipN, sk, stPure)
            stImmFlip.set(sk, stImmFlip.get(sk) + 1)
        f_stAdd(stRunS, stRunN, sk, stRun)
        f_stAdd(stNbcFlipS, stNbcFlipN, sk, stNbc)
        stContS.set(sk, stContS.get(sk) + stConts)
        stDir   := sd
        stPure  := 1
        stRun   := 1
        stNbc   := 0
        stConts := 0

float stAtrV  = ta.atr(st_atr)
float stFixV  = st_fix > 0 ? st_fix : str.contains(syminfo.root, "NQ") ? 50.0 : str.contains(syminfo.root, "ES") ? 20.0 : na

f_stAvg(array<float> s, array<int> n, int k) =>
    n.get(k) > 0 ? str.tostring(s.get(k) / n.get(k), "#.##") + "  (" + str.tostring(n.get(k)) + ")" : "—"

f_stPos(string p) =>
    switch p
        "Top Left"      => position.top_left
        "Top Center"    => position.top_center
        "Top Right"     => position.top_right
        "Middle Left"   => position.middle_left
        "Middle Right"  => position.middle_right
        "Bottom Left"   => position.bottom_left
        "Bottom Center" => position.bottom_center
        => position.bottom_right

var table stTbl = table.new(f_stPos(st_pos), 3, 14, bgcolor=#000000, frame_color=color.new(color.white, 70), frame_width=1, border_color=color.new(color.white, 85), border_width=1)
if barstate.islast and st_on
    string sz = st_sz == "Tiny" ? size.tiny : st_sz == "Normal" ? size.normal : size.small
    color  hd = #e1b31a
    color  wt = color.white
    color  bu = #27ffc3
    color  be = #c77dff
    table.cell(stTbl, 0, 0, "MMM BC FLOW · " + f_tfName(timeframe.period), text_color=hd, text_size=sz)
    table.cell(stTbl, 1, 0, "BULL runs", text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 0, "BEAR runs", text_color=be, text_size=sz)
    table.cell(stTbl, 0, 1, "Pure run → opposite BC: avg BCs (n)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 1, f_stAvg(stPureFlipS, stPureFlipN, 0), text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 1, f_stAvg(stPureFlipS, stPureFlipN, 1), text_color=be, text_size=sz)
    table.cell(stTbl, 0, 2, "Pure run → first NBC: avg BCs (n)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 2, f_stAvg(stPureNbcS, stPureNbcN, 0), text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 2, f_stAvg(stPureNbcS, stPureNbcN, 1), text_color=be, text_size=sz)
    table.cell(stTbl, 0, 3, "Run with NBC pauses → flip: avg BCs (n)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 3, f_stAvg(stRunS, stRunN, 0), text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 3, f_stAvg(stRunS, stRunN, 1), text_color=be, text_size=sz)
    table.cell(stTbl, 0, 4, "NBCs before a FLIP: avg (n)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 4, f_stAvg(stNbcFlipS, stNbcFlipN, 0), text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 4, f_stAvg(stNbcFlipS, stNbcFlipN, 1), text_color=be, text_size=sz)
    table.cell(stTbl, 0, 5, "NBCs before a CONTINUATION: avg (n)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 5, f_stAvg(stNbcContS, stNbcContN, 0), text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 5, f_stAvg(stNbcContS, stNbcContN, 1), text_color=be, text_size=sz)
    table.cell(stTbl, 0, 6, "Continuations per run: avg", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 6, stRunN.get(0) > 0 ? str.tostring(stContS.get(0) / stRunN.get(0), "#.##") : "—", text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 6, stRunN.get(1) > 0 ? str.tostring(stContS.get(1) / stRunN.get(1), "#.##") : "—", text_color=be, text_size=sz)
    table.cell(stTbl, 0, 7, "Flip straight after a BC (no NBC): %", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 7, stRunN.get(0) > 0 ? str.tostring(stImmFlip.get(0) * 100.0 / stRunN.get(0), "#.#") + "%" : "—", text_color=bu, text_size=sz)
    table.cell(stTbl, 2, 7, stRunN.get(1) > 0 ? str.tostring(stImmFlip.get(1) * 100.0 / stRunN.get(1), "#.#") + "%" : "—", text_color=be, text_size=sz)
    table.cell(stTbl, 0, 8, "ATR(" + str.tostring(st_atr) + ") = average candle range, pts", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 8, str.tostring(stAtrV, format.mintick), text_color=wt, text_size=sz)
    table.merge_cells(stTbl, 1, 8, 2, 8)
    table.cell(stTbl, 0, 9, "S6 volatility stop 1.0 / 1.5 / 2.0 × ATR, pts", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 9, str.tostring(stAtrV, "#.##") + " / " + str.tostring(stAtrV * 1.5, "#.##") + " / " + str.tostring(stAtrV * 2.0, "#.##"), text_color=color.orange, text_size=sz)
    table.merge_cells(stTbl, 1, 9, 2, 9)
    table.cell(stTbl, 0, 10, "S0 fixed stop, pts (1:2 target)", text_color=wt, text_size=sz, text_halign=text.align_left)
    table.cell(stTbl, 1, 10, na(stFixV) ? "set it in the inputs" : str.tostring(stFixV, "#.##") + "  →  TP " + str.tostring(stFixV * 2, "#.##"), text_color=color.orange, text_size=sz)
    table.merge_cells(stTbl, 1, 10, 2, 10)
    table.cell(stTbl, 0, 11, "Run = BCs one way until the first opposite BC · Pure = no NBC between · Flip = opposite BC · Continuation = same-side BC after an NBC pause · (n) = how many counted", text_color=color.silver, text_size=size.tiny, text_halign=text.align_left)
    table.merge_cells(stTbl, 0, 11, 2, 11)
'''

TN_INPUT = '''show_tn_step = input.bool(true, "Trend Markers 🟢🟩 / 🔴🟥", group=grp_rng, tooltip="🟢 / 🔴 = T1 of the newest leg (where it started).\\n🟩 / 🟥 = the newest T# of that leg.")
'''

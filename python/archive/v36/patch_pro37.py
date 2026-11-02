import sys, re
sys.path.insert(0, '/home/claude/v36')
import modules as M
from build import fmt

src = open('/home/claude/v36/MMM_Pro_36regen.pine').read()

def rep(old, new, count=1, s=None):
    global src
    tgt = src if s is None else s
    c = tgt.count(old)
    if c != count:
        print("FAIL", c, old[:300]); sys.exit(1)
    out = tgt.replace(old, new)
    if s is None:
        src = out
    return out

def del_line(prefix):
    global src
    i0 = src.find(prefix); assert i0 >= 0, prefix
    i1 = src.find('\n', i0)
    src = src[:i0] + src[i1 + 1:]

# ── header
rep('indicator("MMM Pro @MaxMaserati", overlay=true', 'indicator("MMM Pro @MaxMaserati 3.7", "MMM Pro 3.7", overlay=true')
rep('''//   🟢 / 🔴 = T1 of the newest leg · 🟩 / 🟥 = its newest T#. Every line
//   between the highest and lowest marker is ALWAYS drawn; the max line
//   settings only count lines OUTSIDE that range.''', '''//   🟢 / 🔴 = T1 of the newest leg · 🟩 / 🟥 = its newest T#. Everything
//   between the highest and lowest marker is ALWAYS drawn; outside it only
//   "Max Items" show (50 / 50 bull / bear, newest first, a PO4 + its break
//   + its zone = ONE). 0 = nothing outside except on the marker candles.
//   HTF in LTF: the state machine runs on the STRUCTURE timeframe (closed
//   candles only) and is drawn on the chart. Voids stay on the chart TF.''')

# ── inputs
rep('// ─── 1. GENERAL ───', fmt(M.TF_INPUTS, grp="0. Structure Timeframe (HTF in LTF)") + '\n// ─── 1. GENERAL ───')
rep('t1_width         = input.int(3, "T1   Width"', 't1_width         = input.int(2, "PO4 T1   Width"')
rep('t1_size          = input.string("normal", "Label"', 't1_size          = input.string("small", "Label"')
rep('tn_width         = input.int(2, "T2+  Width"', 'tn_width         = input.int(1, "PO4 T2+  Width"')
rep('tn_size          = input.string("small", "Label", options=["tiny","small","normal","large"], inline="tnsty", group=grp_tier)',
    '''tn_size          = input.string("tiny", "Label", options=["tiny","small","normal","large"], inline="tnsty", group=grp_tier)
cd_width         = input.int(2, "CDS / CDL  Width", minval=1, maxval=5, inline="cdsty", group=grp_tier, tooltip="FLIP breaks (capital CDS / CDL): their break line width and label size. Lowercase internal cds / cdl stay tiny.")
cd_size          = input.string("small", "Label", options=["tiny","small","normal","large"], inline="cdsty", group=grp_tier)
ld_width         = input.int(1, "LD / SD  Width", minval=1, maxval=5, inline="ldsty", group=grp_tier, tooltip="CONTINUATION breaks (LD / SD): their break line width and label size.")
ld_size          = input.string("tiny", "Label", options=["tiny","small","normal","large"], inline="ldsty", group=grp_tier)''')
del_line('max_orig_lines   = input.int(')
del_line('max_cont_lines   = input.int(')
rep('// ─── 6. eBLOCKS / iBLOCKS ───', '// ─── 5. MAX ITEMS OUTSIDE THE RANGE ───\n' + fmt(M.RANGE_INPUTS, grp="5. Lines · Max Outside the 🟢🟩 Range") + '\n// ─── 6. eBLOCKS / iBLOCKS ───')
rep('zone_transp    = input.int(85, "Transparency", minval=0, maxval=100, inline="zn", group=grp_zone)\n',
    '''zone_transp    = input.int(85, "Transparency", minval=0, maxval=100, inline="zn", group=grp_zone)
eblk_size      = input.string("small", "eBlock  Label Size", options=["tiny","small","normal","large"], inline="ebs", group=grp_zone, tooltip="eBlock (flip zone) name size.")
iblk_size      = input.string("tiny", "iBlock  Label Size", options=["tiny","small","normal","large"], inline="ibs", group=grp_zone, tooltip="iBlock (continuation zone) name size.")
''')
i0 = src.find('news_del_mode = input.string('); i1 = src.find('\n', i0)
src = src[:i1 + 1] + '\n' + fmt(M.STATS_INPUTS, grp="12. BC Flow & Volatility Stop") + src[i1 + 1:]

# ── structure timeframe module replaces the chart-TF gate read
rep('[gHi, gLo] = f_gateNow()\n', M.TF_ENGINE + '\n')

# ── types: visibility memory for voids, label size / border for zones
rep('''    box[]  slices
    bool[] sliceTouched
''', '''    box[]  slices
    bool[] sliceTouched
    bool   greyed = false
    bool   dim    = false
    int    t      = 0
''')
rep('''    string blockName     // drawn STRICTLY INSIDE the box via box.new(text=...)
    float  volPct
''', '''    string blockName     // drawn STRICTLY INSIDE the box via box.new(text=...)
    float  volPct
    string tsz = "tiny"
''')


# ════════ 3.7b: Edge gate, solid width-1 pullback / resumption lines, all PO4 blocks kept ════════
rep('p1_width         = input.int(2, "P1   Width"', 'p1_width         = input.int(1, "P1   Width"')
rep('p1_line_style    = input.string("Dashed", "Style"', 'p1_line_style    = input.string("Solid", "Style"')
rep('pn_width         = input.int(2, "P2+  Width"', 'pn_width         = input.int(1, "P2+  Width"')
rep('pn_line_style    = input.string("Dashed", "Style"', 'pn_line_style    = input.string("Solid", "Style"')
rep('max_zones        = input.int(5, "Max Blocks Drawn", minval=0, maxval=500, group=grp_zones, tooltip="Only the newest N blocks are drawn. 0 = no limit.")',
    'max_zones        = input.int(0, "Max Blocks Drawn (cap)", minval=0, maxval=500, group=grp_zones, tooltip="0 = no cap: every eBlock / iBlock lives as long as its PO4 (husband & wife).\\nA number = only the newest N blocks are drawn (the older blocks are removed, their PO4 stays).")')
rep('        bool flipPass = not gateOn or (newSide == 1 ? hitXD : hitXP)', '        bool flipPass = true   // MMM Pro Edge: a flip is structure, never gated')
rep('        bool contPass = not gateOn or (mainSide == 1 ? (bullImp and bullPb) : (bearImp and bearPb))', '        bool contPass = true   // gated before: a small p can never make an LD / SD')
rep('            bool gPass = not gateOn or (side == 1 ? hitXD : hitXP)', '            bool gPass = true')
rep('''f_eps() => math.max(syminfo.mintick * 0.51, 1e-5)
''', '''f_eps() => math.max(syminfo.mintick * 0.51, 1e-5)

// GATE (MMM Pro Edge): which P# / R# node the gate has confirmed (time + price key).
var int   pConfT = na
var float pConfP = na
var int   rConfT = na
var float rConfP = na
f_isPConf(Node n) =>
    not gateOn or (not na(n) and not na(pConfT) and n.t == pConfT and math.abs(n.price - pConfP) <= f_eps())
f_isRConf(Node n) =>
    not gateOn or (not na(n) and not na(rConfT) and n.t == rConfT and math.abs(n.price - rConfP) <= f_eps())
f_gTxt(string t, bool ok, string tag) =>
    ok ? t : TFP + str.lower(str.substring(t, str.length(TFP))) + tag
f_gCol(color c, bool ok) =>
    ok ? c : color.new(c, 40)
''')
rep('''                bullPb := true

    // TWO-WAY CANDLE''', '''                bullPb := true

    // MMM PRO EDGE GATE: the P# stays a small p until the leg reached its own
    // extreme and THEN the pullback reached the OPPOSITE extreme. A close past a
    // small p deletes it (no LD / SD). pConfBefore = the state before this candle.
    Node gPn = na
    if mainSide == 1
        gPn := beStatic
    else if mainSide == -1
        gPn := buStatic
    bool pConfBefore = f_isPConf(gPn)
    if gateOn and not na(gPn) and not pConfBefore and not na(gHi) and not na(gLo)
        if (mainSide == 1 and bullImp and gLo <= 20) or (mainSide == -1 and bearImp and gHi >= 80)
            pConfT := gPn.t
            pConfP := gPn.price
            // as in MMM Pro Edge: only an R formed AFTER the confirmation counts
            if primaryResumptionDone
                if mainSide == 1
                    buStatic := na
                else
                    beStatic := na
                primaryResumptionDone := false
                firstRShiftDone       := false

    // TWO-WAY CANDLE''')
rep('''    bool ldAbsorbed = ldRaw and pb_absorb_filter and not beStatic.isGap and not beStatic.delivered and not primaryResumptionDone
    bool sdAbsorbed = sdRaw and pb_absorb_filter and not buStatic.isGap and not buStatic.delivered and not primaryResumptionDone''',
'''    bool ldGateKill = ldRaw and gateOn and not pConfBefore
    bool sdGateKill = sdRaw and gateOn and not pConfBefore
    bool ldAbsorbed = (ldRaw and pb_absorb_filter and not beStatic.isGap and not beStatic.delivered and not primaryResumptionDone) or ldGateKill
    bool sdAbsorbed = (sdRaw and pb_absorb_filter and not buStatic.isGap and not buStatic.delivered and not primaryResumptionDone) or sdGateKill''')
rep('''        if ldAbsorbed
            beStatic := na
            primaryPullbackDone := false
            firstPShiftDone     := false
        if sdAbsorbed
            buStatic := na
            primaryPullbackDone := false
            firstPShiftDone     := false''', '''        if ldAbsorbed
            beStatic := na
            primaryPullbackDone := false
            firstPShiftDone     := false
            // GATE: a small p closed through -> its small r goes with it (R needs a confirmed P#)
            if ldGateKill and primaryResumptionDone
                buStatic := na
                primaryResumptionDone := false
                firstRShiftDone       := false
        if sdAbsorbed
            buStatic := na
            primaryPullbackDone := false
            firstPShiftDone     := false
            if sdGateKill and primaryResumptionDone
                beStatic := na
                primaryResumptionDone := false
                firstRShiftDone       := false''')
rep('''    // ── STEP 6: Husband & Wife — delete any Tn individually violated.''', '''    // MMM PRO EDGE GATE: the R# stays a small r until a CDL (bull) / CDS (bear)
    // prints while it is alive, with the P# already confirmed.
    if gateOn and primaryResumptionDone
        Node gRn = na
        Node gPc = na
        if mainSide == 1
            gRn := buStatic
            gPc := beStatic
        else if mainSide == -1
            gRn := beStatic
            gPc := buStatic
        if not na(gRn) and not f_isRConf(gRn) and f_isPConf(gPc) and (mainSide == 1 ? cdlFired : cdsFired)
            rConfT := gRn.t
            rConfP := gRn.price

    // ── STEP 6: Husband & Wife — delete any Tn individually violated.''')

# ── split the confirmed block: voids (chart TF) / structure (structure TF)
L = src.split('\n')
def find(pred, start=0):
    for i in range(start, len(L)):
        if pred(L[i]): return i
    raise Exception('not found')
c  = find(lambda s: s == 'if barstate.isconfirmed' and True)
assert L[c + 2].strip().startswith('// GATE MEMORY'), L[c + 2]
v  = find(lambda s: s.strip() == '// STRUCTURAL VOIDS ENGINE (ORIGINAL — untouched)', c) - 1
s1 = find(lambda s: s.strip().startswith('// STEP 1: gap-confirm'), c) - 1
r  = find(lambda s: s.startswith('// RENDER — runs once'), c) - 1
A = L[c + 1:v]; V = L[v:s1]; B = L[s1:r]

# void-only definitions, read on the CHART candles
VOIDDEF_NAMES = ['udg_min', 'bullUdg', 'bearUdg', 'bull_gap_top', 'bull_gap_bot', 'bull_ulg_now', 'bull_uog_now', 'bear_gap_top', 'bear_gap_bot', 'bear_ulg_now', 'bear_uog_now']
vdefs = []
for s in A:
    m = re.match(r'^\s+(?:float|bool)\s+(\w+)\s*=', s)
    if m and m.group(1) in VOIDDEF_NAMES:
        vdefs.append(s)
assert len(vdefs) == len(VOIDDEF_NAMES), vdefs

HIST = {'high[1]': 'bH1', 'low[1]': 'bL1', 'high[2]': 'bH2', 'low[2]': 'bL2', 'open[1]': 'bO1', 'close[1]': 'bC1', 'time[1]': 'bT1'}
CUR = {'open': 'bO', 'high': 'bH', 'low': 'bL', 'close': 'bC', 'time': 'bT'}
def xform_code(code):
    for k, val in HIST.items():
        code = code.replace(k, val)
    assert not re.search(r'\b(open|high|low|close|time|volume)\s*\[', code), code
    code = re.sub(r'(?<![\.\w])(open|high|low|close|time)(?![\w\(])', lambda m: CUR[m.group(1)], code)
    code = re.sub(r'\bg_volPct\b', 'bVp', code)
    assert 'bar_index' not in code, code
    return code
def xform_line(s):
    # code part only (comments untouched), strings untouched
    ci = None
    inq = False
    for i, ch in enumerate(s):
        if ch == '"': inq = not inq
        if not inq and s[i:i + 2] == '//':
            ci = i; break
    code, com = (s, '') if ci is None else (s[:ci], s[ci:])
    parts = re.split(r'("[^"]*")', code)
    parts = [p if p.startswith('"') else xform_code(p) for p in parts]
    return ''.join(parts) + com

A2 = [xform_line(s) for s in A]
B2 = [xform_line(s) for s in B]

# voids: memory of the colour state so the range rule can hide / restore them
Vt = '\n'.join(V)
Vt = Vt.replace('creationBar=bar_index,', 'creationBar=bar_index, t=time,')
assert Vt.count('t=time,') == 6, Vt.count('t=time,')
Vt = rep('''                    if not u.stoppedExtending and not isSlicedLoop and not na(u.mid) and low<=u.mid
                        u.stoppedExtending := true
''', '''                    if not u.stoppedExtending and not isSlicedLoop and not na(u.mid) and low<=u.mid
                        u.stoppedExtending := true
                        u.greyed := true
''', s=Vt)
Vt = rep('''                    if not u.stoppedExtending and not isSlicedLoop and not na(u.mid) and high>=u.mid
                        u.stoppedExtending := true
''', '''                    if not u.stoppedExtending and not isSlicedLoop and not na(u.mid) and high>=u.mid
                        u.stoppedExtending := true
                        u.greyed := true
''', s=Vt)
Vt = rep('''            if newlyTouched and not isSlicedLoop
                if not u.stoppedExtending
''', '''            if newlyTouched and not isSlicedLoop
                if not u.stoppedExtending
                    u.dim := true
''', s=Vt)

new_block = ['if stepNow'] + A2 + B2 + [
    '',
    '// ═══════════════════════════════════════════════════════════════════════════',
    '// STRUCTURAL VOIDS — chart timeframe, closed candles (not part of the',
    '// structure, so they stay on your chart candles).',
    '// ═══════════════════════════════════════════════════════════════════════════',
    'if barstate.isconfirmed'] + vdefs + [''] + Vt.split('\n')
L = L[:c] + new_block + L[r:]
src = '\n'.join(L)
rep('''// CONFIRMED BAR — waterfall (Armor Rule 1): gap-confirm → evaluate breaks →
// resolve → assign this candle → lifetime sweeps.''', '''// CONFIRMED STRUCTURE CANDLE — waterfall (Armor Rule 1): gap-confirm →
// evaluate breaks → resolve → assign this candle → lifetime sweeps.
// HTF in LTF: it runs once per CLOSED structure candle (bO / bH / bL / bC).''')

# ── render
i0 = src.find('// RENDER — runs once on the last bar.')
i0 = src.rfind('\n', 0, i0 - 2) + 1
i1 = src.find('// CANDLE COLORING: Structural Delta Bias')
i1 = src.rfind('\n', 0, i1 - 2) + 1
R = src[i0:i1]

R = rep('''f_inRange(float p, float hi, float lo) =>
    not na(hi) and not na(lo) and p <= hi + f_eps() and p >= lo - f_eps()
''', M.RANGE_HELPERS + '''
f_inRange(float p, float hi, float lo) =>
    not na(hi) and not na(lo) and p <= hi + f_eps() and p >= lo - f_eps()

// A live-range level (P# / R#, MC / GMC, MP / GMP, urgency): always drawn when
// "Always Show the Live Range" is ON, else only inside the range or on the
// marker candle.
f_liveOk(float p, int t, float rHi, float rLo, int hiT, int loT, int spanMs) =>
    showLiveAlways or f_inR(p, rHi, rLo) or f_onMarker(t, hiT, loT, spanMs)

// Void shown / hidden by the range rule, restored to the colour it had.
f_proGapPaint(GapBox u, bool vis) =>
    color hid = color.new(#000000, 100)
    color gl  = color.new(#636363, 60)
    color gb  = color.new(#636363, 85)
    if u.slices.size() > 0
        for j = 0 to u.slices.size() - 1
            color sb = u.sliceTouched.get(j) ? col_partial : (u.gType == "ULG" ? color.new(u.origBorder, 60) : u.origBg)
            box.set_bgcolor(u.slices.get(j), vis ? sb : hid)
    else
        if u.gType == "ULG"
            box.set_border_color(u.b, vis ? (u.greyed ? gl : u.dim ? color.new(u.origBorder, 80) : u.origBorder) : hid)
        else
            box.set_bgcolor(u.b, vis ? (u.greyed ? gb : u.dim ? color.new(u.origBg, 85) : u.origBg) : hid)
    if not na(u.l)
        line.set_color(u.l, vis ? (u.greyed ? gl : u.dim ? color.new(u.origLine, 80) : u.origLine) : hid)
    if not na(u.lbl)
        label.set_textcolor(u.lbl, vis ? (u.greyed or u.dim ? color.new(u.origLblText, 70) : u.origLblText) : hid)
''', s=R)
# husband checks follow the same live-range rule
R = rep('f_slotDrawn(int gT, float gP) =>', 'f_slotDrawn(int gT, float gP, float rHi, float rLo, int hiT, int loT, int spanMs) =>', s=R)
R = rep('''        d := d or show_gmc_lines
    d
''', '''        d := d or show_gmc_lines
    d and f_liveOk(gP, gT, rHi, rLo, hiT, loT, spanMs)
''', s=R)
R = rep('''f_pDrawn(ShiftMarker sm) =>
    Node a = sm.side == -1 ? beStatic : buStatic
    bool pRole = (sm.side == -1 and mainSide == 1) or (sm.side == 1 and mainSide == -1)
    f_pAnchorAlive(sm) and pRole and show_gmp_lines and f_pullbackVisible(a)''', '''f_pDrawn(ShiftMarker sm, float rHi, float rLo, int hiT, int loT, int spanMs) =>
    Node a = sm.side == -1 ? beStatic : buStatic
    bool pRole = (sm.side == -1 and mainSide == 1) or (sm.side == 1 and mainSide == -1)
    f_pAnchorAlive(sm) and pRole and show_gmp_lines and f_pullbackVisible(a) and not na(a) and f_liveOk(a.price, a.t, rHi, rLo, hiT, loT, spanMs)''', s=R)

# markers with their candle times
R = rep('''    float starBullP = na
    float starBearP = na
    float lastBullP = na
    float lastBearP = na
    if poLines.size() > 0
        for mIdx = poLines.size() - 1 to 0
            POLine mp = poLines.get(mIdx)
            if mp.side == 1
                if na(lastBullP)
                    lastBullP := mp.price
                if mp.tier == 1 and na(starBullP)
                    starBullP := mp.price
            else
                if na(lastBearP)
                    lastBearP := mp.price
                if mp.tier == 1 and na(starBearP)
                    starBearP := mp.price
    float rHi = na
    float rLo = na
    for pv in array.from(starBullP, lastBullP, starBearP, lastBearP)
        if not na(pv)
            rHi := na(rHi) ? pv : math.max(rHi, pv)
            rLo := na(rLo) ? pv : math.min(rLo, pv)
''', '''    float starBullP = na
    float starBearP = na
    float lastBullP = na
    float lastBearP = na
    int   starBullT = na
    int   starBearT = na
    int   lastBullT = na
    int   lastBearT = na
    if poLines.size() > 0
        for mIdx = poLines.size() - 1 to 0
            POLine mp = poLines.get(mIdx)
            if mp.side == 1
                if na(lastBullP)
                    lastBullP := mp.price
                    lastBullT := mp.t
                if mp.tier == 1 and na(starBullP)
                    starBullP := mp.price
                    starBullT := mp.t
            else
                if na(lastBearP)
                    lastBearP := mp.price
                    lastBearT := mp.t
                if mp.tier == 1 and na(starBearP)
                    starBearP := mp.price
                    starBearT := mp.t
    float rHi = na
    float rLo = na
    int   hiT = na
    int   loT = na
    array<float> mkP = array.from(starBullP, lastBullP, starBearP, lastBearP)
    array<int>   mkT = array.from(starBullT, lastBullT, starBearT, lastBearT)
    for k = 0 to 3
        float pv = mkP.get(k)
        if not na(pv)
            if na(rHi) or pv > rHi
                rHi := pv
                hiT := mkT.get(k)
            if na(rLo) or pv < rLo
                rLo := pv
                loT := mkT.get(k)
    int spanMs = timeframe.in_seconds(blockTF) * 1000
    array<int> q = f_quota()   // [bull left, bear left] outside the range
''', s=R)

# PO4s: inside / on the marker candle always, outside from the 50 / 50 budget
R = rep('''        int outN = 0
        for plIdx = poLines.size() - 1 to 0
            POLine pl = poLines.get(plIdx)
            bool inR  = f_inRange(pl.price, rHi, rLo)
            bool take = inR or outN < max_orig_lines
            if take and not inR
                outN += 1
            bool hidden = pl.po4_touched and po4_trig_mode == "Hide"
            if take and not hidden
''', '''        for plIdx = poLines.size() - 1 to 0
            POLine pl = poLines.get(plIdx)
            bool hidden = pl.po4_touched and po4_trig_mode == "Hide"
            bool take   = not hidden and f_take(q, f_inR(pl.price, rHi, rLo) or f_onMarker(pl.t, hiT, loT, spanMs), pl.side == 1)
            if take
''', s=R)
R = rep('''string txt = (pl.side == 1 ? "BuPO4" : "BePO4")''', '''string txt = TFP + (pl.side == 1 ? "BuPO4" : "BePO4")''', s=R)
R = rep('''string ct       = f_eng(pl.official ? pl.causeText : str.lower(pl.causeText))''', '''string ct       = TFP + f_eng(pl.official ? pl.causeText : str.lower(pl.causeText))''', s=R)
R = rep('''drawn_lines.push(line.new(pl.causeT, pl.causePrice, causeEnd, pl.causePrice, xloc=xloc.bar_time, color=uc, width=1,''',
        '''drawn_lines.push(line.new(pl.causeT, pl.causePrice, causeEnd, pl.causePrice, xloc=xloc.bar_time, color=uc, width=pl.causeMajor ? (isLdSd ? ld_width : cd_width) : 1,''', s=R)
R = rep('''size=f_sz(pl.causeMajor ? ld_sd_size : "tiny")''', '''size=f_sz(not pl.causeMajor ? "tiny" : isLdSd ? ld_size : cd_size)''', s=R)
R = rep('''                    f_pushZone(temp_zones, pl.c_time, lineEnd, pl.c_high, pl.c_low, pl.c_open, pl.c_close, pl.side == 1, pl.side == 1 ? zone_pel_col : zone_pes_col, f_zoneName(not plIsLdSd, pl.side == 1, ENGT), pl.c_volPct)
''', '''                    f_pushZone(temp_zones, pl.c_time, lineEnd, pl.c_high, pl.c_low, pl.c_open, pl.c_close, pl.side == 1, pl.side == 1 ? zone_pel_col : zone_pes_col, TFP + f_zoneName(not plIsLdSd, pl.side == 1, ENGT), pl.c_volPct)
                    RenderZone rzN = temp_zones.last()
                    rzN.tsz := plIsLdSd ? iblk_size : eblk_size
''', s=R)

# standalone CDS / CDL: with their husband, then the 50 / 50 budget
R = rep('''        int smOut = 0
        for smIdx''', '''        for smIdx''', s=R)
R = rep('''            bool husband = sm.pMarried ? f_pDrawn(sm) : isGuard ? true : (f_inList(poT, poP, sm.guardianT, sm.guardianPrice) or f_slotDrawn(sm.guardianT, sm.guardianPrice))''',
        '''            bool husband = sm.pMarried ? f_pDrawn(sm, rHi, rLo, hiT, loT, spanMs) : isGuard ? true : (f_inList(poT, poP, sm.guardianT, sm.guardianPrice) or f_slotDrawn(sm.guardianT, sm.guardianPrice, rHi, rLo, hiT, loT, spanMs))''', s=R)
R = rep('''            if not f_inRange(sm.price, rHi, rLo)
                if smOut >= max_cont_lines
                    continue
                smOut += 1
''', '''            if not f_take(q, f_inR(sm.price, rHi, rLo) or f_onMarker(sm.ownerT, hiT, loT, spanMs) or f_onMarker(sm.breakT, hiT, loT, spanMs), sm.side == 1)
                continue
''', s=R)
R = rep('''drawn_lines.push(line.new(sm.ownerT, sm.price, sm.breakT, sm.price, xloc=xloc.bar_time, color=useCol, width=1, style=line.style_solid))''',
        '''drawn_lines.push(line.new(sm.ownerT, sm.price, sm.breakT, sm.price, xloc=xloc.bar_time, color=useCol, width=sm.isInternal ? 1 : cd_width, style=line.style_solid))''', s=R)
R = rep('''f_eng(sm.markerTxt), xloc=xloc.bar_time, textcolor=useCol, color=color(na), style=sm.side == 1 ? label.style_label_down : label.style_label_up, size=f_sz(sm.isInternal ? "tiny" : orig_size)))''',
        '''TFP + f_eng(sm.markerTxt), xloc=xloc.bar_time, textcolor=useCol, color=color(na), style=sm.side == 1 ? label.style_label_down : label.style_label_up, size=f_sz(sm.isInternal ? "tiny" : cd_size)))''', s=R)

# live-range levels
out = []
for s in R.split('\n'):
    m = re.match(r'^    if (.*\bnot na\((beStatic|buStatic|buDynRaw|buDynGap|beDynRaw|beDynGap|buCtlRaw|buCtlGap|beCtlRaw|beCtlGap)\).*)$', s)
    if m:
        n = m.group(2)
        s = s + ' and f_liveOk(%s.price, %s.t, rHi, rLo, hiT, loT, spanMs)' % (n, n)
    m2 = re.match(r'^        if (ant_(bull|bear)_active and ant(Bull|Bear)PhaseOk.*)$', s)
    if m2:
        sd = m2.group(2)
        s = s + ' and f_liveOk(ant_%s_price, ant_%s_t, rHi, rLo, hiT, loT, spanMs)' % (sd, sd)
    m3 = re.match(r'^        if not na\(tc_(bull|bear)_lvl\)$', s)
    if m3:
        sd = m3.group(1)
        s = s + ' and f_liveOk(tc_%s_lvl, tc_%s_t, rHi, rLo, hiT, loT, spanMs)' % (sd, sd)
    out.append(s)
R = '\n'.join(out)
assert R.count('f_liveOk(') >= 16, R.count('f_liveOk(')
R = R.replace('f_add_level(fn.price, fn.lbl,', 'f_add_level(fn.price, TFP + fn.lbl,')
n_before = R.count('f_apply_naming(')
R = re.sub(r'(f_add_level\([^,]+, )f_apply_naming\(', r'\1TFP + f_apply_naming(', R)


# GATE naming + solid width-1 pullback / resumption lines
R = rep('''TFP + f_apply_naming(f_staticText(beStatic, beStatic.isForced ? "NBC Forced" : "BeX", true, curTier)), mc_bear_col, isP1 ? p1_width : pn_label_hdr ? pn_width : 2, isP1 ? f_ln_style(p1_line_style) : pn_label_hdr ? f_ln_style(pn_line_style) : line.style_dashed,''',
        '''f_gTxt(TFP + f_apply_naming(f_staticText(beStatic, beStatic.isForced ? "NBC Forced" : "BeX", true, curTier)), f_isPConf(beStatic), " · p"), f_gCol(mc_bear_col, f_isPConf(beStatic)), isP1 ? p1_width : pn_label_hdr ? pn_width : 1, isP1 ? f_ln_style(p1_line_style) : pn_label_hdr ? f_ln_style(pn_line_style) : line.style_solid,''', s=R)
R = rep('''TFP + f_apply_naming(f_staticText(buStatic, buStatic.isForced ? "NBC Forced" : "BuX", true, curTier)), mc_bull_col, isP1 ? p1_width : pn_label_hdr ? pn_width : 2, isP1 ? f_ln_style(p1_line_style) : pn_label_hdr ? f_ln_style(pn_line_style) : line.style_dashed,''',
        '''f_gTxt(TFP + f_apply_naming(f_staticText(buStatic, buStatic.isForced ? "NBC Forced" : "BuX", true, curTier)), f_isPConf(buStatic), " · p"), f_gCol(mc_bull_col, f_isPConf(buStatic)), isP1 ? p1_width : pn_label_hdr ? pn_width : 1, isP1 ? f_ln_style(p1_line_style) : pn_label_hdr ? f_ln_style(pn_line_style) : line.style_solid,''', s=R)
R = rep('''TFP + f_apply_naming(f_staticText(buStatic, "BuX", false, curTier)), mc_bull_col, 2, line.style_dotted,''',
        '''f_gTxt(TFP + f_apply_naming(f_staticText(buStatic, "BuX", false, curTier)), not primaryResumptionDone or f_isRConf(buStatic), " · r"), f_gCol(mc_bull_col, not primaryResumptionDone or f_isRConf(buStatic)), 1, line.style_solid,''', s=R)
R = rep('''TFP + f_apply_naming(f_staticText(beStatic, "BeX", false, curTier)), mc_bear_col, 2, line.style_dotted,''',
        '''f_gTxt(TFP + f_apply_naming(f_staticText(beStatic, "BeX", false, curTier)), not primaryResumptionDone or f_isRConf(beStatic), " · r"), f_gCol(mc_bear_col, not primaryResumptionDone or f_isRConf(beStatic)), 1, line.style_solid,''', s=R)
assert R.count('pbRole ? line.style_dashed : line.style_dotted') == 4
R = R.replace('pbRole ? line.style_dashed : line.style_dotted', 'line.style_solid')
R, nCtl = re.subn(r'1, line\.style_dotted, (bu|be)(CtlRaw|CtlGap)\.t', r'1, line.style_solid, \1\2.t', R)
assert nCtl == 4, nCtl
R = rep('''    f_draw_groups()
''', '''    f_draw_groups()
    f_xdxpDraw()
''', s=R)

# zone label size / border
R = rep('''drawn_zones.push(box.new(left_edge, rz.z_top, futureZone, rz.z_bot, xloc=xloc.bar_time, border_color=na, bgcolor=rz.bg_col, text=zone_show_name ? rz.blockName : "", text_color=txtCol, text_size=size.tiny,''',
        '''drawn_zones.push(box.new(left_edge, rz.z_top, futureZone, rz.z_bot, xloc=xloc.bar_time, border_color=na, bgcolor=rz.bg_col, text=zone_show_name ? rz.blockName : "", text_color=txtCol, text_size=f_sz(rz.tsz),''', s=R)

# voids follow the range rule (lowest priority)
R = rep('''    // ─── eBLOCK / iBLOCK BOXES ───
''', '''    // ─── STRUCTURAL VOIDS: inside / marker candle always, outside from the budget ───
    if visual_gaps.size() > 0
        for i = visual_gaps.size() - 1 to 0
            GapBox u = visual_gaps.get(i)
            f_proGapPaint(u, f_take(q, f_boxInR(u.top, u.bot, rHi, rLo) or f_onMarker(u.t, hiT, loT, spanMs), u.isBull))

    // ─── eBLOCK / iBLOCK BOXES ───
''', s=R)

src = src[:i0] + M.STATS_ENGINE + '\n' + fmt(M.XDXP_ENGINE, bull='mc_bull_col', bear='mc_bear_col') + '\n' + R + src[i1:]
for bad in ['max_orig_lines', 'max_cont_lines', 'ld_sd_size', 'orig_size)', 'g_volPct = ']:
    if bad in src and bad != 'g_volPct = ':
        print('LEFTOVER', bad, [m.start() for m in re.finditer(re.escape(bad), src)][:5])
open('/home/claude/v36/MMM_Pro_3.7.pine', 'w').write(src)
print('ok', src.count('\n'))

import sys, re
sys.path.insert(0, '/home/claude/v36')
import modules as M
from build import fmt

L = open('/home/claude/v35/pro_orig.pine').read().split('\n')
edits = []   # (start, end, expect_start_substr, expect_end_substr, replacement_text or None)

def cut(a, b, s_exp, e_exp, rep=None):
    edits.append((a, b, s_exp, e_exp, rep))

# ── inputs
cut(46, 46, 'show_ent         = input.bool(true,  "Entry Lines"', 'show_ent')
cut(51, 51, 'hvc_enable', 'hvc_enable')
cut(82, 107, '// ─── 5. ENTRY LINES ───', '', None)
cut(108, 122, '// ─── 6. eBLOCKS / iBLOCKS ───', 'max_zones', '''// ─── 6. eBLOCKS / iBLOCKS ───
''' + fmt(M.ZONE_INPUTS, grp="6. eBlocks / iBlocks").replace('grp_zone       = "6. eBlocks / iBlocks"', 'grp_zone       = "6. eBlocks / iBlocks"\ngrp_zones      = grp_zone') + '''zone_gmc         = input.bool(false, "XU iBlock  (Extreme Urgency — GMC)", group=grp_zones, tooltip="Drawn on gap-confirmed momentum levels (GMC / GMCR).")
zone_mc          = input.bool(false, "U iBlock  (Urgency — MC)", group=grp_zones, tooltip="Drawn on raw body closes (MC / MCR) not yet gap-confirmed.")
zone_show_vol    = input.bool(false, "Volume Strength", group=grp_zones, tooltip="Adds a label on the block's edge with the anchor candle's relative volume, e.g. \\"Strong: 180% 🔥\\".")
zone_ext         = input.int(7, "Block Extension (Candles)", minval=0, maxval=100, group=grp_zones)
zone_calc_basis  = input.string("High/Low", "Calculation Basis", options=["High/Low", "Open/Close (Body)"], group=grp_zones, tooltip="Whether the block divides the full wick range or only the candle body. Depth and Premium / Discount side are set in group 9.")
show_50_line     = input.bool(false, "50% Line", inline="50_line", group=grp_zones)
line_50_style    = input.string("Dashed", "", options=["Solid", "Dashed", "Dotted"], inline="50_line", group=grp_zones)
line_50_width    = input.int(1, "Width", minval=1, maxval=10, inline="50_line", group=grp_zones)
max_zones        = input.int(5, "Max Blocks Drawn", minval=0, maxval=500, group=grp_zones, tooltip="Only the newest N blocks are drawn. 0 = no limit.")''')
cut(155, 167, 'hvc_show_ultra', 'hvc_max_bars', fmt(M.GATE_INPUTS, grp="9. Gate · Premium / Discount", gate_tf="") + '\n' + fmt(M.HTF_INPUTS, grp="10. HTF Bias (HTF in LTF)", eng_default="Candle c (PO4)", pos_default="Top Right") + '\n' + fmt(M.NEWS_INPUTS, grp="11. News"))
# ── derived
cut(177, 178, 'color long_ent_col', 'color short_ent_col')
cut(183, 184, 'color zone_pel_col', 'color zone_pes_col', 'color zone_pel_col  = color.new(bull_col, zone_transp)\ncolor zone_pes_col  = color.new(bear_col, zone_transp)')
cut(188, 188, 'int ent_ext', 'int ent_ext')
cut(193, 193, 'string ent_size', 'string ent_size')
cut(201, 206, '// "Max ... Drawn" of 0 = no limit.', 'bool limit_zones', '// "Max ... Drawn" of 0 = no limit (voids, blocks). Lines and markers: see the 🟢🟩 range rule.\nbool limit_gaps       = maxGaps > 0\nbool limit_zones      = max_zones > 0')
# ── types
cut(273, 298, '    // VISUAL BRIDGE', '    int    sbe_freeze_t     = na', '''    // VISUAL BRIDGE — candle OHLC for eBlocks / iBlocks.
    float  c_high           = na
    float  c_low            = na
    float  c_open           = na
    float  c_close          = na
    int    c_time           = na
    float  c_volPct         = na   // anchor candle's relative volume, for the block's volume label''')
cut(316, 318, '    // T1 only: the leg', '    float  legExt', None)
cut(326, 336, '    float  ent_price        = na', '    int    sbe_freeze_t     = na', '''    bool   po4_touched      = false
    int    po4_freeze_t     = na
    bool   official         = true    // the break that made this Tn passed the gate
    bool   against          = false   // the break went against the HTF bias''')
cut(370, 382, '// ─── SBE — Suggested Best Entry', '', None)
# ── state
cut(397, 397, 'var array<SbeLine>     sbeLines', 'sbeLines')
cut(422, 427, '// BALANCE ZONE', '', None)
cut(490, 493, 'bool alert_ent_bull', 'bool alert_sbe_bear', '''bool alert_cdl      = false
bool alert_cds      = false
bool alert_ld       = false
bool alert_sd       = false''')
cut(504, 515, '// ENTRY MATRIX', '', None)
# ── helpers
cut(714, 819, 'f_sbeStr(bool isLong) =>', '', None)
cut(840, 872, 'f_pushZone(array<RenderZone> arr', '    arr.push(RenderZone.new', '''f_pushZone(array<RenderZone> arr, int zt, int zend, float ch, float cl, float co, float cc, bool isBull, color bg, string blockName, float volPct) =>
    float calc_top = zone_calc_basis == "High/Low" ? ch : math.max(co, cc)
    float calc_bot = zone_calc_basis == "High/Low" ? cl : math.min(co, cc)
    [z_top, z_bot] = f_zoneSlice(calc_top, calc_bot, isBull)
    arr.push(RenderZone.new(zt, zend, z_top, z_bot, (z_top + z_bot) / 2, bg, isBull, calc_top, calc_bot, blockName, volPct))''')
# ── confirmed block
cut(902, 918, '    // Balance zone this candle broke out of', '', None)
cut(1171, 1180, '    float bu_void_mid', '', None)
cut(1198, 1201, '            if show_ent and ePbXU', '                f_armOrg(buStatic, true)')
cut(1217, 1218, '            if show_ent and not eTrXU', '                f_copyEnt(buCtlRaw, buCtlGap)')
cut(1221, 1222, '            if show_ent and eTrXU', '                f_armEnt(buCtlGap')
cut(1229, 1232, '            // bull static: P# in a bear trend', '                f_armEnt(buStatic')
cut(1245, 1248, '            if show_ent and ePbXU', '                f_armOrg(beStatic, false)')
cut(1260, 1261, '            if show_ent and not eTrXU', '                f_copyEnt(beCtlRaw, beCtlGap)')
cut(1264, 1265, '            if show_ent and eTrXU', '                f_armEnt(beCtlGap')
cut(1271, 1274, '            // bear static: P# in a bull trend', '                f_armEnt(beStatic')
cut(1439, 1439, '        float nS = not na(promoted) ? promoted.sbe_price', 'bzBrkHi)')
cut(1441, 1445, '        // LEG EXTREME for the Best Entry Zone', '        float legX', None)
cut(1524, 1529, '        if show_ent and eTrO', '            f_armSbe(nS, newPrice, newSide == 1, newTime)')
cut(1575, 1587, '        // The carried node\'s ROLE changed', '                f_armEnt(beCtlRaw, beCtlRaw.c_high, na, beCtlRaw.c_open, false)')
cut(1603, 1603, '        float nS = not na(promoted) ? promoted.sbe_price', 'bzBrkHi)')
cut(1627, 1632, '        if show_ent and eTrO', '            f_armSbe(nS, newPrice, mainSide == 1, newTime)')
cut(1730, 1733, '            // Genesis has no old trend origin', '            float gLegX', None)
cut(1748, 1754, '            if show_ent and eTrO', '                f_armSbe(gS, open, side == 1, time)')
cut(1818, 1821, '                if show_ent and ePbU', '                    f_armOrg(buStatic, true)')
cut(1834, 1837, '                if show_ent and eCtU', '                    f_armOrg(buStatic, true)')
cut(1849, 1850, '                if show_ent and eTrU', '                    f_armEnt(buCtlRaw, low, na, open, true)')
cut(1861, 1864, '                if show_ent and ePbU', '                    f_armOrg(beStatic, false)')
cut(1875, 1878, '                if show_ent and eCtU', '                    f_armOrg(beStatic, false)')
cut(1886, 1887, '                if show_ent and eTrU', '                    f_armEnt(beCtlRaw, high, na, open, false)')
cut(1897, 1900, '        if show_ent and ePbU', '            f_armOrg(beStatic, false)')
cut(1907, 1910, '        if show_ent and ePbU', '            f_armOrg(buStatic, true)')
cut(2053, 2054, '    while sbeLines.size() > max_history', '        sbeLines.remove(0)')
cut(2088, 2158, '    // ═══', '', None)
cut(2160, 2161, '    // cause marker dies with it automatically', '    // A live T1 also extends its leg extreme', '    // cause marker dies with it automatically (fields on the same record). ──')
cut(2168, 2169, '                if pl.tier == 1 and not na(pl.legExt)', '                    pl.legExt :=')
# ── render (whole section) + coloring + alerts
cut(2175, 2604, '// ═══', 'alertcondition(alert_gmc_bear', None)

# sanity + apply bottom-up
edits.sort(key=lambda e: e[0], reverse=True)
prev = None
for a, b, s_exp, e_exp, rep in edits:
    if prev is not None:
        assert b < prev, ("overlap", a, b, prev)
    prev = a
    first = L[a - 1]; last = L[b - 1]
    if s_exp and s_exp not in first:
        print("START MISMATCH", a, repr(first), repr(s_exp)); sys.exit(1)
    if e_exp and e_exp not in last:
        print("END MISMATCH", b, repr(last), repr(e_exp)); sys.exit(1)
    new = [] if rep is None else rep.rstrip('\n').split('\n')
    L[a - 1:b] = new

src = '\n'.join(L)

def rep(old, new, count=1):
    global src
    c = src.count(old)
    if c != count:
        print("FAIL count=%d for:\n%s" % (c, old[:500])); sys.exit(1)
    src = src.replace(old, new)

# remove the SBE arguments from every Node.new
src, n = re.subn(r', sbe_price=[A-Za-z0-9_.]+\)', ')', src)
print('sbe args removed', n)
src, n2 = re.subn(r', legExt=[A-Za-z]+,', ',', src)
print('legExt args removed', n2)

# ── header
rep('''// STATE MACHINE (transplanted verbatim in behaviour):''', '''// MMM FOUNDATION — this is the CANDLE engine "c":
//   Flip         = CDLc / CDSc (the T1 reversal)
//   Continuation = LDc1, LDc2… / SDc1, SDc2… (count runs until the next flip)
//   Gate (NO GATE / MMPD 27 / MMPD fast / MMPD Delta) decides which breaks
//   are OFFICIAL. A failed break keeps its PO4 (✗), sends no alert, no block.
//   🟢 / 🔴 = T1 of the newest leg · 🟩 / 🟥 = its newest T#. Every line
//   between the highest and lowest marker is ALWAYS drawn; the max line
//   settings only count lines OUTSIDE that range.
//   No entries, no stops: see the MMM Indicator Test Plan.
//
// STATE MACHINE (transplanted verbatim in behaviour):''')
rep('''max_history      = input.int(40, "Memory Guard (Max Structures Kept)"''', '''eng_tag          = input.bool(true, "Engine Tag  (CDLc / CDSc / LDc / SDc)", group=grp_gen, tooltip="Adds the engine letter to every break and PO4 so you always know which MMM engine made it.\\nc = Candle engine (MMM Pro) · x = Zone engine (Concepts Pro+) · s = Swing engine (Order Flow Suite).")
max_history      = input.int(40, "Memory Guard (Max Structures Kept)"''')
rep('''label_naming_scheme = input.string("MC / GMC / MP / GMP", "Label Naming",''', '''label_naming_scheme = input.string("MC / GMC / MP / GMP", "Label Naming",''')
rep('''tooltip="Master colors. Used by PO4 origins, GMC / MC / GMP / MP levels, LD / SD markers, entry lines, urgency lines and eBlocks / iBlocks.")''', '''tooltip="Master colors. Used by PO4 origins, GMC / MC / GMP / MP levels, LD / SD markers, urgency lines and eBlocks / iBlocks.")''')
rep('''line_ext         = input.int(13, "Line Extension (Candles)", minval=0, maxval=50, group=grp_gen, tooltip="How far EVERY level line extends to the right of the current bar: PO4, GMC, MC, GMP, MP, entries and urgency lines. eBlocks / iBlocks have their own length in group 6.")''', '''line_ext         = input.int(13, "Line Extension (Candles)", minval=0, maxval=50, group=grp_gen, tooltip="How far EVERY level line extends to the right of the current bar: PO4, GMC, MC, GMP, MP and urgency lines. eBlocks / iBlocks have their own length in group 6.")''')
rep('''size_marker      = input.string("small", "Marker Label Size", options=["tiny","small","normal","large"], group=grp_gen, tooltip="Label size for CDS / CDL, LD / SD, entry and urgency labels.")''', '''size_marker      = input.string("small", "Marker Label Size", options=["tiny","small","normal","large"], group=grp_gen, tooltip="Label size for CDS / CDL, LD / SD and urgency labels.")''')
rep('''max_orig_lines   = input.int(10, "Max PO4 Lines Drawn", minval=0, maxval=500, group=grp_tier, tooltip="Only the newest N origins are drawn. 0 = no limit. This only hides older lines — it never deletes an origin or its CDS / CDL.")''', '''max_orig_lines   = input.int(10, "Max PO4 Lines Outside the 🟢🟩 Range", minval=0, maxval=500, group=grp_tier, tooltip="PO4 lines between the highest and lowest 🟢🟩🔴🟥 marker are ALWAYS drawn, with their CDS / CDL / LD / SD.\\nThis number only counts the PO4 lines OUTSIDE that range (newest first). 0 = none outside.\\nIt only hides lines — it never deletes an origin or its break.")''')
rep('''max_cont_lines   = input.int(5, "Max CDS / CDL Markers & Guardians Drawn", minval=0, maxval=500, group=grp_lvl, tooltip="Only the newest N standalone CDS / CDL markers and forced guardians are drawn. 0 = no limit.")''', '''max_cont_lines   = input.int(5, "Max CDS / CDL Markers Outside the 🟢🟩 Range", minval=0, maxval=500, group=grp_lvl, tooltip="Standalone CDS / CDL markers between the highest and lowest 🟢🟩🔴🟥 marker are ALWAYS drawn.\\nThis number only counts the markers OUTSIDE that range (newest first). 0 = none outside.\\nA marker is only drawn when its husband (P#, R#, PO4 or Forced guardian) is drawn, and a guardian only when one of its markers is drawn: no widows, no orphans.")''')

# ── shared modules after the alert flags
rep('''bool alert_sd       = false
''', '''bool alert_sd       = false

''' + M.GATE_ENGINE + '\n' + M.ZONE_HELPERS + '\n' + M.ZONE_ENGINE + '\n' + fmt(M.HTF_ENGINE, htf_grow='true') + '\n' + M.NEWS_ENGINE + '''
[gHi, gLo] = f_gateNow()
var bool legOfficial = true   // the break that made the current Tn passed the gate
string ENGT = eng_tag ? "c" : ""

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

f_xuName(bool gap, bool isBull) =>
    string b = zone_naming == "eBlock / iBlock" ? (gap ? "MMM XU iBlock" : "MMM U iBlock") : zone_naming == "External / Internal Entry Zone" ? (gap ? "XU Internal Entry Zone" : "U Internal Entry Zone") : (gap ? "XU Continuation Zone" : "U Continuation Zone")
    b + (isBull ? " L" : " S")
''')

# ── gate memory at the top of each confirmed bar
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

# ── reversal gate
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
rep('''isForced=tForced, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV)''', '''isForced=tForced, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV, official=flipPass, against=f_againstHtf(newSide))''')
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
# ── continuation gate
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
rep('''isForced=tForced2, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV)''', '''isForced=tForced2, c_high=nH, c_low=nL, c_open=nO, c_close=nC, c_time=nT, c_volPct=nV, official=contPass, against=f_againstHtf(mainSide))''')
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
# ── genesis gate
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
rep('''isForced=gForced, c_high=high, c_low=low, c_open=open, c_close=close, c_time=time, c_volPct=curVolPct)''', '''isForced=gForced, c_high=high, c_low=low, c_open=open, c_close=close, c_time=time, c_volPct=curVolPct, official=gPass, against=f_againstHtf(side))''')
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

src = src.rstrip('\n') + '\n' + open('/home/claude/v36/pro_render.pine').read().replace('//@@HTF_TABLE@@', fmt(M.HTF_TABLE, bull_col='bull_col', bear_col='bear_col'))
open('/home/claude/v36/MMM_Pro_3.6.pine', 'w').write(src)
print("ok", src.count('\n'))

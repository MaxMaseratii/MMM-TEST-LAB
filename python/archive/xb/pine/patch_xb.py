src = open('xb_orig.pine').read()
L = src.split('\n')

INPUTS = r'''grp_xb      = "8. Xpander Block (XB) · XBS / XBB · FVA"
xb_on       = input.bool(true, "XB Engine", group=grp_xb, tooltip="XB = Xpander Block, read on the STRUCTURE timeframe (closed candles only).\n• It starts when an NBC prints after a body close (BC). The XB high / low = the last high / low from the BC to the NBCs (it grows with wicks in G1).\n• It lives until a candle CLOSES above the XB high (bullish break) or below the XB low (bearish break).\n• Balanced Zone = the top / bottom of the opens / closes of the candles after the BC. Most buying and selling happens there. Never buy or sell inside it.\n• XBB = Balanced top → XB high (the upper zone: sell area).\n• XBS = XB low → Balanced bottom (the lower zone: buy area).\n• On the break: XBS / XBB are deleted, the XB box is hidden, a break line is drawn, and the FVA of the first NBC is kept until a close goes through it.\nTested (NQ 2022–25 + MNQ 2026, 50 pt stop, 1:2): the Balanced Zone was the WORST place to trade on every timeframe. XBS / XBB and the FVA are maps, not entries: no entry passed in both periods.")
xb_box      = input.bool(true, "XB Box (live)", inline="xb1", group=grp_xb)
xb_zones    = input.bool(true, "XBS / XBB Boxes", inline="xb1", group=grp_xb)
xb_bal      = input.bool(false, "Balanced Zone Box", inline="xb2", group=grp_xb, tooltip="Off by default: the XBS / XBB boxes already show where the Balanced Zone ends.")
xb_balLn    = input.bool(false, "Balanced Top / Bottom Lines", inline="xb2", group=grp_xb)
xb_hlLn     = input.bool(false, "XB High / Low Lines", inline="xb3", group=grp_xb, tooltip="Off by default: the XB high / low usually become a PO4 T# / P# / R# of the engine.")
xb_oldBox   = input.bool(false, "Broken XB Boxes", inline="xb3", group=grp_xb)
xb_oldMax   = input.int(3, "Max Broken XB Boxes", minval=0, maxval=30, group=grp_xb)
xb_brkLn    = input.bool(true, "Break Line + Label", inline="xb4", group=grp_xb, tooltip="A line at the broken XB edge, from the BC candle to the break candle. A dotted line joins it to the BC candle high / low (the hidden XB box start).\nCAPITAL (CDLx / CDSx / LDx# / SDx#) = the same close also made that engine event.\nsmall letters (dotted line) = an internal break: cdlx / cdsx = against the current trend · ldx / sdx = with it.")
xb_brkMax   = input.int(6, "Max", minval=0, maxval=50, inline="xb4", group=grp_xb)
xb_fva      = input.bool(true, "BuFVA / BeFVA (until broken)", inline="xb5", group=grp_xb, tooltip="BeFVA (bearish break) = the first NBC of the block, from its body bottom to its high.\nBuFVA (bullish break) = the first NBC, from its low to its body top.\nIt stays until a candle CLOSES through it (BeFVA: above its top · BuFVA: below its bottom).\nTested: about 80% of breaks come back to touch the FVA (about half within 5 candles; after a GMU break only 30% within 5 candles).\nWhen the touch candle CLOSES BACK OUT, the zone held (1h: a limit at the edge made +0.45R / +0.56R). When it CLOSES INSIDE, the FVA broke within 20 candles about 70% of the time. You only know this at the close: entering after it gave no edge.")
xb_fvaMax   = input.int(3, "Max per Side", minval=0, maxval=30, inline="xb5", group=grp_xb)
xb_txt      = input.bool(true, "Names Inside Boxes", inline="xb6", group=grp_xb)
xb_transp   = input.int(85, "Transparency", minval=0, maxval=100, inline="xb6", group=grp_xb)
c_xbs       = input.color(#14b8a6, "XBS", inline="xbc", group=grp_xb)
c_xbb       = input.color(#9c27b0, "XBB", inline="xbc", group=grp_xb)
c_xbal      = input.color(#9c27b0, "Balanced", inline="xbc", group=grp_xb)
c_fvaBu     = input.color(#14b8a6, "BuFVA", inline="xbf", group=grp_xb)
c_fvaBe     = input.color(#9c27b0, "BeFVA", inline="xbf", group=grp_xb)

grp_gmu     = "9. GMU · Gap Momentum Urgency"
gmu_on      = input.bool(true, "Last BuGMU / BeGMU", inline="gm1", group=grp_gmu, tooltip="MU = Momentum Urgency (a body close). GMU = Gap Momentum Urgency (old name GMC): candle 2 is a body close and candle 3 leaves a gap with candle 1 (bull: c3 low above c1 high).\nDrawn: the gap (c1 → c3) and the GMU OPEN line (= c2 open), for the last bull and the last bear GMU on the structure timeframe.\nGMU break = a later CLOSE through the GMU open.\nTested with the XB: when the XB break candle itself becomes a GMU (55–60% of breaks), the FVA comes back later (30% within 5 candles vs 70%) and lives longer. Entering once the gap is confirmed gave no edge.\nGMU ladder test: the C3 range beat the 3-candle range, and the C1 range was the worst. The only GMU that held in both periods: 15m with c3 = AFs against (avg +0.08R, 50 pt stop, 1:2).")
gmu_gap     = input.bool(true, "Gap Box", inline="gm1", group=grp_gmu)
gmu_brk     = input.bool(true, "GMU Breaks", inline="gm2", group=grp_gmu)
gmu_brkMax  = input.int(3, "Max", minval=0, maxval=20, inline="gm2", group=grp_gmu)
gmu_ticks   = input.int(2, "Min Gap (Ticks)", minval=1, maxval=50, group=grp_gmu)
'''

LOGIC = r'''
// ═══════════════════════════════════════════════════════════════
// XPANDER BLOCK (XB) + FVA + GMU — structure timeframe, closed candles.
//  XB      = expander BC + the candles that close back inside its high / low.
//  Balanced Zone = highest / lowest open-close of the candles after the BC.
//  XBB     = Balanced top → XB high · XBS = XB low → Balanced bottom.
//  Break   = a close above the XB high / below the XB low.
//  BeFVA   = first NBC body bottom → its high · BuFVA = first NBC low → its body top.
//  GMU     = c2 body close + gap between c1 and c3. GMU break = a close through the c2 open.
// ═══════════════════════════════════════════════════════════════
type XBlk
    float  h
    float  l
    float  bt
    float  bb
    int    t1
    int    tN
    int    dir
    int    t2
    int    brk
    string kind
    float  fo
    float  fc
    float  fh
    float  fl
    float  bch
    float  bcl

type XFva
    float top
    float bot
    int   t1
    int   dir

type XGmu
    float op
    float g1
    float g2
    int   t1
    int   dir
    int   tb

var bool         xbWait  = false
var bool         xbLive  = false
var float        xExH    = na
var float        xExL    = na
var int          xExT    = na
var int          xExD    = 0
var XBlk         xbCur   = na
var array<XBlk>  xbOld   = array.new<XBlk>()
var array<XFva>  xFvas   = array.new<XFva>()
var XGmu         gmuBu   = na
var XGmu         gmuBe   = na
var array<XGmu>  gmuBrks = array.new<XGmu>()

bool ev_xbBu  = false
bool ev_xbBe  = false
bool ev_gmuBu = false
bool ev_gmuBe = false

if stepNow and xb_on and not na(bC) and not na(bH1) and not na(bL1)
    bool xbu = bC > bH1
    bool xbe = bC < bL1
    bool xbc = xbu or xbe
    // FVA life: a close through it deletes it
    if xFvas.size() > 0
        for i = xFvas.size() - 1 to 0
            XFva f = xFvas.get(i)
            if (f.dir == 1 and bC < f.bot) or (f.dir == -1 and bC > f.top)
                xFvas.remove(i)
    if xbLive
        if bC > xbCur.h or bC < xbCur.l
            int bd = bC > xbCur.h ? 1 : -1
            string kd = ""
            if eType != 0 and eDir == bd
                kd := TFP + (eType == 1 ? (bd == 1 ? "CDLx" : "CDSx") : (bd == 1 ? "LDx" : "SDx") + str.tostring(eNum))
            else
                kd := TFP + (bd == 1 ? (prevSide == 1 ? "ldx" : "cdlx") : (prevSide == -1 ? "sdx" : "cdsx"))
            xbCur.t2   := bT
            xbCur.brk  := bd
            xbCur.kind := kd
            xbOld.push(xbCur)
            while xbOld.size() > 60
                xbOld.shift()
            float fT = bd == 1 ? math.max(xbCur.fo, xbCur.fc) : xbCur.fh
            float fB = bd == 1 ? xbCur.fl : math.min(xbCur.fo, xbCur.fc)
            if fT > fB
                xFvas.push(XFva.new(fT, fB, xbCur.tN, bd))
                while xFvas.size() > 60
                    xFvas.shift()
            ev_xbBu := bd == 1
            ev_xbBe := bd == -1
            xbLive := false
            xbWait := xbc
            if xbc
                xExH := bH
                xExL := bL
                xExT := bT
                xExD := xbu ? 1 : -1
        else
            if boxGrow
                xbCur.h := math.max(xbCur.h, bH)
                xbCur.l := math.min(xbCur.l, bL)
            xbCur.bt := math.max(xbCur.bt, math.max(bO, bC))
            xbCur.bb := math.min(xbCur.bb, math.min(bO, bC))
    else if xbWait
        if xbc
            xExH := bH
            xExL := bL
            xExT := bT
            xExD := xbu ? 1 : -1
        else
            xbLive := true
            xbWait := false
            xbCur  := XBlk.new(boxGrow ? math.max(xExH, bH) : xExH, boxGrow ? math.min(xExL, bL) : xExL, math.max(bO, bC), math.min(bO, bC), xExT, bT, xExD, na, 0, "", bO, bC, bH, bL, xExH, xExL)
    else if xbc
        xbWait := true
        xExH := bH
        xExL := bL
        xExT := bT
        xExD := xbu ? 1 : -1

if stepNow and gmu_on and not na(bC) and not na(bH2) and not na(bL2) and not na(bO1) and not na(bC1) and not na(bT1)
    // GMU break: a close through the GMU open (c2 open)
    if not na(gmuBu) and bC < gmuBu.op
        gmuBu.tb := bT
        gmuBrks.push(gmuBu)
        gmuBu := na
    if not na(gmuBe) and bC > gmuBe.op
        gmuBe.tb := bT
        gmuBrks.push(gmuBe)
        gmuBe := na
    while gmuBrks.size() > 30
        gmuBrks.shift()
    float gMin = gmu_ticks * syminfo.mintick
    bool c2Bu = bC1 > bH2 or (bO1 > bH2 and not (bC1 < bL2))
    bool c2Be = bC1 < bL2 or (bO1 < bL2 and not (bC1 > bH2))
    if c2Bu and bL - bH2 >= gMin
        gmuBu := XGmu.new(bO1, bH2, bL, bT1, 1, na)
        ev_gmuBu := true
    if c2Be and bL2 - bH >= gMin
        gmuBe := XGmu.new(bO1, bL2, bH, bT1, -1, na)
        ev_gmuBe := true
'''

RENDER = r'''    // ─── XPANDER BLOCK / FVA / GMU ───
    if xb_on
        if xbLive and not na(xbCur)
            float xH  = xbCur.h
            float xL  = xbCur.l
            float xBt = math.min(xbCur.bt, xH)
            float xBb = math.max(xbCur.bb, xL)
            string dn = xbCur.dir == 1 ? "BuXB" : "BeXB"
            color  xc = xbCur.dir == 1 ? c_bull_bc : c_bear_bc
            if xb_box
                drawn_boxes.push(box.new(xbCur.t1, xH, futureT, xL, xloc=xloc.bar_time, border_color=color.new(xc, 40), bgcolor=color.new(xc, math.min(100, xb_transp + 7)), text=xb_txt ? TFP + dn : "", text_color=color.new(xc, 0), text_size=size.tiny, text_halign=text.align_center, text_valign=text.align_top))
            if xb_zones
                if xBt < xH
                    drawn_boxes.push(box.new(xbCur.tN, xH, futureT, xBt, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(c_xbb, xb_transp), text=xb_txt ? TFP + "XBB" : "", text_color=color.new(c_xbb, 0), text_size=size.tiny, text_halign=text.align_right, text_valign=text.align_center))
                if xBb > xL
                    drawn_boxes.push(box.new(xbCur.tN, xBb, futureT, xL, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(c_xbs, xb_transp), text=xb_txt ? TFP + "XBS" : "", text_color=color.new(c_xbs, 0), text_size=size.tiny, text_halign=text.align_right, text_valign=text.align_center))
            if xb_bal and xBt > xBb
                drawn_boxes.push(box.new(xbCur.tN, xBt, futureT, xBb, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(c_xbal, xb_transp), text=xb_txt ? TFP + "Balanced Zone" : "", text_color=color.new(c_xbal, 0), text_size=size.tiny, text_halign=text.align_right, text_valign=text.align_center))
            if xb_balLn
                f_add_level(xBt, TFP + "Top of Open / Close", c_xbal, 1, line.style_solid, xbCur.tN, futureT, 1, lvl_size, "Balanced Zone top")
                f_add_level(xBb, TFP + "Bottom of Open / Close", c_xbal, 1, line.style_solid, xbCur.tN, futureT, 1, lvl_size, "Balanced Zone bottom")
            if xb_hlLn
                f_add_level(xH, TFP + dn + " High", xc, 1, line.style_solid, xbCur.t1, futureT, 1, lvl_size, "XB high: a close above it = bullish break")
                f_add_level(xL, TFP + dn + " Low", xc, 1, line.style_solid, xbCur.t1, futureT, 1, lvl_size, "XB low: a close below it = bearish break")
        if xbOld.size() > 0 and (xb_oldBox or xb_brkLn)
            int nB = 0
            int nL = 0
            for i = xbOld.size() - 1 to 0
                if (not xb_oldBox or nB >= xb_oldMax) and (not xb_brkLn or nL >= xb_brkMax)
                    break
                XBlk b = xbOld.get(i)
                color bc2 = b.brk == 1 ? c_bull_po4 : c_bear_po4
                if xb_oldBox and nB < xb_oldMax
                    color oc = b.dir == 1 ? c_bull_bc : c_bear_bc
                    drawn_boxes.push(box.new(b.t1, b.h, b.t2, b.l, xloc=xloc.bar_time, border_color=color.new(oc, 60), border_style=line.style_dotted, bgcolor=color.new(oc, 93)))
                    nB += 1
                if xb_brkLn and nL < xb_brkMax
                    float bp = b.brk == 1 ? b.h : b.l
                    bool cap = str.contains(b.kind, "CD") or str.contains(b.kind, "LD") or str.contains(b.kind, "SD")
                    drawn_lines.push(line.new(b.t1, bp, b.t2, bp, xloc=xloc.bar_time, color=bc2, width=1, style=cap ? line.style_solid : line.style_dotted))
                    drawn_labels.push(label.new(int(math.avg(b.t1, b.t2)), bp, b.kind, xloc=xloc.bar_time, color=color(na), textcolor=bc2, style=b.brk == 1 ? label.style_label_down : label.style_label_up, size=f_szs(brk_size), tooltip=(b.brk == 1 ? "Bullish" : "Bearish") + " XB break" + (cap ? " = engine event" : " (internal)")))
                    float bx = b.brk == 1 ? b.bch : b.bcl
                    if not na(bx) and math.abs(bx - bp) > syminfo.mintick * 0.5
                        drawn_lines.push(line.new(b.t1, bx, b.t1, bp, xloc=xloc.bar_time, color=bc2, width=1, style=line.style_dotted))
                    nL += 1
        if xb_fva and xFvas.size() > 0
            int nBu = 0
            int nBe = 0
            for i = xFvas.size() - 1 to 0
                XFva f = xFvas.get(i)
                bool isBu = f.dir == 1
                if (isBu and nBu < xb_fvaMax) or (not isBu and nBe < xb_fvaMax)
                    color fc = isBu ? c_fvaBu : c_fvaBe
                    drawn_boxes.push(box.new(f.t1, f.top, futureT, f.bot, xloc=xloc.bar_time, border_color=na, bgcolor=color.new(fc, math.max(0, xb_transp - 5)), text=xb_txt ? TFP + (isBu ? "BuFVA" : "BeFVA") : "", text_color=color.new(fc, 0), text_size=size.tiny, text_halign=text.align_right, text_valign=text.align_center))
                    if isBu
                        nBu += 1
                    else
                        nBe += 1
                if nBu >= xb_fvaMax and nBe >= xb_fvaMax
                    break
    if gmu_on
        for g in array.from(gmuBu, gmuBe)
            if not na(g)
                bool  gBu = g.dir == 1
                color gc  = gBu ? c_bull_bc : c_bear_bc
                if gmu_gap
                    drawn_boxes.push(box.new(g.t1, math.max(g.g1, g.g2), futureT, math.min(g.g1, g.g2), xloc=xloc.bar_time, border_color=na, bgcolor=color.new(gc, 80)))
                f_add_level(g.op, TFP + (gBu ? "BuGMU" : "BeGMU"), gBu ? c_bull_po4 : c_bear_po4, 1, line.style_solid, g.t1, futureT, 2, lvl_size, "GMU open (c2 open). A close " + (gBu ? "below" : "above") + " it = GMU break.")
        if gmu_brk and gmuBrks.size() > 0
            int nG = 0
            for i = gmuBrks.size() - 1 to 0
                if nG >= gmu_brkMax
                    break
                XGmu g = gmuBrks.get(i)
                color gc = g.dir == 1 ? c_bull_po4 : c_bear_po4
                drawn_lines.push(line.new(g.t1, g.op, g.tb, g.op, xloc=xloc.bar_time, color=color.new(gc, 30), width=1, style=line.style_dotted))
                drawn_labels.push(label.new(g.tb, g.op, TFP + (g.dir == 1 ? "BuGMU✗" : "BeGMU✗"), xloc=xloc.bar_time, color=color(na), textcolor=color.new(gc, 20), style=g.dir == 1 ? label.style_label_up : label.style_label_down, size=size.tiny, tooltip="GMU break: a close through the GMU open"))
                nG += 1
'''

ALERTS = r'''alertcondition(ev_xbBu, "XB Bullish Break", "XB - close above the Xpander Block high (BuFVA created)")
alertcondition(ev_xbBe, "XB Bearish Break", "XB - close below the Xpander Block low (BeFVA created)")
alertcondition(ev_gmuBu, "BuGMU", "BuGMU - bullish gap momentum urgency")
alertcondition(ev_gmuBe, "BeGMU", "BeGMU - bearish gap momentum urgency")'''

def cut(start_pred, end_pred):
    a = next(i for i, x in enumerate(L) if start_pred(x))
    b = next(i for i in range(a, len(L)) if end_pred(L[i]))
    del L[a:b + 1]
# BC FLOW table removed (Max, Oct 30): group 8 inputs + the stats / table section
cut(lambda x: x.startswith('grp_st  = "8. BC Flow'), lambda x: x.startswith('st_hpos = '))
i_bc = next(i for i, x in enumerate(L) if x.startswith('// BC FLOW STATS'))
j_bc = next(i for i in range(i_bc, len(L)) if L[i].startswith('// XD / XP LABELS (MMM Pro Edge)'))
del L[i_bc - 1:j_bc - 1]
L[:] = [x.replace('show_eblk      = input.bool(true,', 'show_eblk      = input.bool(false,').replace('show_iblk      = input.bool(true,', 'show_iblk      = input.bool(false,') for x in L]

def find(prefix):
    idx = [i for i, x in enumerate(L) if x.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    return idx[0]

i_draw = find('    f_draw_groups()')
L[i_draw:i_draw] = RENDER.rstrip('\n').split('\n')
i_prev = find('var int         prevSide = 0')
L[i_prev + 1:i_prev + 1] = LOGIC.rstrip('\n').split('\n')
i_in = find('news_del_mode = ')
L[i_in + 1:i_in + 1] = [''] + INPUTS.rstrip('\n').split('\n')
L.append(ALERTS)
s = '\n'.join(L)
s = s.replace('indicator( "MMM PRO: Xpander Block Orderflow @MaxMaserati","MMM PRO x @MaxMaserati"', 'indicator("MMM PRO: Xpander Block Orderflow @MaxMaserati 4.0", "MMM PRO x 4.0 @MaxMaserati"')
s = s.replace('// MMM CONCEPTS PRO+ 3.7 — the ZONE engine "x" of the MMM foundation', '''// MMM PRO x 4.0 — the ZONE engine "x" of the MMM foundation
//
//  4.0 (Oct 30 2026) — NEW XPANDER BLOCK LOGIC (groups 9 and 10):
//  XB box + XBS / XBB boxes while the block lives · Balanced Zone box and
//  XB high / low lines are OFF by default · on the break: XBS / XBB deleted,
//  XB box hidden, a break line (CDSx / SDx# / CDLx / LDx# or small letters
//  for internal breaks) and the BuFVA / BeFVA of the first NBC, kept until a
//  close goes through it · the last BuGMU / BeGMU (Gap Momentum Urgency, old
//  GMC) and the GMU breaks.''')
open('MMM_PRO_x_4.0.pine', 'w').write(s)
print(s.count('\n'))

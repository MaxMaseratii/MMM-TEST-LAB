"""MMM EDGE PRO: new NQ rules for C.M4, XCS.M1 (longs) and X.M3 (Oct 30 2026 full-grid findings).
NQ / MNQ (and untested markets) use the new rules; ES, gold and crude keep the old rules (what passed there)."""
src = open('MMM_EDGE_PRO_orig.pine').read()
n_ok = 0
def rep(a, b, cnt=1):
    global src, n_ok
    k = src.count(a)
    assert k == cnt, (k, a[:90])
    src = src.replace(a, b); n_ok += 1

# ── header ──
rep("//  ½ out exits: X.M4, X.M5, C.M3, C.M4, C.M5. C.M6, C.M7 (1m level retest) and C.M8 (09:30 candle) trade full, as tested.",
    "//  NEW RULES (Oct 30 2026 · full grid of entries × stops × targets × exits, picked on NQ 2022–25, checked on MNQ 2026):\n"
    "//   · C.M4   = c3 close · stop 50 · full position · 1:6 · out at the next session open (02:00 · 08:00 · 09:30 NY).\n"
    "//   · XCS.M1 = LONGS: buy limit at MP (75% up) of the break candle, waits 10 candles · stop 50 · 1:2 full. Shorts unchanged.\n"
    "//   · X.M3   = market at the close of the 5m candle where the block is born · stop = block top − 50 · 1:2.\n"
    "//   The new rules run on NQ / MNQ. On ES, gold and crude they did NOT hold, so there the old rules stay.\n"
    "//  ½ out exits: X.M4, X.M5, C.M3, C.M5 (and C.M4 on ES / gold). C.M6, C.M7 (1m level retest) and C.M8 (09:30 candle) trade full, as tested.")

# ── market switch for the new rules ──
rep("bool   PROP  = str.startswith(exitM, \"½\")",
    "bool   PROP  = str.startswith(exitM, \"½\")\n// new rules (Oct 30 2026) on NQ / MNQ and untested markets · ES, gold, crude keep the old rules\nbool   NEWR  = MKT <= 0")

# ── tooltips ──
rep("A bullish GMC where c3 makes a new high but closes back INSIDE c2 (AFs against).\\nEntry = c3 close · Stop = 1 × ATR(14) · Half off at +0.5R, stop to entry · Runner to 1:6.\\nFilter: yesterday's daily candle bullish AND the 1h zone trend (x) bullish.\\nTested (no gate, skip 00–02) · 2022–25 → 2026 · Blended: WR 70% → 74% · 71% · avg RR +0.13 → +0.31 · +0.17 · PF 1.45 → 2.28 · 1.63 · t 2.6 / 3.3 / 3.9 · max 5 losses / 11 wins in a row.",
    "A bullish GMC where c3 makes a new high but closes back INSIDE c2 (AFs against).\\nNQ / MNQ (NEW Oct 30 2026): Entry = market at the c3 close · Stop = 50 pts below the entry · FULL position · Target 1:6 · out at the open of the next session (02:00, 08:00 or 09:30 New York) if neither hits first.\\nTested (no gate, skip 00–02) · 2022–25 → 2026 · Blended: WR 51% → 48% · 50% · avg RR +0.30 → +0.55 · +0.36 · PF 1.90 → 2.16 · 1.98 · t 4.2 / 3.2 / 5.3 · max 13 losses / 10 wins in a row.\\nOld rule (1 × ATR stop · ½ off at +0.5R · runner 1:6): WR 71% · avg RR +0.13 → +0.31 · +0.17.\\nES / gold keep the old rule (the new exit did not hold there).\\nFilter: yesterday's daily candle bullish AND the 1h zone trend (x) bullish.")
rep("A 15m candle of engine x, c or s CLOSES past P5 or later (LD5+ / SD5+, new PO4 T6+). Long and short.\\nEntry = that close · Stop = 50 pts (ES 20 · gold 12 · crude 0.50) · Target 1:2 · out after 60 candles (15 h).\\nAll hours. No MMPD, no daily filter (tested without).\\nWR 40% → 39% · 40% · avg RR +0.12 → +0.15 · +0.13 · PF 1.21 · t 3.1 · 1,172 trades.",
    "A 15m candle of engine x, c or s CLOSES past P5 or later (LD5+ / SD5+, new PO4 T6+). Long and short.\\nLONGS on NQ / MNQ (NEW Oct 30 2026): buy limit at MP of the break candle (low + 75% of its range = 25% down from the high). It waits 10 candles, fills on a touch. If the candle closed below MP, buy at the close. Stop = 50 pts below the fill · Target 1:2 · full · out after 100 candles.\\nLongs tested · 2022–25 → 2026: WR 41% → 44% · avg RR +0.19 → +0.30 · t 3.1 / 2.7 · 744 trades.\\nSHORTS (unchanged): market at the close · Stop 50 · 1:2 full · out after 60 candles. Shorts lost in 2026 (avg RR −0.05): watch.\\nES / gold / crude keep the old rule (market at the close, both sides).\\nAll hours. No MMPD, no daily filter (tested without).\\nBoth sides · Blended: WR 40% · avg RR +0.17 → +0.17 · +0.17 · PF 1.27 · t 3.3 / 1.9 / 3.9 · 1,141 trades.")
rep("Needs a 1m–5m chart. MMM PRO x on 5m candles: a bullish iBlock of a T4+ PO4 (the 3rd continuation or later).\\nEntry = buy limit at the TOP of the block the moment it is born · Stop = 50 pts (ES 20 · gold 12 · crude 0.50) · Target 1:2.\\nThe limit dies on a 5m close below the PO4 line or after 300 candles. A filled trade is out 60 candles after the block dies.\\nAll hours · long only · full trade (as tested).\\nTested: 2,272 trades · WR 41% · avg RR +0.13 · PF 1.24 · t 4.7 · max 23 losses in a row. Watch: 2026 has only Jul–Oct on 5m.",
    "Needs a 1m–5m chart. MMM PRO x on 5m candles: a bullish iBlock of a T4+ PO4 (the 3rd continuation or later).\\nNQ / MNQ (NEW Oct 30 2026): Entry = market at the CLOSE of the 5m candle where the block is born · Stop = block top − 50 pts (so the risk is a bit more than 50: about 66 on average) · Target 1:2 · out after 100 candles · full trade.\\nTested · 2022–25 → 2026 (Jul–Oct): WR 48% → 44% · avg RR +0.12 → +0.17 · PF 1.27 → 1.31 · t 4.9 / 2.3 · 2,572 trades · max 23 losses in a row · worst drawdown 52R (many trades: about 65 a month).\\nOld rule (limit at the block top): avg RR +0.12 → +0.12, t 1.5 in 2026. ES / gold / crude keep the old rule.\\nAll hours · long only.")
rep("Exit Style\", options=[\"½ Out · half at +0.5R\", \"Full · whole position\"], group=g1, tooltip=\"Prop = half the position off at +0.5R, then the stop moves to entry and the runner goes to the setup's target. This is what lifts the win rate above 60%.",
    "Exit Style\", options=[\"½ Out · half at +0.5R\", \"Full · whole position\"], group=g1, tooltip=\"Prop = half the position off at +0.5R, then the stop moves to entry and the runner goes to the setup's target. This is what lifts the win rate above 60%.\\nOn NQ / MNQ, C.M4 and XCS.M1 always trade FULL (their tested rules).")
rep("stSt  = input.string(\"Tested · ATR for X.M4 C.M3 C.M4\", \"Stop Style\", options=[\"Tested · ATR for X.M4 C.M3 C.M4\",",
    "stSt  = input.string(\"Tested · ATR for X.M4 C.M3 C.M4\", \"Stop Style\", options=[\"Tested · ATR for X.M4 C.M3 C.M4\",")  # keep the option text (saved settings)
rep("tooltip=\"Tested: X.M4 = 1.5 × ATR, C.M3 and C.M4 = 1 × ATR.",
    "tooltip=\"Tested: X.M4 = 1.5 × ATR, C.M3 = 1 × ATR, C.M4 = 1 × ATR on ES / gold only (on NQ / MNQ the new C.M4 rule always uses 50).")

# ── f_trades: session-open exit (xm 4) · XCS.M1 limit rules ──
rep("f_trades(bool prp, bool toHit, bool inAsia,", "f_trades(bool prp, bool toHit, bool sxHit, bool inAsia,")
rep("                if toHit or bar_index > t.endB\n                    code := 2\n                else\n                    bool hit = s == 1 ? low <= t.lvl - syminfo.mintick : high >= t.lvl + syminfo.mintick",
    "                if (toHit and t.k != 9) or bar_index > t.endB\n                    code := 2\n                else\n                    // XCS.M1 limit fills on a touch (as tested) · the others need 1 tick through\n                    float thr = t.k == 9 ? 0.0 : syminfo.mintick\n                    bool hit = s == 1 ? low <= t.lvl - thr : high >= t.lvl + thr")
rep("                    else if s == 1 ? high >= t.tgC : low <= t.tgC\n                        code := 2",
    "                    else if t.k != 9 and (s == 1 ? high >= t.tgC : low <= t.tgC)\n                        code := 2")
rep("            else if bar_index > t.fb\n                if toHit and t.k < 9\n                    t.nto += 1",
    "            else if bar_index > t.fb\n                // xm 4 (new C.M4): out at the open of the next session (02:00 · 08:00 · 09:30), never on the first candle after the entry\n                if t.xm == 4\n                    if sxHit and bar_index > t.fb + 1\n                        px   := open\n                        code := 1\n                        why  := 4\n                else if toHit and t.k < 9\n                    t.nto += 1")
rep("                if code == 0 and t.k >= 9 and bar_index - t.fb >= 60",
    "                if code == 0 and t.k >= 9 and bar_index - t.fb >= (t.k == 9 and t.side == 1 and NEWR ? 100 : 60)")
rep("Tr t = Tr.new(k, s, bar_index, mk ? bar_index : -1, lv, mk ? lv : na, d0, sp, rr, lv + s * rr * d0, lv + s * prq * d0, lv + s * 2.0 * d0, ddq, bar_index + 20, xm, idSeq, time_close)",
    "Tr t = Tr.new(k, s, bar_index, mk ? bar_index : -1, lv, mk ? lv : na, d0, sp, rr, lv + s * rr * d0, lv + s * prq * d0, lv + s * 2.0 * d0, ddq, bar_index + (k == 9 ? 10 : 20), xm, idSeq, time_close)")

# ── f_core: toHit without 18:00 for the session-open exit · signals ──
rep("    bool nd     = f_hitT(md, mdp, 1080)\n    bool inAsia",
    "    bool sxHit  = f_hitT(md, mdp, 120) or f_hitT(md, mdp, 480) or f_hitT(md, mdp, 570)\n    bool nd     = f_hitT(md, mdp, 1080)\n    bool inAsia")
rep("            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 2, 1, close, close - (FX50 ? FIXPT : atr), true, 6.0, 0, na, 0.5)",
    "            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 2, 1, close, close - (NEWR or FX50 ? FIXPT : atr), true, 6.0, NEWR ? 4 : 0, na, NEWR ? 0.0 : 0.5)")
rep("        if on10 and m1L\n            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 9, 1, close, close - FIXPT, true, 2.0, 0, na, 1.0)",
    "        if on10 and m1L\n            // NQ: buy limit at MP (low + 75% of the range) of the break candle · a close below MP = buy at the close\n            float lv9 = low + (high - low) * 0.75\n            if NEWR and lv9 < close\n                f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 9, 1, lv9, lv9 - FIXPT, false, 2.0, 0, na, 0.0)\n            else\n                f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 9, 1, close, close - FIXPT, true, 2.0, 0, na, NEWR ? 0.0 : 1.0)")
rep("[sTp, lTp, cTp, eKp, ePp] = f_trades(true, toHit, inAsia,", "[sTp, lTp, cTp, eKp, ePp] = f_trades(true, toHit, sxHit, inAsia,")
rep("[sTf, lTf, cTf, eKf, ePf] = f_trades(false, toHit, inAsia,", "[sTf, lTf, cTf, eKf, ePf] = f_trades(false, toHit, sxHit, inAsia,")

# ── X.M3: market at the birth close (NQ) ──
rep("            q.push(T2.new(k=12, side=1, sb=bar_index, lvl=top, d=FIXPT, stp=top - FIXPT, rr=2.0, tg=na, endB=bar_index + 300, sigT=time_close, dead=kl, xm=3, xv=kl))",
    "            if NEWR\n                // NQ: market at the close of the candle where the block is born · stop = block top − 50 · 1:2 · out after 100 candles\n                q.push(T2.new(k=12, side=1, sb=bar_index, lvl=close, d=FIXPT, stp=top - FIXPT, rr=2.0, tg=na, endB=bar_index, sigT=time_close, mkt=true, xm=4))\n            else\n                q.push(T2.new(k=12, side=1, sb=bar_index, lvl=top, d=FIXPT, stp=top - FIXPT, rr=2.0, tg=na, endB=bar_index + 300, sigT=time_close, dead=kl, xm=3, xv=kl))")
rep("                else if t.xm == 3 and not na(t.tX) and bar_index >= t.tX\n                    px   := close\n                    code := 1\n                    why  := 4",
    "                else if t.xm == 3 and not na(t.tX) and bar_index >= t.tX\n                    px   := close\n                    code := 1\n                    why  := 4\n                else if t.xm == 4 and bar_index >= t.fb + 100\n                    px   := close\n                    code := 1\n                    why  := 4")
rep("// xm: 0 stop / target only · 1 OC: out on a close below the 09:30 low (xv) · 2 C.M7: Max's 2-candle exit · 3 X.M3: out 60 candles after the block dies",
    "// xm: 0 stop / target only · 1 OC: out on a close below the 09:30 low (xv) · 2 C.M7: Max's 2-candle exit · 3 X.M3 (old): out 60 candles after the block dies · 4 X.M3 (new): out after 100 candles")
rep("// 5m CORE — X.M3 · MMM PRO x on 5m candles: a bullish iBlock of a T4+ PO4 → buy limit at the block top the moment it is born.\n// Stop 50 · 1:2 · the limit dies on a 5m close below the PO4 line or after 300 candles · out 60 candles after the block dies. All hours.",
    "// 5m CORE — X.M3 · MMM PRO x on 5m candles: a bullish iBlock of a T4+ PO4.\n// NQ (new): market at the close of the birth candle · stop = block top − 50 · 1:2 · out after 100 candles. All hours.\n// ES / gold / crude (old): buy limit at the block top · stop 50 · 1:2 · the limit dies on a 5m close below the PO4 line or after 300 candles · out 60 candles after the block dies.")

# ── pending text ──
rep("        t := (xP1D == 1 ? \"▲\" : \"▼\") + \" Pending · 15m close \" + (xP1D == 1 ? \"above \" : \"below \") + f_px(xP1L) + \" = P5+ break\"",
    "        t := (xP1D == 1 ? \"▲\" : \"▼\") + \" Pending · 15m close \" + (xP1D == 1 ? \"above \" : \"below \") + f_px(xP1L) + \" = P5+ break\" + (xP1D == 1 and NEWR ? \" → buy limit at MP (75%) of that candle\" : \"\")")

# ── tested numbers / targets ──
rep("        \"C.M4\" => 7.8\n", "        \"C.M4\" => 11.9\n")
rep("        \"X.M3\" => 28.8\n", "        \"X.M3\" => 51.9\n")
rep("        \"XCS.M1\" => 28.6\n", "        \"XCS.M1\" => 28.4\n")
rep("        \"X.M3\" => 49.8\n", "        \"X.M3\" => 66.2\n")
rep("        \"C.M4\" => 32.1\n", "        \"C.M4\" => 50.0\n")
rep("        2 => \"C.M4|½ out|520,71,0.17,1.63,3.9,5,11,8289,4467,32|-|Full,41,0.44,1.78,4.9,8821,520,14,7,17782,8961|",
    "        2 => \"C.M4|1:6 · session open|520,50,0.36,1.98,5.3,13,10,18781,9463,50|-|½ out (old rule) ✖ not the NQ rule,71,0.17,1.63,3.9,3822,520,5,11,8289,4467|")
rep("        7 => \"X.M3|1:2|2272,41,0.13,1.24,4.7,23,17,78326,62990,50|1:7,0.19,30,4.1|½ at 1R,54,0.13,1.30,5.8,15159,2272,14,17,64415,49256|",
    "        7 => \"X.M3|1:2 · market at birth|2572,47,0.13,1.27,5.4,23,22,98487,77965,66|-|-|")
rep("        10 => \"XCS.M1|1:2|1172,40,0.13,1.21,3.1,19,12,42366,34934,50|1:7,0.27,30,3.9|½ at 1R,54,0.14,1.31,4.3,8275,1172,11,14,35371,27096|",
    "        10 => \"XCS.M1|1:2 · longs MP limit|1141,40,0.17,1.27,3.9,17,12,44119,34628,50|-|-|")
rep("f_ep(int i) =>\n    i <= 4", "f_ep(int i) =>\n    i <= 4 and not (i == 2 and MKT <= 0)")
rep("        2 => \"½ at 0.5R → 1:6 RR\"\n", "        2 => \"1:6 RR · full · next session open\"\n")
rep("        7 => \"1:2 RR (max 1:7)\"\n", "        7 => \"1:2 RR · market at the block birth\"\n")
rep("        10 => \"1:2 RR (max 1:7)\"\n", "        10 => \"1:2 RR · longs: limit at MP\"\n")
rep("f_prK(int k) =>\n    k >= 12 ? 0.0 :", "f_prK(int k) =>\n    k >= 12 or (NEWR and k == 2) ? 0.0 :")
rep("(k == 0 or k == 5 ? \" or opp. break\" : k == 8 ? \" or gap-open exit\"",
    "(k == 0 or k == 5 ? \" or opp. break\" : k == 2 and NEWR ? \" or next session open\" : k == 8 ? \" or gap-open exit\"")
rep("k == 12 ? \" or block time-out\"", "k == 12 ? (NEWR ? \" or 100 candles\" : \" or block time-out\")")

# XCS.M1 shorts on NQ trade full too (as tested on the site) · X.M3 new name
rep("        if on10 and m1S\n            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 9, -1, close, close + FIXPT, true, 2.0, 0, na, 1.0)",
    "        if on10 and m1S\n            f_q(nk, ns, nl, np, nm, nr, nx, ndd, npr, 9, -1, close, close + FIXPT, true, 2.0, 0, na, NEWR ? 0.0 : 1.0)")
rep("k >= 12 or (NEWR and k == 2) ? 0.0 :", "k >= 12 or (NEWR and (k == 2 or k == 9)) ? 0.0 :")
rep("\"X.M3 · Block Top Buy · 5m (watch)\"", "\"X.M3 · Block Birth Buy · 5m (watch)\"")
rep("\"X.M3 · BLOCK TOP BUY · WATCH\"", "\"X.M3 · BLOCK BIRTH BUY · WATCH\"")
rep("MMM name: 5m iBlock T4+ Long · Top Limit.", "MMM name: 5m iBlock T4+ Long · Birth Close.")

open('MMM_EDGE_PRO.pine', 'w').write(src)
print('ok', n_ok, len(src))

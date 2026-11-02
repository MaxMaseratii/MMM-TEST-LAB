"""Fair Value Area Break 3.1 -> 3.2: only the strategies that passed the grid (FVA.M1-M4)."""
s = open('/home/claude/fva/pine/MMM_FVA_Break_3.1.pine', encoding='utf-8').read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f'expected {count} x {old[:90]!r}, found {n}')
    s = s.replace(old, new)


rep('"MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.1", "Fair Value Area Break @MaxMaserati 3.1"',
    '"MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.2", "Fair Value Area Break @MaxMaserati 3.2"')

# ── legacy entries OFF by default (none passed the grid as they were)
for a in ['usePesPelPoc       = input.bool(true, "① PES/PEL Touch"', 'usePesPelPlusPoc   = input.bool(true, "② PES/PEL+ Touch"',
          'useCdlCdsBlock     = input.bool(true, "③ CDL/CDS Touch"', 'useCdlCdsPlusBlock = input.bool(true, "④ CDL/CDS+ Touch"',
          'useNestedPoc        = input.bool(true, "Nested PES/PEL"', 'useNestedBlock      = input.bool(true, "Nested CDL/CDS"',
          'useBuxBexEntry   = input.bool(true, "Enable ⑤ BuX (Long) / BeX (Short) Entry"', 'useLqgEntry   = input.bool(true, "⑥ Enable LQG Break Momentum Entry"']:
    rep(a, a.replace('input.bool(true,', 'input.bool(false,'))
rep('grp_entry_types    = "🎯 Standard Entry Selection"', 'grp_entry_types    = "🎯 Raw Entries (box stop · 1:2 · not tested edges)"')

# ── strategy inputs
STRAT = '''// ── ⭐ TESTED STRATEGIES (FVA.M#) ────────────────────────────────────
// Oct 2026 grid: every entry x 6 stops x 7 targets x 12 exits, NQ 2022-25 (1m replay) then MNQ 2026.
// Engine: limit fills 1 tick through, stop wins ties, 1 pt cost, 100-candle max. Random trades: 0 of ~19,000 combos passed.
grp_strat = "⭐ Tested Strategies (FVA.M#)"
sM1   = input.bool(true,  "FVA.M1 · ② PES/PEL+ · 50 pt stop · 1:2 · exit after 2 neutral candles", group=grp_strat, tooltip="Limit at the PES/PEL+ POC (the flip zone), 1 tick through. Stop 50 pts. Target 2R. Exit at the close of the 2nd neutral candle in a row (NBC).\\n15m NQ 2023-25: 1,833 trades · WR 57% · PF 1.68 · avg RR +0.14 · t-score 7.5 (2023 +0.12 · 2024 +0.11 · 2025 +0.18)\\n15m MNQ 2026: 287 trades · WR 58% · PF 1.75 · avg RR +0.22 · t-score 3.8\\n5m: +0.05 → +0.10 · 1h: +0.18 → +0.31 (2026 t 1.7)")
sM2   = input.bool(true,  "FVA.M2 · ④ CDL/CDS+ · 50 pt stop · 1:2 · exit after 2 neutral candles", group=grp_strat, tooltip="Limit at the edge of the flip zone (the last opposite body close), 1 tick through. Stop 50 pts. Target 2R. Exit at the close of the 2nd neutral candle in a row.\\n15m NQ 2023-25: 2,192 trades · WR 55% · PF 1.50 · avg RR +0.11 · t-score 6.5 (2023 +0.08 · 2024 +0.08 · 2025 +0.16)\\n15m MNQ 2026: 348 trades · WR 56% · PF 1.69 · avg RR +0.21 · t-score 3.9\\nBest on 15m only (5m and 1h did not pass in 2026).")
sM3   = input.bool(true,  "FVA.M3 · ② PES/PEL+ · 50 pt stop · target = flip candle high/low · exit on opposite BC", group=grp_strat, tooltip="HIGH WIN RATE version. Limit at the PES/PEL+ POC, 1 tick through. Stop 50 pts. Target = the high (long) / low (short) of the flip candle. Exit at the close of the first opposite body close.\\n15m NQ 2023-25: 1,833 trades · WR 67% · PF 2.02 · avg RR +0.09 · t-score 9.6 (every year t 5+)\\n15m MNQ 2026: 287 trades · WR 67% · PF 2.38 · avg RR +0.18 · t-score 5.4\\nAlso passed 5m (WR 61→66%) and 1h (WR 69→69%).")
sM4   = input.bool(false, "FVA.M4 · ② PES/PEL+ · 50 pt stop · 1:2 · exit on opposite BC", group=grp_strat, tooltip="Limit at the PES/PEL+ POC, 1 tick through. Stop 50 pts. Target 2R. Exit at the close of the first opposite body close.\\n15m NQ 2023-25: WR 46% · PF 1.79 · avg RR +0.13 · t 7.5 → MNQ 2026: WR 43% · avg RR +0.16 · t 2.9\\n5m: +0.06 → +0.14 · 1h: +0.24 → +0.39 (2026 only 52 trades). Off by default: same entry as M1 / M3.")
sStop = input.float(50.0, "Strategy Stop (points)", minval=1.0, step=1.0, group=grp_strat, tooltip="Tested with 50 pts on NQ / MNQ. For ES / MES use 20 pts (not tested in this grid).")

// ── MMPD FILTER ─────────────────────────────────────────────────────'''
rep('// ── MMPD FILTER ─────────────────────────────────────────────────────', STRAT)

# ── EntrySignal: exit mode, 1-tick-through fill, fill bar
rep('    bool    forceExit\n    string  forceExitReason\n    bool    startNext\n',
    '    bool    forceExit\n    string  forceExitReason\n    bool    startNext\n    int     exitMode\n    bool    thru\n    int     fillBar\n')
# PEBox: strategy flags + flip candle extremes
rep('    bool      has_swing_line\n    bool      is_nested\n\n// ═', '    bool      has_swing_line\n    bool      is_nested\n    bool      st_poc_taken\n    bool      st_blk_taken\n    float     flip_hi\n    float     flip_lo\n\n// ═')
rep('bar_index, false, false, 0, 0, not slEx, is_flip_nested))', 'bar_index, false, false, 0, 0, not slEx, is_flip_nested, false, false, high, low))')
rep('bar_index, false, false, 0, 0, not shEx, is_flip_nested))', 'bar_index, false, false, 0, 0, not shEx, is_flip_nested, false, false, high, low))')

# ── createTrade: own R, absolute target, exit mode, tick-through
rep('createTrade(bool isLong, float ep, float slIn, string entryType, int tid, bool activateNow = false, bool startNext = false) =>',
    'createTrade(bool isLong, float ep, float slIn, string entryType, int tid, bool activateNow = false, bool startNext = false, float tRR = na, float tgtPx = na, int exitMode = 0, bool thru = false) =>')
rep('    float tp = isLong ? ep + (rp * rrRatio) : ep - (rp * rrRatio)\n',
    '    float _rr = na(tRR) ? rrRatio : tRR\n'
    '    float tp = not na(tgtPx) ? ((isLong ? tgtPx > ep : tgtPx < ep) ? tgtPx : (isLong ? ep + rp * 100 : ep - rp * 100)) : (isLong ? ep + (rp * _rr) : ep - (rp * _rr))\n')
rep('            float profD = aRisk * rrRatio\n', '            float _tR   = math.abs(tp - ep) / math.max(rp, syminfo.mintick)\n            float profD = aRisk * _tR\n')
rep('" (" + str.tostring(rrRatio, "#.#") + "R) @"', '" (" + str.tostring(_tR, "#.#") + "R) @"')
rep('aRisk, na, na, true, ps, false, "", startNext)', 'aRisk, na, na, true, ps, false, "", startNext, exitMode, thru, int(na))')

# ── grading: 1 tick through for strategy limits + candle events for exits
rep('f_grade(bool isLong, float ep, float sl, float tp, bool actIn) =>', 'f_grade(bool isLong, float ep, float sl, float tp, bool actIn, float thru) =>')
rep('                if isLong ? ll <= ep : hh >= ep\n', '                if isLong ? ll <= ep - thru : hh >= ep + thru\n')
rep('            if isLong ? low <= ep : high >= ep\n', '            if isLong ? low <= ep - thru : high >= ep + thru\n')
rep('// stats in risk units:', '''// candle events for the strategy exits (same definitions as the test engine)
bool coreBuX = close > high[1] or (open > high[1] and not (close < low[1]))
bool coreBeX = close < low[1] or (open < low[1] and not (close > high[1]))
var int nbcRun = 0
nbcRun := (not coreBuX and not coreBeX) ? nbcRun + 1 : 0

// stats in risk units:''')
rep('var int[]   catW  = array.new_int(8, 0)\nvar int[]   catL  = array.new_int(8, 0)\nvar float[] catR  = array.new_float(8, 0.0)',
    'var int[]   catW  = array.new_int(12, 0)\nvar int[]   catL  = array.new_int(12, 0)\nvar float[] catR  = array.new_float(12, 0.0)')
rep('    str.contains(ct, "Nested") and str.contains(ct, "PES/PEL") ? 0 :',
    '    str.contains(ct, "FVA.M1") ? 8 : str.contains(ct, "FVA.M2") ? 9 : str.contains(ct, "FVA.M3") ? 10 : str.contains(ct, "FVA.M4") ? 11 : str.contains(ct, "Nested") and str.contains(ct, "PES/PEL") ? 0 :')

# ── Layer 3: cancel unfilled strategy limits, fill bar, close exits
rep('''            int  _g2     = 0
            bool _wait2  = _tc2.startNext and bar_index == _tc2.creationBar
            if not _wait2 and not _tc2.forceExit
                [_gr2, _ac2] = f_grade(_tc2.isLong, _tc2.entryPrice, _tc2.stopLoss, _tc2.takeProfit, _tc2.activated)
                _g2 := _gr2
                _tc2.activated := _ac2''',
    '''            if _tc2.thru and not _tc2.activated and bar_index > _tc2.creationBar and not _tc2.forceExit
                _tc2.forceExit := true
                _tc2.forceExitReason := "Not filled (needs 1 tick through)"
            int  _g2     = 0
            bool _wait2  = _tc2.startNext and bar_index == _tc2.creationBar
            if not _wait2 and not _tc2.forceExit
                [_gr2, _ac2] = f_grade(_tc2.isLong, _tc2.entryPrice, _tc2.stopLoss, _tc2.takeProfit, _tc2.activated, _tc2.thru ? syminfo.mintick : 0.0)
                _g2 := _gr2
                if _ac2 and not _tc2.activated
                    _tc2.fillBar := bar_index
                _tc2.activated := _ac2
            // strategy exits at the close: 2 neutral candles in a row (M1, M2) · first opposite body close (M3, M4) · 100 candles
            if _tc2.activated and not _tc2.forceExit and _g2 == 0 and _tc2.exitMode > 0
                int  _fb   = na(_tc2.fillBar) ? _tc2.creationBar : _tc2.fillBar
                bool _xNbc = _tc2.exitMode == 1 and bar_index > _fb and nbcRun >= 2
                bool _xOpp = _tc2.exitMode == 2 and bar_index >= _fb and (_tc2.isLong ? coreBeX : coreBuX)
                bool _xTim = bar_index - _fb >= 99
                if _xNbc or _xOpp or _xTim
                    _tc2.forceExit := true
                    _tc2.forceExitReason := _xNbc ? "Exit: 2 neutral candles" : _xOpp ? "Exit: opposite BC" : "Exit: 100 candles"''')

# ── strategy trades on the PE (flip) boxes, before the raw entries
rep('''            // POC/Block Entries
            bool is_nest = pb.is_nested
            string e_poc_name = is_nest ? "② Nested PES/PEL+" : "② PES/PEL+"''',
    '''            // ⭐ tested strategies (FVA.M#): limit at the flip-zone level, 1 tick through, own stop / target / exit
            if not pb.is_nested and not pb.is_violated and pb.vis_ok and isEntryAllowed(pb.is_bull)
                bool _stL = pb.is_bull
                if (sM1 or sM3 or sM4) and not pb.st_poc_taken and not na(pb.poc_price_val) and pb.poc_touched
                    pb.st_poc_taken := true
                    float _ep = pb.poc_price_val
                    float _sp = _stL ? _ep - sStop : _ep + sStop
                    if na(firstTradeTime)
                        firstTradeTime := time
                    if sM1
                        globalTradeId += 1
                        pushTradeToArrays(createTrade(_stL, _ep, _sp, "FVA.M1 PES/PEL+", globalTradeId, false, false, 2.0, na, 1, true))
                    if sM3
                        globalTradeId += 1
                        pushTradeToArrays(createTrade(_stL, _ep, _sp, "FVA.M3 PES/PEL+", globalTradeId, false, false, na, _stL ? pb.flip_hi : pb.flip_lo, 2, true))
                    if sM4
                        globalTradeId += 1
                        pushTradeToArrays(createTrade(_stL, _ep, _sp, "FVA.M4 PES/PEL+", globalTradeId, false, false, 2.0, na, 2, true))
                float _lv = _stL ? pb.fva_top : pb.fva_bot
                if sM2 and not pb.st_blk_taken and not na(_lv) and (_stL ? low <= _lv : high >= _lv)
                    pb.st_blk_taken := true
                    if na(firstTradeTime)
                        firstTradeTime := time
                    globalTradeId += 1
                    pushTradeToArrays(createTrade(_stL, _lv, _stL ? _lv - sStop : _lv + sStop, "FVA.M2 CDL/CDS+", globalTradeId, false, false, 2.0, na, 1, true))

            // POC/Block Entries
            bool is_nest = pb.is_nested
            string e_poc_name = is_nest ? "② Nested PES/PEL+" : "② PES/PEL+"''')

# ── stats table: strategy section
rep('var table _sT = table.new(getTablePosition(statsTablePos), 3, 34,', 'var table _sT = table.new(getTablePosition(statsTablePos), 3, 50,')
TAB = '''    if sM1 or sM2 or sM3 or sM4
        table.cell(_sT, 0, st, "── TESTED STRATEGIES ──", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
        table.cell(_sT, 1, st, "W/L (WR)", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
        table.cell(_sT, 2, st, "avg RR", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
        st += 1
        array<bool>   _sOn = array.from(sM1, sM2, sM3, sM4)
        array<string> _sNm = array.from("FVA.M1 ② 1:2 · 2 NBC", "FVA.M2 ④ 1:2 · 2 NBC", "FVA.M3 ② flip TGT · opp BC", "FVA.M4 ② 1:2 · opp BC")
        array<string> _sTs = array.from("tested 15m: WR 57% · +0.14 → 2026 +0.22", "tested 15m: WR 55% · +0.11 → 2026 +0.21", "tested 15m: WR 67% · +0.09 → 2026 +0.18", "tested 15m: WR 46% · +0.13 → 2026 +0.16")
        for _k = 0 to 3
            if _sOn.get(_k)
                int   _ci = 8 + _k
                int   _sw = array.get(catW, _ci)
                int   _sl = array.get(catL, _ci)
                float _sr = array.get(catR, _ci)
                table.cell(_sT, 0, st, _sNm.get(_k), bgcolor=#000000, text_color=#27ffc3, text_size=getTableTextSize(_sz))
                table.cell(_sT, 1, st, f_wl(_sw, _sl), bgcolor=#000000, text_color=color.white, text_size=getTableTextSize(_sz))
                table.cell(_sT, 2, st, f_avgTx(_sr, _sw + _sl), bgcolor=#000000, text_color=_sw + _sl == 0 ? color.gray : _sr > 0 ? color.lime : color.red, text_size=getTableTextSize(_sz))
                st += 1
                table.cell(_sT, 0, st, _sTs.get(_k), bgcolor=#000000, text_color=color.rgb(150,150,150), text_size=getTableTextSize(_sz))
                table.merge_cells(_sT, 0, st, 2, st)
                st += 1

    table.cell(_sT, 0, st, "── BY ENTRY ──",'''
rep('    table.cell(_sT, 0, st, "── BY ENTRY ──",', TAB)

open('/home/claude/fva/pine/MMM_FVA_Break_3.2.pine', 'w', encoding='utf-8').write(s)
print('ok', s.count('\n') + 1)

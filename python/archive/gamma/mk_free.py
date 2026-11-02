"""Gamma Walls free version: no arrows, no direction, no bias. Walls, flip, magnets, histogram, level map, market type."""
L = open('gb_v4.pine').read().split('\n')
def g(a, b):  # 1-indexed inclusive
    return L[a - 1:b]

out = []
out += ['//@version=6',
        'indicator("Gamma Walls @MaxMaserati", shorttitle="Gamma Walls @MaxMaserati", overlay=true, max_boxes_count=500, max_lines_count=500, max_labels_count=500, max_bars_back=500)',
        '',
        '// Free version (Oct 30 2026): options gamma walls only · no signals, no arrows, no bias.',
        '// 90D walls · today\'s 0DTE walls, flip and magnets · gamma histogram · level map · market type (calm / fast).',
        '']
out += g(15, 35)
out += ['']
out += g(69, 73)
out += ['showRoles      = input.bool(true, "Explain Each Level", group=grp_m, tooltip="Adds a short note: ceiling, floor, magnet, calm / fast line.")']
out += g(75, 80)
out += ['zonePts        = input.float(0.0, "Wall Zone (Points, 0 = auto)", minval=0.0, group=grp_m, tooltip="How close price must be to count as AT a 90D wall (HUD location). NQ: 10-20. ES: 2-5. 0 = half a strike step.")']
out += ['']
out += g(83, 116)
out += ['']
out += [l.replace('inline="c4", ', '') for l in g(122, 125)]
out += ['']
out += g(131, 133)
out += ['hudMode      = input.string("Compact", "HUD Mode", options=["Compact", "Detailed"], group=grp_h, tooltip="Compact = market type and the nearest level above and below.\\nDetailed = the same, plus every level.")']
out += g(135, 158)
out += g(164, 169)
out += [''] + g(181, 181) + ['']
out += g(235, 262)
out += g(300, 307)
out += ['// a short note on what each level is (no direction, no advice)',
        'roleOf(string kind, float p, float px) =>',
        '    bool above = p > px',
        '    switch kind',
        '        "C90" => above ? "ceiling" : "below price"',
        '        "P90" => above ? "above price" : "floor"',
        '        "CT" => above ? "ceiling" : "below price"',
        '        "PT" => above ? "above price" : "floor"',
        '        "Z90" => "calm above · fast below"',
        '        "FT" => "calm above · fast below"',
        '        "MG" => "magnet"',
        '        => ""',
        '']
out += g(344, 350)
out += ['// zone = a wall or a magnet · false = a calm / fast line']
out += g(352, 579)
out += ['']
out += g(805, 808)
out += ['']
body = g(941, 1015) + g(1018, 1088)
body = [l.replace('// nearest wall / magnet above and below = where to sell / buy (regime lines and the plan line are not zones)',
                  '// nearest wall / magnet above and below price (the calm / fast lines are not counted)') for l in body]
out += body
out += r'''
    // ─── HUD ───
    string locTxt = "type your 90D walls"
    if not na(cw) and not na(pw) and not na(zoneBuf90)
        if close > cw + zoneBuf90
            locTxt := "above the 90D call wall"
        else if close >= cw - zoneBuf90
            locTxt := "at the 90D call wall"
        else if close < pw - zoneBuf90
            locTxt := "below the 90D put wall"
        else if close <= pw + zoneBuf90
            locTxt := "at the 90D put wall"
        else
            locTxt := "between the 90D walls"
    string locS = locTxt == "above the 90D call wall" ? "above call wall" : locTxt == "at the 90D call wall" ? "at call wall" : locTxt == "below the 90D put wall" ? "below put wall" : locTxt == "at the 90D put wall" ? "at put wall" : locTxt == "between the 90D walls" ? "between walls" : "no 90D walls"

    string regS    = not na(tFlip) ? "flip" : zgManual ? "zero γ" : "VWAP est."
    string cMarket = na(regLvl) ? "—" : (longGamma ? "CALM · above " : "FAST · below ") + regS + " · " + locS
    string cMktTip = na(regLvl) ? "" : (longGamma ? "CALM: price is above " : "FAST: price is below ") + regName + " " + fmtP(regLvl) + ". " + (longGamma ? "Dealers tend to slow price down: walls tend to hold." : "Dealers tend to speed price up: moves tend to stretch.") + " Location vs the 90D walls: " + locTxt + "."
    string cAbove  = na(sellP) ? "—" : pxd(sellP) + " · " + sellN
    string cBelow  = na(buyP) ? "—" : pxd(buyP) + " · " + buyN
    string srcS    = "today " + (hasToday ? "✓" : "✕") + " · 90D " + (manual90 ? "✓" : "est.")
    bool   idxMismatch = str.length(txtIndex) > 0 and txtIndex != targetIndex

    if showHud
        table.clear(hud, 0, 0, 1, 15)
        int row = 0
        table.cell(hud, 0, row, "GAMMA · " + syminfo.ticker, text_color=color.white, text_size=hudSize, bgcolor=color.rgb(35, 35, 35), text_halign=text.align_left)
        table.cell(hud, 1, row, srcS, text_color=hasToday and manual90 ? color.aqua : color.yellow, text_size=hudSize, bgcolor=color.rgb(35, 35, 35), text_halign=text.align_left, tooltip="Data: today = 0DTE strikes pasted · 90D ✓ = walls typed (est. = estimated from volume).")
        row += 1
        hudRow(hud, row, "MARKET", cMarket, na(regLvl) ? color.gray : longGamma ? color.aqua : color.orange, hudSize, cMktTip)
        row += 1
        hudRow(hud, row, "ABOVE", cAbove, color.silver, hudSize, "The nearest wall or magnet ABOVE price, in points from price" + (na(sellP) ? "." : ": " + fmtP(sellP) + "."))
        row += 1
        hudRow(hud, row, "BELOW", cBelow, color.silver, hudSize, "The nearest wall or magnet BELOW price, in points from price" + (na(buyP) ? "." : ": " + fmtP(buyP) + "."))
        row += 1

        if hudMode == "Detailed"
            hudHead(hud, row, "LEVELS (points from price)", hudSize)
            row += 1
            hudRow(hud, row, "Call wall 90D" + (cwManual ? "" : " (est.)"), pxd(cw), callWallC, hudSize)
            row += 1
            hudRow(hud, row, "Put wall 90D" + (pwManual ? "" : " (est.)"), pxd(pw), putWallC, hudSize)
            row += 1
            hudRow(hud, row, zgManual ? "Zero γ 90D" : "90D VWAP (est. zero γ)", pxd(zg), color.silver, hudSize)
            row += 1
            hudRow(hud, row, "Today (0DTE)", hasToday ? "call " + pxd(tCW) + " · put " + pxd(tPW) + " · flip " + pxd(tFlip) : "paste today's levels", hasToday ? todayCallC : color.gray, hudSize)
            row += 1

        string note = idxMismatch ? "! Pasted " + txtIndex + " levels, but this chart uses " + targetIndex : not hasToday ? "Paste today's levels for the full map" : ""
        if note != ""
            table.cell(hud, 0, row, note, text_color=idxMismatch ? color.orange : color.gray, text_size=idxMismatch ? hudSize : size.tiny, bgcolor=color.black)
            table.merge_cells(hud, 0, row, 1, row)
'''.split('\n')
src = '\n'.join(out).rstrip() + '\n'
src = src.replace('table.new(hudPosition, 2, 34,', 'table.new(hudPosition, 2, 16,')
open('MMM_Gamma_Walls_Free.pine', 'w').write(src)
print(len(src.split('\n')))

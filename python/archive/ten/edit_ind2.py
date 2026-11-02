p='/home/claude/mmmpro-journal/indicators/index.html'; s=open(p).read()
a=s.index('  function stairSVG(L) {'); b=s.index('  function engPaint() {')
new=r'''  var DSIDE = 'bu';
  function stairSVG(L) {
    var bear = DSIDE === 'be', my = function (y) { return bear ? 258 - y : y; };
    var path = 'M20,232 L45,210 L60,224 L80,190 L100,200 L118,160 L132,176 L146,164 L160,180 L174,168 L190,128 L214,112 L232,128 L246,118 L262,132 L276,120 L292,84 L316,70 L332,86 L346,76 L362,90 L376,78 L392,46 L430,26';
    if (bear) path = path.replace(/(\d+),(\d+)/g, function (m, x, y) { return x + ',' + (258 - y); });
    var boxes = [[124, 158, 58, 26], [226, 110, 58, 26], [326, 68, 58, 26]];
    var F = bear ? 'CDS' : 'CDL', D = bear ? 'SD' : 'LD';
    var nodes = [['flip', 62, 226, F + L, 1], ['T1', 45, 210, 'T1', 0], ['P1', 182, 158, 'P1', 2], ['LD1', 190, 128, D + L + '1', 1], ['R1', 124, 184, 'R1 → T2', 3], ['P2', 284, 110, 'P2', 2], ['LD2', 292, 84, D + L + '2', 1], ['R2', 226, 136, 'R2 → T3', 3], ['LD3', 392, 46, D + L + '3', 1]];
    var s = '<svg viewBox="0 0 470 250" role="img" aria-label="MMM trend staircase (' + (bear ? 'bear' : 'bull') + ' example): flip, pullbacks, continuations. Tap a point.">';
    boxes.forEach(function (b) { var y = bear ? 258 - b[1] - b[3] : b[1]; s += '<rect class="bx" x="' + b[0] + '" y="' + y + '" width="' + b[2] + '" height="' + b[3] + '"/>'; });
    [['lvm', 45, 460, 210], ['lv', 124, 200, 158], ['lvm', 124, 460, 184], ['lv', 226, 300, 110], ['lvm', 226, 460, 136], ['lv', 326, 400, 68]].forEach(function (l) { s += '<line class="' + l[0] + '" x1="' + l[1] + '" x2="' + l[2] + '" y1="' + my(l[3]) + '" y2="' + my(l[3]) + '"/>'; });
    s += '<path class="ln" d="' + path + '"/>';
    nodes.forEach(function (n) {
      var on = n[0] === DIAK, cls = n[4] === 1 ? 'mg' : n[4] === 2 ? 'tl' : n[4] === 3 ? 'mut' : 'mg';
      var isLD = n[0].indexOf('LD') === 0, tx = n[0] === 'flip' ? n[1] + 8 : n[0] === 'T1' ? n[1] - 30 : (n[0] === 'R1' || n[0] === 'R2') ? n[1] + 2 : isLD ? n[1] - 8 : n[1] + 6;
      var ty = n[0] === 'flip' ? n[2] + 12 : n[0] === 'T1' ? n[2] + 18 : (n[0] === 'R1' || n[0] === 'R2') ? n[2] + 14 : isLD ? n[2] - 6 : n[2] - 8;
      var cy = my(n[2]); if (bear) ty = cy - (ty - n[2]) + 9;
      s += '<g data-k="' + n[0] + '" style="cursor:pointer" tabindex="0" role="button" aria-label="' + esc(n[3]) + '"><circle cx="' + n[1] + '" cy="' + cy + '" r="' + (on ? 7 : 4.5) + '" style="fill:' + (on ? 'var(--ec)' : '#0f1114') + ';stroke:var(--fg);stroke-width:1.5"/><rect x="' + (isLD ? tx - n[3].length * 7.4 - 3 : tx - 3) + '" y="' + (ty - 12) + '" width="' + (n[3].length * 7.4 + 6) + '" height="16" fill="transparent"/><text class="' + cls + '" x="' + tx + '" y="' + ty + '" text-anchor="' + (isLD ? 'end' : 'start') + '" style="font-weight:' + (on ? 700 : 500) + '" translate="no">' + esc(n[3]) + '</text></g>';
    });
    return s + '<text class="mut" x="20" y="' + (bear ? 14 : 246) + '">start</text><text class="mut" x="465" y="' + (bear ? 14 : 246) + '" text-anchor="end">each step = the trend won again</text></svg>';
  }
  function diaText(k) {
    var d = DIA[k]; if (DSIDE !== 'be') return d;
    var f = function (x) { return swapSide(x).replace(/\bLD(\d)/g, 'SD$1'); };
    return [f(d[0]), f(d[1])];
  }
'''
s=s[:a]+new+s[b:]
o='    var d = DIA[DIAK];\n'; assert o in s; s=s.replace(o,'    var d = diaText(DIAK);\n')
o='<div class="lab">The trend staircase · tap a point</div>'
assert o in s
s=s.replace(o,'<div class="dside"><div class="lab">The trend staircase · tap a point</div><span class="seg" role="group" aria-label="Example side"><button type="button" data-dside="bu" aria-pressed="\' + (DSIDE === \'bu\') + \'">Bull example</button><button type="button" data-dside="be" aria-pressed="\' + (DSIDE === \'be\') + \'">Bear example</button></span></div>')
o="    var g = e.target.closest('#dia g[data-k]'); if (g) { DIAK = g.dataset.k; engPaint(); if (e.detail === 0) { var m = document.querySelector('#dia g[data-k=\"' + DIAK + '\"]'); if (m) m.focus(); } }"
assert o in s
s=s.replace(o,"    var g = e.target.closest('#dia g[data-k]'); if (g) { DIAK = g.dataset.k; engPaint(); flashInfo(); if (e.detail === 0) { var m = document.querySelector('#dia g[data-k=\"' + DIAK + '\"]'); if (m) m.focus(); } return; }\n    var ds = e.target.closest('[data-dside]'); if (ds) { DSIDE = ds.dataset.dside; engPaint(); flashInfo(); var q = document.querySelector('[data-dside=\"' + DSIDE + '\"]'); if (q && e.detail === 0) q.focus(); }")
o='  document.addEventListener(\'keydown\', function (e) { var g = e.target.closest && e.target.closest(\'#dia g[data-k]\');'
assert o in s
s=s.replace(o,"  function flashInfo() { var x = document.getElementById('dinfo'); if (!x) return; x.classList.remove('flash'); void x.offsetWidth; x.classList.add('flash'); }\n"+o)
open(p,'w').write(s); print('ok')

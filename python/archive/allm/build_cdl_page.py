import pandas as pd, numpy as np, grid, html
D=pd.read_parquet('grid_xbbrk.parquet')
D['kind']=D.strat.str.replace(r' (5m|15m|1h|4h)$','',regex=True).str.replace(r'^XB ','',regex=True); D['tf']=D.strat.str.extract(r'(5m|15m|1h|4h)$')
D['pass']=(D.t1>=2)&(D.t2>=2)&(D.n1>=30)&(D.n2>=20)
N=D[D.market=='NQ']
KO=['CDLx/CDSx','LDx/SDx','cdlx/cdsx (internal)','ldx/sdx (internal)','all XB breaks','RANDOM']
TFO=['5m','15m','1h','4h']
def nm(r): return f"{grid.ENAME[r.e]} · {grid.SNAME[r.st]} · 1:{grid.TGT[r.t]:g} · {grid.XNAME[r.x]}"
def c(v,d=2,pct=False):
    if v is None or (isinstance(v,float) and np.isnan(v)): return '<td>–</td>'
    cls='pos' if v>0 else 'neg' if v<0 else ''
    return f'<td class="{cls}">{"+" if v>0 else ""}{v:.{d}f}</td>'
def tt(v):
    if v is None or np.isnan(v): return '<td>–</td>'
    return f'<td class="{"pos" if v>=2 else "neg" if v<=-2 else ""}">{v:.1f}</td>'
def sidename(k,s):
    a={'CDLx/CDSx':('CDLx','CDSx'),'LDx/SDx':('LDx','SDx'),'cdlx/cdsx (internal)':('cdlx','cdsx'),'ldx/sdx (internal)':('ldx','sdx'),'all XB breaks':('bull break','bear break'),'RANDOM':('random long','random short')}[k]
    return a[s]
# table 1: 50/1:2 market
t1=['<tr><th class="l">TF</th><th class="l">Break</th><th class="l">Side</th><th>n P1</th><th>n P2</th><th>WR P1</th><th>WR P2</th><th>PF P1</th><th>PF P2</th><th>avg RR P1</th><th>avg RR P2</th><th>t P1</th><th>t P2</th><th>PASS pairings (of 2,492)</th></tr>']
for tf in TFO:
    first=True
    for k in KO:
        for s in (0,1):
            r=N[(N.kind==k)&(N.tf==tf)&(N.side==s)&(N.e==1)&(N.st==1)&(N.t==2)&(N.x==0)]
            if not len(r): continue
            r=r.iloc[0]; np_=int(N[(N.kind==k)&(N.tf==tf)&(N.side==s)]['pass'].sum())
            hl=' class="hl"' if k=='CDLx/CDSx' else ''
            t1.append(f'<tr{hl}><td class="l">{tf if first else ""}</td><td class="l">{k}</td><td class="l">{sidename(k,s)}</td><td>{int(r.n1)}</td><td>{int(r.n2)}</td><td>{r.wr1:.1f}%</td><td>{r.wr2:.1f}%</td><td>{r.pf1:.2f}</td><td>{r.pf2:.2f}</td>{c(r.avg1,3)}{c(r.avg2,3)}{tt(r.t1)}{tt(r.t2)}<td>{np_}</td></tr>'); first=False
# table 2: walk-forward pick for CDLx/CDSx + LDx
t2=['<tr><th class="l">TF</th><th class="l">Break</th><th class="l">Side</th><th class="l">Best pairing in 2022–25 (entry · stop · target · exit)</th><th>n P1</th><th>n P2</th><th>avg RR P1</th><th>avg RR P2</th><th>t P1</th><th>t P2</th></tr>']
for tf in TFO:
    for k in ['CDLx/CDSx','LDx/SDx','RANDOM']:
        for s in (0,1):
            g=N[(N.kind==k)&(N.tf==tf)&(N.side==s)&(N.n1>=30)&(N.n2>=20)]
            if not len(g): continue
            r=g.sort_values('t1',ascending=False).iloc[0]
            hl=' class="hl"' if k=='CDLx/CDSx' else ''
            t2.append(f'<tr{hl}><td class="l">{tf}</td><td class="l">{k}</td><td class="l">{sidename(k,s)}</td><td class="l">{html.escape(nm(r))}</td><td>{int(r.n1)}</td><td>{int(r.n2)}</td>{c(r.avg1,3)}{c(r.avg2,3)}{tt(r.t1)}{tt(r.t2)}</tr>')
# table 3: foundational
X=pd.read_parquet('xbbrk_desc.parquet'); X=X[X.m.isin(['NQ','MNQ'])]; X['per']=np.where(X.m=='NQ','P1','P2')
t3=['<tr><th class="l">TF</th><th class="l">Break</th><th>Breaks P1 / P2</th><th>BCs before the 1st opposite BC</th><th>BCs before the 1st NBC</th><th>Next candle is an NBC</th><th>Candles to the opposite BC (median)</th><th>Pts moved before the opposite BC (median)</th><th>Close after 10 candles in break direction</th><th>avg pts after 10 candles</th></tr>']
for tf in TFO:
    first=True
    for k in KO[:4]:
        a=X[(X.tf==tf)&(X.kind==k)]; o=a[a.per=='P1']; f=a[a.per=='P2']
        hl=' class="hl"' if k=='CDLx/CDSx' else ''
        t3.append(f'<tr{hl}><td class="l">{tf if first else ""}</td><td class="l">{k}</td><td>{len(o)} / {len(f)}</td><td>{o.bcsBeforeOpp.mean():.2f} / {f.bcsBeforeOpp.mean():.2f}</td><td>{o.bcsBeforeNBC.mean():.2f} / {f.bcsBeforeNBC.mean():.2f}</td><td>{100*(o.bcsBeforeNBC==0).mean():.0f}% / {100*(f.bcsBeforeNBC==0).mean():.0f}%</td><td>{o.candlesToOpp.median():.0f} / {f.candlesToOpp.median():.0f}</td><td>{o.mfeToOpp.median():.1f} / {f.mfeToOpp.median():.1f}</td><td>{100*(o.pts10>0).mean():.0f}% / {100*(f.pts10>0).mean():.0f}%</td><td>{o.pts10.mean():+.1f} / {f.pts10.mean():+.1f}</td></tr>'); first=False
# other markets pass counts
om={mk:{k:int(D[(D.market==mk)&(D.kind==k)]['pass'].sum()) for k in KO} for mk in ['NQ','ES','GC','CL']}
t4=['<tr><th class="l">Break</th>'+''.join(f'<th>{mk}</th>' for mk in om)+'</tr>']
for k in KO: t4.append(f'<tr{" class=hl" if k=="CDLx/CDSx" else ""}><td class="l">{k}</td>'+''.join(f'<td>{om[mk][k]}</td>' for mk in om)+'</tr>')
page=f'''<title>CDLx CDSx Break Test</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: verdict, then the 50 pt 1:2 sheet for every break kind, the honest walk-forward pick, the foundational break stats, other markets. */
:root{{--bg:#f3f5f4;--panel:#fff;--fg:#16201d;--muted:#5b6a65;--line:#d4ddd9;--pos:#0f8a6a;--neg:#c93c3c;--acc:#9c27b0;--hl:#f6eefa;
--f-d:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--f-b:"Source Sans 3","Segoe UI",Arial,sans-serif;--f-m:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0d1211;--panel:#141b19;--fg:#e8efec;--muted:#9aaba5;--line:#2b3734;--pos:#2fd3a6;--neg:#ff6b6b;--acc:#c561e8;--hl:#221a26;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0d1211;--panel:#141b19;--fg:#e8efec;--muted:#9aaba5;--line:#2b3734;--pos:#2fd3a6;--neg:#ff6b6b;--acc:#c561e8;--hl:#221a26;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--fg);font-family:var(--f-b);font-size:16px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 56px}}
.wrap{{max-width:1500px;margin:0 auto;display:grid;gap:24px}}
.eyebrow{{font-family:var(--f-m);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:var(--f-d);font-size:clamp(32px,4.5vw,48px);line-height:1.05;margin:4px 0 8px;text-wrap:balance}}
h2{{font-family:var(--f-d);font-size:26px;margin:0}}
p{{margin:0;max-width:80ch}}
.verdict{{border:1px solid var(--line);border-left:4px solid var(--acc);background:var(--panel);border-radius:0 10px 10px 0;padding:16px 18px;display:grid;gap:8px}}
.verdict ul{{margin:0;padding-left:20px;display:grid;gap:4px}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}}
table{{border-collapse:collapse;width:100%;font-size:13.5px;font-variant-numeric:tabular-nums}}
th,td{{padding:6px 10px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}
th{{font-family:var(--f-m);font-size:10.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);vertical-align:bottom;white-space:normal}}
td.l,th.l{{text-align:left}}
tr.hl td{{background:var(--hl)}}
.pos{{color:var(--pos)}}.neg{{color:var(--neg)}}
.note{{font-size:13.5px;color:var(--muted)}}
section{{display:grid;gap:8px}}
</style>
<div class="wrap">
<header><div class="eyebrow">MMM PRO x 4.0 · XB breaks by kind · NQ 2022–25 (P1) → MNQ 2026 (P2)</div>
<h1>CDLx / CDSx: is the trend-flip XB break a trade?</h1>
<p>Only XB breaks whose close is also a zone-engine flip (CDLx up, CDSx down), next to the other break kinds and random candles. Every entry × stop × target × exit: 16 entries (market at the break close, break-candle ladder, FVA ladder), 6 stops, 7 targets, 4 exits.</p></header>
<section class="verdict"><h2>Verdict: CDLx / CDSx is not a trade on its own</h2><ul>
<li><b>0 of 19,852 CDLx / CDSx pairings</b> passed on NQ (t-score 2+ in both periods), on any timeframe, either side. Random candles: 0 too.</li>
<li>With the 50 pt stop at 1:2, market at the break close: no timeframe and side made money in both periods.</li>
<li>The best 2022–25 pairing faded in 2026 on every timeframe (for example 15m CDLx, limit at the FVA top, ATR stop, 1:6: +0.63 → +0.21, t 2.4 → 0.6).</li>
<li>After a CDLx / CDSx the next candle is an NBC 2 times out of 3, only about 1.4 more BCs come before the first opposite BC, and the close 10 candles later is on the break side about half the time.</li>
<li>The one lead in this test is the <b>LDx continuation break, 5m, longs</b>: 50 pt stop, market at the break close, 1:10 (or exit on a close back through the FVA): +0.12 → +0.45 avg RR, t 3.0 / 2.9 (random 5m longs, same rule: +0.07 → +0.07). It rides the 2022–26 uptrend; shorts do not hold. Watch only.</li>
<li><b>Balanced Zone or not:</b> the earlier tests say the same. Buying / selling in the zones or in the Balanced Zone gives the same coin flip. The only difference is distance: Balanced targets are closer, so they hit more often and pay less.</li></ul></section>
<section><h2>1 · 50 pt stop, 1:2, market at the break close (NQ / MNQ)</h2><div class="tw"><table>{''.join(t1)}</table></div>
<p class="note">PASS pairings = how many of the 2,492 entry × stop × target × exit pairings of that row reached a t-score of 2+ in both periods.</p></section>
<section><h2>2 · Best pairing picked on 2022–25, then checked on 2026</h2><div class="tw"><table>{''.join(t2)}</table></div></section>
<section><h2>3 · What happens after the break (NQ P1 / MNQ P2)</h2><div class="tw"><table>{''.join(t3)}</table></div></section>
<section><h2>4 · PASS pairings on every market</h2><div class="tw"><table>{''.join(t4)}</table></div>
<p class="note">ES, gold and crude: Dec 2025 – Oct 2026 cut in two halves. The crude passes include random candles: that is the crude trend, not the break.</p></section>
<p class="note">CDLx / CDSx = the XB break close is also a flip of the x zone engine · LDx / SDx = also a continuation (a close past P#) · small cdlx / cdsx / ldx / sdx = internal breaks that are no engine event · XB engine = opposite side only (x 4.0 default) · FVA = first NBC body → XB high (bear) / XB low (bull) · WR = win rate · PF = money won ÷ money lost · avg RR = average result per trade in stops after cost · t = t-score (2+ = probably not luck) · stop wins ties · 1 pt cost.</p>
</div>'''
open('/home/claude/xb/xb_cdl_test.html','w').write(page)
print(om)
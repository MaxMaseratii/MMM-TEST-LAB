"""Build the 'Claims vs Results' website from site/data.json -> site/index.html (self-contained, data embedded)."""
import json, sys
sys.path.insert(0, '/home/claude/cf2')
from headlines import INDUSTRY, UNTESTED, INSIGHTS
D = json.load(open('/home/claude/cf2/site/data.json'))
from recheck import RECHECK
D['recheck'] = RECHECK; D['industry'] = INDUSTRY; D['untested'] = UNTESTED; D['insights'] = INSIGHTS
J = json.dumps(D, separators=(',', ':')).replace('</', '<\\/')
HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chart Fanatics: Claims vs Results</title>
<meta name="description" content="Every futures strategy from Chart Fanatics coded from the traders' own rules, tested on NQ, ES and gold, and compared with what they claim. Plus the prop-firm account math behind big payout totals.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
/* Editorial-meets-terminal: big condensed headlines, dense mono tables, gold accent for verdicts. */
:root{--bg:#f4f2ec;--panel:#fffdf8;--line:#ddd7c9;--fg:#141210;--mute:#6b6457;--pos:#0a7d5c;--neg:#c0392b;--gold:#a26f00;--head:#ece7da;--posbg:#dcf1e8;--negbg:#f8e1dd;--warn:#b35c00;
--display:"Barlow Condensed","Arial Narrow",Arial,sans-serif;--body:"Barlow",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0b0a08;--panel:#14120f;--line:#2b2721;--fg:#efe9dc;--mute:#9c9384;--pos:#3ad8a4;--neg:#ff6b5b;--gold:#e8b23a;--head:#1c1915;--posbg:#0f2a21;--negbg:#2d1410;--warn:#ff9f43;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0b0a08;--panel:#14120f;--line:#2b2721;--fg:#efe9dc;--mute:#9c9384;--pos:#3ad8a4;--neg:#ff6b5b;--gold:#e8b23a;--head:#1c1915;--posbg:#0f2a21;--negbg:#2d1410;--warn:#ff9f43;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 var(--body)}
a{color:var(--gold)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);display:flex;gap:4px 18px;flex-wrap:wrap;padding:10px max(16px,env(safe-area-inset-left));align-items:center}
nav b{font:800 19px var(--display);letter-spacing:.04em;margin-right:8px}nav a{font:600 14px var(--body);color:var(--fg);text-decoration:none;opacity:.75}nav a:hover{opacity:1;color:var(--gold)}
main{max-width:1500px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left)) 60px}
section{padding:34px 0 8px;border-bottom:1px solid var(--line)}
h1{font:800 clamp(40px,7vw,86px)/.95 var(--display);letter-spacing:.01em;margin:26px 0 12px;text-wrap:balance}
h2{font:800 clamp(28px,4vw,44px)/1 var(--display);margin:0 0 10px;letter-spacing:.02em;text-wrap:balance}
h3{font:700 22px var(--display);margin:0 0 6px;letter-spacing:.03em}
.lede{font-size:19px;max-width:80ch;color:var(--mute);margin:0 0 18px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px;margin:18px 0}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px}.kpi .n{font:800 46px/1 var(--display)}.kpi .l{color:var(--mute);font-size:14px}
.kpi.bad .n{color:var(--neg)}.kpi.good .n{color:var(--pos)}.kpi.gold .n{color:var(--gold)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:12px;margin:12px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 16px;min-width:0}.card ul{margin:6px 0 0 18px;padding:0}.card li{margin:5px 0}
.card.key{border-color:var(--gold)}
.grid{overflow:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel);max-height:75vh}
table{border-collapse:collapse;width:100%;font:13px/1.35 var(--mono);font-variant-numeric:tabular-nums}
th{position:sticky;top:0;background:var(--head);font:600 12px var(--body);text-transform:uppercase;letter-spacing:.04em;color:var(--mute);text-align:right;padding:8px 9px;border-bottom:1px solid var(--line);white-space:nowrap;z-index:1}
th.l,td.l{text-align:left}td{padding:6px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap;vertical-align:top}td.w{white-space:normal;min-width:260px}
td.g,th.g{border-left:2px solid var(--line)}tr.click{cursor:pointer}tr.click:hover{background:var(--head)}
.pos{color:var(--pos)}.neg{color:var(--neg)}.mu{color:var(--mute)}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font:700 11px var(--body);letter-spacing:.04em;text-transform:uppercase;border:1px solid currentColor;white-space:nowrap}
.v-lose{color:var(--neg)}.v-zero{color:var(--mute)}.v-watch{color:var(--gold)}.v-pass{color:var(--pos)}.v-na{color:var(--warn)}
.legend{color:var(--mute);font-size:13px;margin:8px 2px 16px;max-width:150ch}
.tools{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin:8px 0}
select,button{font:600 14px var(--body);padding:8px 12px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:7px;max-width:100%}
button{cursor:pointer}button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}
select:focus-visible,button:focus-visible,tr:focus-visible,a:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.quote{border-left:3px solid var(--gold);padding:4px 12px;margin:8px 0;font-size:15px}.quote a{font-size:12px}
.bar{height:10px;border-radius:5px;background:var(--line);overflow:hidden;min-width:80px}.bar i{display:block;height:100%}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:14px}
.small{font-size:13px;color:var(--mute)}
details summary{cursor:pointer;font-weight:600;margin:8px 0}
tr.grp td{background:var(--soft,rgba(160,120,0,.08));padding-top:10px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.card ul{margin:6px 0 0 18px;padding:0}.card li{margin:4px 0}
</style></head><body>
<nav aria-label="Sections"><b>CLAIMS vs RESULTS</b><a href="#verdict">Verdict</a><a href="#board">Leaderboard</a><a href="#recheck">Transcript re-check</a><a href="#money">The account machine</a><a href="#trader">Each trader</a><a href="#insights">Insights</a><a href="#method">Method</a></nav>
<main>
<section id="verdict"><h1>They claim millions.<br>Their rules don't show an edge.</h1>
<p class="lede" id="ledeText"></p><div class="kpis" id="kpis"></div><div class="cards" id="topcards"></div></section>
<section id="board"><h2>Leaderboard: claim vs their own rules</h2>
<p class="legend">Each row is the trader's own rule, coded from their page / episode, on NQ (2022–25 = P1, 2026 = P2). avg RR = average result in R after costs; WR = win rate; t-score 2+ in both periods = PASS. "Random" = the same trades at a random time that day. Click a row for everything about that trader.</p>
<div class="grid"><table><thead><tr><th class="l">Trader</th><th class="l">Their claim</th><th class="l">Their rule (headline)</th><th class="g">P1 trades</th><th>WR</th><th>avg RR</th><th>t</th><th class="g">P2 trades</th><th>WR</th><th>avg RR</th><th>t</th><th class="g">Combos tested</th><th>PASS</th><th>Random PASS</th><th class="g l">Verdict</th></tr></thead><tbody id="boardBody"></tbody></table></div></section>
<section id="recheck"><h2>Re-checked from the full transcripts: Kane, Okala, Fabio</h2>
<p class="lede">Max supplied the full episode transcripts. Each model was re-coded from the trader's own words (quotes and timestamps below), then re-tested with every entry × stop × target × exit, a random twin for every trade, and Max's fixed 50 pt 1:2 stop. P1 = NQ 2022–25, P2 = MNQ 2026 (Kane with ES: the two halves of 2026). PASS = t-score 2+ in both periods with 30+ trades each.</p>
<div id="rcBody"></div></section>
<section id="money"><h2>The account machine: how losing rules still post big payouts</h2>
<p class="lede">A trader copies one rule onto many prop accounts, rebuys every account that blows up, and posts the total of all payouts. The simulation below does exactly that with each trader's real backtest trades, and with random trades (no edge at all).</p>
<div class="cards" id="industry"></div>
<div class="tools"><label>Trader <select id="mStrat"></select></label><label>Period <select id="mPer"><option value="P1">2022–25 (NQ)</option><option value="P2">2026 (MNQ)</option></select></label></div>
<div class="grid"><table><thead><tr><th class="l">Accounts copied</th><th>Eval price</th><th class="g">Evals bought</th><th>$ spent on evals</th><th>Payouts</th><th>$ paid out</th><th>Best month (the screenshot)</th><th>Net after evals</th><th class="g">RANDOM trades: $ paid out</th><th>best month</th><th>net</th></tr></thead><tbody id="mBody"></tbody></table></div>
<p class="legend">Assumed generic 50k account: pass at +$3,000 before a $2,500 trailing drawdown, $1,000 daily loss stop; funded payouts of everything above a $2,600 buffer every 8 trading days (min $500, 100% of the first $25k then 90%); a blown account is replaced at once. All accounts take the same trades (a trade copier), started 5 trading days apart. Risk per trade = the trader's own size. Generic rows include no activation fee. Apex-like rows: $25 evaluation + $79 activation per funded account, payouts capped at $2,000 each and at most 6 payouts per account before it must be replaced. No consistency rule is modelled, so real payouts would be a bit lower.</p></section>
<section id="trader"><h2 id="tName">Each trader</h2><div class="tools"><label>Trader <select id="tSel"></select></label></div><div id="tBody"></div></section>
<section id="insights"><h2>Insights</h2><div class="cards" id="insightCards"></div></section>
<section id="method"><h2>Method, data and limits</h2><div class="cards" id="methodCards"></div></section>
<p class="small">Research only. Not financial advice. Built from public strategy pages and episode summaries; claims are the traders' own, unaudited. Data: NQ 1m Dec 2022–Nov 2025, MNQ / MES / MGC 2026.</p>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent),S=D.strategies;const $=s=>document.querySelector(s);
const f=(v,d=2)=>v==null||!isFinite(v)?'<span class="mu">–</span>':(v>0&&d>=2?'+':'')+(+v).toFixed(d);
const cr=v=>v==null||!isFinite(v)?'':v>0?'pos':v<0?'neg':'';const pc=v=>v==null||!isFinite(v)?'–':(v*100).toFixed(0)+'%';
const usd=v=>v==null||!isFinite(v)?'–':(v<0?'−$':'$')+Math.abs(Math.round(v)).toLocaleString();
const esc=s=>String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function verdict(s){const r=s.rules[0];if(!r)return['na','no data'];const a=r[5],b=r[11],t1=r[7],t2=r[13];
 if(s.passed>0)return['pass','passes'];if(r[3]<30)return['na','too few trades'];
 if(a!=null&&b!=null&&a>0&&b>0&&(t1>=1.5||t2>=1.5))return['watch','watch'];
 if(a!=null&&a<=-0.05)return['lose','loses'];return['zero','≈ zero'];}
const tot=S.reduce((a,s)=>a+s.tested,0),pas=S.reduce((a,s)=>a+s.passed,0),rp=S.reduce((a,s)=>a+s.rpassed,0);
$('#ledeText').textContent=`We coded ${S.length} futures strategies from Chart Fanatics traders straight from their own rules and tested them on NQ, ES and gold: every entry × stop × target × exit, two separate periods, and a random twin beside every trade. ${tot} combos had enough trades to judge. ${pas} passed. Random entries passed ${rp}.`;
$('#kpis').innerHTML=[[S.length,'strategies coded and tested','gold'],[tot,'combos with 30+ trades in both periods',''],[pas,'passed (t-score 2+ in both periods)',pas?'good':'bad'],[rp,'random-entry combos that passed (luck level)',''],[D.untested.length,'strategies not testable here (stocks / options / order book)','']].map(k=>`<div class="kpi ${k[2]}"><div class="n">${k[0]}</div><div class="l">${k[1]}</div></div>`).join('');
$('#topcards').innerHTML=D.insights.slice(0,3).map(x=>`<div class="card key"><h3>${esc(x[0])}</h3><p>${x[1]}</p></div>`).join('');
function board(){$('#boardBody').innerHTML=S.map((s,i)=>{const r=s.rules[0]||[];const v=verdict(s);
 return `<tr class="click" tabindex="0" data-i="${i}"><td class="l"><b>${esc(s.name)}</b></td><td class="l w">${esc(s.claims.headline||'')}</td><td class="l w">${esc(r[0])} <span class="mu">${r[1]} ${r[2]>=1440?'daily':r[2]+'m'}</span></td>
 <td class="g">${r[3]??'–'}</td><td>${pc(r[4])}</td><td class="${cr(r[5])}">${f(r[5])}</td><td class="${cr(r[7])}">${r[3]>=10?f(r[7],1):'–'}</td><td class="g">${r[9]??'–'}</td><td>${pc(r[10])}</td><td class="${cr(r[11])}">${f(r[11])}</td><td class="${cr(r[13])}">${r[9]>=10?f(r[13],1):'–'}</td>
 <td class="g">${s.tested}</td><td>${s.passed}</td><td>${s.rpassed}</td><td class="g l"><span class="pill v-${v[0]}">${v[1]}</span></td></tr>`}).join('')+
 D.untested.map(u=>`<tr><td class="l"><b>${esc(u[0])}</b></td><td class="l w">${esc(u[1])}</td><td class="l w mu" colspan="12">${esc(u[2])}</td><td class="g l"><span class="pill v-na">not tested</span></td></tr>`).join('');
 document.querySelectorAll('#boardBody tr.click').forEach(tr=>{const go=()=>{$('#tSel').value=tr.dataset.i;trader();location.hash='trader'};tr.onclick=go;tr.onkeydown=e=>{if(e.key==='Enter')go()}});}

function vRow(x){if((x.n1||0)<30||(x.n2||0)<30)return['na','too few'];if(x.t1>=2&&x.t2>=2)return['pass','passes'];
 if(x.avg1>0&&x.avg2>0)return['watch','watch'];if(x.avg1<=-0.05)return['lose','loses'];return['zero','≈ zero'];}
const yr=y=>y.map(a=>`<span class="${cr(a[3])}">${a[0]} ${f(a[3])}</span><span class="mu"> (${a[1]})</span>`).join(' · ');
$('#rcBody').innerHTML=D.recheck.map(t=>`<div class="card" style="margin:18px 0"><h3>${esc(t.name)}</h3>
<p class="small mu">Source: ${t.url?`<a href="${t.url}" target="_blank" rel="noopener">${esc(t.src)}</a>`:esc(t.src)}</p>
<div class="grid2"><div><h4>What they said</h4><ul>${t.quotes.map(q=>`<li>${q[0]?`<span class="mu">[${q[0]}]</span> `:''}${esc(q[1])}</li>`).join('')}</ul></div>
<div><h4>What was coded</h4><ul>${t.coded.map(c=>`<li>${esc(c)}</li>`).join('')}</ul></div></div>
<p><b>Verdict:</b> ${esc(t.verdict)}</p>
<p class="small mu">${t.grid.combos} combos · ${t.grid.tested} with 30+ trades in both periods · ${t.grid.passed} passed · random entries passed ${t.grid.rpassed}</p>
<div class="grid"><table><thead><tr><th class="l">Rule</th><th class="g">P1 trades</th><th>WR</th><th>avg RR</th><th>PF</th><th>t</th><th>Random</th><th class="g">P2 trades</th><th>WR</th><th>avg RR</th><th>PF</th><th>t</th><th>Random</th><th class="g l">Verdict</th><th class="g l">By year: avg RR (trades)</th></tr></thead>
<tbody>${t.rows.map(x=>{const v=vRow(x);return `<tr><td class="l w">${esc(x.label)}${x.note?`<div class="mu small">${esc(x.note)}</div>`:''}</td>
<td class="g">${x.n1}</td><td>${pc(x.wr1)}</td><td class="${cr(x.avg1)}">${f(x.avg1)}</td><td>${x.pf1==null?'–':x.pf1.toFixed(2)}</td><td class="${cr(x.t1)}">${x.n1>=10&&x.t1!=null&&Math.abs(x.t1)<99?f(x.t1,1):'–'}</td><td class="mu">${f(x.rnd1)}</td>
<td class="g">${x.n2}</td><td>${pc(x.wr2)}</td><td class="${cr(x.avg2)}">${f(x.avg2)}</td><td>${x.pf2==null?'–':x.pf2.toFixed(2)}</td><td class="${cr(x.t2)}">${x.n2>=10&&x.t2!=null&&Math.abs(x.t2)<99?f(x.t2,1):'–'}</td><td class="mu">${f(x.rnd2)}</td>
<td class="g l"><span class="pill v-${v[0]}">${v[1]}</span></td><td class="g l w small">${yr(x.years)}</td></tr>`}).join('')}</tbody></table></div></div>`).join('');

$('#industry').innerHTML=D.industry.map(x=>`<div class="card"><h3>${esc(x[0])}</h3><p>${x[1]}</p><p class="small"><a href="${x[2]}" target="_blank" rel="noopener">source</a></p></div>`).join('');
const withBurn=S.map((s,i)=>[s,i]).filter(([s])=>s.burn.length);
$('#mStrat').innerHTML=withBurn.map(([s,i])=>`<option value="${i}">${esc(s.name)}</option>`).join('');
function money(){const s=S[+$('#mStrat').value],p=$('#mPer').value;const rows=s.burn.filter(b=>b[3]===p);
 const labs=[...new Set(rows.map(b=>b[0]))];
 $('#mBody').innerHTML=labs.map(L=>{const rr=rows.filter(b=>b[0]===L);const h=rr[0];
  return `<tr class="grp"><td class="l" colspan="11"><b>Rule: ${esc(L)}</b> <span class="mu">· ${h[6]} trades taken (one at a time, their daily loss rule) · avg RR ${f(h[7])} · random twins ${f(h[8])}</span></td></tr>`+
  rr.map(b=>`<tr><td class="l">${b[4]} account${b[4]>1?'s':''}</td><td>$${b[5]}<div class="mu" style="font-size:11px">${b[19]==='Apex-like'?'Apex-like rules':'generic 50k'}</div></td><td class="g">${b[9]}</td><td class="neg">${usd(b[10])}</td><td>${b[11]}</td><td>${usd(b[12])}</td><td><b>${usd(b[13])}</b></td><td class="${cr(b[14])}"><b>${usd(b[14])}</b></td><td class="g">${usd(b[16])}</td><td>${usd(b[17])}</td><td class="${cr(b[18])}">${usd(b[18])}</td></tr>`).join('')}).join('')||'<tr><td class="l mu" colspan="11">Not enough trades in this period.</td></tr>';}
$('#mStrat').onchange=money;$('#mPer').onchange=money;
$('#tSel').innerHTML=S.map((s,i)=>`<option value="${i}">${esc(s.name)}</option>`).join('');
const sh=`<th class="g">P1 trades</th><th>WR</th><th>avg RR</th><th>PF</th><th>t</th><th>Random</th><th class="g">P2 trades</th><th>WR</th><th>avg RR</th><th>PF</th><th>t</th><th>Random</th>`;
const sc=(r,o)=>`<td class="g">${r[o]??'–'}</td><td>${pc(r[o+1])}</td><td class="${cr(r[o+2])}">${f(r[o+2])}</td><td>${r[o+3]==null?'–':(+r[o+3]).toFixed(2)}</td><td class="${cr(r[o+4])}">${(r[o]||0)>=10?f(r[o+4],1):'–'}</td><td class="mu">${f(r[o+5])}</td>`;
function trader(){const s=S[+$('#tSel').value],c=s.claims||{},v=verdict(s);$('#tName').textContent=s.name;
 let h=`<div class="two"><div class="card key"><h3>What they claim <span class="pill v-${v[0]}">${v[1]}</span></h3>${(c.quotes||[]).map(q=>`<div class="quote">${esc(q[0])}<br><a href="${q[1]}" target="_blank" rel="noopener">${esc(q[1].replace(/^https?:\/\//,'').slice(0,70))}</a></div>`).join('')||'<p class="mu">No numbers stated.</p>'}</div>
 <div class="card"><h3>What the test shows</h3><p>${c.insight||''}</p><p class="small">${s.tested} combos with 30+ trades in both periods · ${s.passed} passed · random passed ${s.rpassed}.</p></div></div>
 <h3 style="margin-top:16px">Their own rules</h3><div class="grid"><table><thead><tr><th class="l">Rule</th><th class="l">Market</th>${sh}</tr></thead><tbody>${s.rules.map(r=>`<tr><td class="l">${esc(r[0])}</td><td class="l">${r[1]} ${r[2]>=1440?'daily':r[2]+'m'}</td>${sc(r,3)}${sc(r,9)}</tr>`).join('')}</tbody></table></div>
 <h3 style="margin-top:16px">Year by year</h3><div class="grid"><table><thead><tr><th class="l">Rule</th>${[2023,2024,2025,2026].map(y=>`<th class="g">${y} trades</th><th>WR</th><th>avg RR</th><th>Random</th>`).join('')}</tr></thead><tbody>${s.years.map(y=>`<tr><td class="l">${esc(y[0])}</td>${[2023,2024,2025,2026].map(Y=>{const q=y[3].find(z=>z[0]===Y);return q?`<td class="g">${q[1]}</td><td>${pc(q[2])}</td><td class="${cr(q[3])}">${f(q[3])}</td><td class="mu">${f(q[4])}</td>`:'<td class="g mu">–</td><td></td><td></td><td></td>'}).join('')}</tr>`).join('')}</tbody></table></div>
 ${s.money.length?`<h3 style="margin-top:16px">One account, their size</h3><div class="grid"><table><thead><tr><th class="l">Rule</th><th class="l">Period</th><th>Trades</th><th>$ / month</th><th>Best month</th><th>Worst month</th><th>Green months</th><th class="g">50k evals</th><th>Passed</th><th>Risk</th></tr></thead><tbody>${s.money.map(r=>`<tr><td class="l">${esc(r[0])}</td><td class="l">${r[3]}</td><td>${r[4]}</td><td class="${cr(r[5])}">${usd(r[5])}</td><td>${usd(r[6])}</td><td>${usd(r[7])}</td><td>${pc(r[8])}</td><td class="g">${r[9]}</td><td>${pc(r[10])}</td><td>$${r[11]}</td></tr>`).join('')}</tbody></table></div>`:''}
 <details><summary>Every combo (${s.grid.length})</summary><div class="grid"><table><thead><tr><th class="l">Market</th><th class="l">Chart</th><th class="l">Entry</th><th class="l">Stop</th><th class="l">Target</th><th class="l">Exit</th>${sh}</tr></thead><tbody>${s.grid.map(g=>`<tr><td class="l">${g[0]}</td><td class="l">${g[1]>=1440?'daily':g[1]+'m'}</td><td class="l">${esc(g[2])}</td><td class="l">${esc(g[3])}</td><td class="l">${esc(g[4])}</td><td class="l">${esc(g[5])}</td>${sc(g,6)}${sc(g,12)}</tr>`).join('')}</tbody></table></div></details>
 <details><summary>How the rules were coded</summary><p class="small">${esc(s.method)}</p></details>`;
 $('#tBody').innerHTML=h;}
$('#tSel').onchange=trader;
$('#insightCards').innerHTML=D.insights.map(x=>`<div class="card"><h3>${esc(x[0])}</h3><p>${x[1]}</p></div>`).join('');
$('#methodCards').innerHTML=[
 ['Data','NQ 1-minute Dec 2022 – Nov 2025 (P1) and MNQ 2026 (P2; 1-minute covers about 2 months, 5-minute March–October). ES = MES and gold = MGC 2026 only, split into halves. Costs per trade: NQ 1 pt, ES 0.5, gold 0.2.'],
 ['Rules','Each strategy is coded from the trader\'s own Chart Fanatics / TradeZella strategy page and episode summaries. Where a rule is vague, ONE assumption is stated in the code (see "How the rules were coded" under each trader).'],
 ['Grid and controls','Every entry × stop × target × exit is paired, always including a fixed 50 pt (ES 20, gold 12) 1:2 test. Every trade has a random twin: same side, stop size and target in R, at a random time in the same window. PASS = t-score ≥ 2 in BOTH periods with 30+ trades each.'],
 ['What cannot be tested','Order-flow triggers (big-lot bubbles, footprint, CVD, DOM, heatmap) are replaced by volume proxies. Stock, options and forex-only strategies are not tested: no data here.'],
 ['Sources','YouTube blocks automated access, so rules and claims come from chartfanatics.com and tradezella.com strategy pages and public transcript summaries (SozAI, YouTubeSummary and others). Claims are quoted with their source link under each trader.']].map(x=>`<div class="card"><h3>${x[0]}</h3><p>${x[1]}</p></div>`).join('');
board();money();trader();
</script></body></html>'''
open('/home/claude/cf2/site/index.html', 'w').write(HTML.replace('__DATA__', J))
print(len(HTML) // 1024 + len(J) // 1024, 'KB')

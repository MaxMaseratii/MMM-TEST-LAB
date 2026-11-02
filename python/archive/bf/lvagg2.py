from lvagg import *
import warnings; warnings.filterwarnings('ignore')
S='structure (swing)'; F='fixed 1:2 (NQ 50 / ES 20 / GC 12)'
for m in ['NQ','ES','GC']:
  for tf in sorted(D[D.m==m].tf.unique()):
    b=D[(D.m==m)&(D.tf==tf)]; print(f'===== {m} {tf}m')
    L=b[b.variant=='LEVELS']
    for tg in ('her target','3R'):
        x=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==S)&(L.target==tg)]
        line(x,f'NY all levels, aggressive, {tg}')
        line(x[x.conf>=1],f'NY A+ (2+ levels stacked), aggressive, {tg}')
        line(x[x.conf>=2],f'NY 3+ levels stacked, aggressive, {tg}')
    x=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==F)]; line(x,'NY all levels, aggressive, fixed 1:2'); line(x[x.conf>=1],'NY A+, aggressive, fixed 1:2')
    x=L[(L.kind=='LV')&(L.trig=='aggr')&(L.stop==S)&(L.target=='her target')]
    for g in ['PD','LON','NYVP','WKVP','Z30','Z60']: line(x[x.grp==g],f'  NY {g} only, next-level target')
    z=x[x.grp.isin(['Z30','Z60'])&x.lvt.str.endswith('s')&x.fresh]; line(z,'  NY strict zones, first touch')
    z=x[x.lvt.isin(['pVAH','wVAH'])&(x.s==-1)|x.lvt.isin(['pVAL','wVAL'])&(x.s==1)|x.lvt.isin(['pdH'])&(x.s==-1)|x.lvt.isin(['pdL'])&(x.s==1)]; line(z,'  NY her directions only (VAH/PDH short, VAL/PDL long)')
    y=L[(L.kind=='LVA')&(L.trig=='aggr')&(L.stop==S)&(L.target=='her target')]
    line(y,'ASIA all levels, aggressive, next level')
    v=y[y.inVA&((y.lvt=='pVAH')&(y.s==-1)|(y.lvt=='pVAL')&(y.s==1))]; line(v,'ASIA her VP rule: open inside value, VAH short / VAL long')
    a=L[(L.kind=='AV')&(L.stop==S)]
    line(a[a.target=='3R'],'ASIA VWAP retest after range break, 3R'); line(a[a.target=='her target'],'ASIA VWAP retest, next level')
    I=b[(b.variant=='IB')&(b.stop==S)&(b.target=='her target')]
    fa=I[I.kind=='FA']; tc=I[I.kind=='TC']
    line(fa,'IB FA (old, no levels)'); line(fa[fa.conf>=1],'IB FA + swing into a level (her A+)'); line(fa[fa.conf>=2],'IB FA + swing into 2+ levels')
    line(tc,'IB TC (old)'); line(tc[tc.vwOK],'IB TC + VWAP'); line(tc[(tc.conf>=1)],'IB TC + level at IB mid'); line(tc[tc.vwOK&(tc.conf>=1)],'IB TC + VWAP + level')
    A=b[(b.variant=='ASIA')&(b.stop==S)&(b.target=='3R')]
    line(A[(A.kind=='AF')],'Tokyo sweep-fade 3R'); line(A[(A.kind=='AF')&(A.conf>=1)],'Tokyo sweep-fade 3R + level'); line(A[(A.kind=='AB')&A.vwOK],'Tokyo breakout-retest 3R + VWAP')

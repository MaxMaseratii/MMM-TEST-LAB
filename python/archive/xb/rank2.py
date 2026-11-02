import pickle, numpy as np, pandas as pd, json
from grid2 import ENAME, SNAME, TGT, XNAME, GNAME
D = pd.read_parquet('grid2_table.parquet')
O = pickle.load(open('grid2.pkl','rb'))
TFS=['5m','15m','1h','4h']; SIDES=['BULL','BEAR']
out = []
for tf in TFS:
    for sd in (0,1):
        for g in (0,1,2):
            ng_o = O[('old',tf)][1][g][sd]; ng_f = O[('fresh',tf)][1][g][sd]
            q = D[(D.tf==tf)&(D.side==sd)&(D.grp==g)]
            ok = q[(q.n_old>=100)&(q.n_26>=30)]
            for e in range(len(ENAME)):
                b = q[(q.entry==e)&(q.stop==0)&(q.target==2)&(q.exit==0)]
                r = dict(tf=tf, side=SIDES[sd], grp=GNAME[g], entry=ENAME[e], gmus_old=int(ng_o), gmus_26=int(ng_f))
                if len(b):
                    b=b.iloc[0]; r.update(fill_old=round(100*b.n_old/ng_o,1), fill_26=round(100*b.n_26/ng_f,1), wr_old=round(b.wr_old,1), wr_26=round(b.wr_26,1),
                        pf_old=round(b.pf_old,2), pf_26=round(b.pf_26,2), avg_old=round(b.avg_old,3), avg_26=round(b.avg_26,3), t_old=round(b.t_old,2), t_26=round(b.t_26,2), n_old=int(b.n_old), n_26=int(b.n_26))
                k = ok[ok.entry==e]
                if len(k):
                    w = k.sort_values('t_old', ascending=False).iloc[0]
                    r.update(wf_stop=SNAME[int(w.stop)], wf_tgt=f'1:{TGT[int(w.target)]:g}', wf_exit=XNAME[int(w.exit)], wf_avg_old=round(w.avg_old,3), wf_t_old=round(w.t_old,2),
                             wf_avg_26=round(w.avg_26,3), wf_t_26=round(w.t_26,2), wf_wr_26=round(w.wr_26,1), wf_pf_26=round(w.pf_26,2),
                             n_pass=int(((k.t_old>=2)&(k.t_26>=2)).sum()), n_combos=len(k))
                    k2 = k.assign(tmin=k[['t_old','t_26']].min(axis=1)).sort_values('tmin', ascending=False).iloc[0]
                    r.update(bb_stop=SNAME[int(k2.stop)], bb_tgt=f'1:{TGT[int(k2.target)]:g}', bb_exit=XNAME[int(k2.exit)], bb_avg_old=round(k2.avg_old,3), bb_avg_26=round(k2.avg_26,3), bb_t_old=round(k2.t_old,2), bb_t_26=round(k2.t_26,2),
                             bb_wr_old=round(k2.wr_old,1), bb_wr_26=round(k2.wr_26,1), bb_pf_old=round(k2.pf_old,2), bb_pf_26=round(k2.pf_26,2), bb_n_old=int(k2.n_old), bb_n_26=int(k2.n_26))
                out.append(r)
R = pd.DataFrame(out); R.to_parquet('rank2.parquet')
pd.set_option('display.width',260); pd.set_option('display.max_rows',500)
for tf in TFS:
    for sd in SIDES:
        for g in ['ALL','c3 BC (with)','c3 NBC']:
            x = R[(R.tf==tf)&(R.side==sd)&(R.grp==g)].copy()
            x = x.sort_values('wf_avg_26', ascending=False)
            print(f'\n=== {tf} {sd} {g}  GMUs {x.gmus_old.iloc[0]}/{x.gmus_26.iloc[0]}  pass-combos total {x.n_pass.sum()}')
            print(x[['entry','fill_old','fill_26','avg_old','avg_26','t_old','t_26','wf_stop','wf_tgt','wf_exit','wf_avg_old','wf_avg_26','wf_t_26','n_pass']].head(6).to_string(index=False))

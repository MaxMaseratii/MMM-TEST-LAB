import sys; sys.path.insert(0,'/home/claude/pp')
import ppdata, bfeng, numpy as np, pandas as pd
d=ppdata.series('NQ',15)[1]; S=bfeng.signals(d)
o,h,l,c=S['o'],S['h'],S['l'],S['c']; n=len(c)
rs=[]
for i,s in zip(S['fI'],S['fS']):
    if i+2>=n: continue
    ep=c[i]; stop=ep-s*50; tp=ep+s*100; r=None
    for j in range(i+1,min(i+100,n-1)+1):
        if (s==1 and l[j]<=stop) or (s==-1 and h[j]>=stop): r=(min(o[j],stop) if s==1 else max(o[j],stop)); break
        if (s==1 and h[j]>=tp) or (s==-1 and l[j]<=tp): r=tp; break
    if r is None: r=c[min(i+100,n-1)]
    rs.append((s*(r-ep)-1)/50)
rs=np.array(rs); print(len(rs), (rs>0).mean().round(3), rs.mean().round(4), (rs.mean()/rs.std(ddof=1)*np.sqrt(len(rs))).round(3))

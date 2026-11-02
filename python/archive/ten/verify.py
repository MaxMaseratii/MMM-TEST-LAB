from common import *
d1=raw()['old']
h4=rs(d1,'4h')
day=pd.Timestamp('2024-03-12')
b=h4.loc[day+pd.Timedelta(hours=6)]
seg=d1[(d1.index>=day+pd.Timedelta(hours=6))&(d1.index<=day+pd.Timedelta(hours=9,minutes=59))]
print('4H 06:00 bar', b.to_dict()); print('1m 06:00-09:59', seg.open.iloc[0],seg.high.max(),seg.low.min(),seg.close.iloc[-1], seg.index[0], seg.index[-1])
print('4h labels hours', sorted(set(h4.index.hour)))
h1=rs(d1,'1h'); print('1h 09:00', h1.loc[day+pd.Timedelta(hours=9)].to_dict(), 'close of 1m 09:59', d1.loc[day+pd.Timedelta(hours=9,minutes=59)].close)
m15=rs(d1,'15m'); print('15m 09:45', m15.loc[day+pd.Timedelta(hours=9,minutes=45)].to_dict())
# hand tests  (o,h,l,c,pH,pL)
tests=[((10,20,5,19,15,8),'BuC2+'),((10,20,5,16,15,8),'BuC2-'),((10,20,5,6,15,8),'BeC2+'),((10,20,5,7.5,15,8),'BeC2-'),
((10,20,9,19,15,8),'BuBC+'),((10,20,9,16,15,8),'BuBC-'),((10,14,2,3,15,8),'BeBC+'),((10,14,2,6,15,8),'BeBC-'),
((10,16,7,12,15,8),'S&D.BuAF'),((10,16,7,11,15,8),'S&D.BeAF'),((10,14,6,11,15,8),'BuAFs+'),((10,14,6,9,15,8),'BuAFs-'),
((10,16,9,12,15,8),'BeAFs+'),((10,16,9,14,15,8),'BeAFs-'),((10,14,9,12,15,8),'CI.BuAF'),((10,14,9,10,15,8),'CI.BeAF')]
for (a,e) in tests:
    r=ctype(*a); print(a,r,e,'OK' if r==e else 'FAIL', lean(r), family(r))
# real candle check
b5=bars('old','5m'); x=b5.loc[day+pd.Timedelta(hours=9,minutes=55)]; print(x.to_dict())
for k in ['old','fresh']: print(k,'good days',len(good_days(raw()[k])))

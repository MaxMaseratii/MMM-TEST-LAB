"""C/D: every rule / trend-line setting variant through the full grid (all hours + 09:45-12:00, no controls)."""
import sys, bfrun
VARS = {
    'c2_30': dict(kw=dict(c2pct=30.0)), 'c2_40': dict(kw=dict(c2pct=40.0)), 'c2_60': dict(kw=dict(c2pct=60.0)),
    'c2_75': dict(kw=dict(c2pct=75.0)), 'c2_100': dict(kw=dict(c2pct=100.0)),
    'bnd_wick': dict(kw=dict(bndWick=True)),
    'wait5': dict(kw=dict(maxWait=5)), 'wait10': dict(kw=dict(maxWait=10)), 'wait20': dict(kw=dict(maxWait=20)),
    'delta50': dict(kw=dict(dOn=True, dPct=50.0)),
    'step75': dict(kw=dict(stepPct=75.0)), 'step125': dict(kw=dict(stepPct=125.0)), 'step150': dict(kw=dict(stepPct=150.0)),
    'step_anycolor': dict(kw=dict(stepBC=False)),
    'line_body': dict(kw=dict(lvlWick=False)),
    'atr_fixed': dict(kw=dict(), atr_fixed=True),
    'atr7': dict(kw=dict(atrLen=7)), 'atr21': dict(kw=dict(atrLen=21)),
}
if __name__ == '__main__':
    markets = sys.argv[1:]
    for name, v in VARS.items():
        for m in markets:
            bfrun.run_market(m, kw=v['kw'], tag='var_' + name, slot_limit=2, controls=False, atr_fixed=v.get('atr_fixed', False))

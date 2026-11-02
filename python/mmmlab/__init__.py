"""MMM Test Lab - every MMM test tool in one place (Max Maserati, Nov 2026).

from mmmlab import data, candles, grade, money, levels, sessions, flip
  data      candles for NQ / MNQ / MES / MGC / MCL, the two periods, SPEC (fixed stop, cost, tick, $ per point)
  candles   BuBC / BeBC / NBC, ATR, foundation stats (BCs before the opposite BC / before the first NBC, points after 1 / 5 / 10)
  grade     signals -> every entry x stop x target x exit, random twin per trade, stats table, PASS rule (t >= 2 in both periods)
  money     one trade at a time, stop after N losses (no look-ahead), $ per month, 50k prop evaluation
  levels    volume profile, previous day / London / week levels, supply / demand zones, VWAPs, touch-and-reject finder
  sessions  initial balance (failed auction, trend continuation) and Tokyo range setups
  flip      MMM Body Flip Trend engine (C1 / C2 flip, PO4, trend line, ATR line, events) - mirrors the Pine
Archived engines (EDGE PRO, PRO FVA, FVA Break replica, PRO PLUS, XB, GMU, ...) are in archive/ - see archive/INDEX.md.
use_compat() puts compat/ (old mdata / ppdata on the new data pack) first on sys.path so archived scripts import cleanly."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def use_compat():
    p = os.path.join(HERE, 'compat')
    if p not in sys.path: sys.path.insert(0, p)
    return p

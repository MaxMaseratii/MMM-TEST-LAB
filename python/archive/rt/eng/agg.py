import pandas as pd, numpy as np, glob
OUT='/home/claude/rt/out'
def allgrid():
    fs=[f for f in glob.glob(f'{OUT}/[AGZ]_*.parquet')]
    d=pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    return d
if __name__=='__main__':
    d=allgrid(); d.to_parquet(f'{OUT}/ALL_grid.parquet'); print(len(d)); print(d.groupby(['period','family']).size())

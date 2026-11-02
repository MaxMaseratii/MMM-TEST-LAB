"""Honest re-run of the flip-zone entries: same engine, setups from replica3 (limit live from the prior close)."""
import sys; sys.path.insert(0, '/home/claude/fva')
import fva_grid, replica3, os
KEEP = {'② PES/PEL+', '④ CDL/CDS+', '② Nested PES/PEL+', '④ Nested CDL/CDS+'}
fva_grid.replica_run = lambda sig: [t for t in replica3.run(sig) if t['etype'] in KEEP]
fva_grid.OUT = '/home/claude/fva/grid_h'
os.makedirs(fva_grid.OUT, exist_ok=True)
fva_grid.run(sys.argv[1])

# PROJECT: The Generative Ledger
# PURPOSE: Certification harness (Continuity Ledger v2, Resumption Protocol
#          step 3, and Discipline Rule 7). Verifies that an engine file
#          reproduces the ten canonical archived rows BIT-EXACTLY across all
#          four scalar observables. Run this before trusting any engine,
#          instrumented variant, or new environment.
# USAGE:   python3 certify.py [path/to/engine.py]
#          (default: ../engines/rung1_v21_zeno.py; run from certification/)
# EXPECT:  "CERTIFICATION: PASS (10/10 bit-exact)". Anything else = broken
#          environment or modified dynamics. STOP.
# DEPENDENCIES: ../requirements.txt; engines/ on the exec path for the 01Q
#          layer (original or certified shim).

import sys, os
import numpy as np, pandas as pd

ENGINE = sys.argv[1] if len(sys.argv) > 1 else "../engines/rung1_v21_zeno.py"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# The ten canonical rows: (source_csv, mbar, dt, seed) spanning chronic and
# burst schedules, runaway and stable outcomes, and both extremes of the
# capacity lottery (seed 115: F=3.5; seed 103: F=35.6).
PANEL = [("u1_wall_101_120.csv", 16, 1, 101),
         ("u1_wall_101_120.csv", 16, 1, 103),
         ("u1_wall_101_120.csv", 26, 4, 110),
         ("u1_wall_101_120.csv", 40, 8, 120),
         ("u1_wall_101_120.csv", 32, 2, 115),
         ("u1_wall_101_120.csv", 20, 8, 101),
         ("u1_wall_101_120.csv", 26, 1, 114),
         ("u2_knee_121_140.csv", 20, 5, 125),
         ("u2_knee_121_140.csv", 26, 6, 133),
         ("u2_knee_121_140.csv", 32, 7, 140)]

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engines"))
ns = {}
exec(open(os.path.basename(ENGINE) if os.path.dirname(ENGINE) else ENGINE).read()
     if os.path.exists(os.path.basename(ENGINE)) else open(ENGINE).read(), ns)

ok = True
for csv, m, dt, s in PANEL:
    row = pd.read_csv(os.path.join(DATA, csv))
    row = row[(row.mbar == m) & (row.dt == dt) & (row.seed == s)].iloc[0]
    r = ns["grow_native"](seed=s, final_epoch=100, defect_inject_epoch=50,
                          r_core=0.06, pulse_size=m * dt, pulse_every=dt,
                          pulse_start=55, n_pulses=45 // dt)
    el = r.epoch_log
    late = el[el.epoch > 70]
    got = (round(float(np.polyfit(late.epoch, late.backlog, 1)[0]), 3),
           int(el.k.iloc[-1]),
           round(float(late.gamma.mean()), 2),
           round(float(late.served_vac.mean()), 2))
    exp = (row.slope, int(row.k), row.gamma, row.sV)
    match = all(abs(a - b) < 1e-9 for a, b in zip(got, exp))
    ok &= match
    print(f"m={m:2d} dt={dt} seed={s}: {'EXACT' if match else f'MISMATCH got {got} exp {exp}'}")

print("\nCERTIFICATION:", "PASS (10/10 bit-exact)" if ok else
      "FAIL — do not use this engine/environment")
sys.exit(0 if ok else 1)

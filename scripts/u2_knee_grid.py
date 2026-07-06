# PROJECT: The Generative Ledger — U2 knee grid (RESUMABLE v2)
# DATE: 2026-07-05. Pre-registration frozen in u2_calibration.py header and
# u2_knee_PREREG_predictions.csv (generated from calibration BEFORE this ran).
# GRID: mbar {20,26,32} x dt {5,6,7} x seeds 121-140. Frozen classifier:
# slope>1 over epochs 70-100. Frozen reduction: x = mbar/(gamma-sV) per run.
# USAGE: python3 u2_knee_grid.py [budget_seconds]
import os, sys, time
import numpy as np, pandas as pd
OUT = "u2_knee_121_140.csv"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e12
ns = {}; exec(open("rung1_v21_zeno.py").read(), ns)
def one(mbar, dt, seed):
    a = mbar*dt; n = 45//dt
    r = ns["grow_native"](seed=seed, final_epoch=100, defect_inject_epoch=50,
                          r_core=0.06, pulse_size=a, pulse_every=dt,
                          pulse_start=55, n_pulses=n)
    el = r.epoch_log; late = el[el.epoch > 70]
    return dict(mbar=mbar, dt=dt, seed=seed,
                slope=round(float(np.polyfit(late.epoch, late.backlog, 1)[0]),3),
                k=int(el.k.iloc[-1]), gamma=round(float(late.gamma.mean()),2),
                sV=round(float(late.served_vac.mean()),2))
if __name__ == "__main__":
    rows = pd.read_csv(OUT).to_dict("records") if os.path.exists(OUT) else []
    done = {(r["mbar"], r["dt"], r["seed"]) for r in rows}
    jobs = [(m,d,s) for m in [20,26,32] for d in [5,6,7]
            for s in range(121,141) if (m,d,s) not in done]
    t0 = time.time()
    for m,d,s in jobs:
        rows.append(one(m,d,s)); pd.DataFrame(rows).to_csv(OUT, index=False)
        print(f"{len(rows)}/180", m, d, s, rows[-1]["slope"], flush=True)
        if time.time()-t0 > BUDGET:
            print("BUDGET REACHED — resume by re-running", flush=True); sys.exit(0)
    print(f"DONE: {OUT}")

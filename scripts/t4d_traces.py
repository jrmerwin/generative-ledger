# H-T4c trace harvest (RESUMABLE): per-epoch gamma for all adjudication cells.
import os, sys, time
import numpy as np, pandas as pd
OUT = "t4d_traces.csv"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e12
ns = {}; exec(open("rung1_v21i3_instrumented.py").read(), ns)
J  = [("knee", m, d, s, 0.75) for m in [20,26,32] for d in [5,6,7] for s in range(121,141)]
J += [("chronic", m, 0, s, 0.75) for m in [12,16,20,26,32,40] for s in range(141,161)]
J += [("u1", m, d, s, 0.75) for m in [16,20,26,32,40] for d in [1,8] for s in range(101,121)]
def one(grid, m, d, s):
    kw = dict(seed=s, final_epoch=100, defect_inject_epoch=50, r_core=0.06)
    if d == 0: kw.update(m_defects=m)
    else: kw.update(pulse_size=m*d, pulse_every=d, pulse_start=55, n_pulses=45//d)
    el = ns["grow_native"](**kw).epoch_log
    g = el[el.epoch >= 50]
    return [dict(grid=grid, m=m, dt=d, seed=s, epoch=int(r.epoch), gamma=float(r.gamma),
                 sV=float(r.served_vac), D=float(r.vac_demand)) for r in g.itertuples()]
if __name__ == "__main__":
    rows = pd.read_csv(OUT).to_dict("records") if os.path.exists(OUT) else []
    done = {(r["grid"], r["m"], r["dt"], r["seed"]) for r in rows}
    t0 = time.time(); n = len(done)
    for grid,m,d,s,_ in [j for j in J if (j[0],j[1],j[2],j[3]) not in done]:
        rows += one(grid,m,d,s); n += 1
        pd.DataFrame(rows).to_csv(OUT, index=False)
        print(f"{n}/460 {grid} m={m} dt={d} seed={s}", flush=True)
        if time.time()-t0 > BUDGET:
            print("BUDGET REACHED", flush=True); sys.exit(0)
    print(f"DONE: {OUT}")

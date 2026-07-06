# PROJECT: The Generative Ledger — T1 instrumented run set (RESUMABLE)
# See PREREG_T1_transfer_function.md (frozen first). USAGE: python3 t1_transfer.py [budget]
import os, sys, time
import numpy as np, pandas as pd
OUT = "t1_events.csv"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e12
ns = {}; exec(open("rung1_v21i_instrumented.py").read(), ns)
def one(arm, mbar, dt, seed, p=0.75):
    kw = dict(seed=seed, final_epoch=100, defect_inject_epoch=50, r_core=0.06, p_ext=p)
    if dt == 0: kw.update(m_defects=mbar)                    # chronic
    else: kw.update(pulse_size=mbar*dt, pulse_every=dt, pulse_start=55, n_pulses=45//dt)
    el = ns["grow_native"](**kw).epoch_log
    ev = el[el.wedge_removed > 0]
    return [dict(arm=arm, mbar=mbar, dt=dt, seed=seed, epoch=int(r.epoch),
                 tag_pop=int(r.tag_pop), n_tagged=int(r.wedge_tagged),
                 removed=int(r.wedge_removed), gamma=float(r.gamma))
            for r in ev.itertuples()]
JOBS  = [("chronic", m, 0, s) for m in [16,26,40] for s in range(141,151)]
JOBS += [("knee", m, d, s) for m in [20,32] for d in [5,7] for s in range(121,131)]
JOBS += [("waveform", m, d, s) for m in [20,32] for d in [1,8] for s in range(101,111)]
if __name__ == "__main__":
    rows = pd.read_csv(OUT).to_dict("records") if os.path.exists(OUT) else []
    done = {(r["arm"], r["mbar"], r["dt"], r["seed"]) for r in rows}
    t0 = time.time(); ndone = len(done)
    for arm,m,d,s in [j for j in JOBS if j not in done]:
        rows += one(arm,m,d,s); ndone += 1
        pd.DataFrame(rows).to_csv(OUT, index=False)
        print(f"{ndone}/110 {arm} m={m} dt={d} seed={s} events={len(rows)}", flush=True)
        if time.time()-t0 > BUDGET:
            print("BUDGET REACHED — resume by re-running", flush=True); sys.exit(0)
    print(f"DONE: {OUT} total events={len(rows)}")

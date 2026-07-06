# PROJECT: The Generative Ledger — U4R: universality of the RELIEVED constant
# AUTHOR: Claude + J. Merwin   DATE: 2026-07-05
# NOTE: registered as U4R, not U4. Ledger-U4 tests the no-relief 1.30 on v19
# (unavailable; run when v19 is certified). U4R tests the relieved-economy
# constant on v21 (valve armed).
# PRE-REGISTRATION (frozen before any run of this file):
#   Arm 0 (baseline, p_ext=0.75, seeds 141-160, chronic load m in
#     {12,16,20,26,32,40}): H0 = chronic x50 consistent with the U1-derived
#     relieved constant 3.72, 95% CI [3.60,3.87] (fresh-seed, pure-chronic
#     confirmation; also tests schedule-independence vs the pulse-train
#     estimate). Consistency = CIs overlap.
#   Arms 1,2 (p_ext=0.6 and 0.9, same seeds/loads): x50 declared INVARIANT
#     under p iff each arm's 95% bootstrap CI contains Arm 0's point
#     estimate. Either outcome is a paper section (substrate constant vs
#     constant of the mechanism class).
#   Registered caveat (ledger 2.2): for p ~ 0.9 the starvation channel may
#     invert sign. If an arm shows no backlog accumulation at any load
#     (all slopes < 1), report REGIME CHANGE, not a constant shift.
#   Frozen throughout: classifier slope>1 over epochs 70-100; reduction
#     x = m/(gamma - sV) per run, late-window means; MLE logistic fit;
#     2000-resample bootstrap, rng seed 0.
# USAGE: python3 u4r_grid.py [budget_seconds]   (resumable)
import os, sys, time
import numpy as np, pandas as pd
OUT = "u4r_141_160.csv"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e12
ns = {}; exec(open("rung1_v21_zeno.py").read(), ns)
def one(p, m, seed):
    r = ns["grow_native"](seed=seed, final_epoch=100, defect_inject_epoch=50,
                          r_core=0.06, p_ext=p, m_defects=m)
    el = r.epoch_log; late = el[el.epoch > 70]
    return dict(p=p, m=m, seed=seed,
                slope=round(float(np.polyfit(late.epoch, late.backlog, 1)[0]),3),
                k=int(el.k.iloc[-1]), gamma=round(float(late.gamma.mean()),2),
                sV=round(float(late.served_vac.mean()),2))
if __name__ == "__main__":
    rows = pd.read_csv(OUT).to_dict("records") if os.path.exists(OUT) else []
    done = {(r["p"], r["m"], r["seed"]) for r in rows}
    jobs = [(p,m,s) for p in [0.75,0.6,0.9] for m in [12,16,20,26,32,40]
            for s in range(141,161) if (p,m,s) not in done]   # baseline arm first
    t0 = time.time()
    for p,m,s in jobs:
        rows.append(one(p,m,s)); pd.DataFrame(rows).to_csv(OUT, index=False)
        print(f"{len(rows)}/360", p, m, s, rows[-1]["slope"], flush=True)
        if time.time()-t0 > BUDGET:
            print("BUDGET REACHED — resume by re-running", flush=True); sys.exit(0)
    print(f"DONE: {OUT}")

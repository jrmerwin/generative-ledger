# PROJECT: The Generative Ledger
# AUTHOR: Claude + J. Merwin
# DATE: 2026-07-05
# PURPOSE: U2 calibration arm (RESUMABLE v2). Per-seed clear-time law
#          T_clear(A) on fresh seeds 121-140. PRE-REGISTRATION unchanged
#          from v1 (frozen 2026-07-05, before any knee-grid run):
#   H1 primary (drain arithmetic): cell (mbar, dt, seed) burst-stabilized iff
#       T_clear(a = mbar*dt; seed) <= dt, with T_clear from per-seed linear
#       least squares over A in {40,80,120,160,240}, censored runs excluded.
#   Success: >= 80% per-cell accuracy AND monotone knee locus.
#   SECONDARY (planned failure-mode analysis, run only after the primary is
#   reported as frozen): 'thermostat' model -- relief quota floor(tagged/6)
#   scales with population, so T_clear saturates at large A. Test: does a
#   saturating fit + quota-augmented drain recover >= 80%?
#   The primary test is NOT altered in response to calibration data.
# USAGE: python3 u2_calibration.py [budget_seconds]   (resumes from CSV)
import os, sys, time
import numpy as np, pandas as pd
SEEDS = list(range(121, 141)); SPIKES = [40, 80, 120, 160, 240]
OUT = "u2_calibration_121_140.csv"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 1e12
ns = {}; exec(open("rung1_v21_zeno.py").read(), ns)
def one(seed, A):
    r = ns["grow_native"](seed=seed, final_epoch=100, defect_inject_epoch=50,
                          r_core=0.06, spike_epoch=55, spike_ops=A)
    el = r.epoch_log; post = el[el.epoch >= 55]; zero = post[post.backlog == 0]
    t_clear = int(zero.epoch.iloc[0] - 55) + 1 if len(zero) else -1
    pre = el[(el.epoch >= 50) & (el.epoch < 55)]
    return dict(seed=seed, A=A, t_clear=t_clear, k=int(el.k.iloc[-1]),
                gamma_pre=round(float(pre.gamma.mean()), 2),
                sV_pre=round(float(pre.served_vac.mean()), 2),
                gamma_late=round(float(el[el.epoch > 70].gamma.mean()), 2))
if __name__ == "__main__":
    rows = pd.read_csv(OUT).to_dict("records") if os.path.exists(OUT) else []
    done = {(r["seed"], r["A"]) for r in rows}
    jobs = [(s, A) for s in SEEDS for A in SPIKES if (s, A) not in done]
    t0 = time.time()
    for s, A in jobs:
        rows.append(one(s, A)); pd.DataFrame(rows).to_csv(OUT, index=False)
        print(f"{len(rows)}/{len(SEEDS)*len(SPIKES)}", s, A,
              "t_clear=", rows[-1]["t_clear"], flush=True)
        if time.time() - t0 > BUDGET:
            print("BUDGET REACHED — resume by re-running", flush=True); sys.exit(0)
    print(f"DONE: {OUT}")

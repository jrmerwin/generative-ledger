# PROJECT: The Generative Ledger
# PRE-REGISTRATION: H-T4 — THE REDUCED QUEUEING LAW ("computational derivation")
# DATE FROZEN: 2026-07-05, before the reduced model is run against any target.
#
# CLAIM UNDER TEST: the engine's chronic wall and burst-stabilization knee are
# reproduced by a five-rule queue with ZERO fitted parameters. Every constant
# is measured (per-run Gamma, sV from archived CSVs) or derived (the 1/6
# even-quantized controller gain, T1b: 4227/4230 exact).
#
# MODEL (frozen; per epoch t = 50..100):
#   R1 DELIVERY   chronic: a_t = m for t >= 50.
#                 pulsed:  a_t = mbar*dt at t in {55, 55+dt, ...}, 45//dt pulses.
#   R2 SERVICE    forced requests R_f = a_t + B; vacuum demand R_v = sV (declared
#                 proxy); capacity Gamma. If R_f + R_v <= Gamma: serve all.
#                 Else served_f = Gamma * R_f/(R_f+R_v)  (hypergeometric
#                 expectation of the engine's randomized order).
#   R3 BACKLOG    B <- R_f - served_f.
#   R4 GROWTH     pop <- pop + 2*served_f  (each forced split: 1 tagged -> 3).
#                 pop initialized to 3 at injection (anchor split).
#   R5 RELIEF     if B >= Gamma and pop >= 6 (engine's len(_tag)>=6 guard):
#                 n = 2*ceil(max(1, floor(pop/6))/2);  pop -= n;
#                 B = max(0, B - n).   [T1b derived law, exact]
#   Constants per run: Gamma and sV = the archived late-window means of that
#   exact (schedule, seed) cell. No other inputs. Deterministic.
#
# OBSERVABLE + CLASSIFIER (identical to engine): slope of B over epochs 71-100
# (linear fit); runaway iff slope > 1.
#
# ADJUDICATION TARGETS AND SUCCESS CRITERIA (frozen):
#   PRIMARY (per authorization, seeds 121-140): u2_knee_121_140.csv, 180 runs.
#     S1: per-run runaway classification agreement >= 80%.
#     S2: reduced-model x50 (frozen reduction and fit) within the engine's
#         95% CI at each dt in {5,6,7}: [3.50,4.03], [3.94,4.38], [3.77,4.23].
#   SECONDARY: (a) u4r p=0.75 chronic arm (seeds 141-160, 120 runs): S1-type
#     agreement >= 80%; x50 within [3.37,3.71]. (b) u1_wall dt in {1,8}
#     (seeds 101-120): agreement >= 80%; qualitative reproduction of the
#     dt=8 lift (reduced x50(dt=8) > reduced x50(dt=1)).
#   Declared simplifications (candidate residue if criteria fail): constant
#     Gamma per run (engine's is live); sV as vacuum demand proxy; no tagged
#     growth from vacuum splits; no candidate-exhaustion channel; expectation
#     service (no shot noise).
# Either outcome is reportable: PASS = derived law; FAIL = the gap measures
# what the abstract queue misses about the geometry.

# ---------------------------------------------------------------------------
# AMENDMENT H-T4b — FROZEN 2026-07-05, after H-T4 adjudication, before any run
# H-T4 verdicts as frozen: S1 PASS (95.6% / 90.8% / 94.0%); S2 FAIL (dt=7 and
#   chronic walls ~10% high; dt=5,6 in; dt=8 lift reproduced).
# DIAGNOSIS CANDIDATE: expectation service (R2) removes shot noise; a
#   mean-field queue is more stable than a sampled one at equal means.
# H-T4b MODEL CHANGE (still zero fitted parameters): R2 replaced by the
#   engine's literal semantics — served_f ~ Hypergeometric(R_f, round(sV),
#   draw min(Gamma, R_f+round(sV))). All quantities integer. 20 Monte-Carlo
#   replicates per run, rng seed 0; per-run P(runaway) = replicate fraction;
#   classification = P >= 0.5; x50 fit on replicate-level outcomes.
# PREDICTION: walls move DOWN toward engine values; success criteria S1, S2
#   unchanged. If S2 still fails high, the residue is in live-Gamma
#   fluctuation or vacuum-split growth, in that order of suspicion.

# ---------------------------------------------------------------------------
# AMENDMENT H-T4c — FROZEN 2026-07-05, after H-T4b adjudication, before any run
# H-T4b verdict as frozen: prediction FAILED (walls unmoved; shot noise is not
#   the residue). Next-ranked candidate per registration: live-Gamma dynamics.
# H-T4c MODEL CHANGE (single substitution, still zero fitted parameters):
#   constant per-run Gamma replaced by the ENGINE'S OWN measured trace
#   Gamma(t), epochs 50-100, obtained by re-running the archived (schedule,
#   seed) cells on certified v21i2 (deterministic: identical runs). R2 stays
#   stochastic per T4b (hypergeometric, 20 reps, rng seed 0). sV remains the
#   constant late-window mean (one change per amendment; vacuum trace is the
#   next-ranked substitution, T4d, if needed).
# TARGETS: full grids — u2_knee (180), u4r p=0.75 chronic (120),
#   u1_wall dt in {1,8} (160).
# PREDICTION: walls drop INTO the engine CIs (S2 criteria unchanged:
#   dt5 [3.50,4.03], dt6 [3.94,4.38], dt7 [3.77,4.23], chronic [3.37,3.71]).
#   PASS = the ~10% residue is formally attributed to capacity-geometry
#   coupling, INTERNAL TO THE MODEL (ledger Rule 4: no physics referents).

# ---------------------------------------------------------------------------
# AMENDMENT H-T4d — FROZEN 2026-07-05, after T4c adjudication + demand
#   diagnostic, before any T4d adjudication run.
# T4c verdict as frozen: prediction FAILED. Walls unmoved under measured
#   Gamma(t). Capacity-trajectory coupling EXCLUDED as the residue. Bonus
#   robustness finding: wall location insensitive to capacity fluctuations.
# DIAGNOSTIC (30 runs, v21i3, documented): core vacuum demand is a standing
#   pool, 10-125x served rate; Gamma - D < 0 near the wall. The reduced model
#   omitted the second queue of a two-queue system. Sign matches the
#   too-stable bias. Vacuum-split growth demoted (wrong sign).
# T4d MODEL CHANGE (single substitution, zero fitted parameters):
#   R_v = measured per-epoch demand trace D(t) from certified v21i3
#   (bit-exact, 7/7), replacing constant sV. Gamma(t) traces retained from
#   T4c form. All else per T4b (hypergeometric, 20 reps, rng seed 0).
# TARGETS/CRITERIA unchanged (S1 >= 80%; S2 walls in engine CIs). STAGED:
#   primary u2_knee first; secondaries after. PREDICTION: walls drop INTO
#   the CIs. Registered risk: overshoot (walls dropping BELOW engine CIs)
#   would indicate the engine has a stabilizing channel the queue also
#   lacks; report either way.

# PROJECT: The Generative Ledger
# PRE-REGISTRATION: THE THERMOSTAT TRANSFER-FUNCTION TEST (T1)
# DATE FROZEN: 2026-07-05 — before any slope calculation on instrumented data.
# ENGINE: rung1_v21i_instrumented.py — v21 + two logged fields (tag_pop,
#   wedge_tagged); measurement-only patch CERTIFIED bit-exact on 10 archived
#   rows spanning u1_wall_101_120.csv and u2_knee_121_140.csv.
#
# MOTIVATION (from U2): the linear drain-arithmetic prediction FAILED as
# frozen (30.6% accuracy). Failure direction: pulse trains clear faster than
# matched single spikes. Candidate mechanism: relief quota floor(tag/6)
# scales with tagged population — a proportional controller ("thermostat").
#
# UNIT OF ANALYSIS: relief events = epochs with wedge_removed > 0.
#   Predictor: tag_pop logged that epoch. Response: wedge_tagged
#   (obligations voided by that event).
#
# REGISTERED RUN SET (110 runs; no other data enter the primary fits):
#   Chronic arm:  p=0.75, m in {16,26,40},        seeds 141-150
#   Knee arm:     mbar in {20,32} x dt in {5,7},  seeds 121-130
#   Waveform arm: mbar in {20,32} x dt in {1,8},  seeds 101-110
#
# HYPOTHESES AND DECISION RULES (frozen):
#   H-T1 (quota law): per-event wedge_tagged = beta * tag_pop with
#     beta = 1/6 ~ 0.1667, from the quota arithmetic max(1, floor(tag/6)).
#     Fit: OLS through the origin, per condition arm (chronic / knee /
#     waveform). PASS iff each arm's 95% CI contains 1/6.
#   H-T2 (controller constant): beta invariant across arms and loads.
#     Fit: per-(arm, load) slopes; INVARIANT iff each cell's 95% CI contains
#     the pooled beta-hat. If invariant, beta is registered as the valve's
#     controller gain — a new constant of the mechanism.
#   H-T3 (shortfall, secondary): fraction of events with wedge_tagged <
#     floor(tag_pop/6) measures geometric candidate exhaustion (the r90
#     radial gate + guard). Report its dependence on tag_pop; no threshold.
#   H-T4 (exploratory, declared): a two-parameter queue model (gain beta,
#     trigger Gamma) should reproduce the U2 knee ramp x50(dt) =
#     {3.69, 4.16, 4.01, 5.30}. Exploratory: no pass/fail; reported as fit
#     quality only. This is the mechanistic-derivation candidate for the
#     One Surface.
#
# KNOWN CENSOR: k is capped at 1 relief/epoch; event-level analysis is not
# affected by the k-ceiling, but any k~m^b refit must use below-ceiling
# loads only (separate registration; see known_dragons.txt).
#
# All fits: numpy OLS; bootstrap CIs 2000 resamples, rng seed 0, resampling
# at the RUN level (events within a run are correlated).

# ---------------------------------------------------------------------------
# AMENDMENT T1b — FROZEN 2026-07-05, after T1 adjudication, before any T1b run
# T1 verdicts as frozen: H-T1 FAIL, H-T2 NOT INVARIANT, H-T3 no exhaustion.
# DIAGNOSIS (documented, not adjudicated): registered predictor was population
#   at trigger; instrument logged population at epoch end (post-relief).
#   beta_measured -> ~1/5 = n/(pop-n) artifact. A declared-measure violation
#   (manuscript Section 3 class), by the analyst. T1 data are retained; T1
#   verdicts stand and are reported.
# T1b INSTRUMENT: rung1_v21i2_instrumented.py logs pop_trig = len(_tag) read
#   inside the valve at trigger, before any collapse. Certification required:
#   bit-exact scalars on the same 10 archived rows.
# T1b HYPOTHESIS (deterministic, event-level):
#   H-T1b: n_tagged == 2*ceil(max(1, floor(pop_trig/6))/2) for every relief
#     event. PASS iff >= 99% of events match exactly, with all mismatches
#     attributable to candidate exhaustion (n_tagged < prediction).
#   H-T2b (invariance, reframed): exact-match rate invariant across arms and
#     loads (each cell >= 99%). If PASS: the controller gain is exactly 1/6
#     with even quantization -- a derived constant of the valve, closing the
#     mechanism question T1 opened. Same registered run set as T1.

# THE GENERATIVE LEDGER — CONTINUITY DOCUMENT v2
## Project state, discipline rules, and the unification ladder
### Rewritten July 2026 after the Tier-0 campaign; supersedes v1. For resumption by any future collaborator (human or AI).

---

## 0. THE ONE-PARAGRAPH STATE

The DEU's economics is no longer merely measured; its Tier-0 core is DERIVED.
The validated mechanism M (boundary-limited generative bandwidth, backlog
accumulation, threshold-triggered topological relief) is now known to be a
TWO-QUEUE system: forced (defect) backlog and a standing vacuum-demand pool
compete hypergeometrically for boundary capacity Γ, relieved by a
deterministic proportional controller of derived gain 1/6 (even-quantized).
A five-rule reduction of this law, with ZERO fitted parameters, reproduces
per-run outcomes at 95–98% and derives the chronic wall, the
waveform-invariant band, and the burst-stabilization endpoint within
measurement CIs; two information variants of the reduction bracket every
measured wall, bounding a ±3% residue attributed to enumerated service
microstructure. The far-field geometry (Track B) remains the open frontier.
All claims are internal to the model.

## 1. VALIDATED RESULTS (evidence class and file; v1 results retained above the line)

### Carried forward from v1 (all still valid)
| Result | Evidence class | File |
|---|---|---|
| Graded starvation continuum (no bistability) | 30-seed sweep | sweep_v2_101_130.csv |
| No-relief collapse constant x50 = 1.30 (free-capacity units) | BLIND, 3 geometries; CI [1.17,1.45] | + r020 arm |
| Relief extends stability ~3x | matched dual-arm sweep | same |
| Collapse-valve/oracle stitch law k ∝ m^0.57 (see Dragon: k-ceiling) | 30-seed matched adjudication | adjudication_101_130.csv |
| Valve stability surplus (m50 26.2 vs 19.5) | same | same |
| Limit-cycle equilibrium with persistent mass | direct trajectory | v19 diagnostics |
| Acute Render Gate (dead zone below A* ≈ s+Γ) | pre-registered ladder | q1_gate_ladder.csv |
| Zeno-pattern suppression (60-as-10×6 → k=0) | pre-registered, monotone | q2_zeno.csv |
| Witness-loop null | clean negative | v18_1 session |
| Substrate d = 2.00 ± 0.11, bounded degree | 3-seed audit | rung1_v7.py, v7_substrate_audit.csv |

### New this campaign (July 2026)
| Result | Evidence class | File |
|---|---|---|
| U1: chronic wall waveform-invariant for Δt ∈ [1,4]; pooled relieved constant x50 = 3.72 [3.60,3.87] | 400 runs, 20 seeds, frozen classifier/reduction | u1_wall_101_120.csv |
| Per-run reduction x = m/(Γ−D_vac) predicts runaway at AUC 0.98–0.999 on three independent seed cohorts (the "seed lottery" is fully a capacity lottery) | cross-cohort generalization (seeds 101–120, 121–140, 141–160) | u1/u2/u4r CSVs |
| U2 primary: linear drain-arithmetic knee prediction FAILED as frozen (30.6% vs 80% threshold; predicted 1.4% stable vs 70.8% observed) | pre-registered, fresh seeds, prediction table timestamped before grid | u2_knee_PREREG_predictions.csv, u2_calibration_121_140.csv |
| U2: knee located — graded ramp, not a step: x50(Δt=5,6,7,8) = 3.69, 4.16, 4.01, 5.30; onset between Δt=5 and 6; invariance holds through Δt=5 | 180 runs fresh seeds + U1 endpoint | u2_knee_121_140.csv |
| U4R: relieved constant INVARIANT under exterior capacity exponent p ∈ {0.6, 0.75, 0.9}: x50 = 3.53, 3.52, 3.45; baseline PASS vs U1 band; no regime inversion at p=0.9 (registered caveat did not fire) | pre-registered 3-arm, 360 runs, fresh seeds 141–160 | u4r_141_160.csv |
| T1: statistical transfer-function test FAILED as frozen (β ≈ 0.193 ≈ 1/5, invariance rejected). Diagnosis: predictor logged post-relief (n/(pop−n) artifact) — declared-measure violation, design-law occurrence #5, by the analyst; dataset retained as specimen | pre-registered; failure + diagnosis on record before amendment | t1_events.csv, PREREG_T1_transfer_function.md |
| T1b: DERIVED controller law, deterministic and event-exact: n_tagged = 2·⌈max(1,⌊pop_trig/6⌋)/2⌉; 4227/4230 events exact across all schedules/loads/cohorts; 3 misses all exhaustion-side. Gain 1/6 (arithmetic), quantum 2 (topology). First derived (not measured) constant of the economy | pre-registered amendment, corrected instrument certified bit-exact 10/10 | t1b_events.csv, rung1_v21i2_instrumented.py |
| H-T4: five-rule one-queue reduction, zero fitted parameters: per-run agreement 90.8–95.6% (S1 PASS); walls uniformly ~10% high (S2 FAIL) | pre-registered, frozen model spec | PREREG_HT4_reduced_model.md |
| H-T4b: service shot noise is NOT the residue (walls unmoved) | pre-registered amendment, null | same |
| H-T4c: capacity trajectory Γ(t) is NOT the residue (walls unmoved). Bonus: wall location insensitive to capacity fluctuations — only means matter | pre-registered amendment, null; 500-run trace harvest | t4c_gamma_traces.csv |
| STRUCTURAL DISCOVERY: core vacuum demand is a STANDING POOL, 10–125× served rate; Γ − D < 0 near the wall. The economy is a two-queue system; near-wall stability is purchased by relief, not service | instrumented diagnostic (v21i3, certified 7/7) | v21i3 + diagnostic in session log |
| H-T4d: two-queue reduction with measured demand trace D(t): chronic wall DERIVED (3.45 ∈ [3.37,3.71], 98.3% agreement); Δt=1 IN (3.44); Δt=7 IN (3.96); Δt=8 endpoint IN (4.93 ∈ [4.91,5.71]); Δt=5,6 marginally low (3.38, 3.84). BRACKET PROPERTY: every measured wall lies between the T4c (one-queue, high) and T4d (two-queue, low) variants; residue ±3%, attributed to enumerated service microstructure (capacity redistribution on unservable draws) | pre-registered amendment; 4/6 walls in CI, zero fitted parameters | t4d_traces.csv |
| Cross-machine/system reproducibility: engine reproduces archived M2 results bit-exactly (10 diverse rows, all four observables) via certified 01Q shim | certification harness | shim + session log |

## 2. RETRACTED / KILLED (do not resurrect without new evidence)

Unchanged from v1 — no retractions this campaign; registered failures (U2
primary, T1, T4/S2, T4b, T4c) are NOT retractions: they are adjudicated
negative results and live in Section 1 as the path that isolated the
two-queue structure.

- "13/13 staircase law" (circular)
- k_max ≈ 3 curvature saturation (killed by static control)
- Bistable "Death Spiral" (killed by 30-seed statistics)
- "Native economy collapsed the geometry" (measure artifact)
- Hub substrate (node-0 artifact); pre-v7 geometry suspect
- 432 / registry-foam identifications (bridge does not exist; blocked)

## 3. DISCIPLINE RULES (non-negotiable; occurrence counter now at FIVE)

1. Pre-register predictions and fit procedures before runs; frozen targets only.
   Amendments are permitted ONLY with the prior failure and its diagnosis on
   the record first (T1→T1b, T4→T4b→T4c→T4d are the templates).
2. Any observable must declare its measure — node/area/length,
   Eulerian/Lagrangian, AND its timing relative to the event it measures
   (served vs demanded; pre-trigger vs post-relief). New clause forced by T1.
3. Every legal move must respect the metric structure it acts on.
4. Internal claims only: "within the DEU," never "in physics." (Enforced
   twice this campaign against draft manuscript language.)
5. Controls adjudicate hypotheses; enthusiasm does not. Report failures with
   the same prominence as passes — this campaign's chain of three nulls
   (T4b, T4c) and two primary failures (U2, T1) produced its biggest result.
6. Distinguish frozen-engine tests from postulate extensions; count postulates.
7. (New) Instruments are engines: every instrumented variant must be
   certified bit-exact against archived rows before its data are used, and
   its certification scope declared (v21i/v21i2/v21i3: scalar pipeline
   observables only).

## 4. THE UNIFICATION LADDER — STATUS

### TIER 0 — frozen engine, zero new postulates: **COMPLETE**
- U1 One Surface: DONE. One wall for Δt ≤ 5 in free-capacity units; ramp above.
- U2 Boundary: DONE. Primary failed as frozen; knee located; mechanism
  reassigned from drain arithmetic to the thermostat (T1b).
- U3 Acute Violence Ratio: NOT RUN (deprioritized; the two-queue law now
  predicts it — run as a consistency check, not a discovery).
- U4 (ledger-original, no-relief 1.30 under p): OPEN — requires v19
  (unavailable/uncertified). U4R (relieved constant) ran in its place: PASS.

### TIER 0.5 — the DERIVED LAW (zero postulates, zero fitted parameters): **COMPLETE**
The five-rule two-queue reduction (delivery; hypergeometric competition of
forced backlog + standing vacuum demand for Γ; backlog; +2 growth per served
forced op; 1/6 even-quantized relief above trigger with pop ≥ 6 guard).
Constants: Γ, D(t), sV measured; gain derived. Status: derives 4/6 walls
within CIs, brackets all 6, 95–98% per-run agreement. STOPPING POINT
DECLARED: the ±3% residue is token-level service microstructure; modeling it
reimplements the engine and voids the reduction claim. Do not chase it.

### TIER 1 — one declared postulate each (gates now open)
U5 deferred-load construct, U6 χ orientation algebra, U7 native α: unchanged
from v1, including all warnings and the positivity obstruction. The two-queue
law strengthens U7's prospects: Γ/D fluctuation statistics are now
characterized objects.

### FORBIDDEN SHORTCUTS — unchanged from v1, plus:
- Do not "improve" the reduced model past the declared stopping point.
- Do not fit the ±3% residue; it is bounded by the bracket, not modeled.

## 5. OPEN PROBLEMS (gated, specified)
- Far-field Ξ = k/6 (Track B; failure taxonomy = specification). UNCHANGED —
  and now the manuscript's explicitly declared frontier.
- Ledger-U4: does 1.30 (no-relief) move under p? Blocked on locating and
  certifying rung1_v19_livevalve.py.
- The 3.72 (pulse-train) vs ~3.5 (chronic) relieved-constant spread:
  overlapping CIs, but the pattern suggests a small schedule effect.
  Consolidation is a statistics problem (pooled higher-n analysis), not a
  new experiment.
- Δt=5,6 marginal low misses of T4d: bounded by the bracket; revisit only if
  Tier 1 needs them.
- k ∝ m^0.57 below-ceiling refit (see Dragon: k-ceiling). Registered, unrun.
- Valve stability surplus (demand-restructuring hypothesis): still formally
  untested, but the standing-pool discovery is adjacent evidence — a
  collapse removes faces that would otherwise frustrate. Design a matched
  D(t)-trace comparison, oracle vs valve.
- Seed-303 pinch-off; registry↔foam bridge; oracle tight-geometry threshold:
  unchanged. (Note: the "relieved-economy dimensionless constant" open
  problem from v1 is RESOLVED: ≈3.5, universal under p — U4R.)
- Original DEU_GR_Experiment_01Q_coherent_topology_stitch_layer3.py: missing.
  Shim certified for scalar observables only. Any spatial_snapshots /
  geometry claim requires the original or a geometry-scope re-certification.

## 6. RESUMPTION PROTOCOL (v2)
1. Read this file, then the manuscript, then known_dragons.txt.
2. pip install -r requirements.txt (pins: numpy 2.4.4, pandas 3.0.2,
   scipy 1.17.1, networkx 3.6.1).
3. Run the certification harness: rung1_v21_zeno.py (via 01Q original or
   shim) on the 10 canonical rows (7 from u1_wall_101_120.csv incl. seeds
   101/103/110/114/115/120; 3 from u2_knee_121_140.csv: 20-5-125, 26-6-133,
   32-7-140). ALL FOUR observables (slope, k, Γ, sV) must match bit-exactly.
   Anything less = broken environment; stop.
4. Engines are deterministic given seed. Trust nothing in Section 1 without
   its file; trust nothing new without Section 3.
5. All sweep scripts are resumable (incremental CSV, skip-completed, budget
   arg) — required in environments that reap background processes.

## 7. FILE MANIFEST (this campaign)
Engines: rung1_v21_zeno.py; rung1_v21i_instrumented.py (+tag_pop,
wedge_tagged); rung1_v21i2_instrumented.py (+pop_trig); rung1_v21i3_
instrumented.py (+vac_demand); 01Q shim (certified: scalars).
Registrations: u2_calibration.py header (+T1 secondary), u2_knee_grid.py
header, u4r_grid.py header, PREREG_T1_transfer_function.md (T1+T1b),
PREREG_HT4_reduced_model.md (T4+T4b+T4c+T4d).
Data: u1_wall_101_120.csv; u2_calibration_121_140.csv;
u2_knee_PREREG_predictions.csv; u2_knee_121_140.csv; u4r_141_160.csv;
t1_events.csv; t1b_events.csv; t4c_gamma_traces.csv; t4d_traces.csv.
Hazards: known_dragons.txt (stitch_logic.py quarantine; missing 01Q;
background-process reaping; post-relief-logging trap; k-ceiling; seed 303).

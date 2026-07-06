# The Generative Ledger

**Bandwidth economics of topological relief in a Discrete Emergent Universe (DEU) — and the derived two-queue law unifying its chronic and acute regimes.**

Jason Merwin, Independent Researcher, Ashland, Oregon. Simulations and analysis performed in collaboration with Anthropic's Claude (Fable 5); see the manuscript Acknowledgments. **All claims are internal to the model** — see "Scope discipline" in the manuscript, Section 1.

## What this is

A frozen, deterministic simulation engine (a growing degree-regulated triangulated foam with a bandwidth-limited scheduler and a manifold-legal topological relief valve), the complete pre-registered experimental record characterizing its load economics, and a five-rule two-queue reduction that **derives** the engine's collapse walls with zero fitted parameters. The central results:

- The relieved economy's collapse wall is a dimensionless constant (≈3.5 in free-capacity units), invariant across load schedules, three independent seed cohorts, and exterior capacity exponents.
- The relief valve's transfer function is exact: `n = 2·ceil(max(1, floor(pop/6))/2)` — 4227/4230 events. Gain 1/6 (arithmetic), quantum 2 (topology). Derived, not measured.
- A two-queue law (forced backlog + standing vacuum demand competing for boundary capacity, relieved by the derived controller) reproduces per-run outcomes at 95–98% and derives 4/6 measured walls within CIs, bracketing all 6, with **zero fitted parameters**.
- Three consecutive pre-registered failures (drain arithmetic, shot noise, capacity trajectory) are how the two-queue structure was found. They are documented with the same prominence as the passes.

## Repository layout

```
CONTINUITY_LEDGER.md    The truth source. Read this FIRST. Validated results
                        with evidence classes, retractions, discipline rules,
                        the unification ladder, and the resumption protocol.
known_dragons.txt       Code-level hazards. Read this SECOND.
manuscript/             Merged manuscript (tex + pdf) and Figures 5-8
                        (generated from data/ — every plotted point traces
                        to a file in this repo).
engines/                Frozen engines. rung1_v21_zeno.py is the base;
                        v21i/v21i2/v21i3 are certified measurement-only
                        instrumented variants (certification scope: scalar
                        pipeline observables). The 01Q file here is a
                        RECONSTRUCTED SHIM, certified bit-exact for scalars;
                        the original is lost (see Dragons and manuscript
                        Limitations).
registrations/          Frozen pre-registration documents, including the
                        failed primaries and their amendments — the failures
                        are the discovery path, kept intact.
scripts/                Resumable sweep/harvest scripts (incremental CSV,
                        skip-completed, budget arg).
data/                   All per-run CSVs and event datasets behind every
                        table and figure.
certification/          certify.py — the resumption protocol as code.
```

## Reproduction (the resumption protocol)

```bash
pip install -r requirements.txt      # pinned environment
cd certification && python3 certify.py
```

Expected output: `CERTIFICATION: PASS (10/10 bit-exact)`. All engines are deterministic given a seed; every table and figure in the manuscript regenerates from `data/` and `scripts/`. If certification fails, the environment is broken — trust nothing until it passes (Discipline Rule 7: *instruments are engines*).

## Discipline rules (abbreviated — full text in the ledger)

1. Pre-register predictions and fit procedures before runs; amendments only with the prior failure and its diagnosis on the record first.
2. Every observable declares its measure — including its **timing** relative to the event it measures.
3. Every legal move respects the metric structure it acts on.
4. Internal claims only: "within the DEU," never "in physics."
5. Controls adjudicate; enthusiasm does not. Failures are reported with the same prominence as passes.
6. Frozen-engine tests are distinguished from postulate extensions.
7. Instruments are engines: certified bit-exact before their data count.

## Status and frontier

Tier 0 (measurement) and Tier 0.5 (the derived law) are complete; the reduction program has a **declared stopping point** (do not fit the ±3% residue — it is bounded by the bracket, not modeled). The open frontier is the far-field deficit operator (Ξ = k/6), posed in the manuscript with a complete failure taxonomy as its specification. Tier 1 items (U5–U7) are gated postulate extensions; see the ledger before attempting any.

## License

TBD by the author. Until a license file is added, all rights reserved.

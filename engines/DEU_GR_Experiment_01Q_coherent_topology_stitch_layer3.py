# PROJECT: The Generative Ledger
# AUTHOR: Claude (RECONSTRUCTED SHIM -- NOT the original 01Q layer)
# DATE: 2026-07-05
# PURPOSE: Minimal reconstruction of the four symbols rung1_v21_zeno.py
#          imports from the original DEU_GR_Experiment_01Q file:
#          _cs_adj_from_state, _cs_raw_bulk_center,
#          CoherentStitchSnapshot, CoherentStitchRun.
#          VALID ONLY IF certified by exact reproduction of archived CSV
#          rows (deterministic seeds). If certification fails, discard.
# DEPENDENCIES: numpy (via engine namespace); stdlib only here.

import itertools as _it
from collections import deque as _deque
from dataclasses import dataclass, field
from typing import Any

_CENTER_VARIANT = ["boundary_bfs_min"]  # mutable switch for certification


@dataclass
class CoherentStitchSnapshot:
    epoch: int
    active_faces: Any
    face_nodes: Any
    face_types: Any
    face_depth: Any
    face_neighbors: Any
    face_defect: Any
    stats: Any = field(default_factory=dict)


@dataclass
class CoherentStitchRun:
    stats: Any
    spatial_snapshots: Any
    epoch_log: Any


def _cs_adj_from_state(faces, edge_to_faces, active):
    """Face-adjacency over the active set: neighbors share an edge."""
    adj = {f: set() for f in active}
    for e, fs in edge_to_faces.items():
        fl = [f for f in fs if f in adj]
        if len(fl) < 2:
            continue
        for a, b in _it.combinations(fl, 2):
            adj[a].add(b)
            adj[b].add(a)
    return adj


def _cs_raw_bulk_center(adj):
    """Bulk center: multi-source BFS inward from boundary faces
    (faces with < 3 neighbors); center = face at maximal hop depth.
    Returns (center, depth_of_center, depth_map)."""
    if not adj:
        return None, 0, {}
    boundary = sorted(f for f, nb in adj.items() if len(nb) < 3)
    if not boundary:  # closed complex: fall back to eccentricity from min id
        boundary = [min(adj)]
    depth = {f: 0 for f in boundary}
    q = _deque(boundary)
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in depth:
                depth[w] = depth[u] + 1
                q.append(w)
    for f in adj:  # disconnected pieces, if any
        depth.setdefault(f, 0)
    variant = _CENTER_VARIANT[0]
    dmax = max(depth.values())
    deepest = [f for f, d in depth.items() if d == dmax]
    if variant == "boundary_bfs_min":
        center = min(deepest)
    elif variant == "boundary_bfs_max":
        center = max(deepest)
    else:  # first in dict (insertion) order
        center = next(f for f in adj if depth[f] == dmax)
    return center, dmax, depth

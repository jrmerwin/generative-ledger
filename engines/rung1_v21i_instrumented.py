"""v8 NATIVE-OVERFLOW SCHEDULER.
Core window = weighted face-ball (radius r_c) around defect anchor.
Capacity Gamma_core = live count of core boundary edges (counted, not passed).
Forced ops + frustrated splits + flips genuinely compete; unserved forced ops
pile up as literal backlog. Trigger: backlog >= Gamma_core -> wedge surgery
(weighted-metric corridor excision) as the only relief. No B, Qdot, or k-formula
anywhere in the engine.
Substrate: v7 (randomized typing + depth-matched flips). Exterior runs on the
global sub-extensive rule N^0.75 (full tiling is future work; declared).
"""
import itertools, heapq, time
from collections import defaultdict, Counter, deque
import numpy as np, pandas as pd

import os as _os
BASE = _os.environ.get("DEU_DEPS") or next(
    (p for p in [_os.path.join(_os.getcwd(),"..","deps"),
                 _os.path.join(_os.getcwd(),"deps"),
                 _os.path.join(_os.getcwd(),"generative-ledger","deps"),
                 _os.path.join(_os.getcwd(),"..","..","deps")]
     if _os.path.exists(p)), "deps")
g = globals()
# exec(compile(open(f"{BASE}/deu_exp456_minimal.py").read(), "eng", "exec"), g)
# exec(compile(open(f"{BASE}/DEU_GR_Experiment_01Q_coherent_topology_stitch_layer3.py").read(), "01Q", "exec"), g)

exec(compile(open("deu_exp456_minimal.py").read(), "eng", "exec"), g)
exec(compile(open("DEU_GR_Experiment_01Q_coherent_topology_stitch_layer3.py").read(), "01Q", "exec"), g)

# ---------- wedge on live engine state (v6.2 port) ---------------------------
def _node_dijkstra(faces, e2f, depth, v, maxd):
    lengths = {f: (3.0 ** -0.5) ** depth[f] for f in faces}
    adj = defaultdict(list)
    for e, fs in e2f.items():
        if not fs: continue
        w = float(np.mean([lengths[f] for f in fs]))
        a, b = tuple(e); adj[a].append((b, w)); adj[b].append((a, w))
    dist = {v: 0.0}; par = {v: None}; heap = [(0.0, v)]
    while heap:
        du, u = heapq.heappop(heap)
        if du != dist.get(u) or du > maxd: continue
        for w, l in adj[u]:
            nd = du + l
            if nd <= maxd and nd < dist.get(w, 1e18):
                dist[w] = nd; par[w] = u; heapq.heappush(heap, (nd, w))
    return dist, par, adj, lengths

def _npath(par, x):
    p = [x]
    while par[p[-1]] is not None: p.append(par[p[-1]])
    return p[::-1]

def wedge_native(faces, e2f, depth, defect, remove_cb, v, add_cb=None, types=None, dbg=None,
                 r_in=0.003, r_out=0.30, band_w=0.12, frac=1/6., rot=0):
    dist, par, adj, lengths = _node_dijkstra(faces, e2f, depth, v, r_out + 0.2)
    tn=set()
    for f,ok in defect.items():
        if ok and f in faces: tn |= faces[f]
    dv=[dist[n] for n in tn if n in dist]
    if len(dv)>=12:
        r_out=max(1e-4,float(np.percentile(dv,90)))
        r_in=r_out*0.02; band_w=r_out*0.30
    band=[]; bw=band_w
    while bw <= r_out*0.85:
        band = sorted([n for n, d in dist.items() if r_out - bw < d <= r_out])
        if len(band) >= 6: break
        bw *= 1.6
    if len(band) < 4: return None
    bset = set(band)
    x = band[(rot * 37) % len(band)]
    bd = {x: 0.0}; heap = [(0.0, x)]
    while heap:
        du, u = heapq.heappop(heap)
        if du != bd.get(u): continue
        for w, l in adj[u]:
            if w not in bset: continue
            nd = du + l
            if nd < bd.get(w, 1e18): bd[w] = nd; heapq.heappush(heap, (nd, w))
    if len(bd) < 3: return None
    M = max(bd.values()); tgt = 2.0 * M * frac
    y = min(bd, key=lambda n: abs(bd[n] - tgt))
    P1, P2 = _npath(par, x), _npath(par, y)
    cut = set()
    for P in (P1, P2):
        for i in range(len(P) - 1): cut.add(frozenset((P[i], P[i+1])))
    inner = {n for n, d in dist.items() if d < r_in}
    ball = {f for f in faces if all(dist.get(n, 1e9) <= r_out for n in faces[f])}
    if len(ball) < 20: return None
    e0 = frozenset((P1[1], P1[2])) if len(P1) > 2 else None
    if e0 is None: return None
    best = None
    for s in list(e2f.get(e0, [])):
        if s not in ball: continue
        if faces[s] & inner: continue
        reg = {s}; q = deque([s]); ok = True
        while q:
            u = q.popleft()
            for e in [frozenset(p) for p in itertools.combinations(sorted(faces[u]), 2)]:
                if e in cut: continue
                for w in e2f.get(e, ()):
                    if w in reg or w not in ball: continue
                    if faces[w] & inner: continue
                    reg.add(w); q.append(w)
            if len(reg) > 0.55 * len(ball): ok = False; break
        if ok and (best is None or len(reg) < len(best)): best = reg
    if not best: return None
    n_tag = sum(1 for f in best if defect.get(f, False))
    removed_nodes = set().union(*[faces[f] for f in best])
    for f in list(best): remove_cb(f)
    sew_pairs = sew_dup = sew_degen = sew_fill = 0; sew_status = "none"
    if add_cb is not None and types is not None:
        def contract(y, x):
            nonlocal sew_dup, sew_degen
            for fid in [f for f in list(faces) if y in faces[f]]:
                nd = frozenset(x if n == y else n for n in faces[fid])
                tp, dp, df = types[fid], depth[fid], defect[fid]
                remove_cb(fid)
                if len(nd) == 3:
                    dup = False
                    for e in [frozenset(p) for p in itertools.combinations(sorted(nd), 2)]:
                        for gf in e2f.get(e, ()):
                            if faces[gf] == nd: dup = True; break
                        if dup: break
                    if dup: sew_dup += 1
                    else: add_cb(nd, tp, dp, df)
                else: sew_degen += 1
        bedges = [e for e, fs in e2f.items() if len(fs) == 1 and e <= removed_nodes]
        badj = defaultdict(set)
        for e in bedges:
            a, b = tuple(e); badj[a].add(b); badj[b].add(a)
        if bedges and all(len(v) == 2 for v in badj.values()):
            c0 = min(badj, key=lambda n: dist.get(n, 1e18))
            cyc = [c0]; prev = None
            while True:
                nxts = [w for w in badj[cyc[-1]] if w != prev]
                if not nxts: break
                prev = cyc[-1]; cyc.append(nxts[0])
                if cyc[-1] == c0: cyc.pop(); break
                if len(cyc) > 4 * len(bedges): break
            if len(cyc) >= 4 and len(set(cyc)) == len(cyc):
                sew_status = "zipped"; guard_trips = 0
                while len(cyc) > 3 and guard_trips < 3 * len(cyc):
                    x, y = cyc[1], cyc[-1]
                    if x == y or frozenset((x, y)) in e2f:
                        cyc = cyc[1:] + cyc[:1]; guard_trips += 1; continue
                    nbx = {n for f in list(faces) if x in faces[f] for n in faces[f]} - {x}
                    nby = {n for f in list(faces) if y in faces[f] for n in faces[f]} - {y}
                    if (nbx & nby) - {cyc[0]}:
                        cyc = cyc[1:] + cyc[:1]; guard_trips += 1; continue
                    contract(y, x); sew_pairs += 1
                    cyc = [x] + cyc[2:-1]
                if len(cyc) == 3 and not any(frozenset(p) in e2f and
                        len(e2f[frozenset(p)]) > 1 for p in itertools.combinations(cyc, 2)):
                    dps = [depth[f] for e in itertools.combinations(cyc, 2)
                           for f in e2f.get(frozenset(e), ())]
                    if dps:
                        add_cb(tuple(cyc), "S", int(np.median(dps)), False)
                        sew_fill += 1
            else:
                sew_status = "nonsimple"
        elif bedges:
            sew_status = "nonsimple"
    return dict(n_removed=len(best), n_tagged=n_tag, sew_pairs=sew_pairs,
                sew_dup=sew_dup, sew_degen=sew_degen, sew_fill=sew_fill,
                sew_status=sew_status)

# ---------- native engine -----------------------------------------------------
def grow_native(*, final_epoch=100, seed=101, p_ext=0.75, m_defects=0,
                defect_inject_epoch=50, r_core=0.30, snapshot_final=True,
                spike_epoch=None, spike_ops=0,
                pulse_size=0, pulse_every=0, pulse_start=55, n_pulses=0):
    rng = np.random.default_rng(seed)
    faces, face_types, face_depth, face_defect = {}, {}, {}, {}
    edge_to_faces = defaultdict(set); active = set(); ndeg = Counter()
    nf = [0]; nn = [6]; stats = Counter(); epoch_log = []; snaps = {}
    anchor_face = anchor_nodes = anchor_center_node = None
    backlog = 0; k_stitch = 0; rot = [0]

    def add_face(nodes, ftype, depth, defect=False):
        fid = nf[0]; nf[0] += 1
        nodes = frozenset(int(x) for x in nodes)
        faces[fid] = nodes; face_types[fid] = str(ftype)
        face_depth[fid] = int(depth); face_defect[fid] = bool(defect)
        for e in itertools.combinations(sorted(nodes), 2):
            edge_to_faces[frozenset(e)].add(fid)
        active.add(fid)
        for n in nodes: ndeg[n] += 1
        return fid

    def remove_face(fid):
        for n in faces[fid]: ndeg[n] -= 1
        for e in itertools.combinations(sorted(faces[fid]), 2):
            key = frozenset(e); edge_to_faces[key].discard(fid)
            if not edge_to_faces[key]: del edge_to_faces[key]
        active.discard(fid)
        del faces[fid], face_types[fid], face_depth[fid], face_defect[fid]

    def snapshot_raw():
        a0 = set(active)
        n0 = _cs_adj_from_state(faces, edge_to_faces, a0)
        return a0, dict(face_types), dict(face_depth), dict(faces), n0, dict(face_defect)

    def record_snapshot(ep):
        a0, t0, d0, f0, n0, df0 = snapshot_raw(); sd = dict(stats)
        if anchor_center_node is not None: sd["defect_center_node"] = int(anchor_center_node)
        if anchor_nodes is not None:
            sd["defect_anchor_nodes"] = tuple(int(x) for x in anchor_nodes)
            sd["defect_anchor_nodes_repr"] = repr(tuple(int(x) for x in anchor_nodes))
        snaps[int(ep)] = CoherentStitchSnapshot(epoch=int(ep), active_faces=a0,
            face_nodes=f0, face_types=t0, face_depth=d0, face_neighbors=n0,
            face_defect=df0, stats=sd)

    def is_frustrated(fid, t0, n0):
        if t0[fid] != "S": return False
        nts = {t0[n] for n in n0[fid]}
        return ("G" in nts) and ("I" not in nts)

    def split_face(fid, *, forced=False, fdc=None):
        if fid not in active: return None
        old = sorted(faces[fid]); od = int(face_depth[fid])
        cd = bool(face_defect.get(fid, False)) if fdc is None else bool(fdc)
        a, b, c = old; new = nn[0]; nn[0] += 1
        remove_face(fid)
        _tp = [str(t) for t in rng.permutation(["S", "I", "G"])]
        for nd, ft in zip([(new, a, b), (new, a, c), (new, b, c)], _tp):
            add_face(nd, ft, od + 1, cd)
        stats["basin_splits"] += 1
        if forced: stats["forced_defect_splits"] += 1
        return new

    def try_flip(e):
        fs = edge_to_faces.get(e)
        if not fs or len(fs) != 2: return False
        f1, f2 = tuple(sorted(fs))
        if face_depth[f1] != face_depth[f2]: return False
        a, b = tuple(sorted(e))
        cset = faces[f1] - e; dset = faces[f2] - e
        if len(cset) != 1 or len(dset) != 1: return False
        c = next(iter(cset)); d = next(iter(dset))
        if c == d or frozenset((c, d)) in edge_to_faces: return False
        sq = lambda x: (x - 6) ** 2
        dC = (sq(ndeg[a]-1) + sq(ndeg[b]-1) + sq(ndeg[c]+1) + sq(ndeg[d]+1)
              - sq(ndeg[a]) - sq(ndeg[b]) - sq(ndeg[c]) - sq(ndeg[d]))
        if dC >= 0: return False
        d1, t1, df1 = face_depth[f1], face_types[f1], face_defect[f1]
        d2, t2, df2 = face_depth[f2], face_types[f2], face_defect[f2]
        remove_face(f1); remove_face(f2)
        add_face((a, c, d), t1, d1, df1); add_face((b, c, d), t2, d2, df2)
        return True

    def core_partition():
        # weighted face-ball around anchor faces, cutoff r_core
        if anchor_center_node is None: return set(), 0
        lengths = {f: (3.0 ** -0.5) ** face_depth[f] for f in active}
        src = [f for f in active if anchor_center_node in faces[f]]
        if not src:
            lm = set(anchor_nodes or [])
            src = [f for f in active if faces[f] & lm]
        if not src: return set(), 0
        dist = {s: 0.5 * lengths[s] for s in src}
        heap = [(d, s) for s, d in dist.items()]; heapq.heapify(heap)
        while heap:
            du, u = heapq.heappop(heap)
            if du != dist.get(u) or du > r_core: continue
            for e in itertools.combinations(sorted(faces[u]), 2):
                for w in edge_to_faces.get(frozenset(e), ()):
                    if w == u: continue
                    nd = du + 0.5 * (lengths[u] + lengths[w])
                    if nd <= r_core and nd < dist.get(w, 1e18):
                        dist[w] = nd; heapq.heappush(heap, (nd, w))
        core = set(dist)
        gamma = 0
        for e, fs in edge_to_faces.items():
            fl = [f for f in fs]
            if len(fl) == 2 and ((fl[0] in core) != (fl[1] in core)): gamma += 1
        return core, gamma

    add_face((0,1,2),"S",0); add_face((0,1,3),"G",0)
    add_face((2,4,5),"I",0); add_face((3,4,5),"S",0)

    for epoch in range(1, final_epoch + 1):
        if anchor_center_node is None and epoch >= defect_inject_epoch:
            adj = _cs_adj_from_state(faces, edge_to_faces, active)
            center, _, _ = _cs_raw_bulk_center(adj)
            anchor_nodes = tuple(sorted(int(x) for x in faces[center]))
            anchor_center_node = split_face(center, fdc=True)

        a0, t0, d0, f0, n0, df0 = snapshot_raw()
        core, gamma = core_partition()
        served_f = served_v = deferred_f = 0; core_flips = 0; wedge_info = None

        # ---- CORE: native competition for boundary-counted capacity --------
        cap = gamma
        if core:
            tagged = sorted([f for f in a0 if df0.get(f, False) and f in core],
                            key=lambda f: (d0[f], repr(f)), reverse=True)
            if pulse_size>0:
                _pi=(epoch-pulse_start)
                _deliver = pulse_size if (_pi>=0 and _pi%max(1,pulse_every)==0
                                          and _pi//max(1,pulse_every)<n_pulses) else 0
            else:
                _deliver = (spike_ops if (spike_epoch is not None and epoch==spike_epoch) else
                            (0 if spike_epoch is not None else m_defects))
            n_forced_req = (_deliver if anchor_center_node is not None else 0) + backlog
            frus = [f for f in a0 if f in core and is_frustrated(f, t0, n0)]
            reqs = [("F", None)] * n_forced_req + [("V", f) for f in frus]
            rng.shuffle(reqs)
            ti = 0
            for kind, fid in reqs:
                if cap <= 0: 
                    if kind == "F": deferred_f += 1
                    continue
                if kind == "F":
                    # serve one forced op on deepest surviving tagged face
                    while ti < len(tagged) and tagged[ti] not in active: ti += 1
                    if ti >= len(tagged):
                        deferred_f += 1; continue
                    if split_face(tagged[ti], forced=True, fdc=True) is not None:
                        served_f += 1; cap -= 1
                else:
                    if fid in active and split_face(fid) is not None:
                        served_v += 1; cap -= 1
            backlog = deferred_f
            # charged core flips with leftover capacity
            if cap > 0:
                core_nodes = set().union(*[faces[f] for f in core if f in faces]) if core else set()
                edges = [e for e, fs in edge_to_faces.items()
                         if len(fs) == 2 and all(f in core for f in fs)]
                rng.shuffle(edges)
                for e in edges:
                    if cap <= 0: break
                    if try_flip(e): core_flips += 1; cap -= 1
            # ---- native relief valve ----------------------------------------
            if backlog >= gamma and gamma > 0:
                _L=lambda dp:(3.0**-0.5)**dp
                _n2f=defaultdict(set)
                for _f,_nd in faces.items():
                    for _n in _nd: _n2f[_n].add(_f)
                _srcf=[f for f in faces if anchor_center_node in faces[f]]
                _dist={s0:0.5*_L(face_depth[s0]) for s0 in _srcf}
                _hp=[(d,s0) for s0,d in _dist.items()]; heapq.heapify(_hp)
                while _hp:
                    _du,_u=heapq.heappop(_hp)
                    if _du!=_dist.get(_u) or _du>2.0: continue
                    for _e0 in itertools.combinations(sorted(faces[_u]),2):
                        for _w in edge_to_faces.get(frozenset(_e0),()):
                            if _w==_u: continue
                            _nd2=_du+0.5*(_L(face_depth[_u])+_L(face_depth[_w]))
                            if _nd2<2.0 and _nd2<_dist.get(_w,1e18):
                                _dist[_w]=_nd2; heapq.heappush(_hp,(_nd2,_w))
                _tag=[f for f in faces if face_defect.get(f,False)]
                _tag=list(_tag)
                _tv=[_dist[f] for f in _tag if f in _dist]
                _nt=0; _coll=0
                if len(_tag)>=6 and len(_tv)>=6:
                    _pr=float(np.percentile(_tv,90)); _quota=max(1,len(_tag)//6)
                    _dead=set(); _guard=0
                    def _mkc():
                        _out=[]
                        for _f in [x for x in _tag if x in faces and _dist.get(x,9e9)<=_pr]:
                            for _e0 in itertools.combinations(sorted(faces[_f]),2):
                                _fe=frozenset(_e0)
                                if _fe in _dead or anchor_center_node in _fe: continue
                                _fs0=edge_to_faces.get(_fe,())
                                if len(_fs0)!=2: continue
                                _g1,_g2=tuple(_fs0)
                                if not(face_defect.get(_g1,False) and face_defect.get(_g2,False)): continue
                                _e1,_e2=_dist.get(_g1),_dist.get(_g2)
                                if _e1 is None or _e2 is None or _e1>_pr or _e2>_pr: continue
                                _ml0=0.5*(_L(face_depth[_g1])+_L(face_depth[_g2]))
                                if abs(_e1-_e2)<0.45*_ml0: continue
                                _out.append(_fe)
                        return _out
                    _cands=_mkc(); _ci=0
                    while _nt<_quota and _guard<300:
                        _guard+=1
                        _best=None
                        while _ci<len(_cands):
                            _fe=_cands[_ci]; _ci+=1
                            if _fe in _dead or len(edge_to_faces.get(_fe,()))!=2: continue
                            _best=_fe; break
                        if _best is None:
                            _cands=_mkc(); _ci=0
                            if not _cands: break
                            continue
                        _a,_b=sorted(_best); _fs=edge_to_faces.get(_best)
                        if not _fs or len(_fs)!=2: _dead.add(_best); continue
                        _f1,_f2=sorted(_fs)
                        _c=next(iter(faces[_f1]-_best)); _d4=next(iter(faces[_f2]-_best))
                        _na={_n for _f in _n2f[_a] for _n in faces[_f]}-{_a}
                        _nb={_n for _f in _n2f[_b] for _n in faces[_f]}-{_b}
                        if (_na&_nb)!={_c,_d4}: _dead.add(_best); continue
                        _nt+=sum(1 for _f in (_f1,_f2) if face_defect.get(_f,False))
                        for _f in (_f1,_f2):
                            for _n in faces[_f]: _n2f[_n].discard(_f)
                            remove_face(_f)
                        for _f in list(_n2f[_b]):
                            _nnd=frozenset(_a if _n==_b else _n for _n in faces[_f])
                            _tp,_dp,_df=face_types[_f],face_depth[_f],face_defect[_f]
                            _od=_dist.get(_f)
                            for _n in faces[_f]: _n2f[_n].discard(_f)
                            remove_face(_f)
                            if len(_nnd)==3:
                                _g=add_face(_nnd,_tp,_dp,_df)
                                for _n in _nnd: _n2f[_n].add(_g)
                                if _od is not None: _dist[_g]=_od
                        del _n2f[_b]
                        _coll+=1
                if _nt>0:
                    k_stitch+=1
                    wedge_info=dict(n_removed=2*_coll,n_tagged=_nt)
                    backlog=max(0,backlog-_nt)
                    stats["purge_collapses"]+=_coll

        # ---- EXTERIOR: global sub-extensive rule ----------------------------
        a0, t0, d0, f0, n0, df0 = snapshot_raw()
        ebud = max(0, int(round(len(active) ** p_ext)))
        frus_e = [f for f in a0 if f not in core and is_frustrated(f, t0, n0)]
        norm_e = 0; ticks = 0; ext_flips = 0
        if frus_e and ebud > 0:
            rng.shuffle(frus_e)
            for fid in frus_e[:ebud]:
                if fid in active and split_face(fid) is not None:
                    norm_e += 1; ebud -= 1
        else:
            sc, ad, gf, sf = [], [], [], []
            for fid in a0:
                if fid not in active: continue
                nts = {t0[n] for n in n0[fid]}
                if t0[fid] == "I" and "S" in nts and "G" in nts: sc.append(fid)
                if t0[fid] == "I" and "S" in nts: ad.append(fid)
                if t0[fid] == "G": gf.append(fid)
                if t0[fid] == "S": sf.append(fid)
            cand = sc or ad or gf or sf or list(a0)
            rng.shuffle(cand)
            for fid in cand[:int(ebud)]:
                if fid not in active: continue
                old = face_types[fid]
                face_types[fid] = {"I": "S", "G": "I"}.get(old, "G")
                ticks += 1
        if ebud > 0:
            edges = [e for e, fs in edge_to_faces.items()
                     if len(fs) == 2 and any(f not in core for f in fs)]
            rng.shuffle(edges)
            for e in edges[:min(len(edges), 4000)]:
                if ebud <= 0: break
                if try_flip(e): ext_flips += 1; ebud -= 1

        epoch_log.append(dict(epoch=epoch, gamma=gamma, core_faces=len(core),
            served_forced=served_f, served_vac=served_v, backlog=backlog,
            k=k_stitch, core_flips=core_flips, ext_flips=ext_flips,
            wedge_removed=(wedge_info or {}).get("n_removed", 0),
            wedge_tagged=(wedge_info or {}).get("n_tagged", 0),
            tag_pop=int(sum(1 for _v in face_defect.values() if _v)),
            active_faces=len(active), ticks=ticks))
    if snapshot_final: record_snapshot(final_epoch)
    return CoherentStitchRun(stats=dict(stats, k_stitch=k_stitch),
                             spatial_snapshots=dict(snaps),
                             epoch_log=pd.DataFrame(epoch_log))

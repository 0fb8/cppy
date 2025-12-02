from heapq import heappush as hpush, heappop as hpop
from math import inf


def dijkstra(G, sv):
    N = len(G)
    if not (0 <= sv < N):
        raise ValueError
    dist = [inf] * N
    hq = []
    par = [None] * N
    dist[sv] = 0
    hpush(hq, (0, sv))
    while hq:
        d, v = hpop(hq)
        if d > dist[v]:
            continue
        for nv, w in G[v]:
            if w < 0:
                raise ValueError("Negative weight not allowed in Dijkstra")
            nd = d + w
            if not (nd < dist[nv]):
                continue
            dist[nv] = nd
            hpush(hq, (nd, nv))
            par[nv] = v
    return dist, par


def restore_path(par: list[int], tv: int):
    ans = []
    cur = tv
    while cur is not None:
        ans.append(cur)
        cur = par[cur]
    return ans[::-1]

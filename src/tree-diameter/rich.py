def farthest(G: list[list[tuple[int, int]]], sv: int) -> tuple[int, int, list[int]]:
    """
    木 G について, 頂点 sv から最も遠い頂点（とそこまでの距離）をどれか 1 組返す.

    Parameters
    ----------
    G : list[list[tuple[int, int]]]
        木
    sv : int
        始点

    Returns
    -------
    tuple[int, int, list]
        (最遠距離, 最遠頂点, 経路リスト)
    """

    N = len(G)
    if not (0 <= sv < N):
        raise ValueError(f"sv must be in [0,{N}), got {sv}")

    mx_dist = 0
    farthest_v = sv

    dist = [None] * N
    par = [None] * N
    dist[sv] = 0
    stk = [sv]

    while stk:
        v = stk.pop()
        d = dist[v]
        if d > mx_dist:
            mx_dist, farthest_v = d, v
        for nv, w in G[v]:
            if dist[nv] is None:
                dist[nv] = d + w
                par[nv] = v
                stk.append(nv)

    return mx_dist, farthest_v, par


def tree_diameter(G: list[list[tuple[int, int]]]) -> tuple[int, list[int]]:
    """
    木の直径

    Parameters
    ----------
    G : list[list[tuple[int, int]]]
        木

    Returns
    -------
    tuple[int, list[int]]
        (直径の長さ, 直径パス)
    """
    if len(G) == 0:
        return None, []

    _, a, _ = farthest(G, 0)
    d, b, par = farthest(G, a)

    path = []
    cur = b
    while cur is not None:
        path.append(cur)
        cur = par[cur]

    return d, path


if __name__ == "__main__":
    N = int(input())
    G = [[] for _ in range(N)]
    for _ in range(N - 1):
        u, v = map(lambda x: int(x) - 1, input().split())
        G[u].append((v, 1))
        G[v].append((u, 1))

    d, _ = tree_diameter(G)

    ans = d + 1
    print(ans)

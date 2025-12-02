def farthest(G, sv):
    N = len(G)
    if not (0 <= sv < N):
        raise ValueError

    ans_d = 0
    ans_v = sv

    dist = [-1] * N
    dist[sv] = 0
    stk = [sv]

    while stk:
        v = stk.pop()
        d = dist[v]
        if d > ans_d:
            ans_d, ans_v = d, v
        for nv in G[v]:
            if dist[nv] == -1:
                dist[nv] = d + 1
                stk.append(nv)

    return ans_d, ans_v


def tree_diameter(G):
    _, a = farthest(G, 0)
    d, _ = farthest(G, a)
    return d


if __name__ == "__main__":
    N = int(input())
    G = [[] for _ in range(N)]
    for _ in range(N - 1):
        u, v = map(lambda x: int(x) - 1, input().split())
        G[u].append(v)
        G[v].append(u)

    d = tree_diameter(G)
    ans = d + 1
    print(ans)

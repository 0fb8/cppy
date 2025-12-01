def main():

    H, W = map(int, input().split())
    sh, sw = map(int1, input().split())
    gh, gw = map(int1, input().split())
    G = [input() for _ in range(H)]

    dist = [[[inf] * 2 for _ in range(W)] for _ in range(H)]
    dq = deque()

    for t in range(2):
        dist[sh][sw][t] = 0
        dq.append((0, sh, sw, t))

    while dq:
        d, h, w, t = dq.popleft()
        if d > dist[h][w][t]:
            continue

        nd = d
        for dh, dw in DIR[t::2]:
            nh, nw = h + dh, w + dw
            if not (0 <= nh < H and 0 <= nw < W):
                continue
            if G[nh][nw] == "#":
                continue
            if nd >= dist[nh][nw][t]:
                continue
            dist[nh][nw][t] = nd
            dq.appendleft((nd, nh, nw, t))

        nd = d + 1
        nt = t ^ 1
        if nd >= dist[h][w][nt]:
            continue
        dist[h][w][nt] = nd
        dq.append((nd, h, w, nt))

    ans = min(dist[gh][gw])
    print(ans)

    return


from collections import deque
from math import inf

DIR = ((1, 0), (0, 1), (-1, 0), (0, -1))


def int1(x):
    return int(x) - 1

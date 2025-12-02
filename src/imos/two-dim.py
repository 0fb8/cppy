H, W, N = map(int, input().split())
G = [[0] * (W + 1) for _ in range(H + 1)]

for _ in range(N):
    lh, lw, rh, rw = map(lambda x: int(x) - 1, input().split())
    rh, rw = rh + 1, rw + 1

    G[lh][lw] += 1
    G[lh][rw] -= 1
    G[rh][lw] -= 1
    G[rh][rw] += 1

for h in range(H):
    for w in range(W):
        G[h][w + 1] += G[h][w]

for h in range(H):
    for w in range(W):
        G[h + 1][w] += G[h][w]


ans = G
for h in range(H):
    print(*ans[h][:W])

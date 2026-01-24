from functools import cmp_to_key, reduce
from itertools import accumulate, groupby
from math import gcd


def argcmp(r0, r1):
    (x0, y0), (x1, y1) = r0, r1
    h0, h1 = (y0, x0) < (0, 0), (y1, x1) < (0, 0)
    if h0 != h1:
        return 1 if h0 else -1
    return x1 * y0 - y1 * x0


def normalize_direction(xs):
    g = reduce(gcd, xs)
    return tuple(x // g for x in xs)


def abc442e():
    N, Q = map(int, input().split())
    A = [(tuple(map(int, input().split())), i) for i in range(N)]
    A.sort(key=cmp_to_key(lambda x, y: argcmp(x[0], y[0])))

    B = []
    pos = [0] * N
    for _, g in groupby(A, key=lambda x: normalize_direction(x[0])):
        g = list(g)
        for _, t in g:
            pos[t] = len(B)
        B.append(len(g))

    pB = list(accumulate(B, initial=0))

    for _ in range(Q):
        t, s = map(lambda x: int(x) - 1, input().split())
        s, t = pos[s], pos[t]

        if s == t:
            ans = B[s]
        elif s < t:
            ans = pB[t + 1] - pB[s]
        else:
            x = pB[s] - pB[t + 1]
            ans = N - x
        print(ans)

    return


if __name__ == "__main__":
    abc442e()

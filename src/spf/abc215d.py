def build_spf(n: int) -> list[int]:
    """spf[x] := smallest prime factor of positive integer x"""
    spf = list(range(n + 1))
    spf[0] = 0
    if n >= 1:
        spf[1] = 1
    p = 2
    while p * p <= n:
        if spf[p] == p:
            for i in range(p * p, n + 1, p):
                if spf[i] == i:
                    spf[i] = p
        p += 1
    return spf


def factorize(x: int, spf):
    s = set()
    i = x
    while i > 1:
        p = spf[i]
        s.add(p)
        while i % p == 0:
            i //= p
    return s


if __name__ == "__main__":

    def main():
        N, M = map(int, input().split())
        A = list(map(int, input().split()))

        V = max(M, max(A))
        spf = build_spf(V)

        bad_primes = set()
        for a in A:
            bad_primes |= factorize(a, spf)

        ok = [True] * (M + 1)

        for p in bad_primes:
            for i in range(p, M + 1, p):
                ok[i] = False

        ans = [i for i in range(1, M + 1) if ok[i]]
        print(len(ans))
        print("\n".join(map(str, ans)))

    main()

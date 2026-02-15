from collections import Counter


def prime_factorization(n):
    res = Counter()
    if n & 1 == 0:
        e = 0
        while n & 1 == 0:
            e += 1
            n >>= 1
        res[2] = e
    p = 3
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                e += 1
                n //= p
            res[p] = e
        p += 2
    if n > 1:
        res[n] = 1
    return res


if __name__ == "__main__":

    def abc169d():
        N = int(input())

        pf = prime_factorization(N)

        def f(e):
            ok, ng = 0, e + 1
            while abs(ng - ok) > 1:
                mid = (ok + ng) >> 1
                (ok := mid) if mid * (mid + 1) // 2 <= e else (ng := mid)
            return ok

        ans = sum(f(e) for e in pf.values())
        print(ans)
        return

    abc169d()

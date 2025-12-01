from typing import Iterator

import sympy


def divisors(n: int) -> Iterator[int]:
    fi = sympy.factorint(n)

    primes = list(fi.keys())
    exps = list(fi.values())
    ln = len(fi)

    def dfs(divisor, i):
        if i == ln:
            yield divisor
            return
        t = 1
        p = primes[i]
        for e in range(exps[i] + 1):
            yield from dfs(divisor * t, i + 1)
            t *= p

    return dfs(1, 0)


if __name__ == "__main__":
    N = int(input())
    for d in divisors(N):
        print(d)

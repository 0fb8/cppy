from itertools import product

import sympy


def divisors(n: int) -> list[int]:
    fi = sympy.factorint(n)

    pxxe_dict = dict()
    for prime, exp in fi.items():
        t = 1
        pxxe_dict[prime] = [t := t * prime for e in range(1, exp + 1)]

    ans = [1]
    for p, pxxe in pxxe_dict.items():
        ans.extend([a * pe for a, pe in product(ans, pxxe)])
    return ans


if __name__ == "__main__":
    N = int(input())
    ans = divisors(N)
    print("\n".join(map(str, ans)))

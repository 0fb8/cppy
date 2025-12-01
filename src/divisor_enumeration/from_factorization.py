import itertools as it
import operator
from functools import reduce
from typing import Iterator

import sympy


def divisors(n: int) -> Iterator[int]:
    fi = sympy.factorint(n)
    ps = fi.keys()
    for es in it.product(*(range(v + 1) for v in fi.values())):
        divisor = reduce(operator.mul, (p**e for p, e in zip(ps, es)), 1)
        yield divisor


def main():
    N = int(input())
    for d in divisors(N):
        print(d)


if __name__ == "__main__":
    main()

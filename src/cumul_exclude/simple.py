from typing import Iterable, Callable, TypeVar, Generic, List, Optional
from itertools import accumulate

T = TypeVar("T")


class CumulExclude(Generic[T]):
    def __init__(
        self, data: Iterable[T], op: Callable[[T, T], T], e: Optional[T] = None
    ):
        data = list(data)
        self.n = len(data)
        self.op = op
        self.e = e

        if self.n == 0:
            self.pref = []
            self.suff = []
            return

        self.pref = list(accumulate(data, op))
        self.suff = list(accumulate(data[::-1], lambda x, y: op(y, x)))[::-1]

    def exclude(self, idx: int) -> T:
        if not (0 <= idx < self.n):
            raise IndexError(f"Index {idx} out of range")

        if self.n == 1:
            if self.e is None:
                raise ValueError("Identity element is required for n=1")
            return self.e

        if idx == 0:
            return self.suff[1]
        if idx == self.n - 1:
            return self.pref[-2]

        return self.op(self.pref[idx - 1], self.suff[idx + 1])

    def __getitem__(self, idx: int) -> T:
        if idx < 0:
            idx += self.n
        return self.exclude(idx)

    def __len__(self) -> int:
        return self.n

    def __repr__(self) -> str:
        res = [self.exclude(i) for i in range(self.n)]
        return f"{self.__class__.__name__}({res})"


if __name__ == "__main__":
    from math import gcd

    def abc125c():
        N = int(input())
        A = list(map(int, input().split()))
        gcdAex = CumulExclude(A, gcd, 0)
        ans = max((gcdAex[i] for i in range(N)))
        print(ans)

    abc125c()

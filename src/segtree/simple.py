"""segtree/simple.py"""

from typing import *

T = TypeVar("T")


class SegmentTree(Generic[T]):

    __slots__ = "op", "e", "is_abel", "n", "_data"

    def __init__(self, arr: Sequence[T], op: Callable[[T, T], T], e: T, is_abel=False):
        self.op = op
        self.e = e
        self.is_abel = is_abel
        self.n = len(arr)
        if self.n == 0:
            raise ValueError("SegTree cannot be built from empty array.")
        self._data = [self.e] * (self.n << 1)

        self._data[self.n : self.n << 1] = arr
        for i in range(self.n - 1, 0, -1):
            self._data[i] = op(self._data[i << 1 | 0], self._data[i << 1 | 1])

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self._data[self.n:])})"

    def __len__(self):
        return self.n

    def __setitem__(self, idx: int, val: T) -> None:
        if idx < 0:
            idx += self.n
        if not 0 <= idx < self.n:
            raise IndexError
        i = self.n + idx
        self._data[i] = val
        while i > 1:
            i >>= 1
            self._data[i] = self.op(self._data[i << 1 | 0], self._data[i << 1 | 1])

    def __getitem__(self, item: int | slice) -> T:
        if isinstance(item, int):
            idx = item
            if idx < 0:
                idx += self.n
            if not 0 <= idx < self.n:
                raise IndexError
            return self._data[self.n + idx]
        elif isinstance(item, slice):
            start, stop, step = item.indices(self.n)
            if step != 1:
                raise ValueError("Slice step must be 1")
            if start >= stop:
                return self.e
            l, r = start + self.n, stop + self.n
            res_left, res_right = self.e, self.e
            while l < r:
                if l & 1:
                    res_left = self.op(res_left, self._data[l])
                    l += 1
                if r & 1:
                    r -= 1
                    res_right = self.op(self._data[r], res_right)
                l >>= 1
                r >>= 1
            return self.op(res_left, res_right)
        else:
            raise TypeError(f"Invalid argument type: {type(item)}")

    def all_prod(self):
        if not self.is_abel:
            raise ValueError("all_prod is only available for commutative operations.")
        return self._data[1]

    def max_right(self, l: int, is_ok: Callable[[T], bool]) -> int:
        """
        Returns the maximum r for which is_ok( seg[l:r) ) is True.
        - Assumes is_ok( seg[l,i) ) is False ⇒ ∀j >= i, is_ok( seg[l,j) ) is False
        - f(e) must be True.
        """
        if not 0 <= l <= self.n:
            raise IndexError(f"max_right index out of range: {l}")
        if not is_ok(self.e):
            raise ValueError("f(e) == False")
        if l == self.n:
            return self.n

        l += self.n
        r = self.n << 1
        indices_left = []
        indices_right = []
        while l < r:
            if l & 1:
                indices_left.append(l)
                l += 1
            if r & 1:
                r -= 1
                indices_right.append(r)
            l >>= 1
            r >>= 1
        indices = indices_left + indices_right[::-1]

        sm = self.e
        for i in indices:
            nxt = self.op(sm, self._data[i])
            if is_ok(nxt):
                sm = nxt
            else:
                while i < self.n:
                    i <<= 1
                    nxt = self.op(sm, self._data[i])
                    if is_ok(nxt):
                        sm = nxt
                        i |= 1
                return i - self.n
        return self.n

    def min_left(self, r: int, is_ok: Callable[[T], bool]) -> int:
        """
        Returns the minimum l for which is_ok( seg[l:r) ) is True.
        """
        if not 0 <= r <= self.n:
            raise IndexError(f"min_left index out of range: {r}")
        if not is_ok(self.e):
            raise ValueError("f(e) == False")
        if r == 0:
            return 0

        l = self.n
        r += self.n
        indices_left = []
        indices_right = []
        while l < r:
            if l & 1:
                indices_left.append(l)
                l += 1
            if r & 1:
                r -= 1
                indices_right.append(r)
            l >>= 1
            r >>= 1
        indices = indices_right + indices_left[::-1]
        sm = self.e
        for i in indices:
            nxt = self.op(self._data[i], sm)
            if is_ok(nxt):
                sm = nxt
            else:
                while i < self.n:
                    i = i << 1 | 1
                    nxt = self.op(self._data[i], sm)
                    if is_ok(nxt):
                        sm = nxt
                        i ^= 1
                return i + 1 - self.n
        return 0


if __name__ == "__main__":
    from functools import partial
    from sys import stderr

    n, q = map(int, input().split())
    A = list(map(int, input().split()))

    seg = SegmentTree(A, max, -1)

    def f(v, a):
        return v > a

    for _ in range(q):
        # print(seg, file=stderr)
        t, *data = map(int, input().split())

        if t == 1:
            x, v = data
            x -= 1
            seg[x] = v
        elif t == 2:
            l, r = map(lambda x: x - 1, data)
            r += 1
            ans = seg[l:r]
            print(ans)
        elif t == 3:
            x, v = data
            x -= 1
            ans = seg.max_right(x, partial(f, v))
            print(ans + 1)

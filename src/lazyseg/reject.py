from typing import *

S = TypeVar("S")
F = TypeVar("F")

# this is slow probably because it's recursive


class LazySegTree(Generic[S, F]):
    def __init__(
        self,
        arr: Iterable[S],
        op: Callable[[S, S], S],
        e: S,
        mapping: Callable[[F, S], S],
        composition: Callable[[F, F], F],
        id: F,
    ):
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id

        self.n = 1
        while self.n < len(arr):
            self.n <<= 1

        self.data = [e] * (self.n << 1)
        self.lazy = [id] * (self.n << 1)

        for i, a in enumerate(arr):
            i += self.n
            self.data[i] = a
        for i in reversed(range(self.n)):
            self.data[i] = self.op(self.data[i << 1], self.data[i << 1 | 1])

    def _apply(self, idx, l, r, f: F):
        self.data[idx] = self.mapping(f, self.data[idx])
        self.lazy[idx] = self.composition(f, self.lazy[idx])

    def _propagate(self, idx, l, r):
        if self.lazy[idx] == id:
            return
        if idx >= self.n:
            return
        lc_idx, rc_idx = idx << 1, idx << 1 | 1
        mid = (l + r) >> 1
        self._apply(lc_idx, l, mid, self.lazy[idx])
        self._apply(rc_idx, mid, r, self.lazy[idx])
        self.lazy[idx] = id

    def range_add(self, ql, qr, f: F):
        # [ql, qr)
        if not (0 <= ql <= qr <= self.n):
            raise IndexError
        self._range_add(1, 0, self.n, ql, qr, f)

    def _range_add(self, idx, l, r, ql, qr, f):
        if qr <= l or r <= ql:
            return
        if ql <= l <= r <= qr:
            self._apply(idx, l, r, f)
        self._propagate(idx, l, r)
        if idx < self.n:
            lc_idx, rc_idx = idx << 1, idx << 1 | 1
            mid = (l + r) >> 1
            self._range_add(lc_idx, l, mid, ql, qr, f)
            self._range_add(rc_idx, mid, r, ql, qr, f)
            self.data[idx] = self.op(self.data[lc_idx], self.data[rc_idx])

    def range_sum(self, ql, qr):
        # [ql, qr)
        if not (0 <= ql <= qr <= self.n):
            raise IndexError
        return self._range_sum(1, 0, self.n, ql, qr)

    def _range_sum(self, idx, l, r, ql, qr):
        if qr <= l or r <= ql:
            return self.e
        if ql <= l <= r <= qr:
            return self.data[idx]
        if idx > self.n:
            return self.data[idx]
        self._propagate(idx, l, r)
        lc_idx, rc_idx = idx << 1, idx << 1 | 1
        mid = (l + r) >> 1
        lc_val = self._range_sum(lc_idx, l, mid, ql, qr)
        rc_val = self._range_sum(rc_idx, mid, r, ql, qr)
        return self.op(lc_val, rc_val)


if __name__ == "__main__":
    import sys
    from math import inf

    sys.setrecursionlimit(10**7)

    op = max
    e = -inf

    def mapping(f, x):
        return f if f is not None else x

    def composite(f, g):
        return f if f is not None else g

    id = None

    n, q = map(int, input().split())

    seg = LazySegTree([0] * n, op, e, mapping, composite, id)

    for _ in range(q):
        l, r = map(lambda x: int(x) - 1, input().split())
        r += 1

        cur = seg.range_sum(l, r)
        nxt = cur + 1
        seg.range_add(l, r, nxt)
        print(nxt)

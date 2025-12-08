from typing import Generic, TypeVar, Callable, Sequence, Union


M = TypeVar("M")
X = TypeVar("X")


class LazySegTree(Generic[M, X]):
    def __init__(
        self,
        arr: Sequence[X],
        op_x: Callable[[X, X], X],
        e_x: X,
        op_m: Callable[[M, M], M],
        e_m: M,
        action: Callable[[M, X], X],
    ):
        """
        Lazy Segment Tree

        :param arr: Initial array
        :param op_x: Operation for data (e.g., max, +, min)
        :param e_x: Identity element for op_x
        :param op_m: Operation for lazy tags (composition g. f)
        :param e_m: Identity element for op_m
        :param action: Action of lazy tag on data
        """

        self.n = len(arr)
        self.op_x = op_x
        self.e_x = e_x
        self.op_m = op_m
        self.e_m = e_m
        self.action = action

        self._log = (self.n - 1).bit_length()
        self.size = 1 << self._log

        self._dat = [self.e_x] * (self.size << 1)
        self._laz = [self.e_m] * (self.size << 1)

        for i in range(self.n):
            self._dat[self.size + i] = arr[i]

        for k in range(self.size - 1, 0, -1):
            self._update(k)

    def _all_apply(self, k: int, f: M):
        self._dat[k] = self.action(f, self._dat[k])
        if k < self.size:
            self._laz[k] = self.op_m(f, self._laz[k])

    def _push(self, k: int):
        if self._laz[k] == self.e_m:
            return
        self._all_apply(k << 1 | 0, self._laz[k])
        self._all_apply(k << 1 | 1, self._laz[k])
        self._laz[k] = self.e_m

    def _push_ancestors(self, k: int) -> None:
        for h in range(self._log, 0, -1):
            self._push(k >> h)

    def _push_range_ancestors(self, kl: int, kr: int) -> None:
        for h in range(self._log, 0, -1):
            if ((kl >> h) << h) != kl:
                self._push(kl >> h)
            if ((kr >> h) << h) != kr:
                self._push((kr - 1) >> h)

    def _update(self, k: int):
        self._dat[k] = self.op_x(self._dat[k << 1 | 0], self._dat[k << 1 | 1])

    def _update_ancestors(self, k: int) -> None:
        while k > 1:
            k >>= 1
            self._update(k)

    def _update_range_ancestors(self, kl: int, kr: int) -> None:
        for i in range(1, self._log + 1):
            if ((kl >> i) << i) != kl:
                self._update(kl >> i)
            if ((kr >> i) << i) != kr:
                self._update((kr - 1) >> i)

    def set(self, i: int, x: X):
        """seg[i] = x"""
        if not 0 <= i < self.n:
            raise IndexError(f"Index {i} out of range")
        k = i + self.size
        self._push_ancestors(k)
        self._dat[k] = x
        self._laz[k] = self.e_m
        self._update_ancestors(k)

    def get(self, i: int) -> X:
        """Return seg[i]"""
        if not 0 <= i < self.n:
            raise IndexError(f"Index {i} out of range")
        k = i + self.size
        self._push_ancestors(k)
        return self._dat[k]

    def prod(self, l: int, r: int) -> X:
        """Return op_x(a[l], ..., a[r-1])"""
        if not 0 <= l <= r <= self.n:
            raise IndexError(f"Invalid range [{l}, {r})")
        if l == r:
            return self.e_x

        kl = l + self.size
        kr = r + self.size

        self._push_range_ancestors(kl, kr)

        sml, smr = self.e_x, self.e_x
        il, ir = kl, kr
        while il < ir:
            if il & 1:
                sml = self.op_x(sml, self._dat[il])
                il += 1
            if ir & 1:
                ir -= 1
                smr = self.op_x(self._dat[ir], smr)
            il >>= 1
            ir >>= 1

        return self.op_x(sml, smr)

    def all_prod(self) -> X:
        return self._dat[1]

    def apply(self, i: int, f: M):
        """seg[i] = action(f, seg[i])"""
        if not 0 <= i < self.n:
            raise IndexError(f"Index {i} out of range")
        k = i + self.size
        self._push_ancestors(k)
        self._dat[k] = self.action(f, self._dat[k])
        self._update_ancestors(k)

    def apply_range(self, l: int, r: int, f: M):
        """a[i] = action(f, a[i]) for i in [l, r)"""
        if not 0 <= l <= r <= self.n:
            raise IndexError(f"Invalid range [{l}, {r})")
        if l == r:
            return

        kl = l + self.size
        kr = r + self.size

        self._push_range_ancestors(kl, kr)

        il, ir = kl, kr
        while il < ir:
            if il & 1:
                self._all_apply(il, f)
                il += 1
            if ir & 1:
                ir -= 1
                self._all_apply(ir, f)
            il >>= 1
            ir >>= 1

        self._update_range_ancestors(kl, kr)

    def max_right(self, l: int, is_ok: Callable[[X], bool]) -> int:
        """
        Returns the maximum r for which is_ok( seg[l:r) ) is True.
        - Assumes is_ok( seg[l,i) ) is False ⇒ ∀j >= i, is_ok( seg[l,j) ) is False
        - f(e_x) must be True.
        """
        if not 0 <= l <= self.n:
            raise IndexError(f"Index {l} out of range")
        if not is_ok(self.e_x):
            raise ValueError("is_ok(e_x) must be True")
        if l == self.n:
            return self.n

        kl = l + self.size
        self._push_ancestors(kl)

        sm = self.e_x
        i = kl
        while True:
            while i & 1 == 0:
                i >>= 1
            nxt = self.op_x(sm, self._dat[i])
            if is_ok(nxt):
                sm = nxt
                i += 1
                if i & -i == i:
                    return self.n
            else:
                while i < self.size:
                    self._push(i)
                    i <<= 1
                    nxt = self.op_x(sm, self._dat[i])
                    if is_ok(nxt):
                        sm = nxt
                        i |= 1
                return i - self.size

    def min_left(self, r: int, is_ok: Callable[[X], bool]) -> int:
        """
        Returns the minimum l for which is_ok( seg[l:r) ) is True.
        """
        if not 0 <= r <= self.n:
            raise IndexError(f"Index {r} out of range")
        if not is_ok(self.e_x):
            raise ValueError("is_ok(e_x) must be True")
        if r == 0:
            return 0

        kr = r + self.size
        self._push_ancestors(kr - 1)

        sm = self.e_x
        i = kr
        while True:
            i -= 1
            while i > 1 and i & 1:
                i >>= 1
            nxt = self.op_x(self._dat[i], sm)
            if is_ok(nxt):
                sm = nxt
                if i & -i == i:
                    return 0
            else:
                while i < self.size:
                    self._push(i)
                    i = i << 1 | 1
                    nxt = self.op_x(self._dat[i], sm)
                    if is_ok(nxt):
                        sm = nxt
                        i ^= 1
                return i + 1 - self.size

    def __getitem__(self, item: Union[int, slice]) -> X:
        if isinstance(item, int):
            idx = item
            if idx < 0:
                idx += self.n
            return self.get(idx)
        elif isinstance(item, slice):
            start, stop, step = item.indices(self.n)
            if step != 1:
                raise ValueError("Slice step must be 1")
            return self.prod(start, stop)
        else:
            raise TypeError(f"Invalid argument type: {type(item)}")

    def __setitem__(self, idx: int, x: X):
        if idx < 0:
            idx += self.n
        self.set(idx, x)

    def __str__(self):
        return str([self.get(i) for i in range(self.n)])

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    import operator

    # X = (cnt0, cnt1, invnum)
    def op_x(x, y):
        return (
            x[0] + y[0],
            x[1] + y[1],
            x[2] + y[2] + x[1] * y[0],
        )

    e_x = (0, 0, 0)

    op_m = operator.xor
    e_m = 0

    def action(m, x):
        return (
            x[1],
            x[0],
            x[0] * x[1] - x[2],
        )

    N, Q = map(int, input().split())
    A = map(int, input().split())

    seg = LazySegTree(
        [(0, 1, 0) if a else (1, 0, 0) for a in A], op_x, e_x, op_m, e_m, action
    )

    for _ in range(Q):
        t, l, r = map(lambda x: int(x) - 1, input().split())
        r += 1
        if t == 0:
            seg.apply_range(l, r, 1)
        elif t == 1:
            ans = seg[l:r][2]
            print(ans)

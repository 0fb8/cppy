from typing import Optional, List, Tuple, Iterable
from sortedcontainers import SortedList

Interval = Tuple[int, int]


class IntervalSet:
    """
    Manages a set of disjoint intervals [l, r) using a SortedList.
    Supports add, remove, and set operations (union, intersection, etc.).
    """

    def __init__(self, intervals: Optional[Iterable[Interval]] = None):
        self._sl = SortedList()
        self._INF = 2 * 10**18
        # Sentinels to avoid boundary checks
        self._sl.add((-self._INF, -self._INF))
        self._sl.add((self._INF, self._INF))

        self._sz = 0  # Total length of covered intervals

        if intervals:
            for l, r in intervals:
                self.add(l, r)

    @classmethod
    def _from_sorted_disjoint(cls, intervals: List[Interval]) -> "IntervalSet":
        """
        Fast constructor for internal use when intervals are already sorted and disjoint.
        Complexity: O(N)
        """
        instance = cls()
        # Clear default sentinels to rebuild efficiently
        instance._sl.clear()
        instance._sl.update(intervals)
        # Re-add sentinels
        instance._sl.add((-instance._INF, -instance._INF))
        instance._sl.add((instance._INF, instance._INF))

        # Calculate size in O(N)
        instance._sz = sum(r - l for l, r in intervals)
        return instance

    def __repr__(self):
        return f"IntervalSet({list(self)})"

    def __len__(self):
        """Returns the number of disjoint intervals."""
        return len(self._sl) - 2

    def __iter__(self):
        """Iterates over the intervals in ascending order."""
        for i in range(1, len(self._sl) - 1):
            yield self._sl[i]

    def __contains__(self, x: int) -> bool:
        """Checks if x is contained in any interval. O(log N)"""
        idx = self._sl.bisect_left((x, self._INF))
        l, r = self._sl[idx - 1]
        return l <= x < r

    def __getitem__(self, k: int) -> Interval:
        """Returns the k-th interval. O(log N)"""
        n = len(self)
        if k < 0:
            k += n
        if not 0 <= k < n:
            raise IndexError("IntervalSet index out of range")
        return self._sl[k + 1]

    def total_len(self) -> int:
        """Returns the sum of lengths of all intervals."""
        return self._sz

    def canonical(self, x: int) -> Optional[Interval]:
        """Returns the interval containing x, or None."""
        idx = self._sl.bisect_left((x, self._INF))
        l, r = self._sl[idx - 1]
        if l <= x < r:
            return (l, r)
        return None

    def mex(self, x: int) -> int:
        """
        Returns the smallest integer >= x that is NOT in the set.
        If x is not covered, returns x.
        If x is covered by [l, r), returns r.
        """
        idx = self._sl.bisect_left((x, self._INF))
        l, r = self._sl[idx - 1]
        if l <= x < r:
            return r
        return x

    def add(self, l: int, r: Optional[int] = None) -> None:
        """
        Adds interval [l, r). Merges overlapping intervals.
        Complexity: O(log N + K), where K is the number of merged intervals.
        """
        ql, qr = l, r
        if qr is None:
            qr = ql + 1
        if ql >= qr:
            return

        # Find position: (ql, -INF) ensures we look before any interval starting at ql
        idx = self._sl.bisect_left((ql, -self._INF))

        # Check merge with previous interval
        if idx > 0:
            prev_l, prev_r = self._sl[idx - 1]
            if ql <= prev_r:  # Overlap or touch
                ql = min(ql, prev_l)
                qr = max(qr, prev_r)
                self._sz -= prev_r - prev_l
                self._sl.pop(idx - 1)
                idx -= 1

        # Check merge with next intervals
        while idx < len(self._sl):
            next_l, next_r = self._sl[idx]
            if qr < next_l:  # No overlap
                break
            # Overlap or touch
            qr = max(qr, next_r)
            self._sz -= next_r - next_l
            self._sl.pop(idx)

        self._sl.add((ql, qr))
        self._sz += qr - ql

    def discard(self, l: int, r: Optional[int] = None) -> None:
        """
        Removes interval [l, r). Splits intervals if necessary.
        Complexity: O(log N + K).
        """
        ql, qr = l, r
        if qr is None:
            qr = ql + 1
        if ql >= qr:
            return

        idx = self._sl.bisect_left((ql, -self._INF))

        # Check overlap with previous interval
        if idx > 0:
            prev_l, prev_r = self._sl[idx - 1]
            if ql < prev_r:
                # Remove previous, then potentially add back parts
                self._sz -= prev_r - prev_l
                self._sl.pop(idx - 1)
                idx -= 1

                if prev_l < ql:
                    self._sl.add((prev_l, ql))
                    self._sz += ql - prev_l
                    idx += 1

                if qr < prev_r:
                    self._sl.add((qr, prev_r))
                    self._sz += prev_r - qr
                    return

        # Check overlap with next intervals
        while idx < len(self._sl):
            next_l, next_r = self._sl[idx]
            if qr <= next_l:
                break

            self._sz -= next_r - next_l
            self._sl.pop(idx)

            if qr < next_r:
                self._sl.add((qr, next_r))
                self._sz += next_r - qr
                break

    def union(self, other: "IntervalSet") -> "IntervalSet":
        """Returns the union of two IntervalSets. O(N + M)"""
        merged = []
        it0 = iter(self)
        it1 = iter(other)
        cur0 = next(it0, None)
        cur1 = next(it1, None)

        curr_l, curr_r = None, None

        def push(l, r):
            nonlocal curr_l, curr_r
            if curr_l is None:
                curr_l, curr_r = l, r
            else:
                if l <= curr_r:
                    curr_r = max(curr_r, r)
                else:
                    merged.append((curr_l, curr_r))
                    curr_l, curr_r = l, r

        while cur0 is not None or cur1 is not None:
            if cur1 is None or (cur0 is not None and cur0 < cur1):
                push(*cur0)
                cur0 = next(it0, None)
            else:
                push(*cur1)
                cur1 = next(it1, None)

        if curr_l is not None:
            merged.append((curr_l, curr_r))

        return self._from_sorted_disjoint(merged)

    def intersection(self, other: "IntervalSet") -> "IntervalSet":
        """Returns the intersection of two IntervalSets. O(N + M)"""
        result = []
        it0 = iter(self)
        it1 = iter(other)
        cur0 = next(it0, None)
        cur1 = next(it1, None)

        while cur0 and cur1:
            l0, r0 = cur0
            l1, r1 = cur1

            # Intersection exists
            start = max(l0, l1)
            end = min(r0, r1)

            if start < end:
                result.append((start, end))

            if r0 < r1:
                cur0 = next(it0, None)
            else:
                cur1 = next(it1, None)

        return self._from_sorted_disjoint(result)

    def difference(self, other: "IntervalSet") -> "IntervalSet":
        """Returns the difference (self - other). O(N + M)"""
        result = []
        it1 = iter(other)
        cur1 = next(it1, None)

        for l, r in self:
            # Skip other intervals that end before current starts
            while cur1 and cur1[1] <= l:
                cur1 = next(it1, None)

            curr_l = l
            # Subtract overlapping intervals
            while cur1 and cur1[0] < r:
                l1, r1 = cur1
                if curr_l < l1:
                    result.append((curr_l, l1))
                curr_l = max(curr_l, r1)

                if r <= r1:
                    break
                cur1 = next(it1, None)

            if curr_l < r:
                result.append((curr_l, r))

        return self._from_sorted_disjoint(result)

    def symmetric_difference(self, other: "IntervalSet") -> "IntervalSet":
        """Returns the symmetric difference (XOR). O(N + M)"""
        u = self.union(other)
        i = self.intersection(other)
        return u.difference(i)

    def issubset(self, other: "IntervalSet") -> bool:
        """Checks if self <= other. O(N + M)"""
        it1 = iter(other)
        cur1 = next(it1, None)

        for l0, r0 in self:
            # Find an interval in 'other' that might cover 'cur0'
            while cur1 and cur1[1] <= l0:
                cur1 = next(it1, None)

            # If no interval in 'other' covers [l0, r0), return False
            if cur1 is None or not (cur1[0] <= l0 and r0 <= cur1[1]):
                return False

        return True

    def issuperset(self, other: "IntervalSet") -> bool:
        return other.issubset(self)

    def isdisjoint(self, other: "IntervalSet") -> bool:
        """Checks if intersection is empty. O(N + M)"""
        it1 = iter(other)
        cur1 = next(it1, None)
        for l0, r0 in self:
            while cur1 and cur1[1] <= l0:
                cur1 = next(it1, None)
            if cur1 and cur1[0] < r0:
                return False
        return True

    # Operator overloads
    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)

    def __xor__(self, other):
        return self.symmetric_difference(other)

    def __le__(self, other):
        return self.issubset(other)

    def __ge__(self, other):
        return self.issuperset(other)

    def __eq__(self, other):
        return self._sl == other._sl


if __name__ == "__main__":

    iset = IntervalSet()
    iset.add(10, 20)
    iset.add(30, 40)
    print(f"After add: {iset}, {iset.total_len()}")  # [(10, 20), (30, 40)], 20

    iset.add(15, 35)
    print(f"After merge: {iset}, {iset.total_len()}")  # [(10, 40)], 30

    iset.discard(25, 30)
    print(f"After discard: {iset}, {iset.total_len()}")  # [(10, 25), (30, 40)], 25

    print(f"Contains 20?: {20 in iset}")  # True
    print(f"Contains 27?: {27 in iset}")  # False
    print(f"Mex 27: {iset.mex(27)}")  # 27
    print(f"Mex 15: {iset.mex(15)}")  # 25

    s0 = IntervalSet([(1, 5), (10, 15)])
    s1 = IntervalSet([(4, 8), (12, 20)])

    print(f"Union {s0|s1}, {(s0|s1).total_len()}")  # [(1, 8), (10, 20)], 17
    print(f"Intersection {s0&s1}, {(s0&s1).total_len()}")  # [(4, 5), (12, 15)], 4
    print(f"Difference {s0-s1}, {(s0-s1).total_len()}")  # [(1, 4), (10, 12)], 5
    print(
        f"SymDiff {s0^s1}, {(s0^s1).total_len()}"
    )  # [(1, 4), (5, 8), (10, 12), (15, 20)] 13

    print((f"s0 is subset of s1?: {s0<=s1}"))  # False
    print("Subset check", s0 <= (s0 | s1))  # True
    print("Superset check", (s0 | s1) >= s1)  # True

    print("disjoint check", s0.isdisjoint(s1))  # False
    print("disjoint check", (s0 - s1).isdisjoint(s1 - s0))  # True

"""SparseTable/simple.py"""

from typing import List, Callable, TypeVar, Generic

T = TypeVar("T")


class SparseTable(Generic[T]):
    """
    Sparse Table for idempotent operations (e.g., min, gcd, bitwise-and).

    - Construction: O(N log N)
    - Query: O(1)
    - Requirement: The operation `op` must be associative and idempotent (op(x, x) = x).
    """

    def __init__(self, arr: List[T], op: Callable[[T, T], T]) -> None:
        """
        Initialize the Sparse Table.

        :param arr: Input list of elements.
        :param op: A binary idempotent function (e.g., min, math.gcd, operator.and_)
        """
        if not arr:
            raise ValueError("Input array must not be empty.")
        self.arr: List[T] = arr
        self.n: int = len(arr)
        self.op: Callable[[T, T], T] = op

        # Precompute log2 lookup table for O(1) query
        # self.log2[i] returns floor(log2(i))
        self.log2: List[int] = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log2[i] = self.log2[i >> 1] + 1

        # Build Sparse Table
        # st[k][i] covers range [i, i + 2^k)
        K: int = self.log2[self.n]
        self.st: List[List[T]] = [arr[:]]  # k=0: length 1 ranges

        for k in range(1, K + 1):
            prev_row = self.st[-1]
            size = 1 << k
            half = size >> 1
            current_row = [
                op(prev_row[i], prev_row[i + half]) for i in range(self.n - size + 1)
            ]
            self.st.append(current_row)

    def query(self, l: int, r: int) -> T:
        """
        Returns op over the interval arr[l:r).

        :param l: Start index (inclusive).
        :param r: End index (exclusive).
        :return: Result of op applied to the range.
        :raises IndexError: If indices are out of bounds.
        :raises ValueError: If the range is empty (l == r).
        """
        if l >= r:
            raise ValueError(f"Invalid range: l={l}, r={r}. Range must be non-empty.")
        if l < 0 or r > self.n:
            raise IndexError("Query indices out of range: l={l}, r={r}, n={self.n}")

        k = self.log2[r - l]

        # Overlap two ranges of length 2^k
        # One starting at l, one ending at r
        left_val = self.st[k][l]
        right_val = self.st[k][r - (1 << k)]
        return self.op(left_val, right_val)


if __name__ == "__main__":
    # Basic Validation
    data = [5, 2, 7, 3, 6, 2, 1]

    # Test Min
    st_min = SparseTable(data, op=min)
    assert st_min.query(1, 3) == 2  # min([2, 7]) -> 2
    assert st_min.query(2, 6) == 2  # min([7, 3, 6, 2]) -> 2
    assert st_min.query(0, 7) == 1  # min(all) -> 1

    # Test Max
    st_max = SparseTable(data, op=max)
    assert st_max.query(1, 3) == 7  # max([2, 7]) -> 7
    assert st_max.query(0, 1) == 5  # max([5]) -> 5

    # Test GCD
    from math import gcd

    st_gcd = SparseTable(data, op=gcd)
    assert st_gcd.query(3, 5) == 3  # gcd([3, 6]) -> 3
    assert st_gcd.query(0, len(data)) == 1  # gcd(all) -> 1

    # Test Error Handling
    try:
        st_min.query(3, 3)  # Empty range
        assert False, "Should raise ValueError for empty range"
    except ValueError:
        pass

    print("All tests passed!")

from fractions import Fraction
from typing import Union, Self


class DiscreteUniform:
    """
    Represents a discrete uniform random variable X chosen from the semi-open
    integer interval [start, stop).

    The probability mass function is P(X=k) = 1 / (stop - start)
    for k in {start, start+1, ..., stop-1}.
    """

    def __init__(self, start: int, stop: int) -> None:
        if start >= stop:
            raise ValueError("Interval must not be empty (start < stop).")
        self.start: int = start
        self.stop: int = stop
        self.count: int = stop - start
        self.count_f: Fraction = Fraction(self.count)

    def prob_eq(self, other: Union[int, Self]) -> Fraction:
        """P(X == Y) or P(X == value)"""
        other_dist: Self = self._ensure_instance(other)

        inter_l: int = max(self.start, other_dist.start)
        inter_r: int = min(self.stop, other_dist.stop)

        overlap: int = max(0, inter_r - inter_l)
        total: int = self.count * other_dist.count
        return Fraction(overlap, total)

    def prob_gt(self, other: Union[int, Self]) -> Fraction:
        """P(X > Y) or P(X > value)"""
        other_dist: Self = self._ensure_instance(other)

        valid: int = self._count_gt_rect(
            self.start, self.stop, other_dist.start, other_dist.stop
        )
        total: int = self.count * other_dist.count
        return Fraction(valid, total)

    def prob_ge(self, other: Union[int, Self]) -> Fraction:
        """P(X >= Y) or P(X >= value)"""
        # P(X >= Y) = P(X > Y) + P(X == Y)
        return self.prob_gt(other) + self.prob_eq(other)

    def prob_lt(self, other: Union[int, Self]) -> Fraction:
        """P(X < Y) or P(X < value)"""
        other_dist: Self = self._ensure_instance(other)
        # P(X < Y) <=> P(Y > X)
        return other_dist.prob_gt(self)

    def prob_le(self, other: Union[int, Self]) -> Fraction:
        """P(X <= Y) or P(X <= value)"""
        # P(X <= Y) = P(Y >= X)
        other_dist: Self = self._ensure_instance(other)
        return other_dist.prob_ge(self)

    def prob_ne(self, other: Union[int, Self]) -> Fraction:
        """P(X != Y) or P(X != value)"""
        return Fraction(1) - self.prob_eq(other)

    def prob_in_range(self, start: int, stop: int) -> Fraction:
        """P(start <= X < stop)"""
        inter_l: int = max(self.start, start)
        inter_r: int = min(self.stop, stop)

        overlap: int = max(0, inter_r - inter_l)
        return Fraction(overlap, self.count)

    def expected_value(self) -> Fraction:
        """
        Calculates the expected value E[X].
        E[X] = (L + R - 1) / 2 where X in [L, R).
        """
        # (start + (stop - 1)) / 2
        return Fraction(self.start + self.stop - 1, 2)

    def variance(self) -> Fraction:
        """
        Calculates the variance V[X].
        V[X] = (n^2 - 1) / 12 where n is the number of elements (count).
        """
        n: int = self.count
        # n^2 - 1
        numerator: int = n * n - 1
        return Fraction(numerator, 12)

    def _ensure_instance(self, other: Union[int, Self]) -> Self:
        """Helper to treat scalar x as an interval [x, x+1)."""
        if isinstance(other, int):
            return DiscreteUniform(other, other + 1)
        return other

    def _count_gt_rect(self, x1: int, x2: int, y1: int, y2: int) -> int:
        """Count pairs (x, y) where x > y in [x1, x2) x [y1, y2) using inclusion-exclusion."""

        def g(X: int, Y: int) -> int:
            if X <= 0 or Y <= 0:
                return 0
            M: int = min(X, Y)
            c: int = M * (M - 1) // 2
            if X > Y:
                c += (X - Y) * Y
            return c

        return g(x2, y2) - g(x1, y2) - g(x2, y1) + g(x1, y1)

    def __repr__(self) -> str:
        return f"U[{self.start}, {self.stop})"


if __name__ == "__main__":
    from fractions import Fraction as F

    def typical_66():
        N = int(input())

        D = []
        for _ in range(N):
            l, r = map(int, input().split())
            r += 1
            D.append(DiscreteUniform(l, r))

        ans = F(0)

        for i in range(N):
            for j in range(i + 1, N):
                ans += D[i].prob_gt(D[j])

        print(float(ans))

    typical_66()

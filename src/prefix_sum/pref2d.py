class PrefixSum2D:
    """
    2D Cumulative Sum (Prefix Sum) implementation.
    """

    def __init__(self, grid):
        """
        Args:
            grid (List[List[int]]): The input 2D matrix.
        """
        self.h = len(grid)
        self.w = len(grid[0])
        self.s = [[0] * (self.w + 1) for _ in range(self.h + 1)]

        for i in range(self.h):
            row_sum = 0
            for j in range(self.w):
                row_sum += grid[i][j]
                self.s[i + 1][j + 1] = self.s[i][j + 1] + row_sum

    def sum(self, r0, c0, r1, c1):
        """
        Calculate sum of the rectangle [r0, r1) x [c0, c1).
        """
        return self.s[r1][c1] - self.s[r0][c1] - self.s[r1][c0] + self.s[r0][c0]

    def __getitem__(self, item):
        """
        Usage: instance[r0:r1, c0:c1]
        """
        if isinstance(item, tuple) and len(item) == 2:
            r_slice, c_slice = item
            if isinstance(r_slice, slice) and isinstance(c_slice, slice):
                r0 = r_slice.start if r_slice.start is not None else 0
                r1 = r_slice.stop if r_slice.stop is not None else self.h
                c0 = c_slice.start if c_slice.start is not None else 0
                c1 = c_slice.stop if c_slice.stop is not None else self.w
                return self.sum(r0, c0, r1, c1)
        raise IndexError("Index must be a tuple of two slices, e.g., ps[0:2, 1:3]")


if __name__ == "__main__":

    def test():
        grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        ps = PrefixSum2D(grid)

        # [1, 2) x [1, 2) = grid[1][1] = 5
        assert ps.sum(1, 1, 2, 2) == 5

        # [0, 2) x [0, 2) = 1+2+4+5 = 12
        assert ps.sum(0, 0, 2, 2) == 12

        # [1, 3) x [1, 3) = 5+6+8+9 = 28
        assert ps[1:3, 1:3] == 28

        # 4+5+6 + 7+8+9 = 39
        assert ps[1:, :] == 39

        print("All test passed!")

    def tessoku_a08():
        H, W = map(int, input().split())
        X = [list(map(int, input().split())) for _ in range(H)]
        pX = PrefixSum2D(X)
        Q = int(input())
        for _ in range(Q):
            a, b, c, d = map(lambda x: int(x) - 1, input().split())
            c, d = c + 1, d + 1
            ans = pX[a:c, b:d]
            print(ans)

    tessoku_a08()

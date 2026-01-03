from bisect import bisect_left, bisect_right


class LIS:
    def __init__(self, data):
        self.raw_data = data

    def solve(self, increasing=True, strict=True):
        """
        Returns the length of the longest subsequence.

        :param increasing: True for an increasing subsequence, False for a decreasing subsequence
        :param strict: True for strict (<, >), False for non-strict (<=, >=)
        :return: Length of the longest subsequence
        """

        if not self.raw_data:
            return 0

        sign = 1 if increasing else -1
        is_2d = isinstance(self.raw_data[0], (list, tuple))

        if is_2d:
            items = [(sign * x[0], sign * x[1]) for x in self.raw_data]
            return self._solve_2d_lis(items, strict)
        else:
            items = [sign * x for x in self.raw_data]
            return self._solve_1d_lis(items, strict)

    def _solve_1d_lis(self, nums, strict):
        dp = []
        for x in nums:
            if strict:
                idx = bisect_left(dp, x)
            else:
                idx = bisect_right(dp, x)

            if idx < len(dp):
                dp[idx] = x
            else:
                dp.append(x)
        return len(dp)

    def _solve_2d_lis(self, pairs, strict):
        if strict:
            pairs.sort(key=lambda x: (x[0], -x[1]))
        else:
            pairs.sort(key=lambda x: (x[0], x[1]))

        b_vals = [p[1] for p in pairs]
        return self._solve_1d_lis(b_vals, strict)


if __name__ == "__main__":

    def tessoku_a24():
        n = int(input())
        a = list(map(int, input().split()))
        lis = LIS(a)
        ans = lis.solve(increasing=True, strict=True)
        print(ans)

    def abc439e():
        n = int(input())
        ab = list(tuple(map(int, input().split())) for _ in range(n))

        lis = LIS(ab)
        ans = max(lis.solve(increasing=True), lis.solve(increasing=False))
        print(ans)

    abc439e()

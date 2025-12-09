from typing import List, Optional
from collections import deque


def sliding_range_max(
    A: List[int],
    start_offset: int,
    end_offset: int,
    *,
    fillvalue: Optional[int] = None,
) -> List[Optional[int]]:
    """
    Computes the maximum value within the relative half-open interval
    [i + start_offset, i + end_offset) for each index i in array A.
    """
    n = len(A)
    res = [fillvalue] * n
    dq = deque()

    r = 0

    for i in range(n):
        target_start = i + start_offset
        target_end = i + end_offset

        limit = min(target_end, n)
        while r < limit:
            val = A[r]
            while dq and A[dq[-1]] <= val:
                dq.pop()
            dq.append(r)
            r += 1

        while dq and dq[0] < target_start:
            dq.popleft()

        real_start = max(0, target_start)
        real_end = min(n, target_end)

        if real_start < real_end and dq:
            res[i] = A[dq[0]]
        else:
            res[i] = fillvalue

    return res


if __name__ == "__main__":
    from math import inf, isfinite

    W, N = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(N)]

    dp = [-inf] * (W + 1)
    dp[0] = 0

    for l, r, v in items:
        ndp = [-inf] * (W + 1)

        for m, w in zip(
            sliding_range_max(dp, -r, -l + 1, fillvalue=-inf), range(W + 1)
        ):
            ndp[w] = max(m + v, dp[w])

        dp = ndp

    ans = dp[W] if isfinite(dp[W]) else -1
    print(ans)

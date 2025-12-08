from typing import *

X = TypeVar("X")
Prime: TypeAlias = int


def eratosthenes(
    n: int,
    f: Optional[Callable[[Prime], Iterator[Tuple[int, X]]]] = None,
    op: Optional[Callable[[X, X], X]] = None,
    e: Optional[X] = None,
) -> Tuple[List[Optional[X]], List[bool]]:

    if f is None:
        f = lambda p: zip(iter([]), iter([]))

    if op is None:
        op = lambda a, b: b

    ans: List[Optional[X]] = [e for _ in range(n + 1)]
    is_prime: List[bool] = [True] * (n + 1)

    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    for p in range(n + 1):
        if not is_prime[p]:
            continue

        for i in range(p << 1, n + 1, p):
            is_prime[i] = False

        for i, val in f(p):
            if not 0 <= i <= n:
                continue
            ans[i] = op(ans[i], val)

    return ans, is_prime


if __name__ == "__main__":
    import operator
    import itertools as it

    def typical_30():
        N, K = map(int, input().split())

        def f(p):
            return zip(range(p, N + 1, p), it.repeat(1))

        p_cnt, _ = eratosthenes(N, f, operator.add, 0)

        ans = sum(1 for i in p_cnt if i >= K)
        print(ans)

    def abc084d():
        N = 10**5

        def f(p):
            return [(p, 1), ((p << 1) - 1, 1)]

        p_cnt, _ = eratosthenes(N, f, operator.add, 0)

        A = [int(i & 1 and v == 2) for i, v in enumerate(p_cnt)]
        pref = list(it.accumulate(A, initial=0))

        Q = int(input())
        for _ in range(Q):
            l, r = map(int, input().split())
            r += 1
            ans = pref[r] - pref[l]
            print(ans)

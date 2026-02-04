"""floyd_cycle/simple.py"""


def floyd_cycle_finding(f, x0):
    """
    Finds the pre-period length (lambda) and cycle length (mu) of a functional graph.

    Args:
        f: A function that takes a state and returns the next state.
        x0: The initial state.

    Returns:
        (lam, mu): (pre-period length, cycle length)
    """
    # 1. Finding the meeting point
    tortoise = f(x0)
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))

    # 2. Finding lambda (pre-period length)
    tortoise = x0
    lam = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        lam += 1

    # 3. Finding mu (cycle length)
    mu = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        mu += 1

    return lam, mu


if __name__ == "__main__":

    def abc241():
        N, K = map(int, input().split())
        A = list(map(int, input().split()))

        lam, mu = floyd_cycle_finding(lambda x: (x + A[x]) % N, 0)
        cycle_num, nu = divmod(K - lam, mu)
        # K = lam + (cycle_num * mu) + nu

        if K < lam:
            x = 0
            for _ in range(K):
                x += A[x % N]
            print(x)
            return

        x = 0

        for _ in range(lam):
            x += A[x % N]

        y = x
        for _ in range(mu):
            y += A[y % N]
        x += (y - x) * cycle_num

        for _ in range(nu):
            x += A[x % N]

        print(x)
        return

    abc241()

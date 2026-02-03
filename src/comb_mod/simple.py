class CombMod:
    def __init__(self, mod: int, N: int):
        self.mod = mod
        self.N = N

        self._fact = [1] * (N + 1)
        for i in range(1, N + 1):
            self._fact[i] = (self._fact[i - 1] * i) % mod
        self._invfact = [1] * (N + 1)
        self._invfact[N] = pow(self._fact[N], mod - 2, mod)
        for i in range(N, 0, -1):
            self._invfact[i - 1] = (self._invfact[i] * i) % mod

    def _check_n(self, n: int):
        if not (0 <= n <= self.N):
            raise ValueError(f"n must be in [0, {self.N}]")

    def fact(self, n: int) -> int:
        """Return n! % mod."""
        self._check_n(n)
        return self._fact[n]

    def invfact(self, n: int) -> int:
        self._check_n(n)
        return self._invfact[n]

    def nCk(self, n: int, k: int) -> int:
        """Return C(n, k) % mod (0 if k out of range)."""
        self._check_n(n)
        if not 0 <= k <= n:
            return 0
        ans = (
            self._fact[n]
            * self._invfact[k]
            % self.mod
            * self._invfact[n - k]
            % self.mod
        )
        return ans


if __name__ == "__main__":

    def abc034c():
        W, H = map(lambda x: int(x) - 1, input().split())
        MOD = 10**9 + 7

        cm = CombMod(MOD, W + H)
        ans = cm.nCk(W + H, W)
        print(ans)

    abc034c()

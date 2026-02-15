def doubling(arr_f, n):
    res = list(range(len(arr_f)))  # id
    f = arr_f

    for k in range(n.bit_length()):
        if n >> k & 1:
            res = [f[r] for r in res]
        f = [f[a] for a in f]

    return res


if __name__ == "__main__":

    def abc445c():
        N = int(input())
        A = list(map(lambda x: int(x) - 1, input().split()))
        M = 10**100

        ans = doubling(A, M)

        print(*map(lambda x: x + 1, ans))
        return

    abc445c()

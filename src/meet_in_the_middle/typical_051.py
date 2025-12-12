from bisect import bisect_right

N, K, P = map(int, input().split())
A = list(map(int, input().split()))

B = [[] for _ in range(N + 1)]
for bit in range(1 << N // 2):
    k = bit.bit_count()
    s = sum(A[i] for i in range(N // 2) if bit >> i & 1)
    B[k].append(s)

for k in range(N + 1):
    B[k].sort()

ans = 0
for bit in range(1 << (N - N // 2)):
    k = bit.bit_count()
    s = sum(A[i] for i in range(N // 2, N) if bit >> (i - N // 2) & 1)
    res = bisect_right(B[K - k], P - s) if K - k >= 0 else 0
    ans += res

print(ans)

import more_itertools as mit

n, q = map(int, input().split())
p = [tuple(map(int, input().split())) for _ in range(n)]

mn_s, mx_s = mit.minmax(x + y for x, y in p)
mn_d, mx_d = mit.minmax(x - y for x, y in p)

for _ in range(q):
    i = int(input()) - 1
    x, y = p[i]
    s, d = x + y, x - y
    ans = max(mx_s - s, s - mn_s, mx_d - d, d - mn_d)
    print(ans)

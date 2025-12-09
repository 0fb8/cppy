import more_itertools as mit

n = int(input())
p = [tuple(map(int, input().split())) for _ in range(n)]

mn_s, mx_s = mit.minmax(x + y for x, y in p)
mn_d, mx_d = mit.minmax(x - y for x, y in p)

ans = max(mx_s - mn_s, mx_d - mn_d)
print(ans)

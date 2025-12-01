def main():

    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    ans = 0

    cnt = defaultdict(int)  # [il, ir) における値を管理
    ir = 0
    for il in range(N):
        if ir < il:
            ir = il

        # while ir < N and is_ok( A[il, ir] ): ir++
        while ir < N and (A[ir] in cnt or len(cnt) + 1 <= K):
            cnt[A[ir]] += 1
            ir += 1

        # assert is_ok( A[il, ir) )
        # assert ir == N or is_ng( A[il, ir] )
        ans = max(ans, ir - il)

        # il++
        if il < ir:
            cnt[A[il]] -= 1
            if not cnt[A[il]]:
                del cnt[A[il]]

    print(ans)

    return


from collections import defaultdict

class Doubling:
    def __init__(self, arr_f, max_m):
        self.n = len(arr_f)
        self.log_m = max_m.bit_length()

        self.table = [0] * (self.n * self.log_m)
        for i in range(self.n):
            self.table[i] = arr_f[i]

        for k in range(1, self.log_m):
            ofst = (k - 1) * self.n
            nxt_ofst = ofst + self.n
            for i in range(self.n):
                self.table[nxt_ofst + i] = self.table[ofst + self.table[ofst + i]]

    def query(self, start_node, m):
        res = start_node
        for k in range(m.bit_length()):
            if m >> k & 1:
                res = self.table[k * self.n + res]
        return res


if __name__ == "__main__":

    def tessoku_a57():
        N, Q = map(int, input().split())
        A = list(map(lambda x: int(x) - 1, input().split()))
        V = 10**9

        db = Doubling(A, V)

        for _ in range(Q):
            x, y = map(int, input().split())
            x -= 1

            ans = db.query(x, y)
            print(ans + 1)

    tessoku_a57()

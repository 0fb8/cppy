from typing import *
from functools import reduce
from itertools import accumulate

T = TypeVar("T")


class Graph_T:
    def __init__(
        self,
        n: int,
        braid: Callable[[T, T], T],
        augment: Callable[[T, T], T],
    ):
        """
        :param n: number of nodes.
        :param braid: (T, braid) must be commutative semigroup (associative and commutative).
        :param augment: (T, augment) must be semigroup (associative). argument order is (ancestor_side, decendant_side).
        """
        self.n = n
        self.braid = braid
        self.augment = augment

        self.adj_list: List[List[Tuple[int, T]]] = [[] for _ in range(n)]
        self.vertex_weights: List[Optional[T]] = [None] * n

    def add_vertex(self, v: int, wv: T):
        """
        Set weight for a vertex.

        :param v: vertex
        :param wv: weight vertex
        """
        if not 0 <= v < self.n:
            raise IndexError
        self.vertex_weights[v] = wv

    def add_directed_edge(self, v: int, nv: int, we: T):
        """
        Add a directed edge with weight `we`.

        :param v: vertex
        :param nv: next vertex
        :param we: weight edge
        """
        if not (0 <= v < self.n and 0 <= nv < self.n):
            raise IndexError
        self.adj_list[v].append((nv, we))

    def add_undirected_edge(self, v: int, nv: int, we: T):
        """
        Add an undirected edge with weight `we`.
        """
        self.add_directed_edge(v, nv, we)
        self.add_directed_edge(nv, v, we)

    def rerooting(self) -> List[T]:
        """
        Returns a list where list[v] is the result when v is the root.
        """
        if self.n == 0:
            return []

        order = []
        parent = [None] * self.n
        stk = [0]
        visited = [False] * self.n
        parent_edge_weight = [None] * self.n
        while stk:
            v = stk.pop()
            visited[v] = True
            order.append(v)
            for nv, we in self.adj_list[v]:
                if visited[nv]:
                    continue
                parent[nv] = v
                parent_edge_weight[nv] = we
                stk.append(nv)

        # --- Bottom-up ---
        de = [None] * self.n  # down or equal
        for v in reversed(order):
            pv = parent[v]
            wv = self.vertex_weights[v]
            nvs = self.adj_list[v]
            k = len(nvs)

            dt = (
                reduce(
                    self.braid,
                    (self.augment(we, de[nv]) for nv, we in nvs if nv != pv),
                )
                if k >= 2 or (k == 1 and nvs[0][0] != pv)
                else None
            )
            de[v] = self.augment(wv, dt) if dt is not None else wv

        # --- Top-down ---
        ut = [None] * self.n  # up than
        ans = [None] * self.n
        for v in order:
            pv = parent[v]
            wv = self.vertex_weights[v]
            nvs = self.adj_list[v]
            k = len(nvs)

            out_vals = [
                self.augment(we, de[nv]) if nv != pv else ut[v] for nv, we in nvs
            ]

            t = reduce(self.braid, out_vals) if out_vals else None
            ans[v] = self.augment(wv, t) if t is not None else wv

            if k == 0 or (k == 1 and nvs[0][0] == pv):
                continue

            if k == 1 and nvs[0][0] != pv:
                only_nv = nvs[0][0]
                ut[only_nv] = (
                    self.augment(wpe, wv)
                    if (wpe := parent_edge_weight[only_nv]) is not None
                    else None
                )
                continue

            pref = list(accumulate(out_vals, self.braid))
            suff = list(accumulate(reversed(out_vals), self.braid))[::-1]
            for i, (nv, _) in enumerate(nvs):
                if nv == pv:
                    continue

                if i == 0:
                    braided_others = suff[1]
                elif i == k - 1:
                    braided_others = pref[k - 2]
                else:
                    braided_others = self.braid(pref[i - 1], suff[i + 1])

                res = self.augment(wv, braided_others)

                ut[nv] = (
                    self.augment(wpe, res)
                    if (wpe := parent_edge_weight[nv]) is not None
                    else None
                )

        return ans


if __name__ == "__main__":
    import operator
    from math import inf, isfinite

    def apg4b_ex20():
        """
        number of nodes in subtree rooted at v (including v itself).
        """

        n = int(input())
        graph = Graph_T(n, operator.add, operator.add)

        for v in range(n):
            graph.add_vertex(v, 1)

        p_lst = [None] + list(map(int, input().split()))
        for v, pv in enumerate(p_lst):
            if v == 0:
                continue
            graph.add_directed_edge(pv, v, 0)

        ans = graph.rerooting()

        print("\n".join(map(str, ans)))
        return

    def abc428e():
        """
        for each node, find the farthest node (defined by edge count).
        if multiple, choose the largest index.
        """

        def augment(x, y):
            x_w, _ = x
            y_w, y_v = y
            return (x_w + y_w, y_v)

        n = int(input())
        graph = Graph_T(n, max, augment)

        for v in range(n):
            graph.add_vertex(v, (0, v))

        for _ in range(n - 1):
            u, v = map(lambda x: int(x) - 1, input().split())
            graph.add_undirected_edge(u, v, (1, -inf))

        ans = graph.rerooting()

        for d, a in ans:
            print(a + 1)
        return

    def typical_039():
        """
        sum_{u=1}^{N-1} sum_{v=u+1}^{N} dist(u,v)
        """

        def braid(x, y):
            w_x, v_cnt_x = x
            w_y, v_cnt_y = y
            return (w_x + w_y, v_cnt_x + v_cnt_y)

        def augment(x, y):
            w_x, v_cnt_x = x
            w_y, v_cnt_y = y
            return (w_x * v_cnt_y + w_y, v_cnt_x + v_cnt_y)

        n = int(input())
        graph = Graph_T(n, braid, augment)

        for v in range(n):
            graph.add_vertex(v, (0, 1))

        for _ in range(n - 1):
            u, v = map(lambda x: int(x) - 1, input().split())
            graph.add_undirected_edge(u, v, (1, 0))

        res = graph.rerooting()

        sm_w = sum(w for w, c in res)
        ans = sm_w // 2
        print(ans)
        return

    apg4b_ex20()
    # abc428e()
    # typical_039()

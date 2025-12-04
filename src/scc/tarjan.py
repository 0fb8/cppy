"""scc/tarjan.py"""

from typing import List, Optional

Node = int
Graph = List[List[Node]]


def scc(graph: Graph) -> List[List[Node]]:
    """
    Finds Strongly Connected Components (SCC) using Tarjan's algorithm.
    Returns list of SCCs in topological order.
    """

    n = len(graph)
    inf = n + 1

    order: List[Optional[int]] = [None] * n
    lowlink: List[int] = [inf] * n
    tarjan_stk: List[Node] = []
    ans: List[List[Node]] = []

    ptr: List[int] = [0] * n
    call_stk: List[Node] = []
    now_ord = 0

    for sv in range(n):
        if order[sv] is not None:
            continue
        call_stk.append(sv)

        while call_stk:
            v = call_stk[-1]

            if order[v] is None:  # pre
                lowlink[v] = order[v] = now_ord
                now_ord += 1
                tarjan_stk.append(v)

            while ptr[v] < len(graph[v]):  # in
                nv = graph[v][ptr[v]]
                ptr[v] += 1

                if order[nv] is None:
                    call_stk.append(nv)
                    break
                else:
                    lowlink[v] = min(lowlink[v], order[nv])

            else:  # post
                call_stk.pop()
                if lowlink[v] == order[v]:
                    cur_scc = []
                    while True:
                        u = tarjan_stk.pop()
                        order[u] = inf
                        cur_scc.append(u)
                        if u == v:
                            break
                    ans.append(cur_scc)
                if call_stk:
                    pv = call_stk[-1]
                    lowlink[pv] = min(lowlink[pv], lowlink[v])

    return ans[::-1]

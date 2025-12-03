def main():

    return


# ------------------------------
# fmt: off

import os, sys
IS_ATCODER = os.getenv("ATCODER") == "1"
IS_LOCAL = not IS_ATCODER
def debug(*args, **kwargs): print(*args, **kwargs, file=sys.stderr) if IS_LOCAL else None

import bisect
import collections
import copy
import fractions
import functools
import heapq
import itertools as it
import math
import more_itertools as mit
import operator
import random
import sortedcontainers
import string
import sympy
import typing

from bisect import bisect_left, bisect_right
from collections import deque, defaultdict, Counter, namedtuple
from functools import reduce
from heapq import heappush as hpush, heappop as hpop
from itertools import accumulate, groupby, pairwise
from math import inf, isfinite, nan, isnan
from math import gcd, lcm, floor, ceil
from more_itertools import batched, windowed
from sortedcontainers import SortedSet, SortedList, SortedDict
from typing import *

class D4:
    def rotate0(m): return m
    def rotate90(m): return [list(r) for r in zip(*m)][::-1]
    def rotate180(m): return [r[::-1] for r in m[::-1]]
    def rotate270(m): return [list(r)[::-1] for r in zip(*m)]
    def flip_lr(m): return [r[::-1] for r in m]
    def flip_ud(m): return m[::-1]
    def transpose(m): return [list(r) for r in zip(*m)]
    def anti_transpose(m): return [list(r) for r in zip(*m[::-1])][::-1]

trn = D4.transpose
def ins(): return input().split()
def int1(x): return int(x) - 1
def incr(x): return x + 1
def decr(x): return x - 1
def YesNo(ans: bool) -> bool: print("Yes" if ans else "No"); return ans

MOD = 998244353
MOD1 = 10**9 + 7
def add_mod(a, b, M=MOD): return (a + b) % M
def mul_mod(a, b, M=MOD): return (a * b) % M

def rle(A): return list((k, len(list(g))) for (k, g) in groupby(A))

DIR = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIR8 = ((1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1))

def l1d(p, q): return abs(p[0] - q[0]) + abs(p[1] - q[1])
def l2d2(p, q): return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
def linfd(p, q): return max(abs(p[0] - q[0]), abs(p[1] - q[1]))

def popcnt(x): return x.bit_count()

# fmt:on
# ------------------------------


if __name__ == "__main__":
    input = lambda: sys.stdin.readline().rstrip()
    sys.setrecursionlimit(1 << 25)

    testcase = 1

    for _ in range(int(testcase)):
        main()

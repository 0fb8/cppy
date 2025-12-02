from typing import *

T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    """
    Union-Find (Disjoint Set Union) data structure for arbitrary hashable elements.
    Implements path compression and union-by-size.
    """

    def __init__(self, elements: Optional[Iterable[T]] = None):
        """
        Initialize the UnionFind structure.

        Args:
            elements: Optional iterable of elements to add initially.
        """
        self._par: Dict[T, T] = {}
        self._siz: Dict[T, int] = {}

        if elements:
            for x in elements:
                self.add(x)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.groups()})"

    def __len__(self) -> int:
        """Return the total number of elements managed."""
        return len(self._par)

    def __contains__(self, x: T) -> bool:
        return x in self._par

    def add(self, x: T) -> None:
        """
        Add a new element x. If x already exists, do nothing.
        """
        if x in self._par:
            return
        self._par[x] = x
        self._siz[x] = 1

    def find(self, x: T) -> T:
        """
        Find the representative (root) of the set containing x.
        Raises KeyError if x is not found.
        """
        if x not in self._par:
            raise KeyError(f"{x} is not in this UnionFind")

        path = []
        while self._par[x] != x:
            path.append(x)
            x = self._par[x]

        for node in path:
            self._par[node] = x

        return x

    def union(self, x: T, y: T) -> bool:
        """
        Unite the sets containing x and y.
        Returns True if a merge happened, False if they were already in the same set.
        Raises KeyError if x or y are not found.
        """

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self._siz[root_x] < self._siz[root_y]:
            root_x, root_y = root_y, root_x

        self._par[root_y] = root_x
        self._siz[root_x] += self._siz[root_y]
        return True

    def connected(self, x: T, y: T) -> bool:
        """
        Check if x and y are in the same set.
        Raises KeyError if x or y are not found.
        """
        return self.find(x) == self.find(y)

    def size(self, x: T) -> int:
        """Return the size of the set containing x."""
        return self._siz[self.find(x)]

    def roots(self) -> List[T]:
        """Return a list of all roots"""
        return [x for x, p in self._par.items() if x == p]

    def groups(self) -> List[List[T]]:
        """Return all sets as a list of lists."""
        groups_dict: Dict[T, List[T]] = {}
        for x in self._par:
            r = self.find(x)
            groups_dict.setdefault(r, []).append(x)
        return list(groups_dict.values())

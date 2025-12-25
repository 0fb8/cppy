from typing import *

T = TypeVar("T", bound=Hashable)
V = TypeVar("V")


class TrieNode(Generic[T, V]):
    __slots__ = (
        "children",
        "value",
        "has_value",
        "_token",
        "parent",
        "key_in_parent",
    )

    def __init__(
        self,
        parent: Optional["TrieNode[T, V]"] = None,
        key_in_parent: Optional[T] = None,
    ) -> None:
        self.children: Dict[T, "TrieNode[T, V]"] = {}
        self.value: Optional[V] = None
        self.has_value: bool = False
        self._token: int = 0
        self.parent = parent
        self.key_in_parent = key_in_parent

    def __repr__(self):
        return f"{self.value}"


class NodeRef(Generic[T, V]):
    __slots__ = ("_node", "_token")

    def __init__(self, node: TrieNode[T, V], token: int):
        self._node = node
        self._token = token

    def is_valid(self) -> bool:
        return self._node.has_value and (self._node._token == self._token)


class TrieMap(Generic[T, V]):
    """
    Trie-based mapping (Sequence[T] -> V) with support for relative operations.
    """

    def __init__(self, default_factory: Optional[Callable[[], V]] = None) -> None:
        self.root: TrieNode[T, V] = TrieNode()
        self.default_factory = default_factory
        self._size: int = 0

    def _get_start_node(self, start: Optional[NodeRef[T, V]]) -> TrieNode[T, V]:
        if start is None:
            return self.root
        if not start.is_valid():
            raise ReferenceError("Invalid or stale NodeRef")
        return start._node

    def _navigate(
        self, key: Sequence[T], start: TrieNode[T, V], create: bool = False
    ) -> Optional[TrieNode[T, V]]:
        curr = start
        for e in key:
            if e not in curr.children:
                if not create:
                    return None
                curr.children[e] = TrieNode(parent=curr, key_in_parent=e)
            curr = curr.children[e]
        return curr

    def get(
        self,
        key: Sequence[T],
        default: Any = None,
        root: Optional[NodeRef[T, V]] = None,
    ) -> Any:
        """
        Get the value.
        If it doesn't exist, returns the default without inserting it.
        (dict.get behavior).
        """
        node = self._navigate(key, self._get_start_node(root), create=False)
        return node.value if node is not None and node.has_value else default

    def getitem(
        self,
        key: Sequence[T],
        root: Optional[NodeRef[T, V]] = None,
    ) -> V:
        """Get value for key."""
        node = self._navigate(key, self._get_start_node(root), create=True)
        if not node.has_value:
            if self.default_factory is None:
                raise KeyError(key)
            node.value = self.default_factory()
            node.has_value = True
            self._size += 1
        return node.value

    def setitem(
        self, key: Sequence[T], value: V, root: Optional[NodeRef[T, V]] = None
    ) -> NodeRef[T, V]:
        """Set value for key."""
        node = self._navigate(key, self._get_start_node(root), create=True)
        if not node.has_value:
            node.has_value = True
            self._size += 1
        node.value = value
        return NodeRef(node, node._token)

    def delitem(self, key: Sequence[T], root: Optional[NodeRef[T, V]] = None) -> None:
        """Remove and return the value for key."""
        start_node = self._get_start_node(root)
        target = self._navigate(key, start_node, create=False)

        if target is None or not target.has_value:
            raise KeyError(key)

        target.value = None
        target.has_value = False
        target._token += 1
        self._size -= 1

        curr = target
        while curr is not start_node and curr.parent is not None:
            if not curr.children and not curr.has_value:
                p = curr.parent
                del p.children[curr.key_in_parent]
                curr = p
            else:
                break
        return

    def contains(self, key: Sequence[T], root: Optional[NodeRef[T, V]] = None) -> bool:
        node = self._navigate(key, self._get_start_node(root), create=False)
        return node is not None and node.has_value

    def get_ref(
        self, key: Sequence[T], root: Optional[NodeRef[T, V]] = None
    ) -> Optional[NodeRef[T, V]]:
        """Get a valid NodeRef for the key if it exists."""
        node = self._navigate(key, self._get_start_node(root), create=False)
        return NodeRef(node, node._token) if node and node.has_value else None

    def values(self, prefix: Sequence[T] = (), root: Optional[NodeRef[T, V]] = None):
        """Yield value with prefix."""
        start = self._get_start_node(root)
        target = self._navigate(prefix, start, create=False)
        if not target:
            return

        stk: List[TrieNode[T, V]] = [target]
        while stk:
            curr = stk.pop()
            if curr.has_value:
                yield curr.value
            for _, child in sorted(curr.children.items(), reverse=True):
                stk.append(child)

    def items(self, prefix: Sequence[T] = (), root: Optional[NodeRef[T, V]] = None):
        """Yield (key, value) pairs starting with prefix."""
        start = self._get_start_node(root)
        target = self._navigate(prefix, start, create=False)
        if not target:
            return

        is_str = isinstance(prefix, str) or (
            len(prefix) == 0
            and self.root.children
            and isinstance(next(iter(self.root.children.keys())), str)
        )

        stk: List[Tuple[TrieNode[T, V], List[T]]] = [(target, list(prefix))]
        while stk:
            curr, path = stk.pop()
            if curr.has_value:
                yield ("".join(path) if is_str else tuple(path), curr.value)
            for e, child in sorted(curr.children.items(), reverse=True):
                stk.append((child, path + [e]))

    # --- Syntactic Sugars (Absolute Path) ---
    def __setitem__(self, key: Sequence[T], value: V):
        self.setitem(key, value)

    def __getitem__(self, key: Sequence[T]) -> V:
        return self.getitem(key)

    def __delitem__(self, key: Sequence[T]):
        self.delitem(key)

    def __contains__(self, key: Sequence[T]) -> bool:
        return self.contains(key)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"TrieMap({dict(self.items())})"


if __name__ == "__main__":

    def test():
        print("Starting TrieMap tests...")

        # 1.
        trie = TrieMap[str, int](int)
        trie["apple"] = 10
        trie["app"] = 5

        assert trie["apple"] == 10
        assert trie["app"] == 5
        assert trie.get("absent", default=0) == 0
        assert "absent" not in trie
        assert trie["absent"] == 0
        assert "absent" in trie
        print("Check 1: passed.")

        # 2.
        # trie: {app, apple, absent}
        assert len(trie) == 3
        print("Check 2: passed.")

        # 3.
        ref_app = trie.get_ref("app")
        assert ref_app is not None
        assert ref_app.is_valid()

        val_relative = trie.get("le", root=ref_app)  # apple
        assert val_relative == 10

        trie.setitem("ly", 15, root=ref_app)  # apply
        assert trie["apply"] == 15
        assert len(trie) == 4  # apple, app, ansent, apply
        print("Check 3: passed.")

        # 4.
        ref_apply_v1 = trie.get_ref("apply")
        trie["apply"] = 20  # update
        assert ref_apply_v1.is_valid()

        ref_app_v1 = trie.get_ref("app")
        del trie["app"]  # pop
        assert not ref_app_v1.is_valid()
        assert "app" not in trie
        assert len(trie) == 3  # apple, absent, apply
        print("Check 4: passed.")

        # 5.
        # trie: {apple, absent, apply}
        items = list(trie.items(prefix="ap"))
        assert ("apple", 10) in items
        assert ("apply", 20) in items
        assert len(items) == 2

        debug_str = repr(trie)
        assert "apple" in debug_str
        assert "absent" in debug_str
        print("Check 5: passed.")

        # 6.
        del trie["apple"]
        del trie["apply"]
        assert "a" in trie.root.children
        assert len(trie) == 1
        print("Check 6: passed.")

        print("\nAll tests passed successfully!\n")

    def abc437e():
        n = int(input())

        trie = TrieMap(list)
        ref_node = [None] * (n + 1)
        ref_node[0] = trie.get_ref([])

        for i in range(1, n + 1):
            x, y = map(int, input().split())
            pv = ref_node[x]
            val = trie.getitem([y], root=pv)
            val.append(i)
            trie.setitem([y], val, root=pv)
            ref_node[i] = trie.get_ref([y], root=pv)

        from more_itertools import collapse

        ans = collapse(trie.values())
        print(*ans)

    # test()
    abc437e()

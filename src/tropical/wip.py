from abc import ABC, abstractmethod
from math import inf


class SemiRing(ABC):

    @abstractmethod
    def add(self, a, b):
        pass

    @abstractmethod
    def mul(self, a, b):
        pass

    @abstractmethod
    def e0(self):
        pass

    @abstractmethod
    def e1(self):
        pass

    def sum(self, xs):
        acc = self.e0(self)
        for x in xs:
            acc = self.add(self, acc, x)
        return acc

    def prod(self, xs):
        acc = self.e1(self)
        for x in xs:
            acc = self.mul(self, acc, x)
        return acc


class MinPlus_Semiring(SemiRing):

    def add(self, a, b):
        return min(a, b)

    def mul(self, a, b):
        return a + b

    def e0(self):
        return inf

    def e1(self):
        return 0


if __name__ == "__main__":
    A = [3, 1, 4]
    B = [27, 18, 28]

    MP = MinPlus_Semiring
    print(MP.sum(MP, A), MP.sum(MP, B))
    print(MP.prod(MP, A), MP.prod(MP, B))

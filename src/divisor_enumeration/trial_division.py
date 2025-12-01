from typing import *


def divisors(n: int) -> List[int]:
    lower_divisors, upper_divisors = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lower_divisors.append(i)
            if i != n // i:
                upper_divisors.append(n // i)
        i += 1
    return lower_divisors + upper_divisors[::-1]


def main():
    N = int(input())
    ans = divisors(N)
    print("\n".join(str(a) for a in ans))


if __name__ == "__main__":
    main()

from dataclasses import dataclass

repeat_int = 1
@dataclass
class ProxyClass:
    x: int = 0
    y: int = 0


def proxyRef(reff: ProxyClass) -> None:
    reff.x = 1
    reff.y = 1


def proxyRet() -> ProxyClass:
    rett = ProxyClass()
    rett.x = 1
    rett.y = 1
    return rett


def by_reference():
    ref = ProxyClass()
    for _ in range(repeat_int):
        proxyRef(reff=ref)


def by_return():
    for _ in range(repeat_int):
        ret = proxyRet()


if __name__ == '__main__':
    import timeit

    number = 10000000
    repeat = 5
    print("Reference:")
    for _ in range(repeat):
        print(timeit.timeit("by_reference()", number=number, globals=globals()))

    print("Return:")
    for _ in range(repeat):
        print(timeit.timeit("by_return()", number=number, globals=globals()))

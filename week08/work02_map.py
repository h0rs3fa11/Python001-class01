from collections.abc import Iterable


def add_func(a, b):
    # print(a, b)
    return a + b


def multi_func(a, b, c):
    return a * b * c


def diy_map(func, *args):
    """
    @param func: 函数对象
    @param iterable: 一个或多个可迭代对象
    @return: None
    """
    for arg in zip(*args):
        yield func(*arg)


if __name__ == '__main__':
    print(list(diy_map(add_func, [1, 2, 3], [4, 5, 6])))
    print(list(diy_map(multi_func, [1, 2, 3], [4, 5, 6], [1, 2, 3])))

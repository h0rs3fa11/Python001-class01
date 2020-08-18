from collections.abc import Iterable


def add_func(a, b):
    # print(a, b)
    return a + b


def multi_func(a, b, c):
    return a * b * c


def map_generator(func, args):
    # print("start..")
    while True:
        try:
            zip_args = args.__next__()
            yield func(*zip_args)
        except StopIteration:
            return


def diy_map(func, *args):
    """
    @param func: 函数对象
    @param iterable: 一个或多个可迭代对象
    @return: None
    """
    # 判断参数类型
    if not hasattr(func, '__call__'):
        raise TypeError
    for arg in args:
        if not isinstance(arg, Iterable):
            raise TypeError

    # 判断function参数个数和iterable对象个数
    func_args_count = func.__code__.co_argcount
    if func_args_count != len(args):
        print("可迭代对象个数与函数参数个数不符")
        return

    result = []
    args_zip = zip(*args)
    # g = map_generator(func, args_zip.__next__())
    g = map_generator(func, args_zip)
    while True:
        try:
            result.append(next(g))
        except StopIteration:
            break
    return result


if __name__ == '__main__':
    print(list(diy_map(add_func, [1, 2, 3], [4, 5, 6])))
    print(list(diy_map(multi_func, [1, 2, 3], [4, 5, 6], [1, 2, 3])))

import time


def timer(func, *args, **kw):
    def decorator(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        end_time = time.time()
        print(f"函数 {func.__name__}运行时间{end_time - start_time}")
        return result
    return decorator


@timer
def add_test(a, b):
    return a + b


if __name__ == '__main__':
    print(add_test(1, 2))

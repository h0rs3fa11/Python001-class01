import time
import functools

def timer(func):
    @functools.wraps(func)
    def decorator(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        end_time = time.time()
        print(f"函数 {func.__name__}运行时间{end_time - start_time}")
        return result
    return decorator


@timer
def add_test(a, b):
    print(f"function name is {add_test.__name__}")
    return a + b


if __name__ == '__main__':
    print(add_test(1, 2))

from functools import wraps
import time

def timeit(func: callable):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'{func.__name__}{args} took {total_time:.4f}s')
        return result
    return timeit_wrapper

def f2lines_nostrip(fname) -> list[str]:
    return open(fname, 'r').readlines()

def f2lines(fname) -> list[str]:
    return list(map(lambda l: l.strip(), open(fname, 'r').readlines()))

def s2ns(s: str) -> list[int]:
    return list(map(int, s.split()))

def xor(b1, b2):
    return (not b2 and b1) or (not b1 and b2)

def s2is(s: str, sep: str) -> list[int]:
    return list(map(lambda x : int(x.strip()), s.split(sep)))

def idx(os: list, o) -> int:
    return os.index(o) if o in os else -1

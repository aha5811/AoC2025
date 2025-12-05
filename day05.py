import utils
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day05_test.txt')
finput = os.path.join(dir_, 'day05_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    ranges = []
    for l in utils.f2lines(fname):
        if '-' in l:
            ranges.append(tuple(map(int, l.split('-'))))
        elif (len(l) > 0 and
              is_in(int(l), ranges)):
            res += 1
    return res

def is_in(n, ranges):
    for r in ranges:
        if r[0] <= n <= r[1]:
            return True
    return False

def do1():
    assert 3 == part1(ftest)
    assert 694 == part1(finput)

@utils.timeit
def part2naive(fname: str) -> int:
    ids = set()
    for l in utils.f2lines(fname):
        if '-' in l:
            r = tuple(map(int, l.split('-')))
            for n in range(r[0], r[1] + 1):
                ids.add(n)
    return len(ids)

class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

@utils.timeit
def part2(fname: str) -> int:
    ranges = list(
        map(lambda t: Range(t[0], t[1]),
            map(lambda l: tuple(map(int, l.split('-'))),
                filter(lambda l: '-' in l,
                       utils.f2lines(fname)))))
    # merge ranges
    while True:
        merged = None
        for r1 in ranges:
            for r2 in ranges:
                if (r1 == r2 or                                 # same
                    r1.start > r2.end or r1.end < r2.start):    # disjunct
                    continue
                r2.start = min(r1.start, r2.start)
                r2.end = max(r1.end, r2.end)
                merged = r1
                break
            if merged:
                break
        if merged:
            ranges.remove(merged)
        else:
            break
    return sum(map(lambda r: r.end - r.start + 1, ranges))

def do2():
    assert 14 == part2naive(ftest)
    assert 14 == part2(ftest)
    assert 352716206375547 == part2(finput)

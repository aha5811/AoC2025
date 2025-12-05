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
        if len(l) > 0:
            if '-' in l:
                ranges.append(list(map(int, l.split('-'))))
            else:
                if is_in(int(l), ranges):
                    res += 1
    return res

def is_in(id_, ranges):
    for r in ranges:
        if r[0] <= id_ <= r[1]:
            return True
    return False

def do1():
    assert 3 == part1(ftest)
    assert 694 == part1(finput)

@utils.timeit
def part2naive(fname: str) -> int:
    ids = set()
    for l in utils.f2lines(fname):
        if len(l) > 0:
            if '-' in l:
                range_ = list(map(int, l.split('-')))
                for n in range(range_[0], range_[1] + 1):
                    ids.add(n)
    return len(ids)

@utils.timeit
def part2proper(fname: str) -> int:
    ranges = []
    for l in utils.f2lines(fname):
        if len(l) > 0:
            if '-' in l:
                ranges.append(list(map(int, l.split('-'))))

    # TODO
    # merge ranges
    # result is sum of ranges lengths

    return -1


def do2():
    assert 14 == part2naive(ftest)
    assert 0 == part2proper(finput)

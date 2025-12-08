import utils
import os.path
from functools import reduce

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day06_test.txt')
finput = os.path.join(dir_, 'day06_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    number_buckets = []
    for l in utils.f2lines(fname):
        ll = l.strip()
        if ll[0] in '*+':
            for i, s in enumerate(ll.split()):
                res += compute(s, number_buckets[i])
        else:
            for i, n in enumerate(utils.s2ns(ll)):
                if len(number_buckets) < i + 1: number_buckets.append([]) # first line
                number_buckets[i].append(n)
    return res

def compute(op, numbers) -> int:
    if op == '*':
        return reduce(lambda a, b: a * b, numbers, 1)
    else:
        return sum(numbers)

def do1():
    assert 4277556 == part1(ftest)
    assert 3261038365331 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    # python removes trailing whitespaces(?) so we have to compensate
    lines = utils.f2lines_nostrip(fname)
    ll = max(map(len, lines)) # find longest line
    columns = [[] for _ in range(ll)]
    for l in lines:
        for i, char in enumerate(l + ' ' * (ll - len(l))): # add whitespace so line is as long as the longest line
            columns[i].append(None if char in ' \n' else char)
    res = 0
    blob = [] #
    for column in columns:
        if is_empty(column):
            res += compute_blob(blob)
            blob = []
        else:
            blob.append(column)
    return res

def is_empty(l: list[str]) -> bool:
    return len(list(s_filter(l))) == 0

def s_filter(l: list[str]) -> filter:
    return filter(lambda s: s, l)

def compute_blob(blob) -> int:
    l = len(blob[0]) - 1
    ns = []
    for b in blob:
        ns.append(int(reduce(lambda x, y: x + y, s_filter(b[:l]), '')))
    return compute(blob[0][l], ns)

def do2():
    assert 3263827 == part2(ftest)
    assert 8342588849093 == part2(finput)

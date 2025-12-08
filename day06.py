import re
from functools import reduce

import utils
import os.path

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

# python removes empty spaces at end of lines so I had to add _ like
# "123 328  51 64" -> "123 328  51 64_"
# _s are removed in (char if char not in '_ \n' else '')

ftest2 = os.path.join(dir_, 'day06_test2.txt')

@utils.timeit
def part2(fname: str) -> int:
    res = 0

    columns = []
    for l in utils.f2lines_nostrip(fname):
        for i, char in enumerate(l):
            if len(columns) < i + 1: columns.append([])
            columns[i].append(char if char not in '_ \n' else '')

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
    return filter(lambda s: s != '', l)

def compute_blob(blob) -> int:
    l = len(blob[0]) - 1
    ns = []
    for b in blob:
        ns.append(int(reduce(lambda x, y: x + y, s_filter(b[:l]), '')))
    return compute(blob[0][l], ns)

def do2():
    assert 3263827 == part2(ftest2)
    assert 8342588849093 == part2(finput)

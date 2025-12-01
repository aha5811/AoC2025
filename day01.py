import utils
import os.path
import math
dir = os.path.dirname(__file__)
ftest = os.path.join(dir, 'day01_test.txt')
finput = os.path.join(dir, 'day01_input.txt')

def to_m_n(s):
    m = -1 if s[0] == 'L' else +1
    n = int(s[1:])
    return m, n

@utils.timeit
def part1(fname):
    res = 0
    pos = 50
    for s in utils.f2lines(fname):
        m, n = to_m_n(s)
        pos = (pos + 100 + m * n) % 100
        if pos == 0:
            res += 1
    return res

def do1():
    assert 3 == part1(ftest)
    assert 1089 == part1(finput)

@utils.timeit
def part2(fname):
    res = 0
    pos = 50
    for s in utils.f2lines(fname):
        m, n = to_m_n(s)
        res += math.floor(n / 100) # multiple turns
        pos_next = pos + m * (n % 100)
        if pos_next > 100 or pos_next < 0 < pos: res += 1
        pos = pos_next % 100
        if pos == 0: res += 1
    return res

def do2():
    assert 6 == part2(ftest)
    assert 6530 == part2(finput)

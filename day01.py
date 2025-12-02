import utils
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day01_test.txt')
finput = os.path.join(dir_, 'day01_input.txt')

start_pos = 50

def to_m_n(s: str) -> tuple[int, int]:
    # "Lxxx" or "Rxxx"
    m = -1 if s[0] == 'L' else +1 #R
    n = int(s[1:])
    return m, n

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    pos = start_pos
    for s in utils.f2lines(fname):
        m, n = to_m_n(s)
        pos = (pos + m * n) % 100
        if pos == 0:
            res += 1
    return res

def do1():
    assert 3 == part1(ftest)
    assert 1089 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    res = 0
    pos = start_pos
    for s in utils.f2lines(fname):
        m, n = to_m_n(s)
        res += n // 100 # multiple turns
        n %= 100
        pos_next = pos + m * n
        if pos_next > 100 or pos_next < 0 < pos: # went over 0
            res += 1
        pos = pos_next % 100
        if pos == 0:
            res += 1
    return res

def do2():
    assert 6 == part2(ftest)
    assert 6530 == part2(finput)

import utils
from maps import Map, Pos, Dirs
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day04_test.txt')
finput = os.path.join(dir_, 'day04_input.txt')

rop = '@' # roll of paper
rem = 'x' # removed

@utils.timeit
def part1(fname: str) -> int:
    m = Map(fname)
    return sum(1 for p in m.find_all(rop) if is_accessible(m, p))

def is_accessible(m: Map, p: Pos) -> bool:
    return sum(1 for d in Dirs if m.get(p.x + d.x, p.y + d.y) == rop) < 4

def do1():
    assert 13 == part1(ftest)
    assert 1523 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    m = Map(fname)
    ps = set(m.find_all(rop))
    ps_len_start = len(ps)
    while True:
        remove = set()
        for p in ps:
            if is_accessible(m, p):
                m.set(p.x, p.y, rem)
                remove.add(p)
        if not remove:
            break
        ps -= remove
    return ps_len_start - len(ps)

def do2():
    assert 43 == part2(ftest)
    assert 9290 == part2(finput) # 0.4s

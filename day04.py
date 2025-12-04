import utils
import maps
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day04_test.txt')
finput = os.path.join(dir_, 'day04_input.txt')

rop = '@' # roll of paper
rem = 'x' # removed

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    m = maps.Map(fname)
    for p in m.find_all(rop):
        if accessible(m, p):
            res += 1
    return res

def accessible(m: maps.Map, p: maps.Pos) -> bool:
    res = 0
    for d in maps.ds: # all 8
        if m.get(p.x + d[0], p.y + d[1]) == rop:
            res += 1
    return res < 4

def do1():
    assert 13 == part1(ftest)
    assert 1523 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    m = maps.Map(fname)
    ps = set(m.find_all(rop))
    res = 0
    while True:
        remove = set()
        for p in ps:
            if accessible(m, p):
                m.set(p.x, p.y, rem)
                res += 1
                remove.add(p)
        if not remove:
            break
        ps -= remove
    return res

def do2():
    assert 43 == part2(ftest)
    assert 9290 == part2(finput) # 0.4s

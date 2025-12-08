import utils
from maps import Map, Pos
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day07_test.txt')
finput = os.path.join(dir_, 'day07_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    m = Map(fname)
    ts = m.find_all('S')
    while True:
        next_y = ts[0].y + 1
        if m.get(0, next_y) is None: break
        ts_next = []
        for t in ts:
            if m.get(t.x, next_y) == '^':
                res += 1
                add(ts_next, t.x - 1, next_y)
                add(ts_next, t.x + 1, next_y)
            else:
                add(ts_next, t.x, next_y)
        ts = ts_next
    return res

def add(ps: list[Pos], x: int, y: int):
    p = Pos(x, y)
    if p not in ps:
        ps.append(p)

def do1():
    assert 21 == part1(ftest)
    assert 1590 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    m = Map(fname)
    ts = [(m.find_all('S')[0], 1)]
    while True:
        next_y = ts[0][0].y + 1
        if m.get(0, next_y) is None: break
        ts_next = []
        for t in ts:
            (p, cnt) = t
            if m.get(p.x, next_y) == '^':
                add2(ts_next, p.x - 1, next_y, cnt)
                add2(ts_next, p.x + 1, next_y, cnt)
            else:
                add2(ts_next, p.x, next_y, cnt)
        ts = ts_next
    return sum(map(lambda t: t[1], ts))

def add2(ts: list[tuple[Pos, int]], x: int, y: int, cnt: int):
    p = Pos(x, y)
    found = False
    for i in range(len(ts)):
        t = ts[i]
        if t[0] == p:
            ts[i] = (p, t[1] + cnt)
            found = True
    if not found:
        ts.append((p, cnt))

def do2():
    assert 40 == part2(ftest)
    assert 20571740188555 == part2(finput)

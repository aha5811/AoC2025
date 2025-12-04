import utils
import maps
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day04_test.txt')
finput = os.path.join(dir_, 'day04_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    m = maps.Map(fname)
    for p in m.find_all('@'):
        cnt = 0
        for d in maps.ds:
            if m.get(p.x + d[0], p.y + d[1]) == '@':
                cnt += 1
        if cnt < 4:
            res += 1
    return res

def do1():
    assert 13 == part1(ftest)
    assert 1523 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    m = maps.Map(fname)
    while True:
        ps = []
        for p in m.find_all('@'):
            cnt = 0
            for d in maps.ds:
                if m.get(p.x + d[0], p.y + d[1]) == '@':
                    cnt += 1
            if cnt < 4:
                ps.append(p)
        if len(ps) == 0:
            break
        for p in ps:
            m.set(p.x, p.y, 'x')
    return len(m.find_all('x'))

def do2():
    assert 43 == part2(ftest)
    assert 9290 == part2(finput) # 1s

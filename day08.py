import utils
import os.path
from math import sqrt, pow
from functools import reduce, cmp_to_key
import time

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day08_test.txt')
finput = os.path.join(dir_, 'day08_input.txt')

@utils.timeit
def part1(fname: str, cc: int) -> int:

    jbs = []
    circuits = []
    for l in utils.f2lines(fname):
        jb = tuple(utils.s2is(l, ','))
        jbs.append(jb)
        circuits.append([jb])

    dist_2_xy = []
    for x, jb1 in enumerate(jbs):
        for y, jb2 in enumerate(jbs):
            if y > x:
                d = sqrt(pow(jb1[0] - jb2[0], 2) + pow(jb1[1] - jb2[1], 2) + pow(jb1[2] - jb2[2], 2))
                dist_2_xy.append((d, x, y))
    dist_2_xy.sort(key=cmp_to_key(lambda dxy1, dxy2: dxy1[0] - dxy2[0]))

    c = 0
    for dxy in dist_2_xy:
        jb1, jb2 = jbs[dxy[1]], jbs[dxy[2]]
        c1 = get_circuit(jb1, circuits)
        c2 = get_circuit(jb2, circuits)
        if c1 != c2:
            merge(c1, c2)
            circuits.remove(c2)
        c += 1
        if c == cc:
            break

    cls = list(map(len, circuits))
    cls.sort(reverse=True)
    res = reduce(lambda a, b: a * b, cls[:3], 1)
    return res

def merge(c1, c2):
    for c in c2:
        if not c in c1:
            c1.append(c)

def get_circuit(e, circuits) -> list:
    for c in circuits:
        if e in c:
            return c
    return [] # won't happen

def add_connection(e1, e2, circuits):
    added = False
    for c in circuits:
        if e1 in c:
            c.append(e2)
            added = True
        elif e2 in c:
            c.append(e1)
            added = True
        if added:
            break
    if not added:
        circuits.append([e1, e2])

def do1():
    assert 40 == part1(ftest, 10)
    assert 122430 == part1(finput, 1000)

@utils.timeit
def part2(fname: str) -> int:
    res = 0
    # TODO
    return res

def do2():
    assert 25272 == part2(ftest)
    assert 0 == part2(finput)

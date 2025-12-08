import utils
import os.path
from math import sqrt, pow
from functools import reduce, cmp_to_key

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day08_test.txt')
finput = os.path.join(dir_, 'day08_input.txt')

@utils.timeit
def part1(fname: str, cc: int) -> int:
    boxes, dxys, circuits = preprocess(fname)
    for dxy in dxys[:cc]:
        b1, b2 = boxes[dxy[1]], boxes[dxy[2]]
        p1, c1 = get_circuit(b1, circuits)
        p2, c2 = get_circuit(b2, circuits)
        if p1 != p2: # merge c2 into c1
            c1 |= c2
            circuits.pop(p2)
    return reduce(lambda a, b: a * b,
                  sorted(map(len, circuits), reverse=True)[:3], # len dec three
                  1)

def preprocess(fname):
    """
    returns
        list of box tupels (x, y, z)
        sorted list of tupels (distance, index of box1, index of box2)
        initial list of circuits (= sets of length 1)
    """
    boxes = list(map(lambda l: tuple(utils.s2is(l, ',')), utils.f2lines(fname)))
    dxys = []
    for x, b1 in enumerate(boxes):
        for y, b2 in enumerate(boxes):
            if y > x:
                d = sqrt(pow(b1[0] - b2[0], 2) + pow(b1[1] - b2[1], 2) + pow(b1[2] - b2[2], 2))
                dxys.append((d, x, y))
    dxys.sort(key=(lambda t: t[0]))
    return boxes, dxys, list(map(lambda b: {b}, boxes))

def get_circuit(b, circuits):
    """
    returns
        index of found circuit
        found circuit
    """
    for n, c in enumerate(circuits):
        if b in c:
            return n, c
    return None # won't happen

def do1():
    assert 40 == part1(ftest, 10)
    assert 122430 == part1(finput, 1000)

@utils.timeit
def part2(fname: str) -> int:
    boxes, dxys, circuits = preprocess(fname)
    for dxy in dxys:
        b1, b2 = boxes[dxy[1]], boxes[dxy[2]]
        p1, c1 = get_circuit(b1, circuits)
        p2, c2 = get_circuit(b2, circuits)
        if p1 != p2:
            c1 |= c2
            circuits.pop(p2)
            if len(circuits) == 1:
                return b1[0] * b2[0]
    return 0 # won't happen

def do2():
    assert 25272 == part2(ftest)
    assert 8135565324 == part2(finput)

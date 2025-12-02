import utils
import os.path
from math import floor
from utils import f2lines

dir = os.path.dirname(__file__)
ftest = os.path.join(dir, 'day02_test.txt')
finput = os.path.join(dir, 'day02_input.txt')

@utils.timeit
def part1(fname):
    return part(fname, is_invalid_1)

def part(fname, is_invalid):
    res = 0
    for r in f2lines(fname)[0].split(','):
        s, e = r.split('-')
        for id in range(int(s), int(e) + 1):
            if is_invalid(id):
                res += id
    return res

def is_invalid_1(id):
    s = str(id)
    l = len(s)
    if l % 2 == 0:
        split = int(l / 2)
        return s[:split] == s[split:]
    return False

def do1():
    assert 1227775554 == part1(ftest)
    assert 12850231731 == part1(finput) # 0.7s

@utils.timeit
def part2(fname):
    return part(fname, is_invalid_2)

def is_invalid_2(id):
    s = str(id)
    l = len(s)
    for pl in range(1, floor(l / 2) + 1):
        if l % pl == 0:
            all_eq = True
            first = s[:pl]
            for i in range(1, int(l / pl)):
                if first != s[i * pl : (i + 1) * pl]:
                    all_eq = False
                    break
            if all_eq:
                return True
    return False

def do2():
    assert 4174379265 == part2(ftest)
    assert 24774350322 == part2(finput) # 2.5s

import utils
import os.path
from textwrap import wrap
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
    for pl in range(floor(l / 2), 0, -1):
        if l % pl == 0:
            # this could be much faster
            parts = wrap(s, pl)
            if parts.count(parts[0]) == len(parts): # all the same
                return True
    return False

def do2():
    assert 4174379265 == part2(ftest)
    assert 24774350322 == part2(finput) # 36.5s

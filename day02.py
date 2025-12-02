import utils
import os.path
import typing

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day02_test.txt')
finput = os.path.join(dir_, 'day02_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    return part(fname, twice_repeat)

def part(fname: str, is_invalid: typing.Callable[[str], bool]) -> int:
    res = 0
    # a-b,c-d,...
    for r in utils.f2lines(fname)[0].split(','):
        start, end = r.split('-')
        for id_ in range(int(start), int(end) + 1):
            if is_invalid(str(id_)):
                res += id_
    return res

def twice_repeat(id_: str) -> bool:
    l = len(id_)
    if l % 2 == 0:
        half = l // 2
        return id_[:half] == id_[half:]
    return False

def do1():
    assert 1227775554 == part1(ftest)
    assert 12850231731 == part1(finput) # 0.7s

@utils.timeit
def part2(fname: str) -> int:
    return part(fname, n_repeat)

def n_repeat(id_: str) -> bool:
    l = len(id_)
    for part_length in range(1, l // 2 + 1):
        if l % part_length == 0:
            if all_eq(id_, l, part_length):
                return True
    return False

def all_eq(id_: str, l: int, part_length: int) -> bool:
    first_part = id_[:part_length]
    for n in range(1, l // part_length):
        if first_part != id_[n * part_length : (n + 1) * part_length]:
            return False
    return True

# ----------------------------

import re

@utils.timeit
def part2_regex(fname: str) -> int:
    return part(fname, n_repeat_regex)

# from https://www.reddit.com/r/adventofcode/comments/1pc2rcn/comment/nrw5xy5/

n_repeat_regex_re = re.compile(r"^(\d+)\1+$")

def n_repeat_regex(id_: str) -> bool:
    return n_repeat_regex_re.match(id_) is not None

# ----------------------------

def do2():
    assert 4174379265 == part2(ftest)
    assert 24774350322 == part2(finput) # 2.6s
    assert 24774350322 == part2_regex(finput)  # 1.2s


import utils
import os.path
import re

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day12_test.txt')
finput = os.path.join(dir_, 'day12_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0

    shape_dict = {}
    n: int = -1
    shl = []
    for l in utils.f2lines(fname):
        if re.match("^\\d:$", l):
            n = int(l[0])
        elif re.match("^[#.]+$", l):
            shl.append(l)
        elif l == '':
            shape_dict[n] = gen_variants(shl)
            shl = []
        elif re.match("^\\d+x\\d+:.*$", l):
            dims, rest = l.split(':')
            (w, h) = tuple(map(int, dims.split('x')))
            area = [[False for _ in range(h)] for _ in range(w)]
            shape_amnts = []
            for n, amnt in enumerate(utils.s2ns(rest)):
                shape_amnts += [n] * amnt
            res += solve(shape_dict, shape_amnts, area)

    return res

def gen_variants(lines: list[str]):
    variants = []
    v = [[c == '#' for c in l] for l in lines]
    add_variant(v, variants)
    for _ in range(4):
        v = rotate_right(v)
        add_variant(v, variants)
    v = flip_h(v)
    add_variant(v, variants)
    for _ in range(4):
        v = rotate_right(v)
        add_variant(v, variants)
    return variants

def add_variant(shape, shapes):
    if shape not in shapes:
        shapes.append(shape)

def rotate_right(shape: list[list[bool]]) -> list[list[bool]]:
    ret = [[False for _ in range(3)] for _ in range(3)]
    ret[1][1] = shape[1][1]
    outers = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    """
    c1 s2 c2
    s1 x  s
    c  s  c
    """
    for n, o in enumerate(outers):
        prev = outers[n - 2] # s1 -> s2, c1 -> c2
        ret[o[0]][o[1]] = shape[prev[0]][prev[1]]
    return ret

def flip_h(shape: list[list]) -> list[list]:
    return list(map(lambda l: list(reversed(l)), shape))

def solve(
        shape_dict: dict[int, list[list[list[bool]]]],
        shape_amnts: list[int],
        area: list[list[bool]]) -> bool:

    # - iterate over the shape numbers
    # -- iterate over possible shapes in dict
    # --- iterate over x of area
    # ---- iterate over y of area
    # ----- if fits: place + recursion

    return False

def fits(shape, x, y, area) -> bool:
    for xx in range(3):
        for yy in range(3):
            if shape[xx][yy] and area[x + xx][y + yy]:
                return False
    return True

def place(shape, x, y, area):
    area_next = area.copy()
    for xx in range(3):
        for yy in range(3):
            area[x + xx][y + yy] = shape[xx][yy]
    return area_next

def do1():
    assert 2 == part1(ftest)
    assert 0 == part1(finput)

do1()

@utils.timeit
def part2(fname: str) -> int:
    res = 0
    # TODO
    return res

def do2():
    assert 0 == part2(ftest)
    assert 0 == part2(finput)

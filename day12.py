
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
            shapes2fit = []
            for n, amnt in enumerate(utils.s2ns(rest)):
                shapes2fit += [n] * amnt
            is_solvable = solve(shape_dict, shapes2fit, area)
            print(l, is_solvable)
            if is_solvable:
                res += 1

    print(res)
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

# - iterate over the shape numbers
# -- iterate over possible shape variants in dict
# --- iterate over x of area
# ---- iterate over y of area
# ----- if fits: place + recursion

def solve(
        shape_dict: dict[int, list[list[list[bool]]]],
        shapes2fit: list[int],
        area: list[list[bool]]) -> bool:
    if len(shapes2fit) == 0:
        return True
    for p, n in enumerate(shapes2fit):
        if solve_s2f(shape_dict, shapes2fit, p, n, area):
            return True
    return False

def solve_s2f(shape_dict, shapes2fit: list[int], p: int, n: int, area: list[list[bool]]) -> bool:
    for sh in shape_dict[n]:
        if solve_sh(shape_dict, shapes2fit, p, sh, area):
            return True
    return False

def solve_sh(shape_dict, shapes2fit: list[int], p: int, shape: list[list[bool]], area: list[list[bool]]) -> bool:
    for x in range(len(area)):
        if solve_x(shape_dict, shapes2fit, p, shape, area, x):
            return True
    return False

def solve_x(shape_dict, shapes2fit: list[int], p:int, shape: list[list[bool]], area: list[list[bool]], x: int) -> bool:
    for y in range(len(area[0])):
        if fits(shape, x, y, area):
            return solve(shape_dict, dec_shape(shapes2fit, p), place(shape, x, y, area))
    return False

def fits(shape: list[list[bool]], x: int, y: int, area: list[list[bool]]) -> bool:
    if x + 2 >= len(area) or y + 2 >= len(area[0]):
        return False
    for xx in range(3):
        for yy in range(3):
             if shape[xx][yy] and area[x + xx][y + yy]:
                return False
    return True

def place(shape: list[list[bool]], x: int, y: int, area: list[list[bool]]) -> list[list[bool]]:
    print('placing', shape, 'at', x, y)
    area_next = area.copy()
    for xx in range(3):
        for yy in range(3):
            area[x + xx][y + yy] = shape[xx][yy]
    return area_next

def dec_shape(shapes2fit: list[int], p: int) -> list[int]:
    ret = shapes2fit.copy()
    ret.pop(p)
    return ret

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

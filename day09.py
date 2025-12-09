
import utils
from maps import Pos
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day09_test.txt')
finput = os.path.join(dir_, 'day09_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    points = list(map(lambda l: Pos(*utils.s2is(l, ',')), utils.f2lines(fname)))
    a_max = 0
    for n1, p1 in enumerate(points):
        for n2, p2 in enumerate(points):
            if n2 > n1:
                a_max = max(a_max, a(p1, p2))
    return a_max

def a(p1: Pos, p2: Pos) -> int:
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)

def do1():
    assert 50 == part1(ftest)
    assert 4739623064 == part1(finput)

from shapely import Point, Polygon, box

@utils.timeit
def part2(fname: str):
    points = list(map(lambda l: Point(*utils.s2is(l, ',')), utils.f2lines(fname)))
    hull_points = points + [points[0]]
    hull = Polygon(hull_points) # close
    a_max = 0
    b_max = None
    for n1, p1 in enumerate(points):
        for n2, p2 in enumerate(points):
            if n1 <= n2: continue
            a_ = aa(p1, p2)
            if a_ > a_max:
                b = box(min(p1.x, p2.x), min(p1.y, p2.y), max(p1.x, p2.x), max(p1.y, p2.y))
                if b.within(hull):
                    a_max = a_
                    b_max = b
    # plot(hull_points, list(map(lambda t: Point(*t), b_max.boundary.coords)))
    return a_max

def aa(p1: Point, p2: Point) -> int:
    return int((abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1))

def do2():
    assert 24 == part2(ftest)
    assert 1654141440 == part2(finput)

# ----------------------

from matplotlib import pyplot
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def plot(hull_points: list[Point], box_points: list[Point]):
    # hull_points
    vertices = list(map(lambda p: (p.x, p.y), hull_points))
    codes = [Path.MOVETO] + [Path.LINETO] * (len(hull_points) - 1)
    # box_points
    vertices += list(map(lambda p: (p.x, p.y), box_points))
    codes += [Path.MOVETO] + [Path.LINETO] * (len(box_points) - 1)
    #
    path = Path(vertices, codes)
    path_patch = PathPatch(path, facecolor='mistyrose', edgecolor='darkgreen')
    fig, ax = pyplot.subplots()
    ax.add_patch(path_patch)
    ax.set_title(f'{len(hull_points)} points')
    ax.autoscale_view()
    pyplot.show()

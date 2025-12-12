import utils
import os.path

dir_ = os.path.dirname(__file__)
ftest1 = os.path.join(dir_, 'day11_test_1.txt')
ftest2 = os.path.join(dir_, 'day11_test_2.txt')
finput = os.path.join(dir_, 'day11_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    out, start = 'out', 'you'
    nodes = read_nodes(fname, out)
    return cnt_paths(nodes[start], [], nodes[out])

def read_nodes(fname: str, dst: str) -> dict[str, Node]:
    nodes = {}
    lines = utils.f2lines(fname)
    for l in lines:
        name = l.split(':')[0]
        nodes[name] = Node(name)
    nodes[dst] = Node(dst)
    for l in lines:
        name, others = l.split(':')
        for n in others.split():
            nodes[name].add_child(nodes[n])
    return nodes

def cnt_paths(n: Node, path: list[Node], target: Node) -> int:
    if n == target:
        return 1
    if n in path: # cycle
        return 0
    ret = 0
    for c in n.children:
        ret += cnt_paths(c, path + [n], target)
    return ret

class Node:
    def __init__(self, name: str):
        self.name = name
        self.children: list[Node] = []

    def add_child(self, n: Node):
        self.children.append(n)

    def __str__(self):
        return f'N{self.name}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


def do1():
    assert 5 == part1(ftest1)
    assert 428 == part1(finput)

# ----------------------------------------------- v1

@utils.timeit
def part2_v1(fname: str) -> int:
    # get all paths, count all with must have nodes
    out, start = 'out', 'svr'
    nodes = read_nodes(fname, out)
    must_contain = [nodes['dac'], nodes['fft']]
    res = 0
    for p in get_paths(nodes[start], [], nodes[out]):
        if all(m in p for m in must_contain):
            res += 1
    print(res)
    return res

def get_paths(n: Node, path: list[Node], target: Node) -> list[list[Node]]:
    if n == target:
        return [path]
    if n in path:
        return []
    ret = []
    for c in n.children:
        ret += get_paths(c, path + [n], target)
    return ret

# ----------------------------------------------- v2

@utils.timeit
def part2_v2(fname: str) -> int:
    # cnt all paths, only cnt paths with must have nodes
    out, start = 'out', 'svr'
    nodes = read_nodes(fname, out)
    res = cnt_paths_v2(nodes[start], [], nodes[out], [nodes['dac'], nodes['fft']])
    print(res)
    return res

def cnt_paths_v2(n: Node, path: list[Node], target: Node, must_contain: list[Node]) -> int:
    if n == target:
        return 1 if all(m in path for m in must_contain) else 0
    if n in path:
        return 0
    ret = 0
    for c in n.children:
        ret += cnt_paths_v2(c, path + [n], target, must_contain)
    return ret

# ----------------------------------------------- v3

@utils.timeit
def part2_v3(fname: str) -> int:
    out, start = 'out', 'svr'
    nodes = read_nodes(fname, out)
    n_start, n_must1, n_must2, n_end = nodes[start], nodes['dac'], nodes['fft'], nodes[out]
    # split in 3 graphs svr -> must1 -> must2 -> out
    p12 = cnt_paths(n_must1, [], n_must2)
    p21 = cnt_paths(n_must2, [], n_must1)
    if p12 > p21:
        res = cnt_paths(n_start, [], n_must1) * p12 * cnt_paths(n_must2, [], n_end)
    else:
        res = cnt_paths(n_start, [], n_must2) * p21 * cnt_paths(n_must1, [], n_end)
    print(res)
    return res

# ----------------------------------------------- v4

@utils.timeit
def part2_v4(fname: str) -> int:
    p2cs: dict[str, list[str]] = {} # parent 2 children
    c2ps: dict[str, list[str]] = {} # child 2 parents
    for l in utils.f2lines(fname):
        n, r = l.split(':')
        p2cs[n] = r.split()
        for cn in p2cs[n]:
            c2ps[cn] = []
    for n in p2cs:
        for c in p2cs[n]:
            c2ps[c] += [n]

    out, start, must1, must2 = 'out', 'svr', 'dac', 'fft'

    res = 0
    cnt12 = cnt4(must1, must2, c2ps)
    if cnt12: # is dag
        res = cnt4(start, must1, c2ps) * cnt12 * cnt4(must2, out, c2ps)
    else:
        res = cnt4(start, must2, c2ps) * cnt4(must2, must1, c2ps) * cnt4(must1, out, c2ps)
    print(res)
    return res

def cnt4(start: str, target: str, c2ps: dict[str, list[str]]) -> int:
    n2pc: dict[str,int] = {target: 1} # name to path count
    queue = [target]
    while True:
        q_next = []
        for n in queue:
            if n in c2ps:
                for p in c2ps[n]:
                    n2pc[p] = n2pc[n] + (n2pc[p] if p in n2pc else 0)
                    if p not in q_next: q_next.append(p)
        queue = q_next
        if start in queue:
            return n2pc[start]
        if len(queue) == 0:
            break
    return 0

# -----------------------------------------------

def do2():
    assert 2 == part2_v1(ftest2)
    assert 2 == part2_v2(ftest2)
    assert 2 == part2_v3(ftest2)
    assert 2 == part2_v4(ftest2)
    assert 2212708605659763 == part2_v4(finput) # too high

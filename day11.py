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
    if n in path:
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

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


def do1():
    assert 5 == part1(ftest1)
    assert 428 == part1(finput)

@utils.timeit
def part2_v1(fname: str) -> int:
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

@utils.timeit
def part2(fname: str) -> int:
    out, start = 'out', 'svr'
    nodes = read_nodes(fname, out)
    res = cnt_paths2(nodes[start], [], nodes[out], [nodes['dac'], nodes['fft']])
    print(res)
    return res

def cnt_paths2(n: Node, path: list[Node], target: Node, must_contain: list[Node]) -> int:
    if n == target:
        return 1 if all(m in path for m in must_contain) else 0
    if n in path:
        return 0
    ret = 0
    for c in n.children:
        ret += cnt_paths2(c, path + [n], target, must_contain)
    return ret

def do2():
    assert 2 == part2(ftest2)
    assert 0 == part2(finput) # still running

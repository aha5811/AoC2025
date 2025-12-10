
import utils
import re
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day10_test.txt')
finput = os.path.join(dir_, 'day10_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    return sum(map(solve1, utils.f2lines(fname)))

def solve1(line: str) -> int:
    target = [c == '#' for c in re.search(r"\[(.*?)]", line)[1]]
    buttons = read_buttons(line)
    res = 0
    queue = [([], [False] * len(target))]
    while True:
        queue_next = []
        for (pushes, config) in queue:
            last_push = pushes[-1] if pushes else None
            for n in range(len(buttons)):
                if n != last_push:
                    config_next = push1(config, buttons, n)
                    if is_same1(config_next, target):
                        res = len(pushes) + 1
                        break
                    else:
                        queue_next.append((pushes + [n], config_next))
        if res > 0:
            # print(f'{res} ({len(queue)}) for "{line}"')
            break
        queue = queue_next
    return res

def read_buttons(line: str) -> list[tuple[int, ...]]:
    return [tuple(utils.s2is(g, ',')) for g in re.findall(r"\(([\d,]+)\)", line)]

def push1(config: list[bool], buttons: list[tuple[int, ...]], n: int) -> list[bool]:
    ret = [b for b in config]
    for p in buttons[n]:
        ret[p] = not config[p]
    return ret

def is_same1(config: list[bool], target: list[bool]) -> bool:
    for cb, tb in zip(config, target):
        if cb != tb:
            return False
    return True

def do1():
    assert 7 == part1(ftest)
    assert 507 == part1(finput) # 47s

@utils.timeit
def part2(fname: str) -> int:
    return sum(map(solve2, utils.f2lines(fname)))

def solve2(line: str) -> int:
    target = utils.s2is(re.search(r"\{(.*?)}", line)[1], ',')
    buttons = read_buttons(line)
    res = 0
    queue = [([], [0] * len(target))]
    while True:
        queue_next = []
        for (pushes, jolts) in queue:
            for n in range(len(buttons)):
                jolts_next = push2(jolts, buttons, n)
                if is_same2(jolts_next, target):
                    res = len(pushes) + 1
                    break
                elif check_end(jolts_next, target):
                    break
                else:
                    queue_next.append((pushes + [n], jolts_next))
        if res > 0:
            print(f'{res} ({len(queue)}) for "{line}"')
            break
        queue = queue_next
    return res

def check_end(jolts: list[int], target: list[int]) -> bool:
    for j, t in zip(jolts, target):
        if j > t:
            return True
    return False

def push2(jolts: list[int], buttons: list[tuple[int, ...]], n: int) -> list[int]:
    ret = [b for b in jolts]
    for p in buttons[n]:
        ret[p] = jolts[p] + 1
    return ret

def is_same2(jolts: list[int], target: list[int]) -> bool:
    for cb, tb in zip(jolts, target):
        if cb != tb:
            return False
    return True

def do2():
    assert 33 == part2(ftest) # 22s
    # assert 0 == part2(finput) # won't work with brute force

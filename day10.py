from functools import cmp_to_key

import scipy.optimize

import utils
import re
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day10_test.txt')
finput = os.path.join(dir_, 'day10_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    return sum(map(solve1b, utils.f2lines(fname)))

# 29s for input
def solve1a(line: str) -> int:
    target = [c == '#' for c in re.search(r"\[(.*?)]", line)[1]]
    buttons = read_buttons(line)
    res = 0
    queue = [([], [False] * len(target))]
    while True:
        queue_next = [] # uses two queues
        for (pushes, config) in queue:
            last_push = pushes[-1] if pushes else None
            for n in range(len(buttons)):
                if n != last_push:
                    config_next = push_button_1(config, buttons, n)
                    if config_next == target:
                        res = len(pushes) + 1
                        break
                    else:
                        queue_next.append((pushes + [n], config_next))
        if res > 0:
            # print(f'{res} ({len(queue)}) for "{line}"')
            break
        queue = queue_next
    return res

# 107s for input
def solve1b(line: str) -> int:
    target = [c == '#' for c in re.search(r"\[(.*?)]", line)[1]]
    buttons = read_buttons(line)
    res = 0
    queue = [([], [False] * len(target))]
    while True:
        pushes, config = queue.pop(0)
        last_push = pushes[-1] if pushes else None
        for n in range(len(buttons)):
            if n != last_push:
                config_next = push_button_1(config, buttons[n])
                if config_next == target:
                    res = len(pushes) + 1
                    break
                else:
                    queue.append((pushes + [n], config_next)) # uses one queue
        if res > 0:
            # print(f'{res} ({len(queue)}) for "{line}"')
            break
    return res

def push_button_1(config: list[bool], button: tuple[int, ...]) -> list[bool]:
    ret = config.copy()
    for p in button:
        ret[p] = not config[p]
    return ret

def read_buttons(line: str) -> list[tuple[int, ...]]:
    return [tuple(utils.s2is(g, ',')) for g in re.findall(r"\(([\\d,]+)\)", line)]

def do1():
    assert 7 == part1(ftest)
    # assert 507 == part1(finput)

@utils.timeit
def part2(fname: str) -> int:
    return sum(map(solve2_scipy, utils.f2lines(fname)))

# ----------------------------------------

# different solve2_ functions that are too slow for input

# 22s for test
def solve2_breadth_first(line: str) -> int:
    target = read_jolts(line)
    buttons = read_buttons(line)
    res = 0
    queue = [([], [0] * len(target))]
    while True:
        queue_next = []
        for (pushes, jolts) in queue:
            for n in range(len(buttons)):
                jolts_next = push_button_2(jolts, buttons[n])
                if jolts_next == target:
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

def read_jolts(line: str) -> list[int]:
    return utils.s2is(re.search(r"\{(.*?)}", line)[1], ',')

# 532s for test without button sorting

# 512s for test with button sorting according to config
"""
    b2score = {}
    for b in buttons:
        b2score[b] = sum(map(lambda n: target[n], b))
    buttons.sort(key=cmp_to_key(lambda x,y: b2score[x] - b2score[y]),reverse=True)
"""
#  -> {5,1,1} -> buttons with 0 as element count more

# 527s for test with button sorting according to button len
# buttons.sort(key=len,reverse=True)

# 664s for test with button sorting in each recursion

def solve2_depth_first(line: str) -> int:
    target = read_jolts(line)
    buttons = read_buttons(line)
    return _solve_rec([0] * len(target), target, buttons, 0)

def _solve_rec(jolts, target, buttons, push_cnt: int) -> int|None:
    if jolts == target:
        return push_cnt
    elif check_end(jolts, target):
        return None
    else:
        ss = []

        # sort greedy
        buttons_sort = [b for b in buttons]
        diff = [t - j for t, j in zip(target, jolts)]
        max_, max_n = 0, 0
        for n, d in enumerate(diff):
            if d > max_:
                max_ = d
                max_n = n
        def rank(b) -> int:
            return (10 if max_n in b else 0) + len(b)
        buttons_sort.sort(key=rank,reverse=True)

        for n in range(len(buttons_sort)):
            ret = _solve_rec(push_button_2(jolts, buttons_sort[n]), target, buttons_sort, push_cnt + 1)
            if ret:
                ss.append(ret)
        return None if len(ss) == 0 else min(ss)

def check_end(jolts: list[int], target: list[int]) -> bool:
    for j, t in zip(jolts, target):
        if j > t:
            return True
    return False

def push_button_2(jolts: list[int], button: tuple[int, ...]) -> list[int]:
    ret = [j for j in jolts]
    for p in button:
        ret[p] = ret[p] + 1
    return ret

# ----------------------------------------

# solving by solving linear equations
# from https://www.reddit.com/r/adventofcode/comments/1pity70/comment/ntb48ll/

def solve2_scipy(line: str) -> int:
    target = read_jolts(line)
    buttons = read_buttons(line)

    A = [[0 for _ in range(len(buttons))] for _ in range(len(target))]
    for bn, b in enumerate(buttons):
        for p in b:
            A[p][bn] = 1

    c = [1 for _ in range(len(buttons))]

    res = scipy.optimize.linprog(c, A_eq=A, b_eq=target, integrality=1)
    return int(sum(res.x))

def do2():
    assert 33 == part2(ftest)
    assert 18981 == part2(finput)

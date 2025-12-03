import utils
import os.path

dir_ = os.path.dirname(__file__)
ftest = os.path.join(dir_, 'day03_test.txt')
finput = os.path.join(dir_, 'day03_input.txt')

@utils.timeit
def part1(fname: str) -> int:
    res = 0
    for line in utils.f2lines(fname):
        first, fpos = 0, 0
        for p in range(0, len(line) - 1):
            d = int(line[p])
            if d > first:
                first = d
                fpos = p
        second = 0
        for p in range(fpos + 1, len(line)):
            d = int(line[p])
            if d > second:
                second = d
        res += 10 * first + second
    return res

def do1():
    assert 357 == part1(ftest)
    assert 17321 == part1(finput)
    assert 17321 == part(finput, 2)

@utils.timeit
def part2(fname: str) -> int:
    return part(fname, 12)

def part(fname: str, number_length: int) -> int:
    res = 0
    for line in utils.f2lines(fname):
        line_length = len(line)
        start = 0
        digits = []
        for digit_cnt in range(number_length):
            max_digit = 0
            for p in range(start, line_length - (number_length - digit_cnt) + 1):
                digit = int(line[p])
                if digit > max_digit:
                    max_digit = digit
                    start = p + 1
            digits.append(max_digit)
        res += int(''.join(str(d) for d in digits))
    return res

def do2():
    assert 3121910778619 == part2(ftest)
    assert 171989894144198 == part2(finput)

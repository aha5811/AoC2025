
d90 = [(1, 0), (0, 1), (-1, 0), (0, -1)] # E S W N
dE, dS, dW,dN = d90[0], d90[1], d90[2], d90[3]
d45 = [(1, 1), (-1, 1), (-1, -1), (1, -1)] # SE SW NW NE
dSE, dSW, dNW, dNE = d45[0], d45[1], d45[2], d45[3]
dirs = d90 + d45


class Dir:
    def __init__(self, t: tuple[int, int]):
        self.x = Dir._1(t[0])
        self.y = Dir._1(t[1])

    @staticmethod
    def _1(n: int) -> int:
        return 0 if n == 0 else (1 if n > 0 else -1)

D90 = list(map(lambda t: Dir(t), d90))
DE, DS, DW, DN = D90[0], D90[1], D90[2], D90[3]
D45 = list(map(lambda t: Dir(t), d45))
DSE, DSW, DNW, DNE = D45[0], D45[1], D45[2], D45[3]
Dirs = D90 + D45


class Step(Dir):
    def __init__(self, t: tuple[int, int], w: int):
        Dir.__init__(self, t)
        self.set_width(w)

    def set_width(self, w: int):
        self.x = Dir._1(self.x) * w
        self.y = Dir._1(self.y) * w


class Pos:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def __eq__(self, other):
        if isinstance(other, Pos):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash(str(self))

    def step(self, step: Dir):
        self.x += step.x
        self.y += step.y

    def get_step(self, step: Dir) -> Pos:
        return Pos(self.x + step.x, self.y + step.y)


class Map:
    def __init__(self, fname: str):
        self.rows = []
        with open(fname, 'r') as f:
            for line in f:
                self.rows.append(list(line.strip()))
        self.h = len(self.rows)
        self.w = len(self.rows[0])

    def __str__(self):
        res = ""
        for row in self.rows:
            res += "\n" + "".join(row)
        return res[1:]

    def get(self, x: int, y: int) -> str:
        return (
            None
            if x < 0 or x >= self.w or y < 0 or y >= self.h
            else self.rows[y][x])

    def set(self, x: int, y: int, c: str):
        if self.get(x, y) is not None:
            self.rows[y][x] = c

    def get_symbols(self) -> list[str]:
        res = set()
        for x in range(self.w):
            for y in range(self.h):
                res.add(self.get(x, y))
        return list(res)

    def find_all(self, s: str) -> list[Pos]:
        res = []
        for x in range(self.w):
            for y in range(self.h):
                if self.get(x, y) == s:
                    res.append(Pos(x, y))
        return res

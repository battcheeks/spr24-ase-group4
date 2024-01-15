import math
import random

# ----------------------------------------------------------------------------
# Classes

class NUM:
    def __init__(self, s=None, n=None):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = -1E30
        self.lo = 1E30
        self.heaven = 0 if s and s.endswith("-") else 1

    def add(self, x):
        if x != "?":
            self.n += 1
            d = x - self.mu
            self.mu += d / self.n
            self.m2 += d * (x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1)) ** 0.5

    def small(self):
        return the.cohen * self.div()

    def same(self, other, pooled_sd, n12, correction):
        n12 = self.n + other.n
        pooled_sd = ((self.n - 1) * self.div()**2 + (other.n - 1) * other.div()**2) / (n12 - 2)**0.5
        correction = 1 if n12 >= 50 else (n12 - 3) / (n12 - 2.25)
        return abs(self.mu - other.mu) / pooled_sd * correction <= the.cohen

    def norm(self, x):
        return x if x == "?" else (x - self.lo) / (self.hi - self.lo + 1E-30)

    def like(self, x):
        mu, sd = self.mid(), (self.div() + 1E-30)
        nom = 2.718**(-0.5 * (x - mu)**2 / (sd**2))
        denom = sd * 2.5 + 1E-30
        return nom / denom


class SYM:
    def __init__(self, s=None, n=None):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0

    def add(self, x):
        if x != "?":
            self.n += 1
            self.has[x] = 1 + (self.has[x] or 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self):
        e = 0
        for v in self.has.values():
            e -= v / self.n * math.log(v / self.n, 2)
        return e

    def small(self):
        return 0

    def like(self, x, prior):
        return (self.has[x] + the.m * prior) / (self.n + the.m)


class COLS:
    def __init__(self, row):
        self.x = {}
        self.y = {}
        self.all = []
        self.klass = None
        self.names = row.cells

        for at, txt in enumerate(row.cells, 1):
            col = NUM(txt, at) if txt[0].isupper() else SYM(txt, at)
            self.all.append(col)
            if not txt.endswith("X"):
                if txt.endswith("!"):
                    self.klass = col
                (self.y if txt.endswith("!") or txt.endswith("-") or txt.endswith("+") else self.x)[at] = col


class ROW:
    def __init__(self, t):
        self.cells = t


class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None
        self.adds(src, fun)

    def adds(self, src, fun=None):
        if isinstance(src, str):
            for _, x in l_csv(src):
                self.add(x, fun)
        else:
            for _, x in enumerate(src or []):
                self.add(x, fun)
        return self

    def add(self, t, fun=None):
        row = t.cells if isinstance(t, ROW) else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)


# ----------------------------------------------------------------------------
# Functions

def l_csv(src):
    with (open(src) if src != "-" else sys.stdin) as f:
        for i, line in enumerate(f, 1):
            cells = l_cells(line)
            if cells:
                yield i, ROW(cells)


def l_coerce(s1):
    def fun(s2):
        return None if s2 == "nil" else s2 == "true" or s2 != "false" and s2

    return int(s1) if s1.isdigit() else float(s1) if s1

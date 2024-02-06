from Utility import Utility
from ROW import ROW
from COLS import Cols as COLS
import random

# ----------------------------------------------------------------------------
# Data Class

class DATA:
    def __init__(self, the, src, fun=None):
        self.rows = []
        self.cols = None
        self.the = the
        self.util = Utility()
        self.adds(src, fun)
        # print("Construting..")

    def adds(self, src, fun=None):
        if isinstance(src, str):
            # Here the _ is just because pairs returns two values.
            for x in self.util.l_csv(file=src):
                # print(x)
                self.add(x, fun)
        else:
            # for attr in dir(src):
            #     print("obj.%s = %r" % (attr, getattr(src, attr)))
            ## also did some debugging here.
            for x in (src or []):
                self.add(x, fun)
            # self.add(src, fun)
        return self

    def add(self, t, fun=None):
        # Made changes to the following block of code
        # print("Before", t)
        # if t is None:
        #     return 0
        if hasattr(t, 'cells'):
            row = t
        else:
            row = ROW(self.the, t)
        # print("After", row)
        # row = ROW(t) if type(t) is list else t.cells
        # row = t if t.cells else ROW(t)  Check line 182 might be different.
        # print(self.cols)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
            # print(self.rows)
        else:
            self.cols = COLS(self.the, row)

    def mid(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.mid())
        return ROW(self.the, u)

    def div(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.div())
        return ROW(self.the, u)
    
    def small(self):
        u = []
        for col in self.cols.all:
            u.append(col.small())
        return ROW(self.the, u)
    
    def stats(self, cols=None, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        # print(self.rows)
        columns_to_iterate = getattr(self.cols, cols or "y", [])
        for col in columns_to_iterate:
            value = getattr(type(col), fun or "mid")(col)
            #print("Value = " , value)
            u[col.txt] = self.util.rnd(value, ndivs)
            # print(value)
            # u[col.txt] = round(value,2)
        return u
    
    def clone(self, rows=None):
        new = DATA(self.the)
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new
    
    def gate(self, budget0, budget, some):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        # print(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        for i in range(budget):
            best, rest = self.bestRest(lite, len(lite)**some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
        return stats, bests
    
    def split(self, best, rest, lite_rows, dark_rows):
        selected = DATA(self.the, [self.cols.names])
        max_val = 1E30
        out = 1
        # print(dark_rows)
        for i, row in enumerate(dark_rows):
            b = row.like(best, len(lite_rows), 2)
            r = row.like(rest, len(lite_rows), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b + r) / abs(b - r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp
        return out, selected
    
    def bestRest(self, rows, want):
        rows.sort(key=lambda a: a.d2h(self))
        #rows.sort(key=lambda a: a.d2h(self))
        # best = [self.cols['names']]
        # rest = [self.cols['names']]
        best = [self.cols.names]
        rest = [self.cols.names]
        for i, row in enumerate(rows):
            if i <= want:
                best.append(row)
            else:
                rest.append(row)
        return DATA(self.the, best), DATA(self.the, rest)
    
    def farapart(self, the, rows, sortp, a=None, b=None):
        far = int(len(rows) * the.Far)
        evals = 1 if a else 2
        a = a or random.choice(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]

        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a

        return a, b, a.dist(b, self), evals
#data = DATA(src='../data/auto93.csv')

#print(data.stats())
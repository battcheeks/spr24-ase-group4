from Utility import Utility
from ROW import ROW
from COLS import Cols as COLS
from node import NODE
import random

# ----------------------------------------------------------------------------
# Data Class

is_debug = False

class DATA:
    def __init__(self, the, src, fun=None):
        self.rows = []
        self.cols = None
        self.the = the
        self.util = Utility(the)
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
        new = DATA(self.the, [self.cols.names])
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new
    
    def gate(self, budget0, budget, some, clustering_method=None):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        # print(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        for i in range(budget):

            if not clustering_method:
                # Do SMO by default
                best, rest = self.bestRest(lite, len(lite)**some)
            elif clustering_method == "kmeans":
                pass
            
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

    def split_by_b_over_r(self, best, rest, lite_rows, dark_rows):
        selected = DATA(self.the, [self.cols.names])
        max_val = 1E30
        out = 1
        # print(dark_rows)
        for i, row in enumerate(dark_rows):
            b = row.like(best, len(lite_rows), 2)
            r = row.like(rest, len(lite_rows), 2)
            if b > r:
                selected.add(row)
            tmp = abs(b) / abs(r + 1E-300)
            if tmp > max_val:
                out, max_val = i, tmp
        return out, selected
    
    def bestRest(self, rows, want):
        rows.sort(key=lambda a: a.d2h(self))
        # rows.sort(key=lambda a: a.d2h(self))
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
    
    def farapart(self, rows, sortp=None, before=None):
        far = int(len(rows) * self.the.Far)
        evals = 1 if before else 2
        left = before or random.choice(rows).neighbors(self, rows)[far]
        right = left.neighbors(self, rows)[far]
        if sortp and right.d2h(self) < left.d2h(self):
            left, right = right, left
        return left, right, left.dist(right, self), evals


    def half(self, rows, sortp=False, before=None):
        def dist(r1, r2): return r1.dist(r2, self)
        def proj(row)  : return (dist(row,left)**2 + C**2 - dist(row,right)**2)/(2*C)
        left, right, C, _ = self.farapart(random.choices(rows, k=min(self.the.Half, len(rows))), sortp=sortp, before=before)

        lefts,rights = [],[]

        for n, row in enumerate(sorted(rows , key=proj)):
            if n < len(rows) / 2 :
                lefts.append(row)
            else:
                rights.append(row)

        return lefts, rights, left, right

    def tree(self, sortp):
        pass
        evals = 0

        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows) > 2 * len(self.rows) ** 0.5:
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows, sortp, above)
                evals = evals + evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node

        return _tree(self), evals


    def branch(self, rows=None, stop=None, rest=None, evals=1, before=None):
        rows = rows or self.rows
        stop = stop or 2 * len(rows) ** 0.5
        rest = rest or []
        if len(rows) > stop:
            lefts, rights, left, right  = self.half(rows, True, before)
            return self.branch(lefts, stop, rest+rights, evals+1, left)
        else:
            return self.clone(rows), self.clone(rest), evals

#data = DATA(src='../data/auto93.csv')

#print(data.stats())

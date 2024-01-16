from Utility import Utility
from ROW import ROW
from COLS import Cols as COLS

# ----------------------------------------------------------------------------
# Data Class

class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None
        self.util = Utility()
        self.adds(src, fun)

    def adds(self, src, fun=None):
        if isinstance(src, str):
            # Here the _ is just because pairs returns two values.
            for x in self.util.l_csv(file=src):
                self.add(x, fun)
        else:
            for _, x in enumerate(src or []):
                self.add(x, fun)
        return self

    def add(self, t, fun=None):
        row = ROW(t) if type(t) is list else t.cells
        # row = t if t.cells else ROW(t)  Check line 182 might be different.
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)

    def mid(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.mid())
        return ROW(u)

    def div(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.div())
        return ROW(u)
    
    def small(self):
        u = []
        for col in self.cols.all:
            u.append(col.small())
        return ROW(u)
    
    def stats(self, cols=None, fun=None, ndivs=None):
        u = {".N": len(self.rows)}
        print(self.cols.names.cells)
        columns_to_iterate = getattr(self.cols, cols or "y", [])
        for col in columns_to_iterate:
            value = getattr(type(col), fun or "mid")(col)
            #print("Value = " , value)
            #u[col.txt] = self.util.rnd(value, ndivs)
            u[col.txt] = round(value,2)
        return u
    
    def clone(self, rows=None):
        new = DATA()
        new.cols.names = self.cols.names
        for row in rows or []:
            new.add(row)
        return new
    
    def gate(self, budget0, budget, some):
        stats = []
        bests = []
        rows = self.util.shuffle(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]
        for i in range(1, budget+1):
            best, rest = self.bestRest(lite, len(lite)**some)
            todo, selected = self.split(best, rest, lite, dark)
            stats[i] = selected.mid()
            bests[i] = best.rows[0]
            lite.append(dark.pop(todo))
        return stats, bests
    
    def split(self, best, rest, lite_rows, dark_rows):
        selected = DATA(self.cols.names)
        max_val = 1E30
        out = 1
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
        best = [self.cols['names']]
        rest = [self.cols['names']]
        for i, row in enumerate(rows):
            if i <= want:
                best.append(row)
            else:
                rest.append(row)
        return DATA(best), DATA(rest)
    
data = DATA(src='C:/Users/tekem/Documents/Manali/NCSU_Masters/SEM2_Spring2024/CSC591_ASE/spr24-ase-group4/hw/data/auto93.csv')

print(data.stats())
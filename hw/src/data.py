import math

import Utility


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
            for _, x in self.util.l_csv(src):
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

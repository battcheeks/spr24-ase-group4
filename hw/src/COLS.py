from num import NUM
from sym import SYM
import re

class Cols:
    def __init__(self, row):
        self.names = row
        self.all = []
        self.x = []
        self.y = []
        self.target_class = None

        for index, name in enumerate(row.cells):
            col = NUM(name, index) if re.match("^[A-Z]", name) else SYM(name, index)
            self.all.append(col)

            if not name.endswith("X"):
                if name.endswith("!"):
                    self.target_class = col

                if re.search("[!+-]$", name):
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for columns in [self.x, self.y]:
            for col in columns:
                col.add(row.cells[col.at])

    def __repr__(self):
        return f"Cols(names={self.names})"
    
import num as NUM
import sym as SYM
import re

class Cols:
    def __init__(self, names):
        self.names = names
        self.all_columns = []
        self.x_columns = []
        self.y_columns = []
        self.target_class = None

        for index, name in enumerate(names):
            col = NUM(index, name) if re.match("^[A-Z]", name) else SYM(index, name)
            self.all_columns.append(col)

            if not name.endswith("X"):
                if name.endswith("!"):
                    self.target_class = col

                if re.search("[!+-]$", name):
                    self.y_columns.append(col)
                else:
                    self.x_columns.append(col)

    def add(self, row):
        for columns in [self.x_columns, self.y_columns]:
            for col in columns:
                col.add(row.cells[col.at])

    def __repr__(self):
        return f"Cols(names={self.names})"

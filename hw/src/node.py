class NODE:
    def __init__(self, data):
        self.here = data
        self.lefts = None
        self.rights = None

    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self, _show, max_depth):
        def d2h(data):
            return round(data.mid().d2h(self.here), ndigits=6)

        max_depth = 0

        def _show(node, depth, leafp, post):
            nonlocal max_depth
            post = post if leafp else f"{d2h(node.here)}\t{node.here.mid().cells}"
            max_depth = max(max_depth, depth)
            print(('|.. ' * depth) + post)

        self.walk(_show)
        print("")
        print(("    " * max_depth) + f"{d2h(self.here)}\t{self.here.mid().cells}")
        print(("    " * max_depth) + "_\t" + str(self.here.cols.names))
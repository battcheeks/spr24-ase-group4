# ----------------------------------------------------------------------------
# Utility Class for helper functions such as csv reader, etc.
import ast
import re, fileinput
import math, random

DEFAULT_COHEN_VALUE = 0.35  # small effect size
DEFAULT_K_VALUE = 1  # low class frequency kludge
DEFAULT_M_VALUE = 2  # low attribute frequency kludge
DEFAULT_RANDOM_SEED = 31210  # random number seed

class Utility:
    def __init__(self) -> None:
        pass

    def l_csv(self, file="-"):
        with fileinput.FileInput(None if file == "-" else file) as src:
            for line in src:
                # This regex replaces all the characters in bracket and words starting with #. with an empty string.
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                # Then we feed the commma seperated data values to coerce for type conversion.
                if line: yield [self.l_coerce(x) for x in line.split(",")]

    def l_coerce(self, x):
        # literal_eval will convert the string to appropriate data type and the exception is when x is a string.
        try: return ast.literal_eval(x)
        except Exception: return x.strip()

    def rnd(self, n, ndecs=None):
        if not isinstance(n, (int, float)):
            return n
        if n == math.floor(n):
            return n
        mult = 10 ** (ndecs or 2)
        return math.floor(n * mult + 0.5) / mult

    def shuffle(self, t):
        u = t[:]
        random.shuffle(u)
        return u

    def slice(self, t, go=None, stop=None, inc=None):
        if go is not None and go < 0:
            go = len(t) + go
        if stop is not None and stop < 0:
            stop = len(t) + stop

        u = []

        if go is None:
            go = 0
        if stop is None:
            stop = len(t)
        if inc is None:
            inc = 1

        for j in range(go, stop, inc):
            u.append(t[j])

        return u

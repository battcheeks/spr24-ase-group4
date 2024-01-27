import math
class ROW:
    def __init__(self, the, cells):
        self.cells = cells
        self.the = the
    
    #likes()
    def likes(self, datas):
        n, nHypotheses = 0, 0
        most = None
        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses += 1
        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k
        return out, most
    
    #like()
    def like(self,data, n, nHypotheses):
        prior = (len(data.rows) + self.the.k) / (n + self.the.k * nHypotheses)
        out = math.log(prior)
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                # print(inc)
                try:
                    out += math.log(inc)
                except ValueError:
                    out += 0.0001

        return math.exp(1) ** out
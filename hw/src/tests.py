from sym import SYM 
from num import NUM 
from data import DATA
import random

class Tests():
    def __init__(self) -> None:
        self.all = [self.test_sym_1, self.test_sym_2, self.test_num_1, self.test_num_2]
        pass
    
    def test_sym_1(self):
        s = SYM()
        for x in [4, 4, 3, 3, 5, 3, 3]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test1 Passed:", 1.37 < e < 1.38 and mode == 3) 
        print("   - Values Calulated: ", mode, e)

    def test_sym_2(self):
        s = SYM()
        for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 2.20 < e < 2.25 and mode == 2)
        print("   - Values Calulated: ", mode, e)

    def test_num_1(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test1 Passed:", 4.8 < mu < 5.1 and 1 < sd < 1.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))

    def test_num_2(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 14.6 < mu < 15.1 and 3 < sd < 3.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
        
    # def test_data(self):
    #     n = 0
    #     d = DATA("../data/auto93.csv")  # Replace 'the_file' with the actual file path
    #     print(d.rows)
    #     for i, row in enumerate(d.rows):
    #         if (i + 1) % 100 == 0:
    #             n += len(row.cells)
    #             print(row.cells)
    #     print(d.cols.x[1].cells)
    #     return n == 63
    
    
    def run_all_tests(self):
        for i in self.all:
            i()

t = Tests()
t.test_data()
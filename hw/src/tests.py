from sym import SYM 
from num import NUM 
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
        print(mode, e)
        print("Python SYM Test1 Passed:", 1.37 < e < 1.38 and mode == 3) 

    def test_sym_2(self):
        s = SYM()
        for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print(mode, e)
        print("Python SYM Test2 Passed:", 2.20 < e < 2.25 and mode == 2)

    def test_num_1(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print(round(mu, 3), round(sd, 3))
        print("Python NUM Test1 Passed:", 4.8 < mu < 5.1 and 1 < sd < 1.05)

    def test_num_2(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print(round(mu, 3), round(sd, 3))
        print("Python NUM Test2 Passed:", 14.6 < mu < 15.1 and 3 < sd < 3.05)
    
    
    def run_all_tests(self):
        for i in self.all:
            i()

t = Tests()
t.run_all_tests()
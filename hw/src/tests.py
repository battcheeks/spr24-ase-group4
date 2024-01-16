from sym import SYM 
from num import NUM 
import random

def test_sym_1():
    s = SYM()
    for x in [4, 4, 3, 3, 5, 3, 3]:
        s.add(x)
    mode, e = s.mid(), s.div()
    print(mode, e)
    return 1.37 < e < 1.38 and mode == 3
print("Python SYM Test1 Passed:", test_sym_1())

def test_sym_2():
    s = SYM()
    for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
        s.add(x)
    mode, e = s.mid(), s.div()
    print(mode, e)
    return 2.20 < e < 2.25 and mode == 2
print("Python SYM Test2 Passed:", test_sym_2())

def test_num_1():
    e = NUM()
    for _ in range(1000):
        e.add(random.normalvariate(5, 1))
    mu, sd = e.mid(), e.div()
    print(round(mu, 3), round(sd, 3))
    return 4.8 < mu < 5.1 and 1 < sd < 1.05
print("Python NUM Test1 Passed:", test_num_1())

def test_num_2():
    e = NUM()
    for _ in range(1000):
        e.add(random.normalvariate(15, 3))
    mu, sd = e.mid(), e.div()
    print(round(mu, 3), round(sd, 3))
    return 14.6 < mu < 15.1 and 3 < sd < 3.05
print("Python NUM Test2 Passed:", test_num_2())

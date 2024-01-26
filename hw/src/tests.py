from sym import SYM 
from num import NUM 
from data import DATA
from learn import learn
import random

class Tests():
    def __init__(self) -> None:
        self.all = [self.test_sym_1, self.test_sym_2, self.test_sym_3, self.test_num_1, self.test_num_2, self.test_num_3]
        self.num = [self.test_num_1, self.test_num_2, self.test_num_3]
        self.sym = [self.test_sym_1, self.test_sym_2, self.test_sym_3]
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
        
    def test_sym_3(self):
        s = SYM()
        for x in [1, 2, 2, 2, 3, 3, 1, 3, 3, 1]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 1.47 < e < 1.65 and mode == 3)
        print("   - Values Calulated: ", mode, e)

    def test_num_1(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test1 Passed:", 4.7 < mu < 5.1 and 1 < sd < 1.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))

    def test_num_2(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 14.7 < mu < 15.2 and 2.9 < sd < 3.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_num_3(self):
        e = NUM()
        for _ in range(1000):
            e.add(random.normalvariate(10, 2))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 9.8 < mu < 10.2 and 1.9 < sd < 2.4)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_eg_stats(self):
        data = DATA("../data/auto93.csv")
        stats_result = data.stats()
        expected_result = "{'.N': 398, 'Lbs-': 2970.42, 'Acc+': 15.57, 'Mpg+': 23.84}"
        print("Actual Result:", str(stats_result))
        print("Expected Result:", expected_result)
        
        if str(stats_result) == expected_result:
            print("Test Passed!")
        else:
            print("Test Failed!")
            
    def test_eg_bayes(self):
        wme = {'acc': 0, 'datas': [], 'tries': 0, 'n': 0}
        data = DATA("../data/diabetes.csv", lambda data, t: learn(data, t, wme))
        print(wme['acc'] / wme['tries'])
        return wme['acc'] / wme['tries'] > 0.72
        
    ## Running all the tests as per Class ##
    
    def run_num_tests(self):
        for i in self.num:
            i()
            
    def run_sym_tests(self):
        for i in self.sym:
            i()
    
    def run_all_tests(self):
        for i in self.all:
            i()
            
# test = Tests()
# print(test.test_eg_bayes())
# test.run_all_tests()
# test.test_eg_stats()
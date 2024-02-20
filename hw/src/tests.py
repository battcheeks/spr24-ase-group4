from sym import SYM 
from num import NUM 
from data import DATA
from learn import learn
import random
import math
from Utility import Utility

class Tests():
    def __init__(self, the) -> None:
        ## Getting all the variables from the arguments.
        self.the = the
        self.util = Utility()
        
        self.all = [self.test_sym_1, self.test_sym_2, self.test_sym_3, self.test_num_1, self.test_num_2, self.test_num_3]
        self.num = [self.test_num_1, self.test_num_2, self.test_num_3]
        self.sym = [self.test_sym_1, self.test_sym_2, self.test_sym_3]
        pass

    def reset_to_default_seed(self):
        random.seed(self.the.seed)
    
    def test_sym_1(self):
        s = SYM(self.the)
        for x in [4, 4, 3, 3, 5, 3, 3]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test1 Passed:", 1.37 < e < 1.38 and mode == 3) 
        print("   - Values Calulated: ", mode, e)

    def test_sym_2(self):
        s = SYM(self.the)
        for x in [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 2.20 < e < 2.25 and mode == 2)
        print("   - Values Calulated: ", mode, e)
        
    def test_sym_3(self):
        s = SYM(self.the)
        for x in [1, 2, 2, 2, 3, 3, 1, 3, 3, 1]:
            s.add(x)
        mode, e = s.mid(), s.div()
        print("Python SYM Test2 Passed:", 1.47 < e < 1.65 and mode == 3)
        print("   - Values Calulated: ", mode, e)

    def test_num_1(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(5, 1))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test1 Passed:", 4.7 < mu < 5.1 and 1 < sd < 1.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))

    def test_num_2(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(15, 3))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 14.7 < mu < 15.2 and 2.9 < sd < 3.05)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_num_3(self):
        e = NUM(self.the)
        for _ in range(1000):
            e.add(random.normalvariate(10, 2))
        mu, sd = e.mid(), e.div()
        print("Python NUM Test2 Passed:", 9.8 < mu < 10.2 and 1.9 < sd < 2.4)
        print("   - Values Calulated: ", round(mu, 3), round(sd, 3))
    
    def test_eg_stats(self):
        data = DATA(self.the, "../data/auto93.csv")
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
        data = DATA(self.the, self.the.file, lambda data, t: learn(data, t, wme, self.the))
        print("File Used :", self.the.file)
        print("Accurary :", wme['acc'] / wme['tries'] * 100, "%")
        return wme['acc'] / wme['tries'] > 0.72
    
    def test_km(self):
        print("#%4s\t%s\t%s" % ("acc", "k", "m"))
        for k in range(4):
            for m in range(4):
                self.the.k = k
                self.the.m = m
                wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
                data = DATA(self.the, "../data/soybean.csv", lambda data, t: learn(data, t, wme, self.the))
                print("%5.2f\t%s\t%s" % (wme['acc'] / wme['tries'], k, m))
        
    def test_gate(self):
        self.reset_to_default_seed()
        budget0 = 4
        budget = 10
        some = 0.5

        d = DATA(self.the, "../data/auto93.csv")

        def sayd(row, txt):
            distance_to_heaven = self.util.rnd(row.d2h(d))
            print("{0} {1} {2}".format(str(row.cells), txt, distance_to_heaven))

        def say(row, txt):
            print("{0} {1}".format(str(row.cells), txt))

        print("{0} {1} {2}".format(str(d.cols.names.cells), "about", "d2h"))
        print("#overall")
        sayd(d.mid(), "mid")
        say(d.div(), "div")
        say(d.small(), "small=div*" + str(self.the.cohen))

        print("#generality")
        # print(d.rows)
        stats, bests = d.gate(budget0, budget, some)
        for index, stat in enumerate(stats):
            sayd(stat, index + budget0)

        print("#specifically")
        for index, best in enumerate(bests):
            sayd(best, index + budget0)

        print("#optimum")
        d.rows.sort(key=lambda a: a.d2h(d))
        sayd(d.rows[0], len(d.rows))

        print("#random")
        random_rows = self.util.shuffle(d.rows)
        print(len(random_rows), int(math.log(0.05) / math.log(1 - self.the.cohen / 6)))
        random_rows = self.util.slice(random_rows, 1, int(math.log(0.05) / math.log(1 - self.the.cohen / 6)))
        random_rows.sort(key=lambda a: a.d2h(d))
        sayd(random_rows[0], None)

    def test_gate20(self):
        debug = False

        budget0 = 4
        budget = 10
        some = 0.5
        # A list that store the output of each steps
        output_message_list = [[] for _ in range(6)]

        test_case_n = 20
        for _ in range(test_case_n):
            seed_value = random.randint(0, 100000)
            random.seed(seed_value)

            if debug:
                print("seed = {0}".format(seed_value))

            d = DATA(self.the, "../data/auto93.csv")
            d.rows = self.util.shuffle(d.rows)

            # Step 1: Top 6
            top_count_n = 6
            top6_row_y_data = []
            for row_data in d.rows[:top_count_n]:
                y_data = []
                for y_field in d.cols.y:
                    y_data.append(row_data.cells[y_field.at])
                top6_row_y_data.append(y_data)
            output_message = "1. top6 {0}".format(top6_row_y_data)
            output_message_list[0].append(output_message)

            # Step 2: Top 50
            top_count_n = 50
            top50_row_y_data = []
            for row_data in d.rows[:top_count_n]:
                y_data = []
                for y_field in d.cols.y:
                    y_data.append(row_data.cells[y_field.at])
                top50_row_y_data.append(y_data)
            output_message = "2. top50 {0}".format(top50_row_y_data)
            output_message_list[1].append(output_message)


            # Step 3: Most
            d.rows.sort(key=lambda a: a.d2h(d))
            most_result = []
            for y_field in d.cols.y:
                most_result.append(d.rows[0].cells[y_field.at])
            output_message_list[2].append("3. most: {0}".format(most_result))

            d.rows = self.util.shuffle(d.rows)
            lite = self.util.slice(d.rows, 0, budget0)
            dark = self.util.slice(d.rows, budget0 + 1)

            stats = []
            bests = []
            for i in range(budget):
                best, rest = d.bestRest(lite, len(lite)**some)
                todo, selected = d.split(best, rest, lite, dark)
                stats.append(selected.mid())
                bests.append(best.rows[0])

                random_d = DATA(self.the, [d.cols.names])
                for row in random.sample(dark, budget0 + 1):
                    random_d.add(row)

                # Step 4
                random_result = []
                for y_field in d.cols.y:
                    rounded_number = round(random_d.mid().cells[y_field.at], 2)
                    random_result.append(rounded_number)
                output_message_list[3].append("4. rand: {0}".format(random_result))


                # Step 5
                mid_result = []
                for y_field in d.cols.y:
                    rounded_number = round(selected.mid().cells[y_field.at], 2)
                    mid_result.append(rounded_number)
                output_message_list[4].append("5. mid: {0}".format(mid_result))


                # Step 6
                top_result = []
                for y_field in d.cols.y:
                    rounded_number = round(best.rows[0].cells[y_field.at], 2)
                    top_result.append(rounded_number)
                output_message_list[5].append("6. top: {0}".format(top_result))

                lite.append(dark.pop(todo))

        # Sort output message
        for step in range(6):
            output_message_list[step].sort()
            for line in output_message_list[step]:
                print("{0}".format(line))
            print("")

    def test_dist(self):
        d = DATA(self.the, "../data/auto93.csv")
        r1 = d.rows[0]  # In Python, indices start from 0
        rows = r1.neighbors(d)
        for i, row in enumerate(rows):
            if i % 30 == 0:
                print(i+1,"     ",str(row.cells), "     ",round(row.dist(r1, d), 2))

    def test_far(self):
        d = DATA(self.the, "../data/auto93.csv")
        a, b, C, _ = d.farapart(d.rows)
        print(str(a.cells), str(b.cells), round(C, 2))
        print("far1: ",str(a.cells))
        print("far2: ",str(b.cells))
        print("distance = ",C)
    
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
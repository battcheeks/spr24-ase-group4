"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2, GROUP 4
Learn a little, guess a lot, try the strangest guess, repeat

USAGE:
  python3 gate.py [OPTIONS] 

OPTIONS:
  -c --cohen  small effect size               = .35
  -f --file   csv data file name              = '../data/diabetes.csv'
  -h --help   show help                       = False
  -k --k      low class frequency kludge      = 1
  -m --m      low attribute frequency kludge  = 2
  -s --seed   random number seed              = 31210
  -t --todo   start up action                 = 'help' """

#gate.py
import argparse
from data import DATA 
from tests import Tests

def main():
    parser = argparse.ArgumentParser(description="Perform statistics on a CSV file.")
    parser.add_argument("-f", "--file", help="csv data file name              = '../data/diabetes.csv'")
    parser.add_argument("-t", "--task", help="start up action                 = 'help' ")
    parser.add_argument("-k","-k", type=int, help="low class frequency kludge      = 1")
    args = parser.parse_args()
    
    # Initializing the default value of k
    if(not args.k): args.k = 1
    if(not args.file): args.file = "../data/diabetes.csv"
    
    
    # Load data from CSV file
    data = DATA(src=args.file)
    
    # Testing arguments.
    # print(args)
    # Load test cases
    test = Tests(args)

    # Perform the specified task
    if args.task == "stats":
        # Add your statistics logic here
        result = data.stats()
        print(result)
    elif args.task == "num":
        test.run_num_tests()
    elif args.task == "sym":
        test.run_sym_tests()
    elif args.task == "bayes":
        test.test_eg_bayes()
    elif args.task == "all":
        test.run_all_tests()
    else:
        print(__doc__)

if __name__ == "__main__":
    main()

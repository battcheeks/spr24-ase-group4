#gate.py
import argparse
from data import DATA 
from tests import Tests

def main():
    parser = argparse.ArgumentParser(description="Perform statistics on a CSV file.")
    parser.add_argument("-f", "--file", required=True, help="Path to the CSV file.")
    parser.add_argument("-t", "--task", choices=["stats","num", "sym", "all"], required=True, help="Task to perform.")
    args = parser.parse_args()

    # Load data from CSV file
    data = DATA(src=args.file)
    
    # Load test cases
    test = Tests()

    # Perform the specified task
    if args.task == "stats":
        # Add your statistics logic here
        result = data.stats()
        print(result)
    elif args.task == "num":
        test.run_num_tests()
    elif args.task == "sym":
        test.run_sym_tests()
    elif args.task == "all":
        test.run_all_tests()
    else:
        print(f"Unsupported task: {args.task}")

if __name__ == "__main__":
    main()

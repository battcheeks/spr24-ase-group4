#gate.py
import argparse
from data import DATA  # Replace with the actual module where DATA class is defined

def main():
    parser = argparse.ArgumentParser(description="Perform statistics on a CSV file.")
    parser.add_argument("-f", "--file", required=True, help="Path to the CSV file.")
    parser.add_argument("-t", "--task", choices=["stats"], required=True, help="Task to perform.")
    args = parser.parse_args()

    # Load data from CSV file
    data = DATA(src=args.file)

    # Perform the specified task
    if args.task == "stats":
        # Add your statistics logic here
        result = data.stats()
        print(result)
    else:
        print(f"Unsupported task: {args.task}")

if __name__ == "__main__":
    main()

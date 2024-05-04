from data_tools import data_import, data_analyzer
import print_data
import csv
import sys

all_entrances = []
current_shares = {}
previous_shares = {} 


def main():

    if len(sys.argv) < 2:
        filename = input("Please enter a filename: ")
    else:
        filename = sys.argv[1]

    all_entrances = data_import.load_csv_data(filename)    
    current_shares, previous_shares = data_analyzer.analyze_entrances(all_entrances)
    
    print_data.print_current_shares_results(current_shares)
    print_data.print_previous_shares_results(previous_shares)


if __name__ == "__main__":
    main()




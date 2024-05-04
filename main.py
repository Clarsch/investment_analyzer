import csv
import sys

shares = {}
old_shares = {}
current_shares = {}


buy_in = 0.00
number_of_shares = 0
zero_price = 0.00

def convert_to_float(number_string):
    float_string = number_string.replace(".", "").replace(",", ".")
    return float(float_string)

def transaction_is_positive(transaction_type):
    if transaction_type == 'SOLGT':
        return True
    elif transaction_type == 'KØBT':
        return False
    elif transaction_type == 'UDB.':
        return True
    elif transaction_type == 'UDBYTTESKAT':
        return False


def get_zero_price(price, amount):
    if amount == 0:
        return 0.00
    else:
        return -(price / amount)

def float_to_dkk_currency(amount):
    return '{0:,.2f}kr.'.format(amount)


def add_entrance(row):
    global shares
    # print(row)
    if(row[7] == 'Aktier'):
        transaction_type = row[5]
        transaction_value = convert_to_float(row[14])
        share_name = row[6]
        amount = int(row[9])

        buy_in = 0.00
        number_of_shares = 0

        if share_name in shares:
            buy_in = shares[share_name]['buy_in']
            number_of_shares = shares[share_name]['number_of_shares']
        

        buy_in += transaction_value
        
        if transaction_type == 'SOLGT':
            number_of_shares -= amount
        elif transaction_type == 'KØBT':
            number_of_shares += amount
        
        shares[share_name] = {'buy_in': buy_in, 'number_of_shares': number_of_shares}
        #print(f"Share {share_name} has been updated with {transaction_type}:{transaction_value} - {amount} to {buy_in} - {number_of_shares}")

def analyze_shares():
    global old_shares
    global current_shares

    for share_name, share_details in shares.items():
        buy_in = float(share_details['buy_in'])
        number_of_shares = share_details['number_of_shares']
        
        if number_of_shares == 0:
            old_shares[share_name] = {'result': buy_in}  
        else:
            current_shares[share_name] = {'buy_in': buy_in, 'number_of_shares': number_of_shares}


def load_data(csv_filename):

    with open(csv_filename, mode='r', encoding='utf-16le') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        header = next(csv_reader)
        for row in csv_reader: 
            add_entrance(row)
    
        
def print_results():
    for share_name, share_details in current_shares.items(): 
        buy_in = float(share_details['buy_in'])
        buy_in_as_string = float_to_dkk_currency(buy_in)
        number_of_shares = share_details['number_of_shares']
        average_price = float_to_dkk_currency(get_zero_price(buy_in, number_of_shares))
        print(f"{share_name}: You have invested {buy_in_as_string} in {number_of_shares} shares for an average price at {average_price}")

    result_sum = 0.00
    for share_name, share_details in old_shares.items(): 
        result = share_details['result']
        result_sum += result
        result_as_string = float_to_dkk_currency(result)
        print(f"You have owned {share_name} resulting in {result_as_string}")
    print(f"Total result for previous owned shares: {float_to_dkk_currency(result_sum)}")



def main():

    if len(sys.argv) < 2:
        filename = input("Please enter a filename: ")
    else:
        filename = sys.argv[1]

    load_data(filename)        
    analyze_shares()
    print_results()

    


if __name__ == "__main__":
    main()




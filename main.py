import csv
import sys

entrances = []
current_shares = {}
old_shares = {} 


def convert_string_to_float(number_string):
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

def load_data(csv_filename):
    global entrances
    with open(csv_filename, mode='r', encoding='utf-16le') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        header = next(csv_reader)
        for row in csv_reader: 
            if(row[7] == 'Aktier'):
                transaction_type = row[5]
                amount_preload = int(row[9])
                if transaction_type == 'SOLGT':
                    amount = -amount_preload
                elif transaction_type == 'KØBT':
                    amount = amount_preload
                else:
                    amount = 0 

                entrances.append ({
                    'date': row[2],
                    'name': row[6],
                    'transaction_type': transaction_type, 
                    'value': convert_string_to_float(row[14]), 
                    'trading_price': row[10],
                    'amount': amount
                    })

def analyze_entrances():
    global current_shares
    global old_shares

    for entrance in sorted(entrances, key=lambda x: x['date']):
        share_name = entrance['name']
        buy_in = entrance['value']
        number_of_shares = entrance['amount']

        #Loading and adding previous values
        if share_name in current_shares:
            current_share = current_shares[share_name]
            buy_in += current_share['buy_in']
            number_of_shares += current_share['number_of_shares']

        #Archive values if all shares has been sold
        if(number_of_shares == 0):
            if(share_name in old_shares):
                previous_result = old_shares[share_name]['result']
            else:
                previous_result = 0.00
            old_shares[share_name] = {'result': previous_result + buy_in}
            # print(f"Previous result: {previous_result}, buy_in: {buy_in}, new result: {old_shares[share_name]['result']}")
            current_shares.pop(share_name)
        else: 
            current_shares[share_name] = {
                'buy_in': buy_in, 
                'number_of_shares': number_of_shares
                }


        
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
    # add_entrance(row)
       
    analyze_entrances()
    print_results()


if __name__ == "__main__":
    main()




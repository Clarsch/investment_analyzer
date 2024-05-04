import csv


def load_csv_data(csv_filename):
    entrances = []
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
    return entrances

def convert_string_to_float(number_string):
    float_string = number_string.replace(".", "").replace(",", ".")
    return float(float_string)
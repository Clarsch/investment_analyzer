
def analyze_entrances(entrances):
    current_shares = {}
    previous_shares = {}

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
            if(share_name in previous_shares):
                previous_result = previous_shares[share_name]['result']
            else:
                previous_result = 0.00
            previous_shares[share_name] = {'result': previous_result + buy_in}
            # print(f"Previous result: {previous_result}, buy_in: {buy_in}, new result: {old_shares[share_name]['result']}")
            current_shares.pop(share_name)
        else: 
            current_shares[share_name] = {
                'buy_in': buy_in, 
                'number_of_shares': number_of_shares
                }
    return (current_shares, previous_shares)


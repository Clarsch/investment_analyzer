def get_zero_price(price, amount):
    if amount == 0:
        return 0.00
    else:
        return -(price / amount)

def float_to_dkk_currency(amount):
    return '{0:,.2f}kr.'.format(amount)


def print_current_shares_results(current_shares):
    for share_name, share_details in current_shares.items(): 
        buy_in = float(share_details['buy_in'])
        buy_in_as_string = float_to_dkk_currency(buy_in)
        number_of_shares = share_details['number_of_shares']
        average_price = float_to_dkk_currency(get_zero_price(buy_in, number_of_shares))
        print(f"{share_name}: You have invested {buy_in_as_string} in {number_of_shares} shares for an average price at {average_price}")

def print_previous_shares_results(previous_shares):
    result_sum = 0.00
    for share_name, share_details in previous_shares.items(): 
        result = share_details['result']
        result_sum += result
        result_as_string = float_to_dkk_currency(result)
        print(f"You have owned {share_name} resulting in {result_as_string}")
    print(f"Total result for previous owned shares: {float_to_dkk_currency(result_sum)}")

"""@author Andrew Kim"""

from requests import get
from pprint import PrettyPrinter

# API pulls from this website which offers real-time data
BASE_URL = "https://free.currconv.com/"
API_KEY = "fead15c2d6df5ed8320c" # unique API assigned to author

# What does this do
printer = PrettyPrinter()


"""This function calls the API and returns a something
This data is then put into a list and then sorted
"""
def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    
    url = BASE_URL + endpoint # the base url is then appended with the end point which contains our API key. The question mark starts the query to the URL. 

    data = get(url).json()['results'] # this returns a json file that Python can read like a psuedo dictionary

    data = list(data.items()) # this dictionary type data is then converted into a list of tuples. Each tuple in the list contains the abbreviation, name of the currency, and symbol if available

    data.sort() # the data is then sorted by alphabetical order based off the first item which is the abbreviation of the currency

    return data

def print_currencies(currencies):
    # for each name and currency in the tuple
    for name, currency in currencies:
        name = currency['currencyName'] # extract the name
        _id = currency['id'] # extract the abbreviation 
        symbol = currency.get("currencySymbol", "") # extract the symbol if present, else empty space
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}" # here we are querying two desired currencies. The "compact" language means the API is just going to return the exchange rate
    
    url = BASE_URL + endpoint
    data = get(url).json()

    # Error handling
    if len(data) == 0:
        print("Invalid currencies.") # this will print if a currency that is passed in is not recognized
        return

    rate = list(data.values())[0]

    print(f"1 {currency1} is {rate:.4f} {currency2}")

    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None: # if we received an invalid currency
        return
    try:
        amount = float(amount) # convert amount to float
    except:
        print("Invalid amount.") # if passed in amount cannot be converted to a float
        return
    converted_amount = rate * amount
    print(f"{amount:.2f} {currency1} is equal to {converted_amount:.2f} {currency2}")
    return converted_amount

""" MAIN FILE """
def main():
    currencies = get_currencies()

    print("//////////////////////////// Currency Converter ////////////////////////////")
    print("\nCommand Options")
    print("List - lists the available currencies")
    print("Exchange - calculate one currency amount to another")
    print("Rate - get the exchange rate between two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == 'q':
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "exchange":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter the amount in {currency1}: ")
            currency2 = input("Enter the desired currency: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter the desired currency: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")
            
main()
import ccxt
import csv
from datetime import datetime, timedelta
from enum import Enum

# Connecting to Binance
exchange = ccxt.binance()

# Downloading function with iteration for larger data
def download_data(exchange, symbol, timeframe='1d', start_date='2017-01-01', limit=1000):
    all_data = []
    since = exchange.parse8601(f'{start_date}T00:00:00Z')  # Start time
    while since < exchange.milliseconds():  # Continue until today
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        if len(ohlcv) == 0:
            break  # If no more data is returned, stop the loop
        all_data += ohlcv
        since = ohlcv[-1][0] + (24 * 60 * 60 * 1000)  # Move to the next day (in ms)
    return all_data

# Writing data to file
def write_to_file(file_name, ohlcv):
    with open(file_name, 'w', newline='', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for row in ohlcv:
            row[0] = datetime.utcfromtimestamp(row[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(row)

# Enum for coins
Coins = Enum('Coins', {
    'BTC': 'BTC/USDT',
    'ETH': 'ETH/USDT',
    'BNB': 'BNB/USDT',
    'PEPE': 'PEPE/USDT'
})

# Dictionary for filenames
file_names = {
    Coins.BTC: 'btc.csv',
    Coins.ETH: 'eth.csv',
    Coins.BNB: 'bnb.csv',
    Coins.PEPE: 'pepe.csv'
}

# Main function to select currency and download data
def main():
    coins_list = list(Coins)
    
    # Menu for choosing a coin
    print("Which currency do you want to choose?")
    for i, coin in enumerate(coins_list, start=1):
        print(f"{i}. {coin.name}")

    chosen_index = int(input('Enter the number of your chosen currency: '))

    if 1 <= chosen_index <= len(coins_list):
        chosen_coin = coins_list[chosen_index - 1]  # Selected coin
        symbol = Coins[chosen_coin.name].value  # Get the market symbol (e.g. 'BTC/USDT')
        data = download_data(exchange, symbol)  # Download market data
        file_name = file_names[chosen_coin]  # Get the file name for this coin
        write_to_file(file_name, data)  # Save the data to the CSV file
        print(f"Data for {chosen_coin.name} saved in {file_name}")
    else:
        print("Invalid choice.")

# Run the program
if __name__ == "__main__":
    main()

import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'static/stock_scrape_api/tickers.json')

if __name__ == '__main__':
    with open(filename, 'rb') as f:
        t = json.load(f)

    print(t['AAPL'])
    print(t['NFLX'])

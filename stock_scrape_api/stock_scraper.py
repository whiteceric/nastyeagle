import os
from datetime import datetime, timedelta
from pytz import timezone
from bs4 import BeautifulSoup
import requests

def today(_timezone='America/New_York'):
    """
    For debugging, allows me to change what 'today' is.
    """
    return datetime.now(timezone(_timezone)).replace(hour=0, minute=0, second=0, microsecond=0)

def load_stock_page(ticker, daysBack):
    """
    Returns the Beautiful soup object for the stock page
    """
    period2 = int(today('GMT').timestamp())
    period1 = int((today('GMT') - timedelta(daysBack*2)).timestamp())
    compiled_url = f'https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
    source = requests.get(compiled_url).text
    return  BeautifulSoup(source, 'lxml')

def get_latest_n_closing_prices_scrape(ticker, n):
    """
    Returns a dictionary mapping the previous n dates to the closing price on those dates for this stock
    """
    soup = load_stock_page(ticker, n)
    out = []
    close_price_index = 4
    _timezone = timezone('GMT')
    for row in soup.find('table').find_all('tr'):
        row_str = [elm.text for elm in row.find_all('span')]
        if 'Close' in row_str:
            close_price_index = row_str.index('Close')
        try:
            _date = _timezone.localize(datetime.strptime(row_str[0], '%b %d, %Y'))
            out.append((_date, float(row_str[close_price_index].replace(',', ''))))
            if len(out) == n:
                break
        except Exception as e:
            continue # we found one of the end rows with no data
    return out

def get_latest_price_scrape(ticker):
    """
    Scrapes the latest stock price for ticker from finance.yahoo.com
    """
    soup = load_stock_page(ticker, 7)
    return soup.find('span', attrs={"data-reactid": "50"}).text

def get_date_str(date):
    """
    Returns the given date in YYYY-MM-DD format. date is the object returned by datetime.today()
    """
    return date.strftime('%Y-%m-%d')

def market_open():
    """
    Checks if the time is between 9:30am  and 4pm EST on a weekday.
    """
    time = today() 
    time = time.hour + time.minute/60
    return today().weekday() < 5 and time >= 9.5 and time  < 16


def get_prev_day_close(ticker, get_day_change=False):
    """
    Returns the price of the stock ticker at the close of the previous day.
    If get_day_change is set to True returns a tuple containing the previous day close and the day change for the
    previous day.
    """
    yesterday = today() - timedelta(1)
    yesterday_str = get_date_str(yesterday) 
    try:
        latest_week_scrape = get_latest_n_closing_prices_scrape(ticker, 7)
        close_price = latest_week_scrape[0][1] 
        prev_close_price = latest_week_scrape[1][1]
        day_change = close_price - prev_close_price
    except Exception as e:
        print('failed to get previous day close for', ticker, e)
        close_price = 0
        day_change = 0
    return (close_price, day_change) if get_day_change else close_price

def get_current_price(ticker, get_day_change=False):
    """
    Returns the current price of a stock
    If get_day_change is set to True, returns a tuple containing the current price and the day change
    """
    if market_open():
        try:
            current_price = float(get_latest_price_scrape(ticker))
            prev_price = get_prev_day_close(ticker, get_day_change=False)
            return (current_price, current_price - prev_price) if get_day_change else current_price 
        except Exception as e:
            print('failed to get current price for', ticker, e)
            return 0
    else:
        return get_prev_day_close(ticker, get_day_change=get_day_change)

def get_prev_week_endpoints(ticker):
    """
    Returns a list of tuples representing the past 5 closing prices for a stock
    The format for the list is:
    [(-5, 80.54), (-4, 81.2), ... (-1, 85.32)]
    """
    last_week_scrape = get_latest_n_closing_prices_scrape(ticker, n)
    _today = today('GMT')
    return [((_date - _today).days, close_price) for _date, close_price in last_week_scrape]

if __name__ == '__main__':
    #load_stock_data()
    #print(get_prev_day_close('DIS'))
    #save_stock_data()
    #print(get_price_on_date('DIS', '2021/03/01'))
    #print(get_prev_week_endpoints('PINS'))
    #print(get_current_price('AAPL'))
    print(get_current_price('AMZN'))

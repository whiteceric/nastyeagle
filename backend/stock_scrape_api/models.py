from django.db import models
from .stock_scraper import market_open, get_current_price, today_start, EST
from datetime import datetime, timedelta
from pytz import UTC

ONE_DAY = timedelta(days=1)

def time_after_close(timestamp):
    '''
    Checks if timestamp is after the previous day's close
    Returns false if the datetime.now() is during market hours on a weekday

    Specifically, if timestamp is during market hours, returns false. 
    if datetime.now() is after 16:00 EST on a weekday checks if 
    timestamp is after 16:00 EST on the same day.  
    if datetime.now() is before 09:30 EST on a weekday checks if 
    timestamp is after 16:00 EST on the same day.  
    if datetime.now() is on a weekend, checks if timestamp is after 16:00 EST on the
    previous Friday.

    TODO: test this function (maybe some doctests)
    '''
    time = datetime.fromtimestamp(timestamp).astimezone(EST)
    time_dec = time.hour + time.minute/60
    now = datetime.now(EST)
    now_dec = now.hour + now.minute/60
    if market_open(now.astimezone(UTC).timestamp()) or market_open(timestamp):
        return False
    elif now.weekday() >= 5 or (now.weekday() == 0 and now_dec < 9.5): # weekend or monday morning 
        # get the date of the previous Friday
        prev = now - ONE_DAY
        while prev.weekday() != 4:
            prev = now - ONE_DAY

        return prev.date() == time.date() and time_dec >= 16
    else:
        if now_dec >= 16:
            return time.date() == now.date() and time_dec >= 16
        elif now.weekday() != 0 and now_dec < 9.5: # can't look at previous day on a Monday! (likely a redundant check here)
            return (time.date() == now.date() - ONE_DAY and time_dec >= 16) or (time.date() == now.date() and time_dec < 9.5)

class Stock(models.Model):
    ticker = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, blank=True)
    latest_price = models.FloatField(blank=True, null=True)
    latest_day_change = models.FloatField(blank=True, null=True)
    last_updated = models.FloatField(blank=True, null=True)

    def update(self):
        '''
        Update this stock by finding the latest stock price and day change.

        If the market is open finds the most recent price and day change. If the
        market is closed and last_updated is after the last market close
        then no update is made. Otherwise, finds the most recent close price and day change.

        Returns True if an update was made, False otherwise
        '''
        if not self.last_updated or market_open() or not time_after_close(self.last_updated):
            new_price, new_day_change = get_current_price(ticker=self.ticker, get_day_change=True)
            new_day_change = round(new_day_change, 2) # to avoid floating point errors showing up in API responses
            self.latest_price = new_price
            self.latest_day_change = new_day_change
            self.last_updated = datetime.now().timestamp()
            self.save()
            return True
        return False


    def __str__(self):
        return self.ticker

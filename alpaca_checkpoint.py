import alpaca_trade_api as tradeapi
import requests
import time
import numpy as np
import datetime as datetime
from pytz import timezone
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
base_url = 'https://paper-api.alpaca.markets'
api_key_id = 'PKZZSJW3TYRN3VZHWXCL'
api_secret = 'I74UPzZBVMYBIEa2XqdKoMXAMe4tlBq1PHdtyTra'
session = requests.session()
api = tradeapi.REST(
    base_url=base_url,
    key_id=api_key_id,
    secret_key=api_secret
)
def MACD(stock_symbol):
    symbol = stock_symbol
    start = datetime.datetime.today() - datetime.timedelta(days=30)
    end = datetime.datetime.today() - datetime.timedelta(days = 1)
    stock = yf.download(symbol, start=start, end=end)

    # Initialize short/long windows
    smallWindow = 5
    largeWindow = 45
    
    # Initialize the 'signals' DataFrame with the 'signal' column  
    signals = pd.DataFrame(index=stock.index)
    signals['signal'] = 0.0
    
    # Create short simple moving average over short window
    signals['short_mavg'] = stock['Close'].rolling(window = smallWindow, min_periods = 1, center=False).mean()
    
    # Create long simple moving average over the long window
    signals['long_mavg'] = stock['Close'].rolling(window = largeWindow, min_periods=1, center=False).mean()
    
    # Create signalds
signals.loc[signals.index[smallWindow:], 'signal'] = np.where(
    signals['short_mavg'][smallWindow:] > signals['long_mavg'][smallWindow:], 1.0, 0.0
)
    
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    signals['pct_change'] = ((stock['Close'] - stock['Open'])/(stock['Open'])) * 100
    if(signals['positions'].iloc[-1] == 1.0):
        api.submit_order(
            symbol=symbol,
            qty=30,
            side='buy',
            type='market',
            time_in_force='gtc'
            )
        print("Ordered " + symbol + " BUY")
    elif(signals['positions'].iloc[-1] == -1.0):
        api.submit_order(
            symbol=symbol,
            qty=30,
            side='sell',
            type='market',
            time_in_force='gtc'
            )
        print("Ordered " + symbol + " SELL")
    
    #Print yesterday's signal
    print(signals.tail(1))  
    
    
    # Initialize the plot figure
    fig = plt.figure(figsize=(8, 6))

    # Add a subplot and label for y-axis
    ax1 = fig.add_subplot(111,  ylabel='Price in $')

    # Plot the closing price
    stock['Close'].plot(ax=ax1, color='r', lw=2.)

    # Plot the short and long moving averages
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the buy signals
    ax1.plot(signals.loc[signals.positions == 1.0].index, 
             signals.short_mavg[signals.positions == 1.0],
             '^', markersize=10, color='m')

    # Plot the sell signals
    ax1.plot(signals.loc[signals.positions == -1.0].index, 
             signals.short_mavg[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Show the plot
    plt.show()
    
    print(signals['positions'].iloc[-1])
def main():
    # Wait for market open
    isOpen = api.get_clock().is_open
    while(not isOpen):
      clock = api.get_clock()
      openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
      currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
      timeToOpen = int((openingTime - currTime) / 60)
      print(str(timeToOpen) + " minutes til market open.")
      time.sleep(60)
      isOpen = api.get_clock().is_open
    # Wait one minute after market open
    time.sleep(60)
    
    # Run moving average crossover 
    MACD('XLK')
    MACD('AMD')
    MACD('SPY')
    MACD('AAPL')
    MACD('TLRY')
    MACD('TWTR')
    MACD('FB')
    MACD('MSFT')
    MACD('DIS')
    MACD('F')
    MACD('SBUX')
    MACD('BABA')
    MACD('BAC')
    MACD('FIT')
    MACD('AMZN')
    MACD('SQ')
main()
def movingAverageCrossover():
    start = datetime.datetime.today() - datetime.timedelta(days=30)
    end = datetime.datetime.today()
    xlk = pdr.DataReader("XLK", 'yahoo', start, end)
    # Initialize short/long windows
    smallWindow = 5
    largeWindow = 45
    
    # Initialize the 'signals' DataFrame with the 'signal' column
    signals = pd.DataFrame(index=xlk.index)
    signals['signal'] = 0.0
    
    # Create short simple moving average over short window
    signals['short_mavg'] = xlk['Close'].rolling(window = smallWindow, min_periods = 1, center=False).mean()
    
    # Create long simple moving average over the long window
    signals['long_mavg'] = xlk['Close'].rolling(window = largeWindow, min_periods=1, center=False).mean()
    
    # Create signalds
    signals['signal'][smallWindow:] = np.where(signals['short_mavg'][smallWindow:] > signals['long_mavg'][smallWindow:], 1.0, 0.0)
    
    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    signals['pct_change'] = (xlk['Close'])/(xlk['Open']) - 1
    
    #Print 'signals'
    print(signals)
    
    
    # Initialize the plot figure
    fig = plt.figure(figsize=(16, 12))

    # Add a subplot and label for y-axis
    ax1 = fig.add_subplot(111,  ylabel='Price in $')

    # Plot the closing price
    xlk['Close'].plot(ax=ax1, color='r', lw=2.)

    # Plot the short and long moving averages
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the buy signals
    ax1.plot(signals.loc[signals.positions == 1.0].index, 
             signals.short_mavg[signals.positions == 1.0],
             '^', markersize=10, color='m')

    # Plot the sell signals
    ax1.plot(signals.loc[signals.positions == -1.0].index, 
             signals.short_mavg[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Show the plot
    plt.show()
    
movingAverageCrossover()
 
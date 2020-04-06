import pandas as pd 
!pip install yfinance
import yfinance as yf
import matplotlib.pyplot as plt
import datetime 
df = pd.read_csv('https://raw.githubusercontent.com/MaxChenCMC/SnP500_candlestick_pattern_filter/master/S%26P500.csv')# 讀github的csv要點raw格式
def kline(ticker):
    start = datetime.date.today() - datetime.timedelta(days = 14)
    end = datetime.date.today()
    return pd.DataFrame(yf.download(ticker,start,end))
for i in list(df['Symbol']):
    res = kline(str(i))[-10:]
    long = []
    short = []
    try:
        if (len([res['Open'] > res['Adj Close'].shift()*1.02]) >= 1)&(len(res[res['Adj Close'] > res['Open']*1.03]) >= 1 )&(len( res[(res['High'] > res['High'].shift()) & ( res['Low'] > res['Low'].shift())] ) >= 5)&(res['Adj Close'][-1]*1.03 >= res['High'][-10:].max())&(res['Volume'][-3:].mean() > res['Volume'][-10:].mean()*1.1):
            long.append(i) 
        elif (len(res[res['Open'] < res['Adj Close'].shift()*0.98]) >= 1 )&(len(res[res['Adj Close']*1.03 < res['Open']]) >= 1 )&(len(res[ (res['High'] < res['High'].shift()) & (res['Low'] < res['Low'].shift()) ]) >= 4)&(res['Adj Close'][-1]*0.97<=res['Low'][-10:].min())&(len(res[res['Adj Close'] < res['Open']*0.98]) >= 4 )&(len( res [res['Adj Close'] < res['Open']] [res['High'] > res['Adj Close']*1.01] ) >= 1):
           short.append(i) 
        else:
            pass
    except Exception as e:
        print('公司',i,'報價有誤' )
    continue
print(f'做多{long}\n做空{short}')
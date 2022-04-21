import yfinance as yf
import pandas as pd

def historical_data_values(args, ticker="AAPL", start="2022-4-19", end="2022-4-20"):
    return yf.download(ticker.upper(), start, end, interval="1m", rounding=False)

data = pd.DataFrame(historical_data_values(["Datetime", "Close"]))

flag = "start"

counting_14 = 14 #Read WebScoket for 'Closed', after counting 14th candelstick - start calculation

period_EMA = 14
period_MACD_long = 26
period_MACD_short = 12
period_MACD_signal = 9

filters = ['Open', 'Low', 'High', 'Volume', 'Adj Close']    

for foo in filters:
    data.pop(foo)

close_diff = data['Close'].diff()
up = close_diff.clip(lower=0)
down = close_diff.clip(upper=0) * -1
ma_up = up.ewm(com=period_EMA-1, adjust=True, min_periods=period_EMA).mean()
ma_down = down.ewm(com=period_EMA-1, adjust=True, min_periods=period_EMA).mean()
rs = ma_up / ma_down
data['RSI'] = 100 - (100/(1 + rs))

print(data)
rsi_25 = data['RSI'].to_list()
print(rsi_25)

historical_candles = rsi_25

del historical_candles[:len(historical_candles)-24]
del historical_candles[len(historical_candles)-1]

print(historical_candles)

count = 0
for i in range(23):
    if historical_candles[i] < 50:
        count = count + 1
    else:
        pass

count_percent = (count / 23) * 100

if count_percent > 60:
    flag = "baught"
else:
    flag = "waiting"

print(flag)

import matplotlib.pyplot as plt
import pandas_datareader as web

# Stocks interested
tickers = ["AMD", "ATVI", "BABA", "BIDU", "BILI","CEA","GME","GOOGL","HUYA","NVDA"]

# Get Stock Info from Yahoo
multpl_stocks = web.get_data_yahoo(tickers,
start = "2021-01-01",
end = "2021-04-30")

multpl_stock_daily_returns = multpl_stocks['Adj Close']

timeX = multpl_stock_daily_returns.index.values

plt.figure(figsize=(20, 10))

for t in tickers:
    plt.plot(timeX,multpl_stock_daily_returns[t].values,label = t)
    
plt.legend()
plt.show()
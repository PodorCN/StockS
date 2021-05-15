import matplotlib.pyplot as plt
import pandas_datareader as web
from numpy.linalg import inv

# Stocks interested
tickers = ["AMD", "ATVI", "BABA", "BIDU", "BILI","CEA","GME","GOOGL","HUYA","NVDA"]

# Get Stock Info from Yahoo
multpl_stocks = web.get_data_yahoo(tickers,
start = "2021-01-01",
end = "2021-04-30")

multpl_stock_daily_returns = multpl_stocks['Adj Close']

print(multpl_stock_daily_returns)
for i in multpl_stocks['Adj Close']:
    plt.plot(i)
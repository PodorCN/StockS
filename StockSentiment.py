import matplotlib.pyplot as plt
import pandas_datareader as web
from numpy.linalg import inv

# Stocks interested
tickers = ["GME",'RKT','ETSY','AAPL','TSLA ']

# Get Stock Info from Yahoo

multpl_stocks = web.get_data_yahoo(tickers,
start = "2021-01-01",
end = "2021-04-30")

multiStockPrice = multpl_stocks['Adj Close']


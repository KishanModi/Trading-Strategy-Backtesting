# Inbuilt python module yfinance is used to fetch stock data from Yahoo Finance website.
# Processes the fetched data and gives it to ML model

# Importing required modules
import pandas as pd
import numpy as np
import yfinance as yf
import datetime

class FetchData():
    # Function   :- initializes DataFrame
    def __init__(self):
        self.__df = pd.DataFrame()

    # Function   :- fetches data using yfinance
    #
    # Parameters :- stock_name - name of the stock 
    #               start_date/end_date - timeframe for which we want to fetch data
    #
    # Returns    :- DataFrame containing stock data
    def __getdata(self, stock_name, start_date, end_date):
        t = yf.download(stock_name, start_date, end_date)
        return t

    def __RSI(self, series, period):
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
            pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
        return 100 - 100 / (1 + rs)

    # Function   :- adds features to data
    #
    # Parameters :- isTrain - True if fetching train data for ML model
    #                         False if fetching data for backtesting
    def __addfeatures(self, isTrain):
        # adding target to train data for training ML model 
        if isTrain:
            self.__df['Open_next'] = self.__df['Open'].shift(-1)
            self.__df['target'] = np.where(self.__df['Open_next'] > self.__df['Close'], 1, 0)

        # adding technical indicators in data
        self.__df['SMA30'] = self.__df['Adj Close'].rolling(window=30).mean()
        self.__df['SMA60'] = self.__df['Adj Close'].rolling(window=60).mean()
        self.__df['SMA90'] = self.__df['Adj Close'].rolling(window=90).mean()
        self.__df['SMA180'] = self.__df['Adj Close'].rolling(window=180).mean()

        self.__df['SMA6030'] = self.__df['SMA60'] - self.__df['SMA30']
        self.__df['SMA9030'] = self.__df['SMA90'] - self.__df['SMA30']
        self.__df['SMA18030'] = self.__df['SMA180'] - self.__df['SMA30']
        self.__df['SMA9060'] = self.__df['SMA90'] - self.__df['SMA60']
        self.__df['SMA18030'] = self.__df['SMA180'] - self.__df['SMA60']
        self.__df['SMA18090'] = self.__df['SMA180'] - self.__df['SMA90']

        self.__df['EMA10'] = self.__df['Adj Close'].ewm(span=10, adjust=False).mean()
        self.__df['EMA30'] = self.__df['Adj Close'].ewm(span=30, adjust=False).mean()
        self.__df['EMA60'] = self.__df['Adj Close'].ewm(span=60, adjust=False).mean()
        self.__df['EMA90'] = self.__df['Adj Close'].ewm(span=90, adjust=False).mean()
        self.__df['EMA120'] = self.__df['Adj Close'].ewm(span=120, adjust=False).mean()
        self.__df['EMA150'] = self.__df['Adj Close'].ewm(span=150, adjust=False).mean()
        self.__df['EMA180'] = self.__df['Adj Close'].ewm(span=180, adjust=False).mean()

        self.__df['rsi14'] = self.__RSI(self.__df['Adj Close'], 14)
        self.__df['rsi30'] = self.__RSI(self.__df['Adj Close'], 30)
        self.__df['rsi60'] = self.__RSI(self.__df['Adj Close'], 60)
        self.__df['rsi90'] = self.__RSI(self.__df['Adj Close'], 90)
        self.__df['rsi120'] = self.__RSI(self.__df['Adj Close'], 120)
        self.__df['rsi150'] = self.__RSI(self.__df['Adj Close'], 150)
        self.__df['rsi180'] = self.__RSI(self.__df['Adj Close'], 180)

        # droping NULL values in DataFrame
        self.__df.dropna(inplace = True)

    # Function   :- called from train and pred to fetch data
    #
    # Parameters :- stock_name - name of the stock 
    #               start_date/end_date - timeframe for which we want to fetch data
    #               isTrain - True if fetching train data for ML model
    #                         False if fetching data for backtesting
    #
    # Returns    :- DataFrame containing stock data
    def execute(self, stock_name = "AAPL", start_date = datetime.date(2016, 1, 1), end_date = datetime.date(2020, 1, 1), isTrain = False):
        self.__df = self.__getdata(stock_name, start_date, end_date)
        self.__addfeatures(isTrain)
        return self.__df
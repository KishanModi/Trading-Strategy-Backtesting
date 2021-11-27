# Takes output predicted by ML model 
# Outputs how much profit user would have made if he/she would have used model to trade

# Importing required modules
import pandas as pd
import matplotlib.pyplot as plt
from pred import *
import numpy as np

# Function   :- fetches output predicted by ML model
# Returns    :- DataFrame containing output predicted by model
def get_pred(sn, s, e):
    return calls(sn, s, e)

# Function   :- calculates and finds how much profit or loss would have happened if user invested according ML model
# Parameters :- t - DataFrame containing output of ML model
def simulator(t, m):
    # m - amount which user want to invest
    # c - count of stock
    b = []
    s = []
    money = []
    count = []
    profit = []
    p = 0
    om = m
    c = 0
    d = {}
    print(f'Default Money = {m}')
    print("\n")
    # calculating profit or loss according output predicted by ML model
    for i in range(len(t)):
        if (t['pred'][i] > 0):
            if m > t['Close'][i]:
                m = m - t['Close'][i]
                c = c + 1
            b.append(1)
            s.append(0)

        else:
            if c > 0:
                m = m + t['Close'][i]
                c = c - 1
            b.append(0)
            s.append(1)
        p= c*t["Open"][-1] + m - om
        money.append(m)
        count.append(c)
        profit.append(p)

    d["Money"] = m
    d["Stock"] = c
    d["Stock Price"] = t["Open"][-1]
    d["Profit"] = c*t["Open"][-1] + m - om
    d["cp"]=t["Adj Close"][-1]
    d["ip"]=t["Adj Close"][1]
    t["buy"] = b
    t["sell"] = s
    t['m'] = money
    t['c'] = count
    t['pr'] = profit
    t.to_csv(r'x.csv', index = False)
    print(f'Money = {m}')
    print(f'Stock = {c}')
    print(f'Stock Price = {t["Open"][-1]}')

    print(f'Profit = {c*t["Open"][-1] + m - om}')

    return d, t

def graph(t):
    f1 = plt.figure(figsize = (12, 5))
    plt.plot(t['Adj Close'])
    plt.ylabel('closing price')

    f2 = plt.figure(figsize = (12,5))
    plt.plot(t['Adj Close'])
    plt.plot(t['Open'])
    plt.ylabel('opening/closing price')
    plt.legend(loc='upper left')


    f3 = plt.figure(figsize = (12,5))
    plt.plot(t['m'])
    plt.ylabel('money in account')

    f4 = plt.figure(figsize = (12,5))
    plt.plot(t['c'])
    plt.ylabel('stock count')

    f5 = plt.figure(figsize = (12,5))
    plt.plot(t['pr'])
    plt.ylabel('profit/loss')
    # t.to_csv(r'x.csv', index = False)
    t['sell']=np.nan
    t['buy']=np.nan

    for x in range(len(t['pred'])): 
        if t['pred'][x]==0:
            t['sell'][x]=t["Adj Close"][x]
        else:
            t['buy'][x]=t["Adj Close"][x]

    f6 = plt.figure(figsize=(12,5))
    plt.plot(t['Adj Close'], label='Adj Close', color = 'orange', linewidth=2)
    plt.scatter(t.index, t['buy'], label='Buy', marker='^' , color = 'green')
    plt.scatter(t.index, t['sell'], label='sell', marker='v' , color = 'red')
    plt.xlabel('price')
    plt.ylabel('index')
    plt.legend(loc='upper left')

    return f1, f2, f3, f4, f5, f6

# Function   :- fetches output predicted by ML model and give it to simulator()
def execute_s(sn, s, e, m):
    df = get_pred(sn, s, e)
    d, t = simulator(df, m)
    f1, f2, f3, f4, f5, f6 = graph(t)

    return d, f1, f2, f3, f4, f5, f6

if __name__ == '__main__':
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2020, 1, 1)

    d = execute('AAPL', start_date, end_date, 10000)
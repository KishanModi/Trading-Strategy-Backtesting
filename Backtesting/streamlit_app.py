import streamlit as st
import datetime
import time

st.set_page_config(layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


## Main Title ##
st.title('Trading Strategy Backtesting')
st.write(""" This App will Predict the Profit/loss Based on the input such as stock name,
time period and amount given by the user and
on the trading strategy that we have created.
""")


##### User Input #####
st.subheader('Stock Name:')
from data import data
stock_names=data

## Stock Name convert to symbol ##
def format_func(stock):
    return stock_names[stock]


## Stock Name ##
stock = st.selectbox("Stock Name:",index=(len(data)-1),options=list(stock_names.keys()),format_func=format_func)
print(stock)

## Time Period ##
today=datetime.date.today()
c1, c2 = st.columns(2)
with c1:
	st.subheader('Enter Start date:')
	start_date = st.date_input('Start date:',value=datetime.date(2016, 1, 2), min_value=datetime.date(2012, 1, 2),max_value=(today - datetime.timedelta(days=366)))
	print(start_date)
	print(type(start_date))
with c2:
	st.subheader('Enter End date:')
	end_date = st.date_input('End date:',value=datetime.date(2020, 1, 1), min_value=datetime.date(2012, 1, 2),max_value=(today - datetime.timedelta(days=1)))


## Amount ##
st.subheader('Enter the amount of money you want to invest')
money=st.number_input("Amount:",value=50000,step=1000,min_value=1000,max_value=1000000)

## Trading Strategy Model##
st.subheader('Select the Machine Learning Model')
model = st.selectbox('Model Name: ',("DT","KNN"))
# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
# genre = st.radio("Model",('KNN','DT'))

## Submit Button ##
from execute import *
if st.button('Backtest'):
	if stock=="":
		st.error('Enter a valid Stock Name')
		st.stop()
	with st.spinner('Wait for it...'):
		time.sleep(23)
	d, f1, f2, f3, f4, f5, f6 = execute(model, stock, start_date, end_date, money)
	print(d)
	current_price = round(d["cp"],2)
	open_price = d['ip']
	change = round(current_price - open_price,2)

	def stockreturn(stock):
		return stock_names[stock]
	st.title(body=stockreturn(stock))
## analysis	##
	## result ##
	st.header('Backtesting Results')
	col1, col2, col3 = st.columns(3)
	col1.metric("Current Price",current_price, change)
	col2.metric("Money Invested", money,"0 %")
	if d['Profit']<0:
		col3.metric("Loss",round(d['Profit'],2), round(d['Profit'],2))
	else:
		col3.metric("Profit", round(d['Profit'],2), round(d['Profit'],2))

	## chart ##
	with st.container():
		st.header("Stock Price Movement Graphs:")
		col1, col2 = st.columns(2)
		with col1:
			st.subheader('Closing Price of Stock On Each Day:')
			st.pyplot(f1)
		with col2:
			st.subheader('Open/Close Price Graph of Stock:')
			st.pyplot(f2)

	## chart 2##
	with st.container():
		st.header('Profit/Loss Analysis:')
		col1, col2 = st.columns(2)
		with col1:
			st.subheader('Money In the Acount:')
			st.pyplot(f3)
		with col2:
			st.subheader('Profit/Loss Graph:')
			st.pyplot(f5)
	## chart 3##
	st.header("Stocks In The Acount:")
	st.pyplot(f4)
	## chart 4##
	st.header("Buy/Sell Signal Graph:")
	st.pyplot(f6)
	## Success##
	st.success('Backtesting Completed')

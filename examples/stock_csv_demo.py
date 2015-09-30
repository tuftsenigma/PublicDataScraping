## -*- coding: utf-8 -*-
#"""
#Created on Sun Sep 27 17:56:06 2015
#
#@author: mumbosauce
#
#"""
#
#import numpy as np
#import pandas as pd
#from yahoo_finance import Share
#import plotly.plotly as py
#import plotly.tools as tls
#from plotly.graph_objs import *
#
#def csv_to_dataframe(file_name='web_traffic_data_-_updated.csv'):
#    csv = np.genfromtxt(file_name, delimiter=',', dtype=str)
#    df = pd.DataFrame(data=csv)
#    df.columns = df.iloc[0]
#    df = df.ix[1:]
#    return df
#    
#    
#def filter_ticker_symbol(df, ticker='nflx'):
#    df = df[df['Ticker Symbol'] == ticker]
#    return df
#
#    
#def clean_dates(df):
#    for index, row in df.iterrows():
#        row['Date'] = row['Date'][:10] 
#
#
#def web_traffic_and_prices(symbol, web_traffic):
#    prices = Share(symbol).get_historical('2007-01-08', '2015-09-18')
#    prices = pd.DataFrame(data=prices)
#    traffic = filter_ticker_symbol(web_traffic, symbol)
#    clean_dates(traffic)
#    traffic_and_prices = traffic.merge(prices, on='Date')
#    traffic_and_prices.drop(['High', 'Low'], axis=1, inplace=True)
#    traffic_and_prices.sort(columns='Date', inplace=True)
#    return nflx_traffic_and_prices
#
#
#def scatterplot(x1_data, y1_data y2_data):
#    data_1 = [Scatter(x=x_data, y=y1_data, mode='lines+markers')]
#    data_2 = [Scatter(x=x_data, y=y2_data, mode='lines+markers')]
#    title_ = 'Adjusted Closing Stock Price'
#    date_ = Date([data_1, data_2])
#    layout_ = Layout(title=title_, xaxis1=XAxis(title='Date'), yaxis1=YAxis(title='Adj Close'))
#    fig_ = Figure(data=data_, layout=layout_)
#    file_name = 'code-in-finance'
#    py.plot(fig_, filename=file_name)
#
#def plot(df1, df2):
#    py.sign_in('trankmichael','s7chu2030d')
#    scatterplot(df['Date'], df1['Adj Close'], df2)
#
#web_traffic = csv_to_dataframe()
#nflx = web_traffic_and_prices('nflx', web_traffic)
#ebay = web_traffic_and_prices('ebay', web_traffic)
#


# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:56:06 2015

@author: mumbosauce

"""

import numpy as np
from yahoo_finance import Share
from pprint import pprint

try:
    import plotly.plotly as py
    import plotly.tools as tls
    from plotly.graph_objs import *
    do_plot = True
except:
    print('Plot.ly not installed/initialized, to do so run "pip install plotly", and sign up for an account')
    do_plot = False

try: 
    import pandas as pd
    do_plot = True
except:
    print('Plot.ly not installed/initialized, to do so run "pip install pandas')
    has_pandas = False

def csv_to_dataframe(file_name):
    """ Example conversion function from comma seperated values file to pandas DataFrame"""

    if has_pandas:
        csv = np.genfromtxt(file_name, delimiter=',', dtype=str)
        df = pd.DataFrame(data=csv)
        df.columns = df.iloc[0]
        df = df.ix[1:]
        return df
    else:
        return 


def add_trace(x_s, y_s, symbol):
    if do_plot:
        new_trace = Scatter( x=x_s, y=y_s, mode='lines', name=symbol )
        data = Data( [ new_trace ] )
        plot_url = py.plot(data, filename='stock-price-example', fileopt='append')

def scatterplot(x1_data, y1_data, symbol):
    if do_plot:
        data_1 = Scatter(x=x1_data, y=y1_data, mode='lines', name=symbol)
        title_ = 'Adjusted Closing Stock Price'
        data_ = Data([data_1])
        layout_ = Layout(title=title_, xaxis1=XAxis(title='Date'), yaxis1=YAxis(title='Adj Close'))
        fig_ = Figure(data=data_, layout=layout_)
        file_name = 'stock-price-example'
        py.plot(fig_, filename=file_name)

def plot_stock(username, api_key, prices, symbol):
    if do_plot:
        py.sign_in(username, api_key)
        dates = [x['Date'] for x in prices]
        prices = [x['Adj_Close'] for x in prices]
        scatterplot(dates, prices, symbol)

start_date = '2007-01-01'
end_date = '2015-08-31'
plotly_name = 'username'
plotly_api_key = 'api-key'

# get_historical is part of the yahoo-finance module
nflx = Share('nflx')
nflx_prices = nflx.get_historical(start_date, end_date)

# how you can just extract the dates only
nflx_dates = [x['Date'] for x in nflx_prices]

# nflx_prices is currently sorted by dates because thats how the module gave them
sorted_by_price = sorted(nflx_prices, key=lambda x: x['Adj_Close'], reverse=True)

# say you wanted multiple stock prices
ticker_symbols = ['hrl', 'tsn', 'gis', 'k']
foods = {}

if do_plot:
    plot_stock(plotly_name, plotly_api_key, nflx_prices, 'nflx')

for symbol in ticker_symbols:
    foods[symbol] = Share(symbol).get_historical(start_date, end_date)
    foods[symbol].sort(key=lambda x: x['Date'])
    dates = [x['Date'] for x in foods[symbol]]
    prices = [x['Adj_Close'] for x in foods[symbol]]
    if do_plot:
        add_trace(dates, prices, symbol)



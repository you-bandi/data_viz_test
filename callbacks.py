
import requests
import plotly.express as px
from datetime import datetime, timedelta

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from data import get_crypto_list, get_historical_prices

def update_price_chart(crypto_id, time_interval, n_clicks, show_btc_prices):
    # Make an API call to retrieve the historical price data for the selected cryptocurrency and time interval
    end_date = datetime.now().strftime('%d-%m-%Y')
    start_date = (datetime.now() - timedelta(days=time_interval)).strftime('%d-%m-%Y')
        
    if show_btc_prices:
        prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')
        prices_btc, dates = get_historical_prices(crypto_id, time_interval, 'btc')
        print(f'Updating price chart for {crypto_id} with {len(prices_btc)} data points from {start_date} to {end_date}')

        yaxis_title = 'Price in USD and BTC'
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines'), secondary_y=False)
        fig.add_trace(go.Scatter(x=dates, y=prices_btc, name='Price in BTC', mode='lines'), secondary_y=True)
    else:
        prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')
        print(f'Updating price chart for {crypto_id} with {len(prices_usd)} data points from {start_date} to {end_date}')

        yaxis_title = 'Price in USD'
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines'))
        
    fig.update_layout(title=f'Historical Prices for {crypto_id}', xaxis_title='Date', yaxis_title=yaxis_title)
    
    return fig


def update_crypto_options(n_clicks):

    # Make an API call to retrieve the latest trending cryptocurrencies
    cryptocurrencies = get_crypto_list()

    options = [{'label': name, 'value': id} for id, name in cryptocurrencies]
    print(f'Updated crypto options with {len(options)} cryptocurrencies')
    
    value = cryptocurrencies[0][0]
    
    return options, value



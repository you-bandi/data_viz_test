
import requests
import plotly.express as px
from datetime import datetime, timedelta

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st

from data import get_crypto_list, get_historical_prices

def update_price_chart(n_clicks, n_intervals,  crypto_id, time_interval,  show_btc_prices, inputs):

    fig = go.Figure()
    
    # Retrieve the previous inputs from the store
    
    prev_crypto_id = inputs.get('crypto_id', 'bitcoin')
    prev_time_interval = inputs.get('time_interval', '1d')
    prev_show_btc_prices = inputs.get('show_btc_prices', [])

    # Check if the current inputs are the same as the previous inputs
    inputs_changed = (crypto_id != prev_crypto_id) or (time_interval != prev_time_interval) or (show_btc_prices != prev_show_btc_prices)

    # If the inputs haven't changed and the data is already in the store, return the stored data
    if not inputs_changed and 'prices_usd' in inputs:
        fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_usd'], name='Price in USD', mode='lines',line=dict(color='blue')))
        fig.update_layout(title=f'Historical Prices for {crypto_id}',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)')
        return fig, '', inputs
    
    # If the inputs have changed or the data is not in the store, retrieve the data from the API
    else:

        if show_btc_prices:
            prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')
            if isinstance(prices_usd, str):
                print(prices_usd)
                return None, prices_usd, inputs
            
            prices_btc, dates = get_historical_prices(crypto_id, time_interval, 'btc')
            if isinstance(prices_btc, str):
                return None, prices_btc, inputs
            
            

            yaxis_title = 'Price in USD and BTC'
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines',line=dict(color='blue')), secondary_y=False)
            fig.add_trace(go.Scatter(x=dates, y=prices_btc, name='Price in BTC', mode='lines',line=dict(color='red')), secondary_y=True)
            inputs = {'prices_btc': prices_btc}
        else:
            prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')
            if isinstance(prices_usd, str):
                return None, prices_usd, inputs
            

            yaxis_title = 'Price in USD'
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines',line=dict(color='blue')))
        
        fig.update_layout(title=f'Historical Prices for {crypto_id}', xaxis_title='Date', yaxis_title=yaxis_title)

        inputs = {'crypto_id': crypto_id, 
                  'time_interval': time_interval, 
                  'show_btc_prices': show_btc_prices, 
                  'dates': dates, 
                  'prices_usd': prices_usd
                  }
        
        
    return fig, '', inputs


def update_crypto_options(n_clicks):

    # Make an API call to retrieve the latest trending cryptocurrencies
    cryptocurrencies = get_crypto_list()

    options = [{'label': name, 'value': id} for id, name in cryptocurrencies]
    print(f'Updated crypto options with {len(options)} cryptocurrencies')
    
    value = cryptocurrencies[0][0]
    
    return options, value





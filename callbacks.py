import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objs as go
from plotly.subplots import make_subplots


from data import get_crypto_list, get_historical_prices

def update_price_chart(n_clicks, n_intervals,  crypto_id, time_interval,  show_btc_prices, inputs):

    '''
    1. First check if current inputs -> crypto_id, time_interval and show_btc_prices match the last stored set of inputs
    2. If the current inputs match last inputs and there is data in the store then return the stored data. 
    3. If not, then check if show_btc_prices toggle is ON.
    4. If its ON, then create a chart with primary axis as prices in USD and secondary axis as prices in BTC.
    5. Otherwise create chart with primary axis as prices in USD 
    6. Lastly put current inputs into the stored data so that they can be used for the next iteration
    7. This function takes care of API Limit Exceeded Error and throws out a warning for the user to wait for 60 seconds
    8. After waiting for 60 seconds the UI auto refreshes with the last input provided by the user.   
    '''

    fig = go.Figure()
    
    # Retrieve the previous inputs from the store
    prev_crypto_id = inputs.get('crypto_id', 'bitcoin')
    prev_time_interval = inputs.get('time_interval', '1d')
    prev_show_btc_prices = inputs.get('show_btc_prices', [])

    # Check if the current inputs are the same as the previous inputs
    inputs_changed = (crypto_id != prev_crypto_id) or (time_interval != prev_time_interval) or (show_btc_prices != prev_show_btc_prices)

    # If the inputs haven't changed and the data is already in the store, return the stored data
    if not inputs_changed and 'prices_usd' in inputs:
        
        if show_btc_prices and 'prices_btc' in inputs:
            yaxis_title = 'Price in USD'
            yaxis2_title = 'Price in BTC'
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_usd'], name='Price in USD', mode='lines',line=dict(color='blue')), secondary_y=False)
            fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_btc'], name='Price in BTC', mode='lines',line=dict(color='red')), secondary_y=True)
            fig.update_layout(title=f'Historical Prices for {crypto_id}', xaxis_title='Date', yaxis_title=yaxis_title,
                               yaxis2_title_text = yaxis2_title)

            return fig, '', inputs
        else:

            fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_usd'], name='Price in USD', mode='lines',line=dict(color='blue')))
            fig.update_layout(title=f'Historical Prices for {crypto_id}',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)')
            return fig, '', inputs
    
    # If the inputs have changed or the data is not in the store, retrieve the data from the API
    else:
        # Check if show_btc_prices toggle is True or not. If its True show prices in USD and BTC, otherwise just show prices in USD. 
        if show_btc_prices:

            prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')
            prices_btc, dates = get_historical_prices(crypto_id, time_interval, 'btc')
            
            # Check if API Limit Exceeded. Return the current chart and warning message to wait for 60 seconds if API limit exceeds. 
            if isinstance(prices_usd, str) or isinstance(prices_btc, str):
                
                fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_usd'], name='Price in USD', mode='lines',line=dict(color='blue')))
                fig.update_layout(title=f'Historical Prices for {prev_crypto_id}',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)')
                return fig, prices_usd, inputs
            
            # If API limit does not exceed, create a chart with primary axis as price in USD and secondary axis as price in BTC.
            yaxis_title = 'Price in USD'
            yaxis2_title = 'Price in BTC'
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines',line=dict(color='blue')), secondary_y=False)
            fig.add_trace(go.Scatter(x=dates, y=prices_btc, name='Price in BTC', mode='lines',line=dict(color='red')), secondary_y=True)
            fig.update_layout(title=f'Historical Prices for {crypto_id}', xaxis_title='Date', yaxis_title=yaxis_title,
                               yaxis2_title_text = yaxis2_title)

            # Update the price in btc to the inputs.
            inputs['prices_btc'] =  prices_btc
        
        else:
            prices_usd, dates = get_historical_prices(crypto_id, time_interval, 'usd')

            # Check if API Limit Exceeded. Return the current chart and warning message to wait for 60 seconds if API limit exceeds. 
            if isinstance(prices_usd, str):
                fig.add_trace(go.Scatter(x=inputs['dates'], y=inputs['prices_usd'], name='Price in USD', mode='lines',line=dict(color='blue')))
                fig.update_layout(title=f'Historical Prices for {prev_crypto_id}',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)')

                return fig, prices_usd, inputs
            
            # If API limit does not exceed, create a chart with primary axis as price in USD.
            yaxis_title = 'Price in USD'
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=prices_usd, name='Price in USD', mode='lines',line=dict(color='blue')))
            fig.update_layout(title=f'Historical Prices for {crypto_id}', xaxis_title='Date', yaxis_title=yaxis_title)

        inputs ['crypto_id'] =  crypto_id 
        inputs ['time_interval'] =  time_interval
        inputs ['show_btc_prices'] =  show_btc_prices
        inputs ['dates'] =  dates
        inputs ['prices_usd'] =  prices_usd
        
      
    return fig, '', inputs


def update_crypto_options(n_clicks):
    
    # Make an API call to retrieve the latest trending cryptocurrencies
    cryptocurrencies = get_crypto_list()
    if isinstance(cryptocurrencies, str):
        return {}, ''
    options = [{'label': name, 'value': id} for id, name in cryptocurrencies]
    value = cryptocurrencies[0][0]
    
    return options, value
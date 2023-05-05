import requests
import json
from datetime import datetime, timedelta
import time
import streamlit as st

def get_crypto_list():

     # make API request to retrieve list of cryptocurrencies
    trending_url = 'https://api.coingecko.com/api/v3/search/trending'

    try:
        # Retrieve the trending cryptocurrencies
        response = requests.get(trending_url)
        if response.status_code == 429:
            # The request was timed out
            return "API Request Rate Limited. Please wait for 60 seconds and then refresh again!"
            
        
        elif response.status_code == 200:
            data = response.json()
            # create a list of tuples with cryptocurrency ID and name
            cryptocurrencies = [(coin['item']['id'], coin['item']['name']) for coin in data['coins']]
        
        else:
            # Some other error occurred
            print(f"Error: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(e)
    
    return cryptocurrencies


def get_historical_prices (crypto_id, time_interval, currency):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/?vs_currency={currency}&days={time_interval}&interval=daily'
    try:
        # API Request Rate Limited (10-30 / min)
        response = requests.get(url)
        if response.status_code == 429:
            return "API Request Rate Limited, waiting 60 seconds. Will auto-refresh with last input, otherwise please refresh after 60 seconds." , 0

        elif response.status_code == 200:
            data = response.json()
            prices = data['prices']
            dates = [datetime.fromtimestamp(price[0]/1000).strftime('%Y-%m-%d') for price in prices]
            prices = [price[1] for price in prices]
        
        else:
            # Some other error occurred
            print(f"Error: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(e)
    
    return prices[:len(prices)-1], dates[:len(dates)-1]

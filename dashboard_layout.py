import dash
from dash import Dash, dcc, html, Input, Output, State

# Define the layout of the dashboard
'''
1. A dropdown to get the list of trending cryptocurrencies
2. A slider to get the number of days in the past
3. A checkbox to select if the user wants to see the prices in BTC
4. The graph showing historical price trends of the selected cryptocurrency
5. A refresh button to refresh the list of trending cryptocurrencies 
6. A few hidden components for error messages and storing previous inputs. 
'''

def get_layout(cryptocurrencies):
    layout = html.Div([
        dcc.Store(id='input-store', data={'crypto_id':'bitcoin','time_interval':'1d','show_btc_prices':False,
                                           'dates' : [], 'prices_usd':[],'prices_btc':[]}),
        html.H1('Cryptocurrency Price Dashboard',style={'margin-bottom': '10px'}),
        html.Div(id='warning-message',
                 style={'color': 'red',
                        'margin-bottom': '10px'}),
        html.Div([
            html.Label('Select Cryptocurrency',style={'margin-bottom': '100px'}),
            dcc.Dropdown(
                id='crypto-dropdown',
                options=[{'label': name, 'value': id} for id, name in cryptocurrencies],
                value='bitcoin',
                style={'margin-top': '10px'}
            ),
        ], style={'margin-bottom': '20px'}),
        html.Div([
            html.Label('Number of Days in Past'),
            dcc.Slider(
                id='time-slider',
                min=1,
                max=365,
                step=1,
                value=30,
                marks={str(i): str(i) for i in range(1, 366,10)}
            ),
        ]),
        
        html.Div([
            html.Label(''),
            dcc.Checklist(
                id='btc-prices-checkbox',
                options=[{'label': 'Also Show Prices in BTC', 'value': True}],
                value=[],
                labelStyle={'display': 'inline-block'}
            )
        ]),
        dcc.Graph(id='price-chart'),
        html.Button('Refresh', id='refresh-button'),
        
        # Create an interval to update the chart every 60 seconds
        dcc.Interval(
            id='interval-component',
            interval=60*1000,  # 60 seconds * 1000 milliseconds
            n_intervals=0
        )
        
        
    ])

    return layout
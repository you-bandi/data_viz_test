import dash
from dash import Dash, dcc, html, Input, Output, State

# Import the get_layout() function
from dashboard_layout import get_layout
from data import get_crypto_list

import callbacks

cryptocurrencies = get_crypto_list()

app = dash.Dash(__name__)
server = app.server
app.layout = get_layout(cryptocurrencies)

# Define the callback functions here

app.callback(
    [Output('price-chart', 'figure'), Output('warning-message', 'children'), Output('input-store', 'data')],
    [Input('refresh-button', 'n_clicks'), Input('interval-component', 'n_intervals'),
    Input('crypto-dropdown', 'value'), Input('time-slider', 'value'), Input('btc-prices-checkbox', 'value'),Input('input-store', 'data')],
    allow_duplicates=True
)(callbacks.update_price_chart)

app.callback(
    Output('crypto-dropdown', 'options'),
    Output('crypto-dropdown', 'value'),
    [Input('refresh-button', 'n_clicks')],
)(callbacks.update_crypto_options)


if __name__ == '__main__':
    app.run_server(debug=True)



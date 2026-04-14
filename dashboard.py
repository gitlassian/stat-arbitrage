import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from api import fetch_oanda_data
from graph import create_normalized_candlestick_chart
import os

# 1. Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "OANDA Live Stat-Arb"

# 2. Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Live OANDA Stat-Arb Dashboard", className="text-center mt-4"),
            html.P("Fetching data every 5 seconds...", className="text-center text-muted"),
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='live-graph', style={'height': '80vh'}),
        ])
    ]),
    
    # Interval Component: 5 seconds = 5000 milliseconds
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000, 
        n_intervals=0
    )
], fluid=True)

# 3. Callbacks
@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_live(n):
    oanda_symbols = ["WTICO_USD", "BCO_USD"]
    color_pairs = [
        ["#00FF00", "#FF007F"], 
        ["#00FFFF", "#FFD700"]
    ]

    all_data = []
    all_symbols = []

    for symbol in oanda_symbols:
        # Granularity S5 for fast updates
        df = fetch_oanda_data(symbol, count=25, granularity="S5")
        if not df.empty:
            all_data.append(df)
            all_symbols.append(f"OANDA:{symbol}")

    if not all_data:
        return {} # Return empty fig if no data

    # Reuse the same graphing function from graph.py
    fig = create_normalized_candlestick_chart(
        all_data, 
        all_symbols, 
        color_pairs, 
        title=f"OANDA Stat-Arb | Update #{n}"
    )
    
    # Ensure smooth transition - optional, adjust layout for real-time
    fig.update_layout(uirevision='constant') # This prevents the zoom/view from resetting on every update
    
    return fig

# 4. Run Server
if __name__ == '__main__':
    # Run by default on port 8050
    # You can change to any port you want, e.g. port=8888
    port = int(os.environ.get("PORT", 8050))
    print(f"Starting dashboard on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)

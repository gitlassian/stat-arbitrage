import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from decimal import Decimal
import time

start_time = time.time_ns()

ticker_symbol1 = "GBPJPY=X"
ticker_symbol2 = "EURJPY=X"

color_pairs = [
    ["red", "green"],
    ["blue", "yellow"],
    ["cyan", "gray"],
    ["magenta", "orange"],
]

tickers_symbols = [ticker_symbol1, ticker_symbol2]

fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.05)

for ticker_symbol, row in zip(tickers_symbols, range(0, len(tickers_symbols))):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(start="2026-01-22", end="2026-01-23", interval="5m")

    start_point = Decimal(str(data.iloc[0]["Open"]))
    print(start_point)

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"].apply(lambda x: Decimal(str(x)) / start_point),
            high=data["High"].apply(lambda x: Decimal(str(x)) / start_point),
            low=data["Low"].apply(lambda x: Decimal(str(x)) / start_point),
            close=data["Close"].apply(lambda x: Decimal(str(x)) / start_point),
            name=ticker_symbol,
            increasing_line_color=color_pairs[row][0],
            decreasing_line_color=color_pairs[row][1],
        ),
        row=1,
        col=1,
    )

fig.update_layout(xaxis_rangeslider_visible=False, height=800, title_text="Comparison")
fig.show()

end_time = time.time_ns()
print(f"Time taken: {(end_time - start_time) / 1e9} s")

import yfinance as yf
import plotly.graph_objects as go

# Define the ticker symbol (In my case Apple)
ticker_symbol1 = "AAPL"


# Create a Ticker object
ticker = yf.Ticker(ticker_symbol)

tickers = [ticker]

# Fetch historical market data
for ticker in tickers:
    data = ticker.history(period="25y")  # data for the last 25 years
    print(data.keys())


fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'])
                     ])
                     
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()

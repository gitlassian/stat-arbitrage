import os
import pandas as pd
import yfinance as yf
import requests
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from dotenv import load_dotenv

load_dotenv()

def fetch_oanda_data(symbol, count=100, granularity="M5"):
    """
    Fetch historical candle data from OANDA API.
    """
    api_key = os.getenv("OANDA_API_KEY")
    if not api_key:
        raise ValueError("OANDA_API_KEY not found in environment variables.")
        
    client = API(access_token=api_key)
    params = {
        "count": count,
        "granularity": granularity
    }
    
    r = instruments.InstrumentsCandles(instrument=symbol, params=params)
    client.request(r)
    
    raw_data = []
    for candle in r.response['candles']:
        if candle['complete']:
            raw_data.append({
                'time': candle['time'],
                'open': float(candle['mid']['o']),
                'high': float(candle['mid']['h']),
                'low': float(candle['mid']['l']),
                'close': float(candle['mid']['c'])
            })
    
    df = pd.DataFrame(raw_data)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'])
    return df

def fetch_yfinance_data(symbol, start=None, end=None, period="1mo", interval="1m"):
    """
    Fetch historical data from Yahoo Finance.
    """
    ticker = yf.Ticker(symbol)
    if start and end:
        data = ticker.history(start=start, end=end, interval=interval)
    else:
        data = ticker.history(period=period, interval=interval)
    
    # Standardize column names to lowercase to match OANDA format
    data = data.reset_index()
    data.columns = [c.lower() for c in data.columns]
    if 'date' in data.columns:
        data = data.rename(columns={'date': 'time'})
    elif 'datetime' in data.columns:
        data = data.rename(columns={'datetime': 'time'})
        
    return data

def fetch_alpha_vantage_data(symbol, interval="5min", outputsize="compact"):
    """
    Fetch historical data from Alpha Vantage.
    interval: '1min', '5min', '15min', '30min', '60min', 'daily'
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment variables.")
    
    if interval == 'daily':
        function = "TIME_SERIES_DAILY"
        series_key = "Time Series (Daily)"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&apikey={api_key}"
    else:
        function = "TIME_SERIES_INTRADAY"
        series_key = f"Time Series ({interval})"
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={api_key}"
        
    r = requests.get(url)
    data = r.json()
    
    if series_key not in data:
        err_msg = data.get('Error Message') or data.get('Note') or data.get('Information') or data.get('message') or str(data)
        raise ValueError(f"Alpha Vantage API error: {err_msg}")
            
    raw_data = []
    for timestamp, values in data[series_key].items():
        raw_data.append({
            'time': timestamp,
            'open': float(values['1. open']),
            'high': float(values['2. high']),
            'low': float(values['3. low']),
            'close': float(values['4. close']),
            'volume': float(values.get('5. volume', 0))
        })
        
    df = pd.DataFrame(raw_data)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values('time')
    return df

def fetch_polygon_data(symbol, multiplier=1, timespan="minute", from_date="2023-01-01", to_date="2023-01-02"):
    """
    Fetch historical data from Polygon.io.
    """
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        raise ValueError("POLYGON_API_KEY not found in environment variables.")
        
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}?adjusted=true&sort=asc&apiKey={api_key}"
    r = requests.get(url)
    data = r.json()
    
    if 'results' not in data:
        err_msg = data.get('message') or data.get('error') or data.get('status') or str(data)
        raise ValueError(f"Polygon API error: {err_msg}")
        
    raw_data = []
    for item in data['results']:
        raw_data.append({
            'time': item['t'], # Unix timestamp in milliseconds
            'open': item['o'],
            'high': item['h'],
            'low': item['l'],
            'close': item['c'],
            'volume': item['v']
        })
        
    df = pd.DataFrame(raw_data)
    if not df.empty:
        df['time'] = pd.to_datetime(df['time'], unit='ms')
    return df
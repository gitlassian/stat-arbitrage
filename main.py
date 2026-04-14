import time
from api import fetch_oanda_data, fetch_yfinance_data, fetch_alpha_vantage_data, fetch_polygon_data
from graph import create_normalized_candlestick_chart

def main():
    start_time = time.time_ns()

    # Configuration
    oanda_symbols = ["GBP_JPY", "EUR_JPY"]
    yf_symbols = ["USDTRY=X"] # Example mix
    
    color_pairs = [
        ["#00FF00", "#FF007F"], # Neon Green / Hot Pink
        ["#00FFFF", "#FFD700"], # Cyan / Gold
        ["#FFFFFF", "#AAAAAA"]  # White / Gray for YF
    ]

    all_data = []
    all_symbols = []

    # 1. Fetch OANDA data
    for symbol in oanda_symbols:
        print(f"Fetching OANDA data for {symbol}...")
        df = fetch_oanda_data(symbol, count=50, granularity="S5")
        if not df.empty:
            all_data.append(df)
            all_symbols.append(f"OANDA:{symbol}")

    # 2. Fetch yfinance data (example)
    # for symbol in yf_symbols:
    #     print(f"Fetching yfinance data for {symbol}...")
    #     # Note: adjust period/interval as needed to overlap with OANDA
    #     df = fetch_yfinance_data(symbol, period="5d", interval="5m")
    #     if not df.empty:
    #         all_data.append(df)
    #         all_symbols.append(f"YF:{symbol}")

    # 3. Fetch Alpha Vantage data (example)
    print("Fetching Alpha Vantage data for IBM...")
    df_av = fetch_alpha_vantage_data("IBM", interval="daily")
    if not df_av.empty:
        all_data.append(df_av)
        all_symbols.append("AV:IBM")

    # 4. Fetch Polygon.io data (example)
    print("Fetching Polygon data for AAPL...")
    df_poly = fetch_polygon_data("AAPL", multiplier=1, timespan="minute", from_date="2025-01-09", to_date="2025-01-10")
    if not df_poly.empty:
        all_data.append(df_poly)
        all_symbols.append("POLYGON:AAPL")

    # 5. Create Graph
    if all_data:
        fig = create_normalized_candlestick_chart(
            all_data, 
            all_symbols, 
            color_pairs, 
            title="OANDA vs yfinance Comparison (Normalized)"
        )
        fig.show()
    else:
        print("No data fetched.")

    end_time = time.time_ns()
    print(f"Time taken: {(end_time - start_time) / 1e9} s")

if __name__ == "__main__":
    main()
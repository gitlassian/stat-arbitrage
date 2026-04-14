import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_normalized_candlestick_chart(data_list, symbols, color_pairs, title="Stat-Arb Comparison (Normalized)"):
    """
    data_list: List of pandas DataFrames (must have time, open, high, low, close)
    symbols: List of symbol names corresponding to data_list
    color_pairs: List of [increasing_color, decreasing_color] for each trace
    """
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)

    for i, (df, symbol) in enumerate(zip(data_list, symbols)):
        if df.empty:
            continue
            
        # Normalization (Start at first 'open' point)
        start_point = df.iloc[0]["open"]
        
        # Determine colors (fallback if not enough pairs)
        increasing = color_pairs[i % len(color_pairs)][0]
        decreasing = color_pairs[i % len(color_pairs)][1]

        fig.add_trace(
            go.Candlestick(
                x=df["time"],
                open=df["open"] / start_point,
                high=df["high"] / start_point,
                low=df["low"] / start_point,
                close=df["close"] / start_point,
                name=symbol,
                increasing_line_color=increasing,
                decreasing_line_color=decreasing,
            )
        )

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False, 
        height=800, 
        title_text=title,
        yaxis_title="Normalized Price"
    )
    
    return fig

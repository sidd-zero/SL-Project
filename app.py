import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Stock Market Intelligence Dashboard", layout="wide")
st.title("📈 Real-Time Stock Market Intelligence Dashboard")

# --- SIDEBAR: USER INPUTS ---
st.sidebar.header("Dashboard Controls")
company_to_ticker = {
    "Tesla": "TSLA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta": "META",
}

selected_company = st.sidebar.selectbox(
    "Quick Select Company",
    ["Custom"] + list(company_to_ticker.keys()),
    index=1,
)

default_ticker = company_to_ticker.get(selected_company, "TSLA")
if selected_company != "Custom":
    st.sidebar.caption(f"Selected company: {selected_company} ({default_ticker})")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker (e.g., TSLA, AAPL, GOOGL)",
    default_ticker,
).strip().upper()
time_period = st.sidebar.selectbox("Select Time Period", ["1mo", "6mo", "1y"], index=2)

# --- DATA FETCHING FUNCTION ---
@st.cache_data
def load_data(symbol, period):
    df = yf.download(symbol, period=period, interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

data = load_data(ticker, time_period)

# --- MAIN DASHBOARD ---
if data is None or data.empty:
    st.warning(f"No data found for ticker '{ticker}' and period '{time_period}'. Please check the ticker symbol or try a different time period.")
else:

    # --- METRIC CARDS ---
    if 'Close' in data.columns and 'Volume' in data.columns:
        current_price = float(data['Close'].iloc[-1].item() if hasattr(data['Close'].iloc[-1], "item") else data['Close'].iloc[-1])
        if len(data) > 1:
            prev_close = float(data['Close'].iloc[-2].item() if hasattr(data['Close'].iloc[-2], "item") else data['Close'].iloc[-2])
            daily_change = ((current_price - prev_close) / prev_close) * 100
        else:
            prev_close = current_price
            daily_change = 0
        volume = float(data['Volume'].iloc[-1].item() if hasattr(data['Volume'].iloc[-1], "item") else data['Volume'].iloc[-1])

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${current_price:,.2f}")
        col2.metric("Daily Change (%)", f"{daily_change:+.2f}%")
        col3.metric("Trading Volume", f"{volume:,.0f}")

        # Extra factors that are useful during analysis and presentation.
        rolling_window = min(len(data), 252)
        high_52w = float(data['High'].tail(rolling_window).max())
        low_52w = float(data['Low'].tail(rolling_window).min())
        annualized_volatility = float(data['Close'].pct_change().std() * (252 ** 0.5) * 100)

        st.subheader("Other Factors Snapshot")
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("Previous Close", f"${prev_close:,.2f}")
        f2.metric("52-Week High", f"${high_52w:,.2f}")
        f3.metric("52-Week Low", f"${low_52w:,.2f}")
        f4.metric("Annualized Volatility", f"{annualized_volatility:.2f}%")
    else:
        st.warning("Data does not contain 'Close' or 'Volume' columns.")

    # --- CANDLESTICK CHART WITH MOVING AVERAGES ---
    st.subheader(f"Price Action & Technical Trend: {ticker}")
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    fig = go.Figure()
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="OHLC",
        increasing_line_color='lime', decreasing_line_color='red'
    ))
    # MA50
    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA50'],
        mode='lines', name='MA50', line=dict(color='orange', width=2, dash='dash')
    ))
    # MA200
    fig.add_trace(go.Scatter(
        x=data.index, y=data['MA200'],
        mode='lines', name='MA200', line=dict(color='cyan', width=2, dash='dot')
    ))
    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=True,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- MULTIVARIATE CORRELATION HEATMAP ---
    st.subheader("Market Correlation (Closing Prices)")
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    compare_tickers = st.multiselect(
        "Select Tickers to Compare", default_tickers, default=["AAPL", "TSLA"]
    )
    if compare_tickers:
        corr_data = yf.download(compare_tickers, period=time_period, interval="1d", progress=False)['Close']
        if isinstance(corr_data, pd.Series):
            corr_data = corr_data.to_frame()
        if corr_data.isnull().all().all():
            st.warning("No data available for the selected tickers and period.")
        else:
            corr_matrix = corr_data.corr()
            fig2, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax, fmt=".2f")
            ax.set_title("Correlation Heatmap of Closing Prices")
            st.pyplot(fig2)

    # --- DATA PREVIEW (OPTIONAL) ---
    with st.expander("Show Raw Data Table"):
        st.dataframe(data.tail(30), use_container_width=True)
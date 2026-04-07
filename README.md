# Stock Market Intelligence Dashboard

This project is a Streamlit dashboard for real-time stock analysis using Yahoo Finance data.

It helps you:
- Track a selected stock (price, daily change, volume)
- View candlestick charts with moving averages (MA50 and MA200)
- Compare multiple stocks with a correlation heatmap
- Review additional market factors (previous close, 52-week high/low, annualized volatility)

## 1. Project Structure

- `app.py`: Main Streamlit application
- `requirements.txt`: Python dependencies

## 2. Prerequisites

- Python 3.10+ (you are already using a virtual environment)
- Internet connection (required for Yahoo Finance data)

## 3. Install Dependencies

From the project folder:

```powershell
pip install -r requirements.txt
```

If your virtual environment is active, this installs packages into that environment.

## 4. Run the Dashboard

Use Streamlit (not plain Python):

```powershell
streamlit run app.py
```

After running this command, Streamlit opens a local URL in your browser.

## 5. How to Use the App

1. Use **Quick Select Company** in the sidebar for correctly spelled names like Tesla, Apple, Microsoft, etc.
2. Optionally type a custom ticker symbol (example: `TSLA`, `AAPL`, `GOOGL`).
3. Choose a time period (`1mo`, `6mo`, or `1y`).
4. Review top metrics:
   - Current Price
   - Daily Change (%)
   - Trading Volume
5. Review **Other Factors Snapshot**:
   - Previous Close
   - 52-Week High
   - 52-Week Low
   - Annualized Volatility
6. Analyze the candlestick chart and moving averages.
7. Use the correlation section to compare multiple stocks.
8. Expand **Show Raw Data Table** for latest rows.

## 6. What Was Improved

- Added a quick company selector with correct spellings:
  - Tesla, Apple, Microsoft, Alphabet (Google), Amazon, NVIDIA, Meta
- Added an **Other Factors Snapshot** section for richer analysis.
- Improved data handling for edge cases when data shape changes.
- Reduced noisy download output during fetch operations.

## 7. Presentation Script (Tomorrow)

Use this short flow while presenting:

1. "This dashboard provides real-time market intelligence for stocks."
2. "I can quickly select a company like Tesla or Apple, or manually enter any ticker."
3. "The top cards summarize price action and market activity."
4. "The candlestick chart plus MA50/MA200 helps identify trends."
5. "The other factors section adds risk and range context with volatility and 52-week levels."
6. "The heatmap compares stocks and shows how strongly they move together."
7. "Raw data is also available for transparency and validation."

## 8. Troubleshooting

- If app does not open: rerun `streamlit run app.py`.
- If data is missing: verify ticker symbol and internet connection.
- If dependencies fail: run `pip install -r requirements.txt` again.

## 9. Future Enhancements

- Add RSI, MACD, and Bollinger Bands
- Add downloadable PDF or CSV reports
- Add portfolio tracking and watchlist support

## 10. Deploy to GitHub (Step by Step)

Follow these commands in your project folder:

1. Initialize Git (already done in this project):

```powershell
git init
```

2. Create commits one by one:

```powershell
git add .gitignore
git commit -m "chore: add python gitignore"

git add app.py requirements.txt
git commit -m "feat: add stock dashboard with technical and correlation analysis"

git add README.md
git commit -m "docs: add complete usage and presentation guide"
```

3. Create an empty repository on GitHub, then connect it:

```powershell
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Replace `<your-username>` and `<your-repo-name>` with your actual values.

## 11. Dashboard Factors Explained

Your dashboard currently covers these key factors:

- Current Price: Latest closing value of the selected stock.
- Daily Change (%): Percentage movement from previous close to current close.
- Trading Volume: Number of shares traded in the latest session.
- Previous Close: Last session's closing value.
- 52-Week High: Highest price observed in roughly the last 252 trading days.
- 52-Week Low: Lowest price observed in roughly the last 252 trading days.
- Annualized Volatility: Risk indicator derived from daily returns and scaled to yearly terms.
- MA50 and MA200: Short- and long-term moving averages for trend direction.
- Correlation Heatmap: Measures how selected stocks move together over the chosen time period.

## 12. Quick Presentation Flow (2-3 Minutes)

1. Start with the objective: real-time stock monitoring and trend insight.
2. Show Quick Select Company using names like Tesla and Apple.
3. Explain top metrics and Other Factors Snapshot.
4. Walk through candlestick chart and MA50/MA200 trend lines.
5. Show correlation heatmap and explain diversification insight.
6. End with how this can be extended with RSI/MACD and alerts.

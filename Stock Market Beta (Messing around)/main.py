import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIG ---
ticker = "AAPL"
benchmark = "^GSPC"
start_date = "2022-01-01"
end_date = "2024-01-01"
window_size = 30

# --- DATA FETCH ---
stock_data = yf.download(ticker, start=start_date, end=end_date)["Close"]
benchmark_data = yf.download(benchmark, start=start_date, end=end_date)["Close"]

# --- RETURNS ---
returns = pd.concat([benchmark_data.pct_change(), stock_data.pct_change()], axis=1)
returns.columns = ["SP500", ticker]
returns.dropna(inplace=True)

# --- ROLLING METRICS ---
betas, alphas, corrs, tracking_errors, r_squared = [], [], [], [], []
dates = []

for i in range(window_size, len(returns)):
    window = returns.iloc[i-window_size:i]
    x = window["SP500"]
    y = window[ticker]
    
    cov = np.cov(x, y)[0][1]
    var = np.var(x)
    beta = cov / var if var != 0 else np.nan
    
    alpha = np.mean(y - beta * x)
    corr = np.corrcoef(x, y)[0][1]
    tracking_err = np.sqrt(np.mean((y - x) ** 2))
    
    # R-squared from linear regression
    residuals = y - (beta * x + alpha)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan

    betas.append(beta)
    alphas.append(alpha)
    corrs.append(corr)
    tracking_errors.append(tracking_err)
    r_squared.append(r2)
    dates.append(returns.index[i])

# --- CREATE DF ---
metrics_df = pd.DataFrame({
    "Date": dates,
    "Beta": betas,
    "Alpha": alphas,
    "Correlation": corrs,
    "Tracking Error": tracking_errors,
    "R-Squared": r_squared
}).set_index("Date")

# --- DISPLAY UI SUMMARY ---
print("\n📊 Summary of Rolling 30-day Metrics for", ticker)
print(metrics_df.describe().round(4))

# --- PLOTTING ---
metrics_df.plot(figsize=(12, 8), title=f"{ticker} vs S&P 500 - Rolling {window_size}-Day Metrics")
plt.grid(True)
plt.tight_layout()
plt.show()
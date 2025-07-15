import yfinance as yf
import matplotlib.pyplot as plt

ticker = 'AAPL'  
data = yf.download(ticker, period='1mo', interval='1d')



# Plot the closing prices
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label=f"{ticker} Close")
plt.title(f"{ticker} Closing Prices - Last 6 Months")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
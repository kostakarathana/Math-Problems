import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Download data
sp500 = yf.download("^GSPC", start="2022-01-01", end="2024-01-01")["Close"]
stock = yf.download("AAPL", start="2022-01-01", end="2024-01-01")["Close"]

# Calculate returns
returns = pd.concat([sp500.pct_change(), stock.pct_change()], axis=1)
returns.columns = ["SP500", "AAPL"]
returns.dropna(inplace=True)

# Rolling beta
window_size = 30
betas = []
dates = []

for i in range(window_size, len(returns)):
    window = returns.iloc[i-window_size:i]
    cov = window.cov().iloc[0,1]
    var = window["SP500"].var()
    beta = cov / var
    betas.append(beta)
    dates.append(returns.index[i])

# 3D plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Convert time to numerical axis
time_axis = np.arange(len(betas))
y_axis = np.zeros(len(betas))  # all from same stock
z_axis = betas

ax.plot(time_axis, y_axis, z_axis, label="Rolling Beta (AAPL vs S&P)", color='b')

ax.set_xlabel('Time')
ax.set_ylabel('Stock (AAPL)')
ax.set_zlabel('Beta')
ax.set_title("Rolling 30-day Beta of AAPL vs S&P 500")

plt.show()
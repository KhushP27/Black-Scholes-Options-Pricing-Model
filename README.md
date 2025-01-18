# Black-Scholes-Options-Pricing-Model
This Streamlit app provides a user-friendly interface for visualizing option prices calculated using the Black-Scholes model. The app generates interactive heatmaps for call and put option prices based on user-defined inputs, allowing users to explore the relationship between stock prices, volatilities, and option prices.

## Key Features
#### Single Option Price Calculation:
- Calculate the price of a single call or put option based on user inputs for spot price, strike price, volatility, time to expiration, and risk-free interest rate.

#### Heatmap Visualization:
- Generate dynamic heatmaps for call and put option prices over a range of stock prices and volatilities.

#### Profit and Loss (P&L) Heatmaps:
- Input custom call and put prices to visualize potential profit or loss (P&L) across stock prices and volatilities.

#### Interactive Controls:
- Customize ranges for spot prices, volatilities, and other parameters using an intuitive sidebar.

## Required Packages:
numpy pandas seaborn matplotlib streamlit scipy

### How to run
1. Download BlackScholes.py
2. Run: pip install -r requirements.txt
3. Run: streamlit run BlackScholes.py



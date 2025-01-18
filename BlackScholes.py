import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm
from matplotlib.colors import LinearSegmentedColormap

# Add this at the very top of your script, after the imports
st.set_page_config(layout="wide")

# Sample Data for Heatmap
def calculate_call_price(spot, vol, strike, time, risk):
    call_data = []
    for v in vol: # Loop now iterates over volatilities in rows
        call_row = []
        for price in spot:
            # Black-Scholes Call Option Price Calculation
            call_price = price * norm.cdf((np.log(price / strike) + (risk + 0.5 * v**2) * time) / (v * np.sqrt(time))) - \
                        strike * np.exp(-risk * time) * norm.cdf((np.log(price / strike) + (risk - 0.5 * v**2) * time) / (v * np.sqrt(time)))
            call_row.append(call_price)
        call_data.append(call_row)
    return pd.DataFrame(call_data, index=vol, columns=spot)

def calculate_put_price(spot, vol, strike, time, risk):
    put_data = []
    for v in vol:
        put_row = []
        for price in spot:
            # Black-Scholes Put Option Price Calculation
            put_price = strike * np.exp(-risk * time) * norm.cdf(-(np.log(price/strike) + (risk - 0.5 * v**2) * time) / (v * np.sqrt(time))) - \
                       price * norm.cdf(-(np.log(price/strike) + (risk + 0.5 * v**2) * time) / (v * np.sqrt(time)))
            put_row.append(put_price)
        put_data.append(put_row)
    return pd.DataFrame(put_data, index=vol, columns=spot)

# Heatmap Function
def plot_heatmap(data, title_suffix=""):
    plt.figure(figsize=(10, 8))
    
    # Use different colormaps for P&L vs regular price heatmaps
    if "P&L" in title_suffix:
        # Create custom colormap: red for negative, white for zero, green for positive
        colors = [(0.8, 0, 0), (1, 1, 1), (0, 0.8, 0)]  # dark red to white to dark green
        n_bins = 100  # More bins for smooth transition
        cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
        center = 0
    else:
        # For regular price heatmaps, use viridis (no center needed)
        cmap = "viridis"
        center = None
    
    ax = sns.heatmap(data, annot=True, cmap=cmap, fmt=".2f", 
                     cbar_kws={'label': 'Option Price'},
                     center=center)
    ax.set_xticklabels([f'{x:.2f}' for x in data.columns])
    ax.set_yticklabels([f'{x:.2f}' for x in data.index])
    ax.set_ylabel('Volatility')
    ax.set_xlabel('Stock Price')
    plt.title(f"Option Price Heatmap {title_suffix}")
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit Stuff

# Streamlit App
st.title("Black-Scholes Option Heatmap")

# User Inputs
st.sidebar.header("Inputs")

# Inputs for specific option calculation
st.sidebar.header("Single Option Parameters")
strike = st.sidebar.number_input("Strike Price", min_value=1.0, max_value=200.0, value=120.0, step=1.0)
time = st.sidebar.number_input("Time to Expiration (years)", min_value=0.1, max_value=2.0, value=1.00, step=0.1)
risk_free_interest_rate = st.sidebar.number_input("Risk Free Interest Rate", min_value=0.01, max_value=1.0, value=0.05, step=0.01)
volatility = st.sidebar.number_input("Volatility", min_value=0.01, max_value=1.00, value=0.20, step=0.01)
spot = st.sidebar.number_input("Spot Price", min_value=1.0, max_value=200.0, value=100.0, step=1.0)

# Calculate single option prices directly using Black-Scholes formulas
d1 = (np.log(spot/strike) + (risk_free_interest_rate + 0.5 * volatility**2) * time) / (volatility * np.sqrt(time))
d2 = d1 - volatility * np.sqrt(time)

# Single call and put prices from the given inputs
single_call_price = spot * norm.cdf(d1) - strike * np.exp(-risk_free_interest_rate * time) * norm.cdf(d2)
single_put_price = strike * np.exp(-risk_free_interest_rate * time) * norm.cdf(-d2) - spot * norm.cdf(-d1)

# Display single option (put and call) prices
st.markdown("""
    <div style='padding: 20px; border: 2px solid #f0f2f6; border-radius: 10px; margin-bottom: 20px; text-align: center;'>
        <h2>Current Option Prices</h2>
        <h3 style='display: inline-block; margin: 0 20px;'>Call Option Price: ${:.2f}</h3>
        <h3 style='display: inline-block; margin: 0 20px;'>Put Option Price: ${:.2f}</h3>
    </div>
""".format(single_call_price, single_put_price), unsafe_allow_html=True)

# Inputs for heatmap ranges
st.sidebar.markdown("### Heatmap Parameters")
spot_price_range = st.sidebar.slider("Stock Price Range for Heatmap", 50, 200, (80, 120), step=10)
volatility_range = st.sidebar.slider("Volatility Range for Heatmap (0-1)", 0.1, 1.0, (0.1, 0.3), step=0.1)

# Inputs for call and put prices set by user
user_call = st.sidebar.number_input("Input Call Price", value=None)
user_put = st.sidebar.number_input("Input Put Price", value=None)

# Generate Data
spot_prices = np.linspace(spot_price_range[0], spot_price_range[1], 10) # Takes 10 evenly spaced spot prices in the spot range specified by the user
volatilities = np.linspace(volatility_range[0], volatility_range[1], 10) # Takes 10 evenly spaced volatilies in the volatility range specified by the user

# Call and Put Data Calculations
call_data = calculate_call_price(spot_prices, volatilities, strike, time, risk_free_interest_rate)
put_data = calculate_put_price(spot_prices, volatilities, strike, time, risk_free_interest_rate)

# Plot the original heatmaps in columns
col1, col2 = st.columns(2)

# Plot call options in first column
with col1:
    st.write("### Call Option Prices")
    plot_heatmap(call_data)

# Plot put options in second column
with col2:
    st.write("### Put Option Prices")
    plot_heatmap(put_data)

# Plot the P&L Heatmaps in columns if user inputs exist
if user_call is not None or user_put is not None:
    pnl_col1, pnl_col2 = st.columns(2)
    
    # Plot call P&L in first column if user_call exists
    with pnl_col1:
        if user_call is not None:
            st.write("### Call Option P&L")
            call_pnl = call_data - user_call
            plot_heatmap(call_pnl, title_suffix="(P&L)")
    
    # Plot put P&L in second column if user_put exists
    with pnl_col2:
        if user_put is not None:
            st.write("### Put Option P&L")
            put_pnl = put_data - user_put
            plot_heatmap(put_pnl, title_suffix="(P&L)")

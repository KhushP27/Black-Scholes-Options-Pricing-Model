import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import norm

# Add this at the very top of your script, after the imports
st.set_page_config(layout="wide")

# Sample Data for Heatmap
def calculate_call_price(spot, vol, strike, time, risk):
    call_data = []
    for price in spot:
        call_row = []
        for v in vol:
            # Black-Scholes Call Option Price Calculation
            call_price = price * norm.cdf((np.log(price / strike) + (risk + 0.5 * v**2) * time) / (v * np.sqrt(time))) - \
                        strike * np.exp(-risk * time) * norm.cdf((np.log(price / strike) + (risk - 0.5 * v**2) * time) / (v * np.sqrt(time)))
            call_row.append(call_price)
        call_data.append(call_row)
    return pd.DataFrame(call_data, index=spot, columns=vol)

def calculate_put_price(spot, vol, strike, time, risk):
    put_data = []
    for price in spot:
        put_row = []
        for v in vol:
            # Black-Scholes Put Option Price Calculation
            put_price = strike * np.exp(-risk * time) * norm.cdf(-(np.log(price / strike) + (risk + 0.5 * v**2) * time) / (v * np.sqrt(time))) - \
                       price * norm.cdf(-(np.log(price / strike) + (risk + 0.5 * v**2) * time) / (v * np.sqrt(time)))
            put_row.append(put_price)
        put_data.append(put_row)
    return pd.DataFrame(put_data, index=spot, columns=vol)

# Heatmap Function
def plot_heatmap(data, title_suffix=""):
    plt.figure(figsize=(15, 12))
    ax = sns.heatmap(data, annot=True, cmap="coolwarm", fmt=".2f", 
                     cbar_kws={'label': 'Option Price'})
    ax.set_xticklabels([f'{x:.2f}' for x in data.columns])
    ax.set_yticklabels([f'{x:.2f}' for x in data.index])
    ax.set_xlabel('Volatility')
    ax.set_ylabel('Stock Price')
    plt.title(f"Option Price Heatmap {title_suffix}")
    st.pyplot(plt)

# Streamlit Stuff

# Streamlit App
st.title("Black-Scholes Option Heatmap")

# User Inputs
st.sidebar.header("Inputs")

# Pre-set strike, time, and risk values
strike = st.sidebar.number_input("Strike Price", min_value=0, max_value=200, value=100)
time = st.sidebar.number_input("Time to Expiration (years)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
risk_free_interest_rate = st.sidebar.number_input("Risk Free Interest Rate", min_value=0.01, max_value=1.0, value=0.05, step=0.01)

spot_price_range = st.sidebar.slider("Stock Price Range", 50, 200, (50, 150), step=10) # Slider to change the range of spot prices
volatility_range = st.sidebar.slider("Volatility Range (0-1)", 0.1, 1.0, (0.1, 0.5), step=0.1) # Slider to change the range of volatilities

# Generate Data
spot_prices = np.linspace(spot_price_range[0], spot_price_range[1], 10) # Takes 10 evenly spaced spot prices in the spot range specified by the user
volatilities = np.linspace(volatility_range[0], volatility_range[1], 10) # Takes 10 evenly spaced volatilies in the volatility range specified by the user

# Call and Put Data Calculations
call_data = calculate_call_price(spot_prices, volatilities, strike, time, risk_free_interest_rate)
put_data = calculate_put_price(spot_prices, volatilities, strike, time, risk_free_interest_rate)

# Create two columns
col1, col2 = st.columns(2)

# Plot call options in first column
with col1:
    st.write("### Call Option Prices")
    plot_heatmap(call_data)

# Plot put options in second column
with col2:
    st.write("### Put Option Prices")
    plot_heatmap(put_data)
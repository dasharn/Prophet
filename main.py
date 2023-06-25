import numpy as np
import pandas as pd
import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import time

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

n_years = st.sidebar.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache_data
def get_historical_data(tickers):
    data = pd.DataFrame()
    for ticker in tickers:
        stock_data = yf.download(ticker, START, TODAY)
        stock_data.reset_index(inplace=True)
        stock_data['Ticker'] = ticker  # Add a column to track the stock ticker
        data = pd.concat([data, stock_data], ignore_index=True)

    # Convert the 'Date' column to datetime type
    data['Date'] = pd.to_datetime(data['Date'])

    return data


def plot_historical_data(data):
    if data.empty:
        st.write("No stock data available.")
        return

    if 'Ticker' in data.columns:
        for ticker, stock_data in data.groupby('Ticker'):
            st.subheader(f"Raw data for {ticker}")
            st.dataframe(stock_data)
    else:
        st.subheader("Raw data")
        st.dataframe(data)


# Using forecasting algorithm used by Facebook
@st.cache_data
def predict_forecast(data):
    forecasts = {}
    models = {}
    accuracies = {}
    for ticker, stock_data in data.groupby('Ticker'):
        df_train = stock_data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        m = Prophet()
        m.fit(df_train)

        # Calculate accuracy on training data
        future = m.make_future_dataframe(periods=0)  # Use training data for accuracy calculation
        forecast = m.predict(future)
        #assessing percentage different of calculated value from true
        accuracy = np.mean(np.abs(forecast['yhat'].values - df_train['y'].values) / df_train['y'].values) * 100
        accuracies[ticker] = accuracy

        # Make future predictions
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        forecasts[ticker] = forecast
        models[ticker] = m
    return forecasts, models, accuracies

def plot_forecast(forecasts, models, accuracies):
    st.subheader('Forecast data')

    display_option = st.sidebar.radio('Display Option', ('Forecast Plot', 'Forecast Components', 'Forecast Table', 'Forecast Data'))

    if display_option == 'Forecast Plot':
        st.write(f'Forecast plot for {n_years} years')
        fig1 = go.Figure()
        for ticker, model in models.items():
            fig1.add_trace(go.Scatter(x=forecasts[ticker]['ds'], y=forecasts[ticker]['yhat'], name=ticker))
        fig1.layout.update(title_text='Forecast', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig1)

        st.write('Accuracy:')
        for ticker, accuracy in accuracies.items():
            st.write(f'{ticker}: {accuracy:.2f}%')


    elif display_option == 'Forecast Components':
        for ticker, model in models.items():
            st.write(f"Forecast components - {ticker}")
            fig2 = model.plot_components(forecasts[ticker])
            st.write(fig2)

    elif display_option == 'Forecast Table':
        for ticker, forecast in forecasts.items():
            st.write(f'Forecast table for {ticker}')
            st.write(forecast)

    

def main():
    st.sidebar.title('Prophet - Your Stock Prediction App')

    stocks = {
        'Google': 'GOOGL',
        'Microsoft': 'MSFT',
        'Amazon': 'AMZN',
        'Apple': 'AAPL',
        'Palantir': 'PLTR'
    }

    page = st.sidebar.selectbox('Select Page', ('Historical Data', 'Forecast'))

    if page == 'Historical Data':
        st.title('Historical Stock Data')
        selected_stocks = st.sidebar.multiselect('Select stocks', list(stocks.keys()))

        if not selected_stocks:
            st.warning('Please select at least one stock.')
            return

        stock_symbols = [stocks[stock] for stock in selected_stocks]

        # Measure execution time without caching
        start_time = time.time()
        data = get_historical_data(stock_symbols)
        execution_time_no_cache = time.time() - start_time

        data_load_state = st.text('Loading data...')
        data_load_state.text('Loading data... done!')

        # Measure execution time with caching
        start_time = time.time()
        data_cached = get_historical_data(stock_symbols)
        execution_time_with_cache = time.time() - start_time

        execution_time_difference = execution_time_with_cache - execution_time_no_cache
        percentage_difference = (execution_time_difference / execution_time_no_cache) * 100

        st.write(f"Execution time without cache: {execution_time_no_cache} seconds")
        st.write(f"Execution time with cache: {execution_time_with_cache} seconds")
        st.write(f"Percentage difference: {percentage_difference}%")

        plot_historical_data(data)

    elif page == 'Forecast':
        st.title('Stock Price Forecast')
        selected_stocks = st.sidebar.multiselect('Select stocks', list(stocks.keys()))

        if not selected_stocks:
            st.warning('Please select at least one stock.')
            return

        stock_symbols = [stocks[stock] for stock in selected_stocks]

        # Measure execution time without caching
        start_time = time.time()
        data = get_historical_data(stock_symbols)
        execution_time_no_cache = time.time() - start_time

        data_load_state = st.text('Loading data...')
        data_load_state.text('Loading data... done!')

        forecasts, models, accuracies = predict_forecast(data)

        # Measure execution time with caching
        start_time = time.time()
        forecasts_cached, models_cached, accuracies_cached = predict_forecast(data)
        execution_time_with_cache = time.time() - start_time

        execution_time_difference = execution_time_with_cache - execution_time_no_cache
        percentage_difference = (execution_time_difference / execution_time_no_cache) * 100

        st.write(f"Execution time without cache: {execution_time_no_cache} seconds")
        st.write(f"Execution time with cache: {execution_time_with_cache} seconds")
        st.write(f"Percentage difference: {percentage_difference}%")

        plot_forecast(forecasts_cached, models_cached, accuracies_cached)

main()

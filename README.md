# Prophet - Stock Price Prediction App

This project is a stock price prediction app developed using Python, Streamlit, and Yahoo Finance API. The app allows users to analyze historical stock data, generate forecasts, and visualize the predicted trends.

## Features

- Historical Stock Data: Users can select specific stocks and view their historical data, including opening and closing prices, volume, and other relevant information.

- Stock Price Forecast: The app utilizes the Prophet library to train time series models for forecasting stock prices. Users can choose multiple stocks and generate future price predictions.

- Interactive Visualization: The app incorporates Plotly for interactive data visualization. It provides charts and graphs to visualize historical data, forecasted trends, and accuracy metrics.

- Caching for Improved Performance: The app utilizes caching to improve the execution time of data retrieval and forecast generation. This caching mechanism significantly enhances the user experience by reducing wait times.

## Installation

1. Clone the repository:


2. Install the required dependencies:


3. Run the Streamlit app:


4. Access the app in your browser by visiting [http://localhost:8501](http://localhost:8501).

## Usage

1. Select the "Historical Data" page to analyze the historical stock data of different companies. Choose the desired stocks and view their historical data in tables.

2. Navigate to the "Forecast" page to generate future price predictions. Select the stocks of interest and explore the forecasted trends using interactive charts.

3. Adjust the number of years for the forecast using the slider on the sidebar.

4. Interact with the charts by zooming, panning, and hovering over data points for detailed information.

## Credits

- Yahoo Finance API: Data for historical stock prices is obtained from the Yahoo Finance API.

- Prophet: The Prophet library, developed by Facebook, is used for time series forecasting.

- Plotly: Interactive visualizations are created using the Plotly library.

## License

This project is licensed under the [MIT License](LICENSE).


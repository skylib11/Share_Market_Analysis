# Share-Market-Analysis
# Share Market Data Processing & Trend Analysis

## Overview
This project is designed for analyzing the **Indian Share Market** by processing stock data and identifying key trading signals. The scripts use stock data retrieved via **Yahoo Finance** and generate insights based on **RSI (Relative Strength Index) and SMA (Simple Moving Average)** indicators. 

## Features
- **Data Preprocessing**: Cleans and formats raw stock data for analysis.
- **Trend Indicators**: Identifies buy/sell signals based on **RSI_14 and SMA indicators**.
- **Works with Yahoo Finance Symbols**: Requires a list of **NSE/BSE stock symbols** in `company_list.csv`.
- **Automated Signal Detection**: Logs and saves buy/sell signals for analysis.

## Files in the Repository
### 1. `share_data_preprocessing.py`
   - Reads stock symbols from `company_list.csv`.
   - Fetches historical data using Yahoo Finance.
   - Preprocesses data (handles missing values, formats dates, calculates SMA & RSI).
   - Saves processed data as CSV files.

### 2. `share_market_trend_indicator.py`
   - Reads processed stock data.
   - Analyzes trends based on **RSI_14 and SMA indicators**.
   - Detects **Buy/Sell signals** and logs them.
   - Saves trade signals to CSV for further review.

### 3. `company_list.csv`
   - Contains a list of **Yahoo Finance stock symbols** for NSE/BSE.
   - Example format:
     ```csv
     Symbol,Company
     RELIANCE.NS, Reliance Industries
     TCS.NS, Tata Consultancy Services
     HDFCBANK.NS, HDFC Bank
     ```

## Requirements
Ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  ```bash
  pip install pandas numpy yfinance ta
  ```

## How to Use
1. **Prepare the stock symbol list:**
   - Edit `company_list.csv` and include the **Yahoo Finance symbols** of the companies you want to analyze.

2. **Run Data Preprocessing:**
   ```bash
   python share_data_preprocessing.py
   ```
   - This will fetch stock data and save processed CSV files in a `processed_data` folder.

3. **Run Trend Analysis:**
   ```bash
   python share_market_trend_indicator.py
   ```
   - This will analyze the processed data and generate buy/sell signals in a `signals` folder.

## Output
- **Processed Data**: Stored in `processed_data/`
- **Trade Signals**: Saved in `signals/` with timestamps.
- **Logs**: Buy/sell signal detection logs are stored in `logs/`.

## Notes
- The project focuses on the **Indian Share Market** (NSE/BSE stocks).
- Make sure stock symbols in `company_list.csv` are correct for **Yahoo Finance**.
- Modify threshold values (RSI, SMA) as per your trading strategy.

## Contribution
Feel free to fork the repository, report issues, or submit improvements via pull requests.

## Disclaimer
This project is for **educational and informational purposes only**. It is not intended as financial advice. Always conduct your own research before making any trading decisions.


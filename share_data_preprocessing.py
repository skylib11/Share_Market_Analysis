"""
Stock Data Processing Script

Author: S.T. Sathish (SKYLIB)
Date: March 2025
Description: This script fetches historical stock price data from Yahoo Finance, cleans the data, performs feature engineering, and saves it in multiple formats.

Features:
- Fetches stock data for given tickers from Yahoo Finance
- Cleans missing values and formats date
- Adds technical indicators (SMA_20, SMA_50, SMA_200, RSI_14, Daily Return, Volatility)
- Saves raw, cleaned, and processed data for further analysis
- Logs processing details into a log file

Made with ChatGPT Assistance
"""

import os
import yfinance as yf
import pandas as pd
from datetime import datetime

def setup_logging():
    """Setup logging mechanism."""
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "data_processing.log")
    return log_file

def log_message(message):
    """Log messages to the log file and print to console."""
    log_file = setup_logging()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file, "a") as f:
        f.write(log_entry + "\n")

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch historical stock price data from Yahoo Finance and clean it."""
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    
    # Data Cleaning
    data.dropna(subset=['Open', 'High', 'Low', 'Close'], inplace=True)  # Remove rows with missing values
    data.index = pd.to_datetime(data.index)  # Ensure index is datetime
    data.sort_index(inplace=True)  # Sort by date
    
    # Format Date Column
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    data['Date'] = data['Datetime'].dt.strftime('%d-%m-%Y')  # Convert to dd-mm-yyyy format
    data.drop(columns=['Datetime'], inplace=True)  # Remove original datetime column
    
    # Round numerical values to 2 decimal places
    data = data.round(2)
    
    return data

def add_features(data):
    """Perform feature engineering by adding technical indicators."""
    data['SMA_20'] = data['Close'].rolling(window=20).mean()  # 20-day Simple Moving Average
    data['SMA_50'] = data['Close'].rolling(window=50).mean()  # 50-day Simple Moving Average
    data['SMA_200'] = data['Close'].rolling(window=200).mean()  # 200-day Simple Moving Average
    data['RSI_14'] = 100 - (100 / (1 + data['Close'].diff(1).apply(lambda x: max(x, 0)).rolling(14).mean() / 
                                      data['Close'].diff(1).apply(lambda x: abs(x)).rolling(14).mean()))  # RSI Calculation
    data['Daily_Return'] = data['Close'].pct_change() * 100  # Daily Returns in percentage
    data['Volatility_20'] = data['Daily_Return'].rolling(window=20).std()  # 20-day Rolling Volatility
    
    # Round selected features to 2 decimal places
    data[['SMA_20', 'SMA_50', 'SMA_200', 'RSI_14', 'Daily_Return', 'Volatility_20']] = \
        data[['SMA_20', 'SMA_50', 'SMA_200', 'RSI_14', 'Daily_Return', 'Volatility_20']].round(2)
    
    return data

# Ensure required folders exist
raw_data_folder = "raw_data"
cleaned_data_folder = "cleaned_data"
processed_data_folder = "processed_data"
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(cleaned_data_folder, exist_ok=True)
os.makedirs(processed_data_folder, exist_ok=True)

# Load company symbols from CSV
try:
    company_list = pd.read_csv("company_list.csv")
    company_list.columns = company_list.columns.str.strip()  # Remove extra spaces in headers
    log_message("CSV Loaded Successfully.")
    
    if 'Ticker' not in company_list.columns:
        raise KeyError("CSV file does not contain a 'Ticker' column.")
    
    tickers = company_list['Ticker'].dropna().tolist()  # Remove any empty values
    
    start_date = "2023-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")  # Get today's date dynamically
    
    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        log_message(f"Fetched data for {ticker}")
        
        # Save raw data
        raw_file_path = os.path.join(raw_data_folder, f"{ticker}_historical_data.csv")
        stock_data.to_csv(raw_file_path, index=False)
        log_message(f"Saved raw data to {raw_file_path}")
        
        # Save cleaned data
        cleaned_file_path = os.path.join(cleaned_data_folder, f"{ticker}_cleaned_data.csv")
        stock_data.to_csv(cleaned_file_path, index=False)
        log_message(f"Saved cleaned data to {cleaned_file_path}")
        
        # Add feature engineering
        processed_data = add_features(stock_data)
        processed_file_path = os.path.join(processed_data_folder, f"{ticker}_processed_data.csv")
        processed_data.to_csv(processed_file_path, index=False)
        log_message(f"Saved processed data with features to {processed_file_path}")

except FileNotFoundError:
    log_message("Error: company_list.csv not found. Please check the file path.")
except KeyError as e:
    log_message(f"Error: {e}")
except Exception as e:
    log_message(f"An unexpected error occurred: {e}")

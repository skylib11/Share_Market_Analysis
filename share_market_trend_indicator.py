"""
Share Market Buy/Sell Signal Detection

Author: S.T. Sathish (SKYLIB)
Date: 6 March 2025
Description: This script analyzes processed share market data to identify buy and sell opportunities based on RSI_14 and SMA indicators.

Signals:
- Buy: RSI_14 < 30 and Close price crosses above SMA_20
- Sell: RSI_14 > 70 and Close price drops below SMA_20
- Bullish Crossover: SMA_20 crosses above SMA_50 (Potential Buy Signal)
- Bearish Crossover: SMA_20 crosses below SMA_50 (Potential Sell Signal)

Made with ChatGPT Assistance
"""

import os
import pandas as pd
from datetime import datetime, timedelta

def setup_logging():
    """Setup logging mechanism."""
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "buy_sell_signals.log")
    return log_file

def log_message(message):
    """Log messages to the log file and print to console."""
    log_file = setup_logging()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file, "a") as f:
        f.write(log_entry + "\n")

def analyze_signals(file_path):
    """Analyze stock data for buy/sell signals for the last 10 days and save results to CSV."""
    try:
        log_message(f"Processing file: {file_path}")
        data = pd.read_csv(file_path)
        
        # Ensure required columns exist
        required_columns = {"Date", "Close", "SMA_20", "SMA_50", "RSI_14"}
        if not required_columns.issubset(data.columns):
            log_message(f"Skipping {file_path} - Missing required columns.")
            return
        
        # Convert Date column to datetime format
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce', dayfirst=True)
        
        # Filter last 10 days of data
        last_10_days = datetime.now() - timedelta(days=10)
        data = data[data["Date"] >= last_10_days]
        
        # Identify buy and sell signals with reasons
        data["Buy_Signal"] = ""
        data["Sell_Signal"] = ""
        data["Reason"] = ""
        
        buy_condition = (data["RSI_14"] < 30) & (data["Close"] > data["SMA_20"])
        sell_condition = (data["RSI_14"] > 70) & (data["Close"] < data["SMA_20"])
        bullish_crossover = (data["SMA_20"].shift(1) < data["SMA_50"].shift(1)) & (data["SMA_20"] > data["SMA_50"])
        bearish_crossover = (data["SMA_20"].shift(1) > data["SMA_50"].shift(1)) & (data["SMA_20"] < data["SMA_50"])
        
        data.loc[buy_condition, "Buy_Signal"] = "Buy"
        data.loc[buy_condition, "Reason"] = "RSI_14 below 30 and Close crossed above SMA_20"
        
        data.loc[sell_condition, "Sell_Signal"] = "Sell"
        data.loc[sell_condition, "Reason"] = "RSI_14 above 70 and Close dropped below SMA_20"
        
        data.loc[bullish_crossover, "Buy_Signal"] = "Buy"
        data.loc[bullish_crossover, "Reason"] = "SMA_20 crossed above SMA_50 (Bullish Crossover)"
        
        data.loc[bearish_crossover, "Sell_Signal"] = "Sell"
        data.loc[bearish_crossover, "Reason"] = "SMA_20 crossed below SMA_50 (Bearish Crossover)"
        
        # Filter only the rows where signals appear
        signals = data[(data["Buy_Signal"] == "Buy") | (data["Sell_Signal"] == "Sell")]
        
        if not signals.empty:
            log_message(f"Signals found in {file_path}:")
            log_message(signals[["Date", "Close", "SMA_20", "SMA_50", "RSI_14", "Buy_Signal", "Sell_Signal", "Reason"]].to_string(index=False))
            
            # Save signals to CSV
            signals_folder = "signals"
            os.makedirs(signals_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(signals_folder, f"{os.path.basename(file_path).replace('_processed_data.csv', '')}_trade_signals_{timestamp}.csv")
            signals.to_csv(output_file, index=False)
            log_message(f"Saved trade signals to {output_file}")
        else:
            log_message(f"No buy/sell signals detected in the last 10 days for {file_path}.")
        
    except Exception as e:
        log_message(f"Error processing {file_path}: {e}")

# Folder where processed data is stored
processed_data_folder = "processed_data"




log_message("Buy/Sell Signal Detection Script Started")
if os.path.exists(processed_data_folder):
    for filename in os.listdir(processed_data_folder):
        if filename.endswith("_processed_data.csv"):
            analyze_signals(os.path.join(processed_data_folder, filename))
else:
    log_message("Processed data folder not found. Run data processing script first.")
log_message("Buy/Sell Signal Detection Script Completed Successfully.")


# Moving content from 7_rsi.py
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime
import time

class RSIBot:
    def __init__(self, api_key, api_secret, symbol='BTCUSDT', interval='1h', rsi_period=14, 
                 oversold=30, overbought=70):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.interval = interval
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_rsi(self, data):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    def get_historical_data(self):
        klines = self.client.get_historical_klines(
            self.symbol, 
            self.interval,
            f"{self.rsi_period + 1} days ago UTC"
        )
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
        
    def generate_signals(self, df):
        df['RSI'] = self.calculate_rsi(df)
        df['Position'] = 0
        df.loc[df['RSI'] < self.oversold, 'Position'] = 1  # Buy signal
        df.loc[df['RSI'] > self.overbought, 'Position'] = -1  # Sell signal
        return df
        
    def run_bot(self):
        while True:
            try:
                df = self.get_historical_data()
                df = self.generate_signals(df)
                
                current_position = df['Position'].iloc[-1]
                print(f"Current Position Signal: {current_position}")
                print(f"Current Price: {df['close'].iloc[-1]}")
                print(f"Current RSI: {df['RSI'].iloc[-1]}")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(60)  # Wait before retrying

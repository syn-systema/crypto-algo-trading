# Moving content from 6_sma.py
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime
import time

class SMABot:
    def __init__(self, api_key, api_secret, symbol='BTCUSDT', interval='1h', sma_period=20):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.interval = interval
        self.sma_period = sma_period
        
    def calculate_sma(self, data):
        return data['close'].rolling(window=self.sma_period).mean()
        
    def get_historical_data(self):
        klines = self.client.get_historical_klines(
            self.symbol, 
            self.interval,
            f"{self.sma_period + 1} days ago UTC"
        )
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
        
    def generate_signals(self, df):
        df['SMA'] = self.calculate_sma(df)
        df['Position'] = 0
        df.loc[df['close'] > df['SMA'], 'Position'] = 1
        df.loc[df['close'] < df['SMA'], 'Position'] = -1
        return df
        
    def run_bot(self):
        while True:
            try:
                df = self.get_historical_data()
                df = self.generate_signals(df)
                
                current_position = df['Position'].iloc[-1]
                print(f"Current Position Signal: {current_position}")
                print(f"Current Price: {df['close'].iloc[-1]}")
                print(f"Current SMA: {df['SMA'].iloc[-1]}")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(60)  # Wait before retrying

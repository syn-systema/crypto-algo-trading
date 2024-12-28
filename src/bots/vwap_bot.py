# Moving content from 8_vwap.py
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime
import time

class VWAPBot:
    def __init__(self, api_key, api_secret, symbol='BTCUSDT', interval='1h'):
        self.client = Client(api_key, api_secret)
        self.symbol = symbol
        self.interval = interval
        
    def calculate_vwap(self, df):
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['price_volume'] = df['typical_price'] * df['volume']
        df['cumulative_price_volume'] = df['price_volume'].cumsum()
        df['cumulative_volume'] = df['volume'].cumsum()
        return df['cumulative_price_volume'] / df['cumulative_volume']
        
    def get_historical_data(self):
        klines = self.client.get_historical_klines(
            self.symbol, 
            self.interval,
            "1 day ago UTC"
        )
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
        
    def generate_signals(self, df):
        df['VWAP'] = self.calculate_vwap(df)
        df['Position'] = 0
        df.loc[df['close'] > df['VWAP'], 'Position'] = 1  # Buy signal
        df.loc[df['close'] < df['VWAP'], 'Position'] = -1  # Sell signal
        return df
        
    def run_bot(self):
        while True:
            try:
                df = self.get_historical_data()
                df = self.generate_signals(df)
                
                current_position = df['Position'].iloc[-1]
                print(f"Current Position Signal: {current_position}")
                print(f"Current Price: {df['close'].iloc[-1]}")
                print(f"Current VWAP: {df['VWAP'].iloc[-1]}")
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(60)  # Wait before retrying

# Moving content from historical-data-source.py
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import os

class HistoricalDataManager:
    def __init__(self, api_key, api_secret, base_path='data/historical'):
        self.client = Client(api_key, api_secret)
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        
    def fetch_historical_data(self, symbol, interval, start_date, end_date=None):
        """
        Fetch historical data from Binance and save to CSV
        """
        klines = self.client.get_historical_klines(
            symbol, 
            interval,
            start_date,
            end_date
        )
        
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        
        # Convert timestamp columns
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        
        # Convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                       'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        # Save to CSV
        filename = f"{symbol}_{interval}_{start_date.replace(' ', '_')}.csv"
        filepath = os.path.join(self.base_path, filename)
        df.to_csv(filepath, index=False)
        
        return df
    
    def load_historical_data(self, symbol, interval, start_date):
        """
        Load historical data from CSV if it exists
        """
        filename = f"{symbol}_{interval}_{start_date.replace(' ', '_')}.csv"
        filepath = os.path.join(self.base_path, filename)
        
        if os.path.exists(filepath):
            return pd.read_csv(filepath, parse_dates=['timestamp', 'close_time'])
        return None

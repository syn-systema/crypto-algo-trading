import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import ccxt
from ..config import EXCHANGE_API_KEY, EXCHANGE_SECRET_KEY

class MarketAnalysis:
    """
    Market data analysis tools as specified in PRD section 3.4
    """
    
    def __init__(self, exchange_id: str = 'binance'):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': EXCHANGE_API_KEY,
            'secret': EXCHANGE_SECRET_KEY,
            'enableRateLimit': True
        })
        
    async def fetch_historical_data(self, symbol: str, timeframe: str = '1h',
                                  limit: int = 1000) -> pd.DataFrame:
        """
        Fetch historical OHLCV data as specified in PRD 3.4.1
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
            
    def process_ohlcv_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process OHLCV data as specified in PRD 3.4.2
        """
        if df is None or df.empty:
            return None
            
        # Add basic technical indicators
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['rsi'] = self.calculate_rsi(df['close'])
        df['atr'] = self.calculate_atr(df)
        
        return df
        
    def calculate_support_resistance(self, df: pd.DataFrame, 
                                  window: int = 20,
                                  threshold: float = 0.02) -> Dict[str, List[float]]:
        """
        Calculate support and resistance levels as specified in PRD 3.4.3
        """
        if df is None or df.empty:
            return {'support': [], 'resistance': []}
            
        highs = df['high'].rolling(window=window, center=True).max()
        lows = df['low'].rolling(window=window, center=True).min()
        
        # Find potential levels
        resistance_levels = []
        support_levels = []
        
        for i in range(window, len(df) - window):
            # Resistance
            if highs.iloc[i] == df['high'].iloc[i] and \
               all(abs(highs.iloc[i] - level) / level > threshold for level in resistance_levels):
                resistance_levels.append(highs.iloc[i])
                
            # Support
            if lows.iloc[i] == df['low'].iloc[i] and \
               all(abs(lows.iloc[i] - level) / level > threshold for level in support_levels):
                support_levels.append(lows.iloc[i])
        
        return {
            'support': sorted(support_levels),
            'resistance': sorted(resistance_levels)
        }
        
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
        
    @staticmethod
    def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

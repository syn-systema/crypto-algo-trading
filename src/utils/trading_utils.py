# Moving content from nice_funcs.py
from binance.client import Client
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_historical_klines(client, symbol, interval, start_str, end_str=None):
    """
    Get historical klines/candlestick data for any given timeframe and convert to DataFrame
    """
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                     'close_time', 'quote_asset_volume', 'number_of_trades',
                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    
    # Convert numeric columns
    numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume',
                      'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
    
    # Convert timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    
    return df

def calculate_technical_indicators(df):
    """
    Calculate common technical indicators
    """
    # SMA
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # EMA
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    return df

def get_current_position(client, symbol):
    """
    Get current position for a symbol
    """
    try:
        position = float(client.get_asset_balance(symbol.replace('USDT', ''))['free'])
        return position
    except Exception as e:
        print(f"Error getting position: {e}")
        return 0

def calculate_position_size(account_balance, risk_percentage, entry_price, stop_loss):
    """
    Calculate position size based on risk management parameters
    """
    if stop_loss >= entry_price:
        raise ValueError("Stop loss must be below entry price for long positions")
    
    risk_amount = account_balance * (risk_percentage / 100)
    position_size = risk_amount / abs(entry_price - stop_loss)
    return position_size

def place_order(client, symbol, side, order_type, quantity, price=None):
    """
    Place an order with error handling
    """
    try:
        if order_type == 'MARKET':
            order = client.create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
        else:
            order = client.create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

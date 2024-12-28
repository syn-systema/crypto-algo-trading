"""
HyperLiquid Trading Bot - Version 1

This bot implements a basic trading strategy on the HyperLiquid DEX (Decentralized Exchange).
It places both buy and sell orders with configurable parameters, using the order book
to determine optimal entry and exit prices.

Key Components:
- Order book data retrieval (ask/bid prices)
- Decimal precision handling for different coins
- Limit order execution with customizable parameters
- Position management with reduce-only orders
"""

# Essential imports for different functionalities
import dontshare as d                # Custom module storing private keys and sensitive data
from eth_account.signers.local import LocalAccount  # Ethereum account management for signing transactions
import eth_account                   # Core Ethereum account functionality
import json                         # JSON parsing for API responses
import time                         # Time-related functions for delays
from hyperliquid.info import Info   # HyperLiquid market information
from hyperliquid.exchange import Exchange  # HyperLiquid exchange interface for trading
from hyperliquid.utils import constants  # HyperLiquid constants (URLs, etc.)
import ccxt                         # Universal cryptocurrency exchange library
import pandas as pd                 # Data manipulation and analysis
import datetime                     # Date and time operations
import schedule                     # Task scheduling
import requests                     # HTTP requests for API calls
import logging                      # Logging functionality

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Trading configuration
symbol = 'WIF'                      # Trading pair symbol (e.g., WIF/USD)
timeframe = '4h'                    # Candlestick timeframe for analysis

def ask_bid(symbol):
    """
    Fetches current market prices from HyperLiquid's order book.
    
    Technical Details:
    - Uses L2 order book data (level 2 market depth)
    - Retrieves best ask (lowest selling price) and best bid (highest buying price)
    - Returns both prices plus full order book data for additional analysis
    
    Parameters:
    symbol (str): Trading pair to query (e.g., 'WIF')
    
    Returns:
    tuple: (ask_price, bid_price, full_orderbook_data)
    """
    try:
        # API endpoint for order book data
        url = 'https://api.hyperliquid.xyz/info'
        headers = {'Content-Type': 'application/json'}
        
        # Request parameters for L2 order book
        data = {'type': 'l2book',
                'coin': symbol  
                }
        
        # Fetch and parse order book data
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise exception for bad status codes
        
        l2_data = response.json()
        l2_data = l2_data['levels']  # Extract price levels

        # Parse best bid and ask prices
        bid = float(l2_data[0][0]['px'])  # Highest buy order
        ask = float(l2_data[1][0]['px'])  # Lowest sell order
        
        return ask, bid, l2_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error in ask_bid: {e}")
        raise
    except (KeyError, IndexError) as e:
        logger.error(f"Data parsing error in ask_bid: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in ask_bid: {e}")
        raise

def get_sz_px_decimals(coin):
    """
    Determines the correct decimal precision for order sizes and prices.
    This is crucial for order placement as different coins have different precision requirements.
    
    Technical Details:
    - First attempts to get precision from exchange metadata
    - Falls back to calculating from current prices if metadata unavailable
    - Handles both integer and decimal precisions
    
    Parameters:
    coin (str): Trading pair symbol
    
    Returns:
    tuple: (size_decimals, price_decimals)
    """
    try:
        # Try to get precision from exchange metadata
        url = 'https://api.hyperliquid.xyz/info'
        headers = {'Content-Type': 'application/json'}
        data = {'type': 'meta'}
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
        # Primary method: Get from exchange metadata
        if response.status_code == 200:
            data = response.json()
            symbols = data['universe']
            symbol_info = next((s for s in symbols if s['name'] == coin), None)
            if symbol_info:
                sz_decimals = symbol_info['szDecimals']  # Size precision
                px_decimals = symbol_info['pxDecimals']  # Price precision
                return sz_decimals, px_decimals
            else:
                logger.warning(f'Symbol {coin} not found in metadata')
        
        # Fallback method: Calculate from current prices
        ask = ask_bid(coin)[0]
        ask_str = str(ask)
        if '.' in ask_str:
            px_decimals = len(ask_str.split('.')[1])
        else:
            px_decimals = 0
            
        bid = ask_bid(coin)[1]
        bid_str = str(bid)
        if '.' in bid_str:
            sz_decimals = len(bid_str.split('.')[1])
        else:
            sz_decimals = 0
            
        logger.info(f'{coin} price decimals: {px_decimals}, size decimals: {sz_decimals}')
        return sz_decimals, px_decimals
        
    except Exception as e:
        logger.error(f"Error in get_sz_px_decimals: {e}")
        raise

def limit_order(coin, is_buy, limit_px, reduce_only, account, sz=0.01):  
    """
    Places a limit order on HyperLiquid with specified parameters.
    
    Technical Details:
    - Uses GTC (Good Till Cancelled) order type
    - Applies proper decimal rounding
    - Supports both regular and reduce-only orders
    - Provides detailed logging for debugging
    
    Parameters:
    coin (str): Trading pair symbol
    is_buy (bool): True for buy orders, False for sell orders
    limit_px (float): Target price for the limit order
    reduce_only (bool): If True, order will only reduce existing position
    account (obj): Ethereum account for transaction signing
    sz (float): Order size in base currency
    
    Returns:
    dict: Full order response from exchange
    """
    try:
        # Initialize exchange connection with authentication
        exchange = Exchange(account, constants.MAINNET_API_URL)
        
        # Apply proper size rounding
        rounding = get_sz_px_decimals(coin)[0]
        sz = round(sz, rounding)  
        
        # Detailed logging for debugging
        logger.info(f'Order Parameters:')
        logger.info(f'coin: {coin}, type: {type(coin)}')
        logger.info(f'is_buy: {is_buy}, type: {type(is_buy)}')
        logger.info(f'sz: {sz}, type: {type(sz)}')
        logger.info(f'reduce_only: {reduce_only}, type: {type(reduce_only)}')
        logger.info(f'placing limit order for {coin} {sz} @ {limit_px}')
        
        # Submit order to exchange
        order_result = exchange.order(
            coin,               # Trading pair
            is_buy,            # Order direction
            sz,                # Order size
            limit_px,          # Limit price
            {"limit": {"tif": 'Gtc'}},  # Good Till Cancelled
            reduce_only=reduce_only      # Position reduction flag
        )
        
        # Log order result with safe access to nested dictionary
        try:
            status = order_result['response']['data']['statuses'][0]
        except (KeyError, IndexError) as e:
            status = 'Unknown - Error retrieving status'
            logger.error(f'Error accessing order status: {e}')
        
        order_type = "BUY" if is_buy else "SELL"
        logger.info(f"Limit {order_type} order placed, status: {status}")
        
        return order_result
        
    except Exception as e:
        logger.error(f"Error in limit_order: {e}")
        raise

def main():
    """
    Main execution function for the trading bot.
    Implements the core trading logic with proper error handling.
    """
    try:
        # Trading execution setup
        coin = symbol                    # Set trading pair
        sz = 0.01                        # Set order size
        
        # Get current market prices
        ask, bid, l2 = ask_bid(coin)
        
        # Initialize trading account
        account = eth_account.Account.from_key(d.private_key)
        
        # Place buy order
        is_buy = True
        reduce_only = False  # Allow opening new position
        limit_px = bid      # Buy at current bid price
        limit_order(coin, is_buy, limit_px, reduce_only, account, sz)
        
        # Wait before placing sell order
        logger.info("Waiting 5 seconds before placing sell order...")
        time.sleep(5)
        
        # Place sell order
        is_buy = False
        reduce_only = True   # Only reduce existing position
        limit_px = ask      # Sell at current ask price
        limit_order(coin, is_buy, limit_px, reduce_only, account, sz)
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()
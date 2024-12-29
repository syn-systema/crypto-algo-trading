"""
Phemex Exchange Risk Management System
====================================

This module implements a comprehensive risk management system for trading on the Phemex exchange.
It provides functionality for:
- Position monitoring and management
- Order execution with risk controls
- Automated position closing (kill switch)
- PnL-based position management
- Size-based risk management

Key Features:
- Supports multiple trading pairs (BTC, ETH, APE, DOGE, SHIB)
- Implements post-only orders for better execution
- Automated position closing at target profit or maximum loss
- Position size monitoring and risk controls
"""

import ccxt
import key_file as k
import time, schedule 
import pandas as pd 

# Initialize Phemex exchange connection with API credentials
phemex = ccxt.phemex({
    'enableRateLimit': True,  # Prevents rate limiting issues
    'apiKey': k.xP_KEY,
    'secret': k.xP_SECRET
})

# Default trading parameters
symbol = 'uBTCUSD'  # Default trading pair
size = 1            # Default position size
bid = 29000        # Default bid price (placeholder)
params = {'timeInForce': 'PostOnly',}  # Use post-only orders to ensure maker fees

def open_positions(symbol=symbol):
    """
    Retrieves and processes information about open positions for a given symbol.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'uBTCUSD', 'ETHUSD')
        
    Returns:
        tuple: Contains:
            - list: Raw position data from exchange
            - bool: Whether position exists
            - float: Position size
            - bool: True if long, False if short, None if no position
            - int: Index of position in exchange data
    """
    # Map symbols to their position indices in the exchange response
    if symbol == 'uBTCUSD':
        index_pos = 4
    elif symbol == 'APEUSD':
        index_pos = 2
    elif symbol == 'ETHUSD':
        index_pos = 3
    elif symbol == 'DOGEUSD':
        index_pos = 1
    elif symbol == 'u100000SHIBUSD':
        index_pos = 0
    else:
        index_pos = None 

    # Fetch current positions from exchange
    params = {'type':'swap', 'code':'USD'}
    phe_bal = phemex.fetch_balance(params=params)
    open_positions = phe_bal['info']['data']['positions']

    # Extract position details
    openpos_side = open_positions[index_pos]['side']
    openpos_size = open_positions[index_pos]['size']

    # Determine position direction
    if openpos_side == ('Buy'):
        openpos_bool = True 
        long = True 
    elif openpos_side == ('Sell'):
        openpos_bool = True
        long = False
    else:
        openpos_bool = False
        long = None 

    print(f'open_positions... | openpos_bool {openpos_bool} | openpos_size {openpos_size} | long {long} | index_pos {index_pos}')
    return open_positions, openpos_bool, openpos_size, long, index_pos

def ask_bid(symbol=symbol):
    """
    Fetches current ask and bid prices from the order book.
    
    Args:
        symbol (str): Trading pair symbol
        
    Returns:
        tuple: (ask_price, bid_price)
    """
    ob = phemex.fetch_order_book(symbol)
    bid = ob['bids'][0][0]  # Best bid price
    ask = ob['asks'][0][0]  # Best ask price
    
    print(f'this is the ask for {symbol} {ask}')
    return ask, bid

def kill_switch(symbol=symbol):
    """
    Emergency position closure system. Continues attempting to close position
    until successful using limit orders at the current bid/ask.
    
    Args:
        symbol (str): Trading pair to close position for
    """
    print(f'starting the kill switch for {symbol}')
    openposi = open_positions(symbol)[1]  # Check if position exists
    long = open_positions(symbol)[3]      # Position direction
    kill_size = open_positions(symbol)[2]  # Position size to close

    print(f'openposi {openposi}, long {long}, size {kill_size}')

    while openposi == True:
        print('starting kill switch loop til limit fil..')
        temp_df = pd.DataFrame()
        print('just made a temp df')

        # Cancel all existing orders before attempting to close
        phemex.cancel_all_orders(symbol)
        
        # Refresh position information
        openposi = open_positions(symbol)[1]
        long = open_positions(symbol)[3]
        kill_size = open_positions(symbol)[2]
        kill_size = int(kill_size)
        
        # Get current market prices
        ask = ask_bid(symbol)[0]
        bid = ask_bid(symbol)[1]

        # Place appropriate closing order based on position direction
        if long == False:
            phemex.create_limit_buy_order(symbol, kill_size, bid, params)
            print(f'just made a BUY to CLOSE order of {kill_size} {symbol} at ${bid}')
        elif long == True:
            phemex.create_limit_sell_order(symbol, kill_size, ask, params)
            print(f'just made a SELL to CLOSE order of {kill_size} {symbol} at ${ask}')
        else:
            print('++++++ SOMETHING I DIDNT EXCEPT IN KILL SWITCH FUNCTION')

        print('sleeping for 30 seconds to see if it fills..')
        time.sleep(30)
        openposi = open_positions(symbol)[1]

# Default PnL targets
target = 9     # Take profit percentage
max_loss = -8  # Stop loss percentage

def pnl_close(symbol=symbol, target=target, max_loss=max_loss):
    """
    Monitors position PnL and closes positions when they hit profit target
    or maximum loss threshold.
    
    Args:
        symbol (str): Trading pair symbol
        target (float): Profit target percentage
        max_loss (float): Maximum loss percentage
        
    Returns:
        tuple: Contains:
            - bool: Whether position was closed
            - bool: Whether in position
            - float: Position size
            - bool: True if long, False if short
    """
    print(f'checking to see if its time to exit for {symbol}... ')

    # Fetch current position information
    params = {'type':"swap", 'code':'USD'}
    pos_dict = phemex.fetch_positions(params=params)
    
    index_pos = open_positions(symbol)[4]
    pos_dict = pos_dict[index_pos]
    
    # Extract position details
    side = pos_dict['side']
    size = pos_dict['contracts']
    entry_price = float(pos_dict['entryPrice'])
    leverage = float(pos_dict['leverage'])
    current_price = ask_bid(symbol)[1]

    print(f'side: {side} | entry_price: {entry_price} | lev: {leverage}')

    # Calculate PnL percentage
    if side == 'long':
        diff = current_price - entry_price
        long = True
    else: 
        diff = entry_price - current_price
        long = False

    try: 
        perc = round(((diff/entry_price) * leverage), 10)
    except:
        perc = 0

    perc = 100*perc
    print(f'for {symbol} this is our PNL percentage: {(perc)}%')

    pnlclose = False 
    in_pos = False

    # Check if position should be closed based on PnL
    if perc > 0:
        in_pos = True
        print(f'for {symbol} we are in a winning postion')
        if perc > target:
            print(':) :) we are in profit & hit target.. checking volume to see if we should start kill switch')
            pnlclose = True
            kill_switch(symbol)
        else:
            print('we have not hit our target yet')

    elif perc < 0:
        in_pos = True
        if perc <= max_loss:
            print(f'we need to exit now down {perc}... so starting the kill switch.. max loss {max_loss}')
            kill_switch(symbol)
        else:
            print(f'we are in a losing position of {perc}.. but chillen cause max loss is {max_loss}')

    else:
        print('we are not in position')

    print(f' for {symbol} just finished checking PNL close..')
    return pnlclose, in_pos, size, long

def size_kill():
    """
    Monitors total position size and closes positions if they exceed
    maximum risk threshold.
    
    Maximum risk is set to 1000 USD.
    """
    max_risk = 1000

    # Fetch current positions
    params = {'type':"swap", "code": "USD"}
    all_phe_balance = phemex.fetch_balance(params=params)
    open_positions = all_phe_balance['info']['data']['positions']

    try:
        pos_cost = open_positions[0]['posCost']
        pos_cost = float(pos_cost)
        
        if pos_cost > max_risk:
            print(f'position cost {pos_cost} > max risk {max_risk}')
            kill_switch()
        else:
            print(f'position cost {pos_cost} < max risk {max_risk}')
            
    except Exception as e:
        print(f'error in size kill: {e}')

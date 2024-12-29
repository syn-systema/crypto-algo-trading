"""
HyperLiquid Exchange Risk Management Functions
===========================================

This module provides utility functions for managing trading operations on the HyperLiquid DEX.
It includes functions for:
- Order book data retrieval
- Precision handling
- Order placement
- Account balance monitoring
- Position management
- Order cancellation
- Emergency position closure (kill switch)
- PnL monitoring and management

The module is designed to work with the HyperLiquid API and provides a robust
set of tools for implementing trading strategies with proper risk management.
"""

import dontshare as d 
import nice_funcs as n 
from eth_account.signers.local import LocalAccount
import eth_account 
import json 
import time 
from hyperliquid.info import Info 
from hyperliquid.exchange import Exchange 
from hyperliquid.utils import constants 
import ccxt 
import pandas as pd 
import datetime 
import schedule 
import requests 

symbol='WIF'  # Default trading symbol

def ask_bid(symbol):
    """
    Retrieves the current ask and bid prices from HyperLiquid's order book.
    
    Args:
        symbol (str): Trading pair symbol
        
    Returns:
        tuple: (ask_price, bid_price, full_orderbook_data)
    """
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}

    data = {
        'type': 'l2Book', 
        'coin': symbol
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    l2_data = response.json()
    l2_data = l2_data['levels']

    # Extract best bid and ask prices
    bid = float(l2_data[0][0]['px'])
    ask = float(l2_data[1][0]['px'])

    return ask, bid, l2_data

def get_sz_px_decimals(coin):
    """
    Determines the correct decimal precision for size and price for a given coin.
    
    Args:
        coin (str): Coin symbol
        
    Returns:
        tuple: (size_decimals, price_decimals)
    """
    url = 'https://api.hyperliquid.xyz/info'
    headers = {'Content-Type': 'application/json'}
    data = {'type': 'meta'}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        data = response.json()
        symbols = data['universe']
        symbol_info = next((s for s in symbols if s['name'] == symbol), None)
        if symbol_info:
            sz_decimals = symbol_info['szDecimals']
        else:
            print('symbol not found')
    else:
        print('Error:', response.status_code)

    # Determine price decimals from current market price
    ask = ask_bid(symbol)[0]
    ask_str = str(ask)
    if '.' in ask_str:
        px_decimals = len(ask_str.split('.')[1])
    else:
        px_decimals = 0 

    print(f'{symbol} this is the price {sz_decimals} decimals')
    return sz_decimals, px_decimals

def limit_order(coin, is_buy, sz, limit_px, reduce_only, account):
    """
    Places a limit order on HyperLiquid with proper size rounding.
    
    Args:
        coin (str): Trading pair
        is_buy (bool): True for buy, False for sell
        sz (float): Order size
        limit_px (float): Limit price
        reduce_only (bool): Whether order should only reduce position
        account: Trading account object
        
    Returns:
        dict: Order result from exchange
    """
    exchange = Exchange(account, constants.MAINNET_API_URL)
    rounding = get_sz_px_decimals(coin)[0]
    sz = round(sz, rounding)
    
    print(f'coin: {coin}, type: {type(coin)}')
    print(f'is_buy: {is_buy}, type: {type(coin)}')
    print(f'sz: {sz}, type: {type(limit_px)}')
    print(f'reduce_only: {reduce_only}, type: {type(reduce_only)}')

    print(f'placing limit order for {coin} {sz} @ {limit_px}')
    order_result = exchange.order(coin, is_buy, sz, limit_px, 
                                {"limit": {"tif": 'Gtc'}}, 
                                reduce_only=reduce_only)

    if is_buy == True:
        print(f"limit BUY order placed thanks moon dev, resting: {order_result['response']['data']['statuses'][0]}")
    else:
        print(f"limit SELL order placed thanks moon dev, resting: {order_result['response']['data']['statuses'][0]}")

    return order_result

def acct_bal(account):
    """
    Retrieves current account balance and value.
    
    Args:
        account: Trading account object
        
    Returns:
        float: Account value in USD
    """
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    user_state = info.user_state(account.address)
    
    print(f'this is current account value: {user_state["marginSummary"]["accountValue"]}')
    return user_state["marginSummary"]["accountValue"]

def get_position(symbol, account):
    """
    Retrieves detailed information about current positions.
    
    Args:
        symbol (str): Trading pair
        account: Trading account object
        
    Returns:
        tuple: Contains:
            - list: Raw position data
            - bool: Whether in position
            - float: Position size
            - str: Position symbol
            - float: Entry price
            - float: PnL percentage
            - bool: True if long, False if short
    """
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    user_state = info.user_state(account.address)
    
    print(f'this is current account value: {user_state["marginSummary"]["accountValue"]}')
    
    positions = []
    print(f'this is the symbol {symbol}')
    print(user_state["assetPositions"])

    # Search for position matching symbol
    for position in user_state["assetPositions"]:
        if (position["position"]["coin"] == symbol) and float(position["position"]["szi"]) != 0:
            positions.append(position["position"])
            in_pos = True 
            size = float(position["position"]["szi"])
            pos_sym = position["position"]["coin"]
            entry_px = float(position["position"]["entryPx"])
            pnl_perc = float(position["position"]["returnOnEquity"])*100
            print(f'this is the pnl perc {pnl_perc}')
            break 
    else:
        in_pos = False 
        size = 0 
        pos_sym = None 
        entry_px = 0 
        pnl_perc = 0

    # Determine position direction
    if size > 0:
        long = True 
    elif size < 0:
        long = False 
    else:
        long = None 

    return positions, in_pos, size, pos_sym, entry_px, pnl_perc, long

def cancel_all_orders(account):
    """
    Cancels all open orders for the account.
    
    Args:
        account: Trading account object
    """
    exchange = Exchange(account, constants.MAINNET_API_URL)
    info = Info(constants.MAINNET_API_URL, skip_ws=True)

    open_orders = info.open_orders(account.address)

    print('above are the open orders... need to cancel any...')
    for open_order in open_orders:
        exchange.cancel(open_order['coin'], open_order['oid'])

def kill_switch(symbol, account):
    """
    Emergency position closure system. Continues attempting to close position
    until successful using limit orders at the current bid/ask.
    
    Args:
        symbol (str): Trading pair to close
        account: Trading account object
    """
    position, im_in_pos, pos_size, pos_sym, entry_px, pnl_perc, long = get_position(symbol, account)

    while im_in_pos == True:
        cancel_all_orders(account)
        ask, bid, l2 = ask_bid(symbol)
        pos_size = abs(pos_size)

        if long == True:
            limit_order(pos_sym, False, pos_size, ask, True, account)
            print('kill switch - SELL TO CLOSE SUBMITTED ')
        elif long == False:
            limit_order(pos_sym, True, pos_size, bid, True, account)
            print('kill switch - BUY TO CLOSE SUBMITTED ')

        time.sleep(5)
        position, im_in_pos, pos_size, pos_sym, entry_px, pnl_perc, long = get_position(symbol, account)

    print('position succesfully closed in the kill switch')

def pnl_close(symbol, target, max_loss, account):
    """
    Monitors position PnL and closes positions when they hit profit target
    or maximum loss threshold.
    
    Args:
        symbol (str): Trading pair
        target (float): Profit target percentage
        max_loss (float): Maximum loss percentage
        account: Trading account object
    """
    print('starting pnl close')
    position, im_in_pos, pos_size, pos_sym, entry_px, pnl_perc, long = get_position(symbol, account)

    if im_in_pos:
        print(f'we are in a position.. checking if we need to close')
        print(f'pnl percentage is: {pnl_perc}')

        if pnl_perc >= target:
            print(f'we hit our target of {target}!! closing position..')
            kill_switch(symbol, account)
        elif pnl_perc <= max_loss:
            print(f'we hit our max loss of {max_loss}!! closing position..')
            kill_switch(symbol, account)
        else:
            print(f'we are at {pnl_perc} which is between our tp of {target} and sl of {max_loss}')
    else:
        print('we are not in a position')

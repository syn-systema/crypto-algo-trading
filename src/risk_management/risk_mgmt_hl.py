"""
HyperLiquid Risk Management Bot
============================

This module implements a risk management bot for the HyperLiquid DEX.
It continuously monitors positions and implements various risk management strategies:

Features:
- PnL-based position monitoring and automated closing
- Account value monitoring with minimum balance protection
- Integration with HyperLiquid's API for real-time data
- Automated position closure when risk thresholds are breached

The bot is designed to run continuously and protect trading positions
from excessive losses while securing profits at defined targets.
"""

import nice_funcs as n 
import dontshare as d 
from eth_account.signers.local import LocalAccount 
import eth_account 
import json, time 
from hyperliquid.info import Info 
from hyperliquid.exchange import Exchange 
from hyperliquid.utils import constants 
import ccxt 
import pandas as pd 
import datetime 
import schedule 
import requests 

# Trading parameters
symbol = 'WIF'          # Trading pair
max_loss = -2          # Maximum allowed loss percentage
target = 1.5           # Target profit percentage
acct_min = 9          # Minimum account balance threshold
timeframe = '4h'      # Trading timeframe
size = 1              # Position size (reduced for testing)
coin = symbol         # Coin symbol (same as trading pair)

# Initialize account connection
secret_key = d.private_key
account = LocalAccount = eth_account.Account.from_key(secret_key)

def get_position(symbol, account):
    """
    Retrieves position details for the specified trading pair and account.
    
    Args:
        symbol (str): Trading pair
        account: Trading account object
        
    Returns:
        tuple: (position, in_position, size, symbol, entry_price, pnl_percentage, long)
    """
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    user_state = info.user_state(account.address)
    print(f'this is current account value: {user_state["marginSummary"]["accountValue"]}')
    
    positions = []
    in_position = False
    size = 0
    pos_symbol = None
    entry_price = 0
    pnl_perc = 0
    long = None

    print(f'checking position for symbol: {symbol}')
    print(user_state["assetPositions"])

    # Search for matching position
    for position in user_state["assetPositions"]:
        if (position["position"]["coin"] == symbol) and float(position["position"]["szi"]) != 0:
            positions.append(position["position"])
            in_position = True
            size = float(position["position"]["szi"])
            pos_symbol = position["position"]["coin"]
            entry_price = float(position["position"]["entryPx"])
            pnl_perc = float(position["position"]["returnOnEquity"]) * 100
            print(f'pnl percentage is: {pnl_perc}')
            break

    # Determine position direction
    if size > 0:
        long = True
    elif size < 0:
        long = False

    return positions, in_position, size, pos_symbol, entry_price, pnl_perc, long

def cancel_all_orders(account):
    """
    Cancels all open orders for the account.
    
    Args:
        account: Trading account object
    """
    exchange = Exchange(account, constants.MAINNET_API_URL)
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    open_orders = info.open_orders(account.address)

    print('cancelling all open orders...')
    for open_order in open_orders:
        exchange.cancel(open_order['coin'], open_order['oid'])

def kill_switch(symbol, account):
    """
    Closes the position for the specified trading pair and account.
    
    Args:
        symbol (str): Trading pair
        account: Trading account object
    """
    positions, in_position, size, pos_symbol, entry_price, pnl_perc, long = get_position(symbol, account)
    
    while in_position:
        # Cancel existing orders
        cancel_all_orders(account)
        
        # Get current market prices
        ask, bid, l2 = n.ask_bid(symbol)
        pos_size = abs(size)

        # Place appropriate closing order
        if long:
            n.limit_order(pos_symbol, False, pos_size, ask, True, account)
            print('kill switch - SELL TO CLOSE SUBMITTED')
        else:
            n.limit_order(pos_symbol, True, pos_size, bid, True, account)
            print('kill switch - BUY TO CLOSE SUBMITTED')

        time.sleep(5)  # Wait before checking position status
        positions, in_position, size, pos_symbol, entry_price, pnl_perc, long = get_position(symbol, account)

    print('position successfully closed in kill switch')

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
    positions, in_position, pos_size, pos_symbol, entry_price, pnl_perc, long = get_position(symbol, account)

    if not in_position:
        print('no position to monitor')
        return

    print(f'current position PnL: {pnl_perc}%')

    if pnl_perc > target:
        print(f'pnl gain is {pnl_perc}% and we hit our target of {target}%!! closing position as a WIN')
        kill_switch(pos_symbol, account)
    elif pnl_perc < max_loss:
        print(f'pnl loss is {pnl_perc}% and we hit our max loss of {max_loss}%!! closing position as a LOSS')
        kill_switch(pos_symbol, account)
    else:
        print(f'we are at {pnl_perc}% which is between our tp of {target}% and sl of {max_loss}%')

def bot():
    """
    Main bot function that implements risk management strategies.
    
    The bot performs the following checks:
    1. Monitors position PnL and closes if target/max loss is hit
    2. Monitors account value and closes positions if below minimum
    """
    print('starting risk management bot')
    print('monitoring positions and account value...')

    try:
        # Monitor PnL and close positions if needed
        pnl_close(symbol, target, max_loss, account)

        # Monitor account value
        acct_val = float(n.acct_bal(account))
        print(f'current account value: ${acct_val}')

        # Close positions if account value drops below minimum
        if acct_val < acct_min:
            print(f'account value (${acct_val}) below minimum (${acct_min})')
            kill_switch(symbol, account)
            
    except Exception as e:
        print(f'Error in bot execution: {str(e)}')

if __name__ == "__main__":
    bot()
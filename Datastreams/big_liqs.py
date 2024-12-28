"""
Binance Futures Large Liquidation Monitor

Focused on tracking significant liquidation events (>$100k) on Binance Futures markets.
These large liquidations often indicate major market moves and potential trading opportunities.

Size Display:
- Values shown in 10k USD units (e.g., 25 = $250,000)
- Makes large numbers more readable and meaningful

Thresholds:
- MEGA:   > $1M    (100+ units)
- LARGE:  > $500k  (50+ units)
- MEDIUM: > $250k  (25+ units)
- SMALL:  > $100k  (10+ units)
"""

import asyncio
import json
import os
from datetime import datetime
import pytz
from websockets import connect
from termcolor import cprint
import csv
from collections import defaultdict

# Configuration
WEBSOCKET_URL = 'wss://fstream.binance.com/ws/!forceOrder@arr'
CSV_FILE = 'binance_bigLiqs.csv'
MIN_SIZE_USD = 100_000  # Only track liquidations above 100k USD

# Liquidation counters
liq_stats = defaultdict(lambda: {'count': 0, 'volume': 0})

def format_size(size_usd):
    """Convert USD size to readable units (10k USD per unit)"""
    return size_usd / 10_000

async def binance_liquidation():
    """Monitor significant liquidation events on Binance Futures"""
    
    # Initialize CSV if needed
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            f.write("timestamp,symbol,side,size_usd,price,units\n")

    print("\nMonitoring large liquidations (>$100k)...")
    print("Values shown in 10k USD units (e.g., 25 = $250,000)\n")
    
    async with connect(WEBSOCKET_URL) as websocket:
        while True:
            try:
                # Process liquidation data
                data = json.loads(await websocket.recv())['o']
                
                # Calculate liquidation size
                qty = float(data['q'])
                price = float(data['p'])
                usd_size = qty * price
                
                # Only process large liquidations
                if usd_size < MIN_SIZE_USD:
                    continue
                
                # Format data
                symbol = data['s'].replace('USDT', '')
                side = data['S']
                units = format_size(usd_size)
                timestamp = datetime.fromtimestamp(
                    int(data['T']) / 1000, 
                    pytz.timezone('US/Central')
                ).strftime('%H:%M:%S')
                
                # Update statistics
                liq_stats[symbol]['count'] += 1
                liq_stats[symbol]['volume'] += usd_size
                
                # Format output
                liq_type = ' LONG LIQ' if side == 'BUY' else ' SHORT LIQ'
                output = f"{timestamp} {liq_type} {symbol:<8} {units:>6.1f} units"
                
                # Display based on size
                if usd_size > 1_000_000:  # > $1M
                    stars = ' ' * 3
                    cprint(f"{stars}{output}{stars}", 'white', 'on_red', attrs=['bold', 'blink'])
                    print(f"MEGA LIQUIDATION: ${usd_size:,.0f}")
                elif usd_size > 500_000:  # > $500k
                    cprint(output, 'white', 'on_yellow', attrs=['bold'])
                elif usd_size > 250_000:  # > $250k
                    cprint(output, 'white', 'on_blue', attrs=['bold'])
                else:  # > $100k
                    cprint(output, 'yellow', attrs=['bold'])
                
                # Log to CSV
                with open(CSV_FILE, 'a', newline='') as f:
                    f.write(f"{timestamp},{symbol},{side},{usd_size:.0f},{price},{units:.1f}\n")
                
                # Show summary every 50 liquidations
                if sum(s['count'] for s in liq_stats.values()) % 50 == 0:
                    print("\nTop Liquidated Assets:")
                    sorted_stats = sorted(
                        liq_stats.items(), 
                        key=lambda x: x[1]['volume'], 
                        reverse=True
                    )[:5]
                    for sym, stats in sorted_stats:
                        vol_units = format_size(stats['volume'])
                        print(f"{sym:<8} Count: {stats['count']:>3} Volume: {vol_units:>6.1f} units")
                    print("")
                
            except Exception as e:
                print(f"Error: {str(e)}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(binance_liquidation())
    except KeyboardInterrupt:
        print("\nMonitor stopped by user")

"""
Binance Futures Liquidation Monitor

This script monitors and analyzes liquidation events on Binance Futures markets. Liquidations occur 
when a trader's position is forcefully closed due to insufficient margin to maintain the position.

Market Intelligence from Liquidation Data:
1. Market Direction Signals
   - Clusters of long liquidations often precede further downside
   - Clusters of short liquidations often precede further upside
   - Large liquidations can cause cascading effects and volatility

2. Risk Management Applications
   - High liquidation volumes indicate increased market risk
   - Helps identify price levels with significant liquidation clusters
   - Can be used to avoid placing stops at common liquidation levels

3. Trading Opportunities
   - Large liquidations often create temporary price dislocations
   - Liquidation cascades can lead to overshooting and mean reversion opportunities
   - Can be used to identify potential market bottoms/tops when combined with other indicators

4. Market Health Monitoring
   - Excessive liquidations indicate overleveraged market conditions
   - Low liquidation periods suggest healthier, spot-driven price action
   - Helps gauge overall market leverage and risk

Data Collection Purpose:
- Track size and frequency of liquidations
- Identify market stress points
- Monitor leverage conditions
- Alert on significant forced position closures
- Build historical liquidation database for analysis

Output Color Coding:
- Red Background: Short liquidations (longs got liquidated) > $25,000
- Green Background: Long liquidations (shorts got liquidated) > $25,000
- White Text: Standard liquidations > $3,000
"""

import asyncio
import json
import os
from datetime import datetime
import pytz
from websockets import connect
from termcolor import cprint
import csv

# WebSocket endpoint for Binance Futures liquidation feed
websocket_url = 'wss://fstream.binance.com/ws/!forceOrder@arr'

# CSV file for historical data storage and analysis
filename = 'binance_liqs.csv'

# Initialize CSV file with headers if it doesn't exist
if not os.path.isfile(filename):
    with open(filename, 'w', newline='') as f:
        f.write(",".join([
            'symbol', 'side', 'order_type', 'time_in_force',
            'original_quantity', 'price', 'average_price', 'order_status',
            'order_last_filled_quantity', 'order_filled_accumulated_quantity',
            'order_trade_time', 'usd_size'
        ])+ "\n")
    
async def binance_liquidation(uri, filename):
    """
    Monitors Binance Futures WebSocket for liquidation events.
    
    Args:
        uri (str): WebSocket endpoint URL
        filename (str): CSV file path for data storage
    
    The function:
    1. Maintains WebSocket connection to Binance
    2. Processes incoming liquidation events
    3. Formats and displays significant liquidations
    4. Stores all liquidation data for analysis
    """
    async with connect(uri) as websocket:
        while True:
            try:
                # Receive and parse liquidation event
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract order data from message
                data = data['o']
                
                # Process trade details
                symbol = data['s'].replace('USDT', '')
                side = data['S']
                timestamp = int(data['T'])
                filled_quantity = float(data['q'])
                price = float(data['p'])
                usd_size = filled_quantity * price
                
                # Convert timestamp to Central time
                cst = pytz.timezone('US/Central')
                time_cst = datetime.fromtimestamp(timestamp / 1000, cst).strftime('%Y-%m-%d %H:%M:%S')
                
                # Display significant liquidations (> $3,000)
                if usd_size > 3000:
                    # Format liquidation type and symbol
                    liquidation_type = 'L LIQ' if side == 'SELL' else 'S LIQ'
                    symbol = symbol[:6]
                    output = f"{liquidation_type} {symbol} {time_cst} ${usd_size:,.0f}"
                    color = 'green' if side == 'SELL' else 'red'
                    attrs = ['bold'] if usd_size > 10000 else []

                    # Format based on liquidation size
                    if usd_size > 250000:
                        stars = '*' * 3
                        attrs.append('blink')
                        output = f'{stars} {output} {stars}'
                        for _ in range(4):
                            cprint(output, 'white', f'on_{color}', attrs=attrs)
                            await asyncio.sleep(0.1)

                    elif usd_size > 100000:
                        stars = '*' * 1
                        attrs.append('blink')
                        output = f'{stars} {output} {stars}'
                        for _ in range(2):
                            cprint(output, 'white', f'on_{color}', attrs=attrs)
                            await asyncio.sleep(0.1)

                    elif usd_size > 25000:
                        cprint(output, 'white', f'on_{color}')
                    else:
                        cprint(output, color, attrs=attrs)

                    print('')  # Spacing between liquidations
                
                # Store liquidation data in CSV
                msg_values = [str(data[key]) for key in ['s', 'S', 'o', 'f', 'q', 'p', 'ap', 'X', 'l', 'z', 'T']]
                msg_values.append(str(usd_size))
                with open(filename, 'a') as f:
                    trade_info = ','.join(msg_values) + '\n'
                    trade_info = trade_info.replace('USDT', '')
                    f.write(trade_info)
                
            except Exception as e:
                print(f"Error processing trade: {str(e)}")
                await asyncio.sleep(5)

# Start the liquidation monitor
asyncio.run(binance_liquidation(websocket_url, filename))

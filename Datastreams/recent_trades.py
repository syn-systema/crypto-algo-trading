"""
Cryptocurrency Recent Trade Monitor

This script tracks and analyzes recent trades on Binance Futures markets in real-time.
As a quantitative trader, monitoring recent trades provides crucial market microstructure
insights and trading signals:

Why Track Recent Trades?
1. Market Impact Analysis
   - Observe how large trades affect price movements
   - Identify potential market manipulation or whale activity
   - Understand market depth and liquidity conditions

2. Price Discovery
   - Track the flow of aggressive orders (market orders)
   - Identify which side (buyers/sellers) is more aggressive
   - Detect potential short-term price trends

3. Trading Volume Patterns
   - Monitor distribution of trade sizes
   - Identify unusual trading activity
   - Detect potential accumulation or distribution

4. Market Participant Behavior
   - Distinguish between maker and taker orders
   - Understand institutional vs retail trading patterns
   - Track smart money movement through size-based analysis

Color Coding System:
- Green: Buy trades (taker is buyer)
- Red: Sell trades (taker is seller)
- Cyan: Large buy trades (≥$500k)
- Magenta: Large sell trades (≥$500k)
- Bold: Trades ≥$50k
- Stars (*): Additional emphasis based on size
  * Single star: ≥$100k
  ** Double star: ≥$500k

Trade Size Categories:
- Regular: $15k - $50k
- Notable: $50k - $100k
- Large: $100k - $500k
- Whale: ≥$500k

This data is valuable for:
- Algorithmic trading strategies
- Risk management
- Market making
- Alpha generation
- Execution optimization
"""

import asyncio  # Import asyncio for handling asynchronous operations
import json  # Import json for parsing JSON data
import os  # Import os for interacting with the operating system
from datetime import datetime  # Import datetime for handling date and time
import pytz  # Import pytz for timezone handling
from websockets import connect  # Import connect for WebSocket connections
from termcolor import cprint  # Import cprint for colored console output

# List of symbols you want to track
symbols = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'dogeusdt', 'wifiusdt', 'xrpusdt']
websocket_url_base = 'wss://fstream.binance.com/ws'  # Base URL for Binance WebSocket API
trades_filename = 'binance_trades.csv'  # Filename for logging trades

# Check if the CSV file exists
if not os.path.isfile(trades_filename):
    with open(trades_filename, 'w') as f:  # Open the file in write mode
        # Write the header row for the CSV file
        f.write('Event Time,Symbol,Aggregate Trade ID,Price,Quantity,Trade Time,Is Buyer Maker\n')

# Asynchronous function to handle the Binance trade stream
async def binance_trade_stream(uri, symbol, filename):
    async with connect(uri) as websocket:  # Establish a WebSocket connection
        while True:  # Loop indefinitely to keep receiving messages
            try:
                message = await websocket.recv()  # Receive a message from the WebSocket
                data = json.loads(message)  # Parse the JSON message
                event_time = int(data['E'])  # Extract event time
                agg_trade_id = int(data['a'])  # Extract aggregate trade ID
                price = float(data['p'])  # Extract price of the trade
                quantity = float(data['q'])  # Extract quantity of the trade
                trade_time = int(data['T'])  # Extract trade time
                is_buyer_maker = data['m']  # Determine if the buyer is the maker
                cst = pytz.timezone('US/Central')  # Set timezone to US/Central
                # Convert trade time to a readable format
                readable_trade_time = datetime.fromtimestamp(trade_time / 1000, cst).strftime('%H:%M:%S')
                usd_size = price * quantity  # Calculate the USD size of the trade
                display_symbol = symbol.upper().replace('USDT', '')  # Format the symbol for display
                
                # Check if the USD size is greater than $14,999
                if usd_size > 14999:
                    trade_type = 'SELL' if is_buyer_maker else "BUY"  # Determine trade type
                    color = 'red' if trade_type == 'SELL' else 'green'  # Set color based on trade type
                    
                    stars = ''  # Initialize stars for highlighting
                    attrs = ['bold'] if usd_size >= 50000 else []  # Bold attribute for large trades
                    repeat_count = 1  # Initialize repeat count for output
                    # Determine star marking and color for very large trades
                    if usd_size >= 500000:
                        stars = '*' * 2
                        repeat_count = 1
                        color = 'magenta' if trade_type == 'SELL' else 'cyan'
                    elif usd_size >= 100000:
                        stars = '*' * 1
                        repeat_count = 1
                    # Prepare the output string for console display
                    output = f"{stars} {trade_type} {display_symbol} {readable_trade_time} {usd_size:,.0f}"
                    
                    # Print the output to the console with color and attributes
                    for _ in range(repeat_count):
                        cprint(output, 'white', f'on_{color}', attrs=attrs)
                    
                    # Log the trade details to the CSV file
                    with open(filename, 'a') as f:
                        f.write(f"{event_time},{symbol.upper()},{agg_trade_id},{price},{quantity},"
                                 f"{trade_time},{is_buyer_maker}\n")
            except json.JSONDecodeError as e:
                # Handle JSON decoding errors
                print(f"Error decoding JSON for {symbol}: {e}")
                await asyncio.sleep(5)  # Wait before retrying
            except Exception as e:
                # Handle unexpected errors
                print(f"Unexpected error for {symbol}: {e}")
                await asyncio.sleep(5)  # Wait before retrying

# Main asynchronous function to manage trade streams
async def main():
    # Create a task for each symbol trade stream
    tasks = []
    for symbol in symbols:
        stream_url = f"{websocket_url_base}/{symbol}@aggTrade"  # Construct the WebSocket URL for each symbol
        tasks.append(binance_trade_stream(stream_url, symbol, trades_filename))  # Add the task to the list

    await asyncio.gather(*tasks)  # Run all tasks concurrently

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function
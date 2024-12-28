"""
Cryptocurrency Funding Rate Monitor

This script tracks funding rates on Binance Futures markets. Funding rates are periodic payments
between traders holding long and short positions in perpetual futures contracts.

Why Track Funding Rates?
- Funding rates indicate market sentiment (positive rates suggest bullish sentiment, negative rates bearish)
- High positive rates mean longs pay shorts (expensive to hold long positions)
- Negative rates mean shorts pay longs (profitable to hold long positions)
- Extreme funding rates can signal potential market reversals or opportunities for funding arbitrage
- The annualized rate helps visualize the yearly cost/profit of holding positions

Color Coding System:
- Red (>50% APR): Extremely expensive to hold longs
- Yellow (>30% APR): Very expensive for longs
- Cyan (>5% APR): Moderately expensive for longs
- Green (<-10% APR): Profitable to hold longs
- Blue (<-30% APR): Very profitable to hold longs
- Magenta (<-50% APR): Extremely profitable for longs
- White: Neutral funding rate
"""

# Import required libraries
import asyncio  # For async/await functionality
import json    # For parsing WebSocket messages
from datetime import datetime, timedelta  # For timestamp handling
import pytz    # For timezone conversion
from websockets import connect  # For WebSocket connections
from termcolor import cprint   # For colored terminal output
import logging  # For error logging
import csv     # For data export (if needed)
from pathlib import Path  # For file path handling
import random  # For potential jitter in reconnection attempts

# List of cryptocurrency trading pairs to monitor
# Each pair is suffixed with 'usdt' as these are USDT-margined perpetual futures
symbols = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'dogeusdt', 'wifiusdt', 'xrpusdt']

# Base WebSocket URL for Binance Futures
websocket_url_base = 'wss://fstream.binance.com/ws'

# Shared counter to track when all symbols have reported their funding rates
# Using a dict for mutability in async context
shared_symobl_counter = {'count': 0}

# Lock to prevent concurrent terminal output from different coroutines
# Ensures clean, non-overlapping output in the terminal
print_lock = asyncio.Lock()

# Configuration constants
CSV_FILE = 'funding_rates.csv'

class FundingRateLogger:
    def __init__(self):
        self.csv_path = Path(CSV_FILE)
        self._setup_csv()

    def _setup_csv(self):
        """Initialize CSV file with headers if it doesn't exist."""
        if not self.csv_path.exists():
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Symbol', 'Funding Rate', 'Yearly Rate', 'Mark Price'])

    def log_funding(self, timestamp: str, symbol: str, funding_rate: float, 
                   yearly_rate: float, mark_price: float) -> None:
        """
        Log all funding rate data to CSV.
        """
        try:
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    symbol,
                    f"{funding_rate:.6f}",
                    f"{yearly_rate:.2f}%",
                    f"${mark_price:,.2f}"
                ])
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")

# Initialize the funding rate logger
funding_logger = FundingRateLogger()

async def binance_funding_stream(symbol, shared_counter):
    """
    Connects to Binance's WebSocket stream for a specific trading pair and monitors its funding rate.
    Pulls data immediately and then every 6 hours.
    """
    global print_lock
    websocket_url = f"{websocket_url_base}/{symbol}@markPrice"
    
    while True:
        try:
            async with connect(websocket_url) as websocket:
                # Receive and parse the WebSocket message
                message = await websocket.recv()
                data = json.loads(message)
                
                # Process the data
                event_time = datetime.fromtimestamp(data['E'] / 1000, pytz.timezone('US/Central'))
                event_time_str = event_time.strftime('%Y-%m-%d %H:%M:%S')
                display_time = event_time.strftime('%H:%M:%S')
                
                symbol_display = data['s'].replace('USDT', '')
                funding_rate = float(data['r'])
                yearly_funding_rate = (funding_rate * 3 * 365) * 100
                mark_price = float(data['p'])
                
                # Log to CSV
                funding_logger.log_funding(
                    event_time_str,
                    symbol_display,
                    funding_rate,
                    yearly_funding_rate,
                    mark_price
                )
                
                # Determine color coding
                if yearly_funding_rate > 50:
                    text_color, back_color = 'black', 'on_red'
                elif yearly_funding_rate > 30:
                    text_color, back_color = 'black', 'on_yellow'
                elif yearly_funding_rate > 5:
                    text_color, back_color = 'black', 'on_cyan'
                elif yearly_funding_rate < -10:
                    text_color, back_color = 'black', 'on_green'
                elif yearly_funding_rate < -30:
                    text_color, back_color = 'black', 'on_blue'
                elif yearly_funding_rate < -50:
                    text_color, back_color = 'black', 'on_magenta'
                else:
                    text_color, back_color = 'black', 'on_white'
                
                async with print_lock:
                    cprint(f"{display_time} {symbol_display} {yearly_funding_rate:.2f}%", 
                          text_color, back_color, attrs=['bold'])
                    shared_counter['count'] += 1
                    if shared_counter['count'] >= len(symbols):
                        next_update = datetime.now(pytz.timezone('US/Central')) + \
                                    timedelta(hours=6)
                        next_update_str = next_update.strftime('%Y-%m-%d %H:%M:%S')
                        cprint(f"{display_time} yrly fund - Next update at {next_update_str}", 
                              'white', 'on_black')
                        shared_counter['count'] = 0
                        
                        # Sleep for 6 hours before next update
                        await asyncio.sleep(6 * 60 * 60)  # 6 hours in seconds

        except Exception as e:
            logging.error(f"Error processing {symbol}: {str(e)}")
            await asyncio.sleep(5)

async def main():
    """
    Main entry point of the script.
    Creates and runs concurrent tasks for monitoring each trading pair's funding rate.
    """
    # Create a separate monitoring task for each symbol
    tasks = [binance_funding_stream(symbol, shared_symobl_counter) for symbol in symbols]
    # Run all monitoring tasks concurrently
    await asyncio.gather(*tasks)

# Start the monitoring system
asyncio.run(main())

"""
Large Trade Monitor for Cryptocurrency Markets

This script specializes in detecting and analyzing large trades (≥$500k) and mega trades
(≥$30M) on Binance Futures markets. Monitoring whale activity is crucial for institutional
traders and market makers for several reasons:

Key Benefits:
1. Market Structure Analysis
   - Identify institutional order flow
   - Detect potential market manipulation
   - Track smart money positioning
   - Monitor whale accumulation/distribution patterns

2. Risk Management
   - Early warning system for large position changes
   - Detect potential market moving orders
   - Identify periods of institutional activity
   - Monitor market impact of large trades

3. Alpha Generation
   - Track institutional trading patterns
   - Identify potential market reversals
   - Monitor order flow imbalances
   - Detect institutional accumulation zones

4. Market Making Optimization
   - Adjust spreads based on whale activity
   - Manage inventory risk during large trades
   - Identify potential toxic order flow
   - Optimize quote depths

Features:
- Real-time monitoring of trades ≥$500,000
- Special highlighting for mega trades ≥$30,000,000
- Trade aggregation by time bucket
- Persistent CSV logging for analysis
- Timezone-aware timestamps (US/Central)

Display Format:
- Blue Background: Large buy orders
- Magenta Background: Large sell orders
- Flashing Effect: Mega trades (≥$30M)
- Bold: All large trades
- Size Display: Shown in millions (e.g., "1.5M")

Use Cases:
- Algorithmic trading strategy inputs
- Risk management triggers
- Market making parameters
- Portfolio rebalancing signals
- Research and backtesting
"""

import asyncio
import json
from datetime import datetime
import pytz
from websockets import connect
from termcolor import cprint
import logging
import csv
from typing import Dict, Tuple
from pathlib import Path

# Configuration
SYMBOLS = ['btcusdt', 'ethusdt', 'solusdt', 'bnbusdt', 'dogeusdt', 'wifiusdt', 'xrpusdt']
WEBSOCKET_URL = 'wss://fstream.binance.com/ws'
MIN_TRADE_SIZE = 500000  # $500k minimum
MEGA_TRADE_SIZE = 30000000  # $30M for special highlighting
CSV_FILE = 'large_trades.csv'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TradeAggregator:
    def __init__(self):
        self.trade_buckets: Dict[Tuple[str, str, bool], float] = {}
        self.tz = pytz.timezone('US/Central')
        self._setup_csv()

    def _setup_csv(self):
        """Setup CSV file with headers if it doesn't exist."""
        self.csv_path = Path(CSV_FILE)
        if not self.csv_path.exists():
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Symbol', 'Trade Type', 'Size USD', 'Price', 'Quantity'])

    async def add_trade(self, symbol: str, timestamp: int, price: float, quantity: float, is_buyer_maker: bool) -> None:
        """Add a trade to the aggregator with proper timezone handling."""
        trade_time = datetime.fromtimestamp(timestamp / 1000, self.tz)
        second = trade_time.strftime('%H:%M:%S')
        usd_size = price * quantity
        
        trade_key = (symbol.upper().replace('USDT', ''), second, is_buyer_maker)
        self.trade_buckets[trade_key] = self.trade_buckets.get(trade_key, 0) + usd_size

        # Save large individual trades immediately
        if usd_size >= MIN_TRADE_SIZE:
            self._save_to_csv(trade_time.strftime('%Y-%m-%d %H:%M:%S'), 
                            symbol.upper().replace('USDT', ''),
                            "SELL" if is_buyer_maker else "BUY",
                            usd_size,
                            price,
                            quantity)

    def _save_to_csv(self, timestamp: str, symbol: str, trade_type: str, 
                    usd_size: float, price: float, quantity: float) -> None:
        """Save trade data to CSV file."""
        try:
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, symbol, trade_type, f"${usd_size:,.2f}", 
                               f"${price:,.2f}", f"{quantity:,.8f}"])
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")

    async def check_and_print_trades(self) -> None:
        """Check for and print large trades with proper formatting."""
        current_time = datetime.now(self.tz).strftime('%H:%M:%S')
        deletions = []

        for (symbol, second, is_buyer_maker), usd_size in self.trade_buckets.items():
            if second < current_time and usd_size >= MIN_TRADE_SIZE:
                self._print_trade(symbol, second, usd_size, is_buyer_maker)
                deletions.append((symbol, second, is_buyer_maker))

        # Clean up processed trades
        for key in deletions:
            del self.trade_buckets[key]

    def _print_trade(self, symbol: str, timestamp: str, usd_size: float, is_buyer_maker: bool) -> None:
        """Format and print a trade with proper styling."""
        trade_type = "SELL" if is_buyer_maker else "BUY"
        back_color = 'on_magenta' if is_buyer_maker else 'on_blue'
        
        if usd_size >= MEGA_TRADE_SIZE:
            size_str = f"${usd_size/1000000:.2f}M"
            text = f"\033[5m{trade_type} {symbol} {timestamp} {size_str}\033[0m"
        else:
            size_str = f"{usd_size/1000000:.2f}M"
            text = f"{trade_type} {symbol} {timestamp} {size_str}"
            
        cprint(text, 'white', back_color, attrs=['bold'])

async def connect_websocket(uri: str, max_retries: int = 5) -> connect:
    """Connect to websocket with retry logic."""
    for attempt in range(max_retries):
        try:
            return await connect(uri)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            logging.error(f"Connection attempt {attempt + 1} failed. Retrying in {wait_time}s... Error: {str(e)}")
            await asyncio.sleep(wait_time)

async def process_trades(websocket, symbol: str, aggregator: TradeAggregator) -> None:
    """Process incoming trades from websocket stream."""
    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            
            await aggregator.add_trade(
                symbol=symbol,
                timestamp=data['T'],
                price=float(data['p']),
                quantity=float(data['q']),
                is_buyer_maker=data['m']
            )
        except Exception as e:
            logging.error(f"Error processing {symbol} trade: {str(e)}")
            await asyncio.sleep(1)

async def monitor_trades(aggregator: TradeAggregator) -> None:
    """Continuously monitor and print trades."""
    while True:
        try:
            await aggregator.check_and_print_trades()
            await asyncio.sleep(1)
        except Exception as e:
            logging.error(f"Error monitoring trades: {str(e)}")
            await asyncio.sleep(1)

async def main() -> None:
    """Main function to run the trade monitoring system."""
    trade_aggregator = TradeAggregator()
    
    # Create tasks for each symbol
    trade_tasks = []
    for symbol in SYMBOLS:
        uri = f"{WEBSOCKET_URL}/{symbol}@aggTrade"
        websocket = await connect_websocket(uri)
        trade_tasks.append(process_trades(websocket, symbol, trade_aggregator))
    
    # Create monitoring task
    monitor_task = asyncio.create_task(monitor_trades(trade_aggregator))
    
    # Run all tasks
    try:
        await asyncio.gather(monitor_task, *trade_tasks)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete.")
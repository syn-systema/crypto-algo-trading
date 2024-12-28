import asyncio
import json
import csv
from datetime import datetime
from typing import List, Dict
import websockets
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init()

class TradeMonitor:
    """
    Cryptocurrency recent trade monitor as specified in PRD section 3.3
    """
    
    def __init__(self, symbols: List[str], csv_path: str = "data/trades.csv"):
        self.symbols = symbols
        self.csv_path = csv_path
        self.ws_url = "wss://fstream.binance.com/ws"
        self.running = False
        
    def get_subscribe_message(self) -> Dict:
        """Create WebSocket subscription message for multiple symbols"""
        streams = [f"{symbol.lower()}@trade" for symbol in self.symbols]
        return {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": 1
        }
        
    async def connect(self):
        """
        Establish WebSocket connection for trade streaming as specified in PRD 3.3.1
        """
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    # Subscribe to trade streams
                    await websocket.send(json.dumps(self.get_subscribe_message()))
                    await self.handle_messages(websocket)
            except Exception as e:
                print(f"{Fore.RED}Connection error: {e}{Style.RESET_ALL}")
                await asyncio.sleep(5)
                
    async def handle_messages(self, websocket):
        """
        Process incoming trade messages
        """
        async for message in websocket:
            data = json.loads(message)
            if 'e' in data and data['e'] == 'trade':
                await self.process_trade(data)
                
    async def process_trade(self, trade):
        """
        Process and display trade data as specified in PRD 3.3.2
        """
        timestamp = datetime.fromtimestamp(trade['T'] / 1000)
        symbol = trade['s']
        side = 'BUY' if trade['m'] else 'SELL'  # true for maker = sell, false for maker = buy
        size = float(trade['q'])
        price = float(trade['p'])
        value_usd = size * price
        
        # Color coding based on trade type and size
        color = Fore.RED if side == 'SELL' else Fore.GREEN
        if value_usd >= 100000:  # Highlight large trades
            color += Style.BRIGHT
            
        # Display trade
        print(f"{color}[TRADE] {timestamp} {symbol}: {side} {size} @ {price} (${value_usd:,.2f}){Style.RESET_ALL}")
        
        # Log trade
        self.log_trade(timestamp, symbol, side, size, price, value_usd)
        
    def log_trade(self, timestamp, symbol, side, size, price, value_usd):
        """
        Log trade data to CSV as specified in PRD 3.3.4
        """
        try:
            with open(self.csv_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp.isoformat(),
                    symbol,
                    side,
                    size,
                    price,
                    value_usd
                ])
        except Exception as e:
            print(f"{Fore.RED}Error logging trade: {e}{Style.RESET_ALL}")
            
    async def start(self):
        """Start monitoring"""
        self.running = True
        await self.connect()
        
    async def stop(self):
        """Stop monitoring"""
        self.running = False

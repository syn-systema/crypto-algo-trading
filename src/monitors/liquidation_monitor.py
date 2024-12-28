import asyncio
import json
import csv
from datetime import datetime
from typing import Optional
import websockets
from colorama import Fore, Style, init
from ..config import BINANCE_MIN_LIQUIDATION_SIZE_USD

# Initialize colorama for cross-platform color support
init()

class LiquidationMonitor:
    """
    Binance Futures liquidation monitor as specified in PRD section 3.2
    """
    
    def __init__(self, csv_path: str = "data/liquidations.csv"):
        self.ws_url = "wss://fstream.binance.com/ws/!forceOrder@arr"
        self.csv_path = csv_path
        self.running = False
        self.total_liquidations = 0
        self.total_volume_usd = 0
        
    async def connect(self):
        """
        Establish WebSocket connection as specified in PRD 3.2.1
        """
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    await self.handle_messages(websocket)
            except Exception as e:
                print(f"{Fore.RED}Connection error: {e}{Style.RESET_ALL}")
                await asyncio.sleep(5)  # Wait before reconnecting
                
    async def handle_messages(self, websocket):
        """
        Process incoming messages as specified in PRD 3.2.2
        """
        async for message in websocket:
            data = json.loads(message)
            for event in data.get('data', []):
                if self.is_significant_liquidation(event):
                    await self.process_liquidation(event)
                    
    def is_significant_liquidation(self, event) -> bool:
        """
        Filter liquidations based on size threshold
        """
        size_usd = float(event['o']['q']) * float(event['o']['p'])
        return size_usd >= BINANCE_MIN_LIQUIDATION_SIZE_USD
        
    async def process_liquidation(self, event):
        """
        Handle significant liquidation events as specified in PRD 3.2.3 and 3.2.4
        """
        timestamp = datetime.fromtimestamp(event['E'] / 1000)
        symbol = event['o']['s']
        side = event['o']['S']
        size = float(event['o']['q'])
        price = float(event['o']['p'])
        size_usd = size * price
        
        # Update statistics
        self.total_liquidations += 1
        self.total_volume_usd += size_usd
        
        # Display alert
        color = Fore.RED if side == 'SELL' else Fore.GREEN
        print(f"{color}[LIQUIDATION] {timestamp} {symbol}: {side} {size} @ {price} (${size_usd:,.2f}){Style.RESET_ALL}")
        
        # Log to CSV
        self.log_liquidation(timestamp, symbol, side, size, price, size_usd)
        
    def log_liquidation(self, timestamp, symbol, side, size, price, size_usd):
        """
        Log liquidation data to CSV as specified in PRD 3.2.4
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
                    size_usd
                ])
        except Exception as e:
            print(f"{Fore.RED}Error logging liquidation: {e}{Style.RESET_ALL}")
            
    async def start(self):
        """Start monitoring"""
        self.running = True
        await self.connect()
        
    async def stop(self):
        """Stop monitoring"""
        self.running = False

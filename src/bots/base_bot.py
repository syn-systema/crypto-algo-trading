import logging
import time
from abc import ABC, abstractmethod
import ccxt
from ..config import (
    EXCHANGE_API_KEY,
    EXCHANGE_SECRET_KEY,
    MAX_POSITION_SIZE,
    STOP_LOSS_PERCENTAGE,
    TAKE_PROFIT_PERCENTAGE,
)

class BaseBot(ABC):
    def __init__(self, exchange_id='binance', symbol='BTC/USDT', timeframe='1h'):
        self.exchange_id = exchange_id
        self.symbol = symbol
        self.timeframe = timeframe
        
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': EXCHANGE_API_KEY,
            'secret': EXCHANGE_SECRET_KEY,
            'enableRateLimit': True,
        })
        
        # Setup logging
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.setLevel(logging.INFO)
        
        # Initialize state
        self.position = None
        self.last_price = None
    
    @abstractmethod
    def calculate_signals(self, data):
        """Calculate trading signals based on the strategy."""
        pass
    
    def fetch_data(self):
        """Fetch OHLCV data from the exchange."""
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=self.symbol,
                timeframe=self.timeframe,
                limit=100
            )
            return ohlcv
        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            return None
    
    def get_position_size(self):
        """Calculate position size based on risk management rules."""
        try:
            balance = self.exchange.fetch_balance()
            available = balance['free']['USDT']
            return min(available * MAX_POSITION_SIZE, available)
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0
    
    def place_order(self, side, amount):
        """Place an order with the exchange."""
        try:
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='market',
                side=side,
                amount=amount
            )
            self.logger.info(f"Placed {side} order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return None
    
    def set_stop_loss(self, entry_price, side):
        """Set stop loss order."""
        try:
            if side == 'buy':
                stop_price = entry_price * (1 - STOP_LOSS_PERCENTAGE)
            else:
                stop_price = entry_price * (1 + STOP_LOSS_PERCENTAGE)
                
            order = self.exchange.create_order(
                symbol=self.symbol,
                type='stop_loss',
                side='sell' if side == 'buy' else 'buy',
                amount=self.position['amount'],
                price=stop_price
            )
            self.logger.info(f"Set stop loss at {stop_price}")
            return order
        except Exception as e:
            self.logger.error(f"Error setting stop loss: {e}")
            return None
    
    def run(self):
        """Main bot loop."""
        self.logger.info(f"Starting {self.__class__.__name__} on {self.symbol}")
        
        while True:
            try:
                # Fetch latest data
                data = self.fetch_data()
                if not data:
                    continue
                
                # Calculate signals
                signal = self.calculate_signals(data)
                
                # Execute trades based on signals
                if signal == 'buy' and not self.position:
                    amount = self.get_position_size()
                    order = self.place_order('buy', amount)
                    if order:
                        self.position = order
                        self.set_stop_loss(order['price'], 'buy')
                
                elif signal == 'sell' and self.position:
                    order = self.place_order('sell', self.position['amount'])
                    if order:
                        self.position = None
                
                # Sleep to avoid hitting rate limits
                time.sleep(self.exchange.rateLimit / 1000)
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def backtest(self, historical_data):
        """Run strategy on historical data."""
        results = []
        position = None
        balance = 10000  # Initial balance in USDT
        
        for candle in historical_data:
            signal = self.calculate_signals([candle])
            
            if signal == 'buy' and not position:
                position = {
                    'price': candle[4],  # Close price
                    'amount': (balance * MAX_POSITION_SIZE) / candle[4]
                }
                balance -= position['amount'] * position['price']
            
            elif signal == 'sell' and position:
                balance += position['amount'] * candle[4]
                position = None
            
            results.append({
                'timestamp': candle[0],
                'price': candle[4],
                'position': position,
                'balance': balance
            })
        
        return results

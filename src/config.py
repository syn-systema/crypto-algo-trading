import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Exchange API Keys
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')
EXCHANGE_SECRET_KEY = os.getenv('EXCHANGE_SECRET_KEY')

# HyperLiquid Configuration
HYPERLIQUID_TESTNET = os.getenv('HYPERLIQUID_TESTNET', 'false').lower() == 'true'
HYPERLIQUID_DEFAULT_LEVERAGE = 1

# Binance Configuration
BINANCE_MIN_LIQUIDATION_SIZE_USD = 100000  # $100k minimum for significant liquidations
BINANCE_LARGE_TRADE_THRESHOLD_USD = 100000  # $100k for large trade highlighting

# Trading Parameters
DEFAULT_TIMEFRAME = '1h'
DEFAULT_SYMBOLS = ['BTC/USDT', 'ETH/USDT']

# Risk Management
MAX_POSITION_SIZE = 0.1  # 10% of portfolio
STOP_LOSS_PERCENTAGE = 0.02  # 2%
TAKE_PROFIT_PERCENTAGE = 0.04  # 4%

# Technical Analysis
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

SMA_SHORT_PERIOD = 20
SMA_LONG_PERIOD = 50

VWAP_PERIOD = '1d'

# Backtesting
INITIAL_BALANCE = 10000  # USDT
TRADING_FEE = 0.001  # 0.1%

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Data Storage
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

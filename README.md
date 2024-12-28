# Crypto Algorithmic Trading Platform

A comprehensive cryptocurrency trading platform that implements various algorithmic trading strategies.

## Features

- Multiple trading strategies:
  - RSI (Relative Strength Index)
  - SMA (Simple Moving Average)
  - VWAP (Volume Weighted Average Price)
  - Hyperliquid Integration
- Real-time data streaming
- Backtesting capabilities
- Risk management
- Performance analytics

## Project Structure

```
crypto-algo-trading/
├── src/
│   ├── bots/           # Trading bot implementations
│   ├── analysis/       # Technical analysis tools
│   ├── data/           # Data handling and storage
│   └── utils/          # Utility functions
├── Backtesting/        # Backtesting framework
└── Datastreams/        # Real-time data handling
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-algo-trading.git
cd crypto-algo-trading
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
EXCHANGE_API_KEY=your_api_key
EXCHANGE_SECRET_KEY=your_secret_key
```

## Usage

1. To run a specific trading bot:
```bash
python src/bots/rsi_bot.py
```

2. For backtesting:
```bash
python backtesting/backtest.py --strategy rsi --timeframe 1d
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

# Trading Bot — Binance Futures Demo

A Python trading bot for placing orders on Binance Futures Demo (USDT-M).

## Setup

1. Clone the repo and navigate to the project folder:
   ```bash
   cd trading_bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your API credentials from [demo.binance.com](https://demo.binance.com/en/my/settings/api-management):
   ```bash
   cp .env.example .env
   ```

## How to Run

### CLI
```bash
# Market BUY order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Limit SELL order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 90000

# Stop-Limit BUY order (bonus — supported on live exchange, not demo)
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.01 --price 85000 --stop-price 84000
```

### Web UI (bonus)
```bash
python app.py
```
Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
trading_bot/
├── bot/
│   ├── client.py          # API auth and connection
│   ├── orders.py          # order placement logic
│   ├── validators.py      # input validation
│   └── logging_config.py  # logging setup
├── logs/                  # log files (auto-created)
├── cli.py                 # CLI entry point
├── .env                   # API credentials (not committed)
├── .env.example           # credentials template
└── requirements.txt
```

## Assumptions

- Uses Binance Futures Demo (`https://demo-fapi.binance.com`)
- API key must have "Enable Futures" permission enabled
- Credentials stored in `.env`, never committed to git
- Logs saved to `logs/trading_bot_YYYYMMDD.log`
- STOP order type is a Stop-Limit order (requires both `--price` and `--stop-price`)

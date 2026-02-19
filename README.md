# Binance Futures Testnet Trading Bot

A lightweight Python CLI trading bot for placing orders on Binance Futures Testnet (USDT-M).
Supports MARKET, LIMIT, and STOP orders with structured logging and error handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client (signing, requests)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/
│   └── trading_bot.log    # Auto-generated log file
├── cli.py                 # Entry point
├── Dockerfile
├── .env                   # API credentials (not committed)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Get Testnet API Keys
- Go to https://testnet.binancefuture.com
- Log in with **GitHub** (only login method supported)
- Click **API Key** in the top navigation bar
- Copy your `API Key` and `Secret Key` — secret is shown only once

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/trading_bot.git
cd trading_bot
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Credentials
Create a `.env` file in the root folder:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### Normal Python
```bash
python cli.py
```

### Docker
```bash
# Build the image
docker build -t trading_bot .

# Run with interactive mode
docker run -it trading_bot
```


## Assumptions

- Testnet only — base URL is `https://testnet.binancefuture.com`
- API credentials are stored in `.env` and never committed to version control
- Supported symbols limited to: `BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT`
- STOP order uses `STOP` type (not `STOP_MARKET`) — requires both a limit price and stop trigger price
---

## Requirements

```
requests
python-dotenv
```

Install with:
```bash
pip install -r requirements.txt
```

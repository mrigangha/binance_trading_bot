import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import validate_order

load_dotenv()
logger = setup_logger()


def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Missing API credentials in .env")
        sys.exit(1)
    return BinanceClient(api_key, api_secret)


def get_input():
    print("   Binance Futures Testnet — Trading Bot   ")

    # Symbol
    print("Available symbols: BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT")
    symbol = input("Enter symbol (e.g. BTCUSDT): ").strip().upper()

    # Side
    print("Available sides: BUY, SELL")
    side = input("Enter side (BUY/SELL): ").strip().upper()

    # Order type
    print("Available order types: MARKET, LIMIT, STOP")
    order_type = input("Enter order type: ").strip().upper()

    # Quantity
    quantity = input("Enter quantity (e.g. 0.002): ").strip()

    # Price — only for LIMIT / STOP
    price = None
    stop_price = None

    if order_type in ("LIMIT", "STOP"):
        price = input("Enter price: ").strip()
        price = float(price) if price else None

    if order_type == "STOP":
        stop_price = input("Enter stop price: ").strip()
        stop_price = float(stop_price) if stop_price else None

    return symbol, side, order_type, float(quantity), price, stop_price


def main():
    symbol, side, order_type, quantity, price, stop_price = get_input()

    # The Order Request Values
    print("Order Request")
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price:
        print(f"Price      : {price}")
    if stop_price:
        print(f"Stop Price : {stop_price}")

    try:
        validate_order(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as e:
        print(f"Validation error:\n{e}")
        sys.exit(1)

    confirm = input("Confirm order? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Order cancelled.")
        exit(0)

    client = get_client()
    try:
        resp = place_order(
            client, symbol, side, order_type, quantity, price, stop_price
        )
    except Exception as e:
        print(f"Failed:{e}")
        exit(0)

    # Final Order Response
    print("Order Response")
    print(f"  Order ID     : {resp.get('orderId')}")
    print(f"  Status       : {resp.get('status')}")
    print(f"  Executed Qty : {resp.get('executedQty')}")
    print(f"  Avg Price    : {resp.get('avgPrice', 'N/A')}")
    print("Order Placed Successfully!\n")


if __name__ == "__main__":
    main()

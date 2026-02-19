from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()
ENDPOINT = "/fapi/v1/order"


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None,
) -> dict:
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    elif order_type.upper() == "STOP":
        params["price"] = price
        params["stopPrice"] = stop_price
        params["timeInForce"] = "GTC"

    logger.info(
        f"Placing {order_type} {side} | symbol={symbol} qty={quantity}"
        + (f" price={price}" if price else "")
        + (f" stopPrice={stop_price}" if stop_price else "")
    )

    response = client.post(ENDPOINT, params)

    logger.info(
        f"Order success | orderId={response.get('orderId')} "
        f"status={response.get('status')} "
        f"executedQty={response.get('executedQty')} "
        f"avgPrice={response.get('avgPrice')}"
    )
    return response

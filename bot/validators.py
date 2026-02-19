VALID_SYMBOLS = {"BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT"}
VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}


def validate_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    errors = []

    if symbol.upper() not in VALID_SYMBOLS:
        errors.append(f"Invalid symbol '{symbol}'. Valid: {','.join(VALID_SYMBOLS)}")

    if side.upper() not in VALID_SIDES:
        errors.append(f"Invalid side '{side}'. Must be BUY or SELL.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        errors.append(f"Invalid order type. Valid: MARKET, LIMIT, STOP.")

    try:
        qty = float(quantity)
        if qty <= 0:
            errors.append("Quantity must be greater than 0.")
    except (TypeError, ValueError):
        errors.append("Quantity must be a valid number.")

    if order_type.upper() in ("LIMIT", "STOP"):
        if price is None:
            errors.append("Price is required for LIMIT and STOP orders.")
        else:
            try:
                if float(price) <= 0:
                    errors.append("Price must be greater than 0.")
            except (TypeError, ValueError):
                errors.append("Price must be a valid number.")

    if order_type.upper() == "STOP" and stop_price is None:
        errors.append("--stop-price is required for STOP orders.")

    if errors:
        raise ValueError("\n".join(errors))

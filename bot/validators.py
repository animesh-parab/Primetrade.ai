from bot.logging_config import setup_logger

logger = setup_logger("validators")

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP"}

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    errors = []

    if not symbol or not symbol.isalpha():
        errors.append(f"Invalid symbol: '{symbol}'. Must be alphabetic (e.g. BTCUSDT).")

    if side.upper() not in VALID_SIDES:
        errors.append(f"Invalid side: '{side}'. Must be BUY or SELL.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        errors.append(f"Invalid order type: '{order_type}'. Must be MARKET, LIMIT, or STOP.")

    if quantity <= 0:
        errors.append(f"Invalid quantity: '{quantity}'. Must be greater than 0.")

    if order_type.upper() == "LIMIT":
        if price is None:
            errors.append("Price is required for LIMIT orders.")
        elif price <= 0:
            errors.append(f"Invalid price: '{price}'. Must be greater than 0.")

    if order_type.upper() == "STOP":
        if price is None:
            errors.append("Price (limit price) is required for STOP orders.")
        elif price <= 0:
            errors.append(f"Invalid price: '{price}'. Must be greater than 0.")
        if stop_price is None:
            errors.append("Stop price is required for STOP orders.")
        elif stop_price <= 0:
            errors.append(f"Invalid stop price: '{stop_price}'. Must be greater than 0.")

    if errors:
        for e in errors:
            logger.error(f"Validation error: {e}")
        raise ValueError("\n".join(errors))

    logger.debug(f"Inputs validated: symbol={symbol}, side={side}, type={order_type}, qty={quantity}, price={price}, stop_price={stop_price}")

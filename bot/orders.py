import time
import requests
from bot.client import BASE_URL, get_credentials, sign, get_headers
from bot.logging_config import setup_logger

logger = setup_logger("orders")

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None) -> dict:
    api_key, api_secret = get_credentials()

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
        "timestamp": int(time.time() * 1000),
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    if order_type.upper() == "STOP":
        params["price"] = price
        params["stopPrice"] = stop_price
        params["timeInForce"] = "GTC"

    params["signature"] = sign(params, api_secret)

    logger.debug(f"Placing order: {params}")

    try:
        r = requests.post(
            f"{BASE_URL}/fapi/v1/order",
            headers=get_headers(api_key),
            params=params,
            timeout=10
        )
        response = r.json() if r.text.strip() else {}
        logger.debug(f"Order response: {response} (status: {r.status_code})")

        if r.status_code not in (200, 202):
            msg = response.get("msg", r.text)
            logger.error(f"API error {response.get('code')}: {msg}")
            raise Exception(f"API error {response.get('code')}: {msg}")

        # 202 with empty body = order accepted by demo API
        if not response:
            response = {"status": "ACCEPTED", "note": "Order accepted (demo API returned empty body)"}

        return response

    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        raise

import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger("client")

BASE_URL = "https://demo-fapi.binance.com"

def get_credentials():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        logger.error("Missing API credentials. Check your .env file.")
        raise EnvironmentError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")
    return api_key, api_secret

def sign(params: dict, secret: str) -> str:
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

def get_headers(api_key: str) -> dict:
    return {"X-MBX-APIKEY": api_key}

def test_connection() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/fapi/v1/ping", timeout=5)
        if r.status_code in (200, 202):
            logger.info("Connection to Binance Futures Testnet successful.")
            return True
        logger.error(f"Ping failed: {r.status_code} {r.text}")
        return False
    except requests.RequestException as e:
        logger.error(f"Connection error: {e}")
        return False

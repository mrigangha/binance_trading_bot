import hashlib
import hmac
import time

import requests

from bot.logging_config import setup_logger

BASE_URL = "https://testnet.binancefuture.com"
logger = setup_logger()


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query = "&".join(f"{k}={v}" for k, v in params.items())
        signature = hmac.new(
            self.api_secret.encode(), query.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.debug(
            f"POST {url} | params: { {k: v for k, v in signed.items() if k != 'signature'} }"
        )
        try:
            resp = self.session.post(url, params=signed, timeout=10)
            data = resp.json()
            logger.debug(f"Response [{resp.status_code}]: {data}")
            resp.raise_for_status()
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | Response: {resp.text}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Network error: could not reach Binance testnet")
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise

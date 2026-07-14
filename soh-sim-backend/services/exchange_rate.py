import logging
import time
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

_FREE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
_FALLBACK_API_URL = "https://open.er-api.com/v6/latest/USD"

_CACHE = {"rates": {}, "updated_at": 0}
_CACHE_TTL = 30 * 60


def _fetch_from_api(url, timeout=10):
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _get_rates_raw():
    now = time.time()
    if _CACHE["rates"] and (now - _CACHE["updated_at"]) < _CACHE_TTL:
        return _CACHE["rates"], _CACHE["updated_at"], "cache"

    try:
        data = _fetch_from_api(_FREE_API_URL)
        source = "api.exchangerate-api.com"
    except Exception:
        logger.warning("Primary exchange rate API failed, trying fallback")
        data = _fetch_from_api(_FALLBACK_API_URL)
        source = "open.er-api.com"

    rates = data.get("rates", {})
    _CACHE["rates"] = rates
    _CACHE["updated_at"] = now

    return rates, now, source


def get_all_rates():
    rates, ts, source = _get_rates_raw()
    updated_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    items = {}
    for code, rate in rates.items():
        items[code] = {"rate": rate, "source": source, "date": updated_str}
    return items, updated_str


def get_rate(currency):
    rates, ts, source = _get_rates_raw()
    updated_str = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    rate = rates.get(currency.upper())
    if rate is None:
        return None
    return {"rate": rate, "source": source, "date": updated_str}, updated_str


def refresh_all_rates():
    _CACHE["updated_at"] = 0
    return get_all_rates()

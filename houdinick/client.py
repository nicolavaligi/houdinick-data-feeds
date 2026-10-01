"""Houdinick Data Feeds — Lightweight Python Client (Zero Dependencies).

Allows programmatic streaming of Italian B2B feeds:
1. Public Tenders & PNRR Contracts (Gare d'Appalto)
2. Environmental Remediation & Brownfields (Bonifiche Ambientali)
3. Photovoltaic Land & Expropriations (Terreni FV ed Espropri)
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any, Dict, Generator, List, Optional


class HoudinickClient:
    """Client for Houdinick Data APIs."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        rapidapi_key: Optional[str] = None,
        base_url_tenders: str = "https://houdinick-data-api-production.up.railway.app",
        base_url_remediation: str = "https://houdinick-remediation-api-production.up.railway.app",
        base_url_data: str = "https://houdinick-data-api-production.up.railway.app",
    ):
        self.api_key = api_key
        self.rapidapi_key = rapidapi_key
        self.base_url_tenders = base_url_tenders.rstrip("/")
        self.base_url_remediation = base_url_remediation.rstrip("/")
        self.base_url_data = base_url_data.rstrip("/")

    def _get_headers(self) -> Dict[str, str]:
        headers = {"User-Agent": "Houdinick-Python-SDK/1.0"}
        if self.rapidapi_key:
            headers["X-RapidAPI-Key"] = self.rapidapi_key
            headers["X-RapidAPI-Host"] = urllib.parse.urlparse(self.base_url_tenders).netloc
        elif self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        filtered_params = {k: v for k, v in params.items() if v is not None}
        if filtered_params:
            query_string = urllib.parse.urlencode(filtered_params)
            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}{query_string}"
        else:
            full_url = url

        req = urllib.request.Request(full_url, headers=self._get_headers())
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)

    # ------------------------------------------------------------------
    # 1. Tenders & PNRR Contracts
    # ------------------------------------------------------------------
    def get_tenders(
        self,
        category: Optional[str] = None,
        location: Optional[str] = None,
        since_seq: int = 0,
        value_min: Optional[float] = None,
        value_max: Optional[float] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Fetch a page of public tenders and PNRR contracts."""
        url = f"{self.base_url_tenders}/api/v1/tenders"
        params = {
            "category": category,
            "location": location,
            "since_seq": since_seq,
            "value_min": value_min,
            "value_max": value_max,
            "limit": limit,
        }
        return self._request(url, params)

    def stream_tenders(
        self,
        category: Optional[str] = None,
        location: Optional[str] = None,
        start_seq: int = 0,
        batch_size: int = 100,
    ) -> Generator[Dict[str, Any], None, None]:
        """Stream tenders continuously using the monotonic incremental cursor."""
        current_seq = start_seq
        while True:
            page = self.get_tenders(
                category=category,
                location=location,
                since_seq=current_seq,
                limit=batch_size,
            )
            items = page.get("items", [])
            if not items:
                break
            for item in items:
                yield item
            current_seq = page.get("next_seq", current_seq)
            if len(items) < batch_size:
                break

    # ------------------------------------------------------------------
    # 2. Environmental Remediation & Brownfields
    # ------------------------------------------------------------------
    def get_remediation_sites(
        self,
        category: Optional[str] = None,
        location: Optional[str] = None,
        since_seq: int = 0,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Fetch a page of contaminated sites, SIN and brownfields."""
        url = f"{self.base_url_remediation}/api/v1/feed"
        params = {
            "category": category,
            "location": location,
            "since_seq": since_seq,
            "limit": limit,
        }
        return self._request(url, params)

    # ------------------------------------------------------------------
    # 3. Solar PV Land & Expropriations
    # ------------------------------------------------------------------
    def get_solar_land(
        self,
        category: Optional[str] = None,
        location: Optional[str] = None,
        since_seq: int = 0,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """Fetch a page of photovoltaic land opportunities and expropriations."""
        url = f"{self.base_url_data}/api/v1/feed"
        params = {
            "category": category,
            "location": location,
            "since_seq": since_seq,
            "limit": limit,
        }
        return self._request(url, params)

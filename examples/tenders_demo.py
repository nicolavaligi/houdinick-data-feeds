#!/usr/bin/env python3
"""Example: Monitor Italian Public Tenders & PNRR Contracts with Houdinick API."""
import os
import sys

# Allow importing local houdinick module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from houdinick import HoudinickClient


def main():
    # Retrieve API Key from environment or use test key
    api_key = os.getenv("HOUDINICK_API_KEY", "hn_tenders_test_key_001")
    client = HoudinickClient(api_key=api_key)

    print("=== Houdinick Tenders API Demo ===")
    print("Fetching major PNRR contracts in Lombardia above €10M...\n")

    page = client.get_tenders(
        category="pnrr_appalto",
        location="Lombardia",
        value_min=10_000_000,
        limit=5,
    )

    tenders = page.get("items", [])
    print(f"Found {len(tenders)} contracts:")
    for t in tenders:
        payload = t.get("payload", {})
        print(f"[{payload.get('codice_cig')}] {t.get('title')}")
        print(f"   Stazione Appaltante: {payload.get('stazione_appaltante')}")
        print(f"   Importo a base d'asta: €{t.get('value_num'):,.2f}")
        print(f"   Scadenza: {payload.get('scadenza_offerte')}")
        print(f"   Location: {t.get('location')}")
        print("-" * 60)

    print(f"\nNext cursor sequence for polling: since_seq={page.get('next_seq')}")


if __name__ == "__main__":
    main()

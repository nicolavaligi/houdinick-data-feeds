#!/usr/bin/env python3
"""Example: Discover Industrial Land & Substation Proximity for Solar PV with Houdinick API."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from houdinick import HoudinickClient


def main():
    api_key = os.getenv("HOUDINICK_API_KEY", "hn_UrUVEJYpojMUXkHKwIykZ36qyi2MK4Rg7RCU8mtjcwY")
    client = HoudinickClient(api_key=api_key)

    print("=== Houdinick Solar PV & Expropriation Demo ===")
    print("Fetching top-ranked industrial land opportunities for solar PV in Milano...\n")

    page = client.get_solar_land(
        category="fotovoltaico",
        location="Milano",
        limit=3,
    )

    sites = page.get("items", [])
    print(f"Found {len(sites)} sites:")
    for s in sites:
        payload = s.get("payload", {})
        print(f"[{s.get('source_id')}] {s.get('title')}")
        print(f"   Superficie: {s.get('value_num'):,} mq")
        print(f"   Cabina Primaria di Riferimento: {payload.get('cabina')}")
        print(f"   Punteggio Idoneità: {payload.get('punteggio')}/100")
        print(f"   OpenStreetMap: {payload.get('osm')}")
        print("-" * 60)

    print(f"\nNext cursor sequence: since_seq={page.get('next_seq')}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Example: Query Italian Contaminated Sites, SIN and Brownfields with Houdinick API."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from houdinick import HoudinickClient


def main():
    api_key = os.getenv("HOUDINICK_API_KEY", "hn_remediation_test_key_001")
    client = HoudinickClient(api_key=api_key)

    print("=== Houdinick Remediation API Demo ===")
    print("Fetching National Priority Contaminated Sites (SIN) in Veneto...\n")

    page = client.get_remediation_sites(
        category="sin",
        location="Veneto",
        limit=5,
    )

    sites = page.get("items", [])
    print(f"Found {len(sites)} contaminated sites / brownfields:")
    for s in sites:
        payload = s.get("payload", {})
        print(f"[{s.get('source_id')}] {s.get('title')}")
        print(f"   Stato Bonifica: {s.get('value_text')}")
        print(f"   Superficie: {s.get('value_num')} ha ({payload.get('superficie_mq', 0):,} mq)")
        print(f"   Contaminanti: {', '.join(payload.get('contaminanti_principali', []))}")
        print(f"   Idoneità Rinnovabili: {payload.get('potenziale_repowering_rinnovabili')}")
        print("-" * 60)

    print(f"\nNext cursor sequence: since_seq={page.get('next_seq')}")


if __name__ == "__main__":
    main()

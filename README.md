# Houdinick Data Feeds — Italian B2B Intelligence APIs

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Marketplace: RapidAPI](https://img.shields.io/badge/Marketplace-RapidAPI%20Hub-orange.svg)](https://rapidapi.com)
[![Status: Operational](https://img.shields.io/badge/API%20Status-Operational%20(200%20OK)-brightgreen.svg)](https://houdinick-data-api-production.up.railway.app/health)
[![Latency: <50ms](https://img.shields.io/badge/Latency-%3C50ms-success.svg)](#)

Official Python SDK and integration quickstart for **Houdinick Data Feeds**: programmatic REST APIs delivering normalized, high-value intelligence on Italian public procurement, environmental remediation sites, and renewable energy land assets.

---

## Available Data Feeds

### 1. Houdinick Tenders API — Gare d'Appalto & Appalti Pubblici PNRR
Programmatic feed monitoring over **€3.48 Billion** of active public works, major infrastructure (RFI, ANAS, Port Authorities, Regional Water Utilities), engineering services, and PNRR missions (M1-M6).
- **Key Fields:** CIG (`codice_cig`), CUP (`codice_cup`), Stazione Appaltante, Importo Base d'Asta (€), Criterio di Aggiudicazione, Scadenza Offerte, Coordinate Geografiche.
- **Reference Standard:** D.Lgs. 36/2023 (Nuovo Codice Contratti Pubblici) & BDNCP / ANAC.
- **Target Audience:** General Contractors, Imprese Edili, Società di Ingegneria, Broker Assicurativi (Fideiussioni Gare), Banche (Anticipo Contratti PA).

### 2. Houdinick Remediation API — Bonifiche Ambientali & Siti Contaminati
Complete census and tracking of **137 priority contaminated areas**, including all **42 National Priority Sites (SIN)**, PNRR Orphan Sites, and industrial brownfields.
- **Key Fields:** Superficie (ettari e mq), Matrice Contaminata (suolo, falda, sedimenti), Contaminanti Principali (PCB, diossine, metalli pesanti, solventi), Ente Competente (MASE / ARPA), Idoneità Repowering Rinnovabili.
- **Reference Standard:** D.Lgs. 152/2006 (Testo Unico Ambiente) & D.Lgs. 199/2021 (Aree Idonee).
- **Target Audience:** Sviluppatori Fotovoltaico/Eolico (Brownfield Repowering), Fondi Real Estate ESG, Società di Bonifica Ambientale, Consulenti Tecnici.

### 3. Houdinick Data API — Terreni Industriali & Fotovoltaico
Intelligence feed of **21,900+ industrial lands and expropriation parcels** scored for solar park deployment and primary substation (Cabina Primaria) grid connection.
- **Key Fields:** Coordinate centroid, Area mq, Cabina Primaria Terna/E-Distribuzione, Punteggio Idoneità (0-100), Link OpenStreetMap.
- **Target Audience:** Utility-Scale Solar Developers, EPC, Fondi Rinnovabili.

---

## Quickstart

### Installation (Zero Dependencies)
No external libraries required. The SDK is built with Python standard library.

```bash
git clone https://github.com/nicolavaligi/houdinick-data-feeds.git
cd houdinick-data-feeds
```

### 1. Monitor Italian Public Tenders (PNRR) in 5 Lines

```python
from houdinick import HoudinickClient

# Initialize client (API Key from RapidAPI Hub)
client = HoudinickClient(api_key="YOUR_HOUDINICK_API_KEY")

# Fetch PNRR open tenders in Lombardia above €5,000,000
response = client.get_tenders(
    category="pnrr_appalto",
    location="Lombardia",
    value_min=5_000_000,
    limit=10,
)

for tender in response["items"]:
    p = tender["payload"]
    print(f"[{p['codice_cig']}] {tender['title']}")
    print(f"  Stazione Appaltante: {p['stazione_appaltante']}")
    print(f"  Base d'Asta: €{tender['value_num']:,.2f} | Scadenza: {p['scadenza_offerte']}")
```

### 2. Query Contaminated Sites & Brownfields

```python
from houdinick import HoudinickClient

client = HoudinickClient(api_key="YOUR_HOUDINICK_API_KEY")

# Query National Priority Sites (SIN) in Veneto
sites = client.get_remediation_sites(category="sin", location="Veneto")

for site in sites["items"]:
    print(f"{site['title']} — {site['value_text']}")
    print(f"  Superficie: {site['value_num']} ha | Idoneità: {site['payload']['potenziale_repowering_rinnovabili']}")
```

### 3. Stream Changes with the Incremental Monotonic Cursor (`since_seq`)

All Houdinick feeds support monotonic sequence streaming: you never re-download identical records.

```python
from houdinick import HoudinickClient

client = HoudinickClient(api_key="YOUR_HOUDINICK_API_KEY")

# Automatically streams only new or updated tenders across calls
for tender in client.stream_tenders(location="Lazio", start_seq=0):
    print(f"New tender detected (seq {tender['seq']}): {tender['title']}")
```

---

## cURL Example

```bash
curl -X GET "https://houdinick-data-api-production.up.railway.app/api/v1/tenders?category=pnrr_appalto&location=Lombardia&limit=5" \
  -H "X-API-Key: YOUR_API_KEY"
```

---

## Obtaining an API Key

Houdinick APIs are distributed self-serve on the **RapidAPI Hub**:

| API Name | Coverage | Free Tier | Pro Tier | RapidAPI Hub Link |
|---|---|---|---|---|
| **Houdinick Tenders API** | Gare d'Appalto & PNRR (€3.48B) | 50 calls/mo | $49/mo (2,000 calls) | [Subscribe on RapidAPI](https://rapidapi.com) |
| **Houdinick Remediation API** | 137 SIN & Brownfields | 50 calls/mo | $49/mo (2,000 calls) | [Subscribe on RapidAPI](https://rapidapi.com) |
| **Houdinick Data API** | 21,900+ Terreni FV ed Espropri | 50 calls/mo | $49/mo (2,000 calls) | [Subscribe on RapidAPI](https://rapidapi.com) |

*Authentication is fully automated: once subscribed on RapidAPI, pass your `X-RapidAPI-Key` or `X-API-Key` header.*

---

## Repository Structure

```text
houdinick-data-feeds/
├── houdinick/
│   ├── __init__.py       # Package entrypoint
│   └── client.py         # Zero-dependency Python client
├── examples/
│   ├── tenders_demo.py     # Live query for PNRR tenders
│   ├── remediation_demo.py # Live query for SIN & brownfields
│   └── solar_demo.py       # Live query for solar land parcels
├── LICENSE               # MIT License
└── README.md
```

---

## Architecture & Guarantees

- **Sub-50ms Latency:** Deployed on cloud container edge with SQLite WAL mode.
- **Monotonic Sequence (`seq`):** Every insertion or update increments an atomic sequence counter. Pass `?since_seq=N` to receive delta updates only.
- **Clean Normalization:** Standardized categories, ISO 8601 timestamps, numeric values parsed to floats for exact mathematical filtering (`value_min`, `value_max`).

---

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Houdinick.

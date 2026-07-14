#!/usr/bin/env python3
"""
Refresh Tesla Supercharger public data from the public Tesla Find Us pages.

The page contains a public Next.js JSON payload in:
<script id="__NEXT_DATA__" type="application/json">...</script>

Updated fields:
- pricing for Tesla vehicles/members
- congestion fees
- access hours
- exit/access instructions
- number of stalls
- maximum power
- status
- coordinates and address when available
- last updated date
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

NEXT_DATA_RE = re.compile(
    r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

USER_AGENT = (
    "Mozilla/5.0 (compatible; TeslaChargeCompanion/1.0; "
    "+https://github.com/)"
)


def fetch_html(url: str, timeout: int = 30) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.7",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_next_data(page: str) -> dict[str, Any]:
    match = NEXT_DATA_RE.search(page)
    if not match:
        raise ValueError("__NEXT_DATA__ introuvable")
    return json.loads(html_lib.unescape(match.group(1)))


def days_object(twenty_four_seven: bool, regular_hours: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if twenty_four_seven:
        return {
            str(i): {"open": True, "start": "00:00", "end": "24:00"}
            for i in range(7)
        }

    result = {
        str(i): {"open": False, "start": "00:00", "end": "00:00"}
        for i in range(7)
    }
    # Tesla uses 1=Monday ... 7=Sunday. JS Date uses 0=Sunday ... 6=Saturday.
    weekday_map = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "0"}
    for item in regular_hours or []:
        key = weekday_map.get(int(item.get("weekday", 0)))
        if key is None:
            continue
        result[key] = {
            "open": True,
            "start": item.get("periodBegin") or "00:00",
            "end": item.get("periodEnd") or "24:00",
        }
    return result


def member_price_rules(pricebooks: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], float]:
    rules: list[dict[str, Any]] = []
    congestion_fee = 0.0

    charging = [
        p
        for p in pricebooks or []
        if p.get("vehicleMakeType") == "TSLA"
        and p.get("isMemberPricebook") is True
        and p.get("feeType") == "CHARGING"
    ]

    base = next((p for p in charging if not p.get("isTou")), None)
    tou = [p for p in charging if p.get("isTou")]

    if base:
        rules.append(
            {
                "scope": "allDay",
                "billing": "kwh" if str(base.get("uom", "")).lower() == "kwh" else "minute",
                "currency": base.get("currencyCode") or "EUR",
                "pricePerKwh": float(base.get("rateBase") or 0),
                "chargePerMinute": float(base.get("rateBase") or 0)
                if str(base.get("uom", "")).lower() != "kwh"
                else 0,
                "connectionFee": 0,
                "idlePerMinute": 0,
            }
        )

    for item in tou:
        start = item.get("startTime") or "00:00"
        end = item.get("endTime") or "24:00"
        uom = str(item.get("uom", "")).lower()
        rules.append(
            {
                "scope": "timeWindow",
                "start": start,
                "end": end,
                "billing": "kwh" if uom == "kwh" else "minute",
                "currency": item.get("currencyCode") or "EUR",
                "pricePerKwh": float(item.get("rateBase") or 0) if uom == "kwh" else 0,
                "chargePerMinute": float(item.get("rateBase") or 0) if uom != "kwh" else 0,
                "connectionFee": 0,
                "idlePerMinute": 0,
            }
        )

    congestion = next(
        (
            p
            for p in pricebooks or []
            if p.get("vehicleMakeType") == "TSLA"
            and p.get("isMemberPricebook") is True
            and p.get("feeType") == "CONGESTION"
        ),
        None,
    )
    if congestion:
        congestion_fee = float(congestion.get("rateBase") or 0)

    return rules, congestion_fee


def update_station(station: dict[str, Any], payload: dict[str, Any]) -> bool:
    formatted = payload.get("props", {}).get("pageProps", {}).get("formattedData", {})
    details = formatted.get("chargerDetails", {})
    pricebooks = details.get("effectivePricebooks", [])
    rules, congestion = member_price_rules(pricebooks)

    if not rules:
        raise ValueError("aucun tarif Tesla/membre trouvé")

    station["operator"] = "Tesla"
    station["source"] = "teslaSupercharger"
    station["pricing"] = {"type": "rules", "rules": rules}
    station["congestionFeePerMinute"] = congestion
    station["stalls"] = int(details.get("publicStallCount") or formatted.get("chargerQuantity") or station.get("stalls") or 0)
    station["powerKw"] = float(details.get("maxPowerKw") or formatted.get("chargerMaxPower") or station.get("powerKw") or 0)
    station["lastUpdated"] = date.today().isoformat()
    station["status"] = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("locationData", {})
        .get("key_data", {})
        .get("status", {})
        .get("name", "Open")
    )

    address = details.get("address", {})
    street = " ".join(filter(None, [address.get("streetNumber"), address.get("street")])).strip()
    city_line = " ".join(filter(None, [address.get("postalCode"), address.get("city")])).strip()
    if street or city_line:
        station["address"] = ", ".join(filter(None, [street, city_line, address.get("country")]))

    entry = details.get("entryPoint", {})
    if entry.get("latitude") is not None:
        station["latitude"] = float(entry["latitude"])
    if entry.get("longitude") is not None:
        station["longitude"] = float(entry["longitude"])

    access_hours = details.get("accessHours", {})
    twenty_four_seven = bool(access_hours.get("twentyFourSeven"))
    regular_hours = access_hours.get("regularHours") or []
    nearest_entrance = address.get("nearestEntrance") or ""

    station["access"] = {
        "limited": not twenty_four_seven,
        "days": days_object(twenty_four_seven, regular_hours),
        # Tesla public data may include a code/instruction permitting exit after closing.
        "afterCloseMode": "exit_allowed" if nearest_entrance else "must_stop",
        "afterCloseNote": nearest_entrance
        or ("Accessible 24 h/24." if twenty_four_seven else "Respecter les horaires d’accès du site."),
    }
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stations", default="data/tesla_stations.json")
    parser.add_argument("--delay", type=float, default=0.35)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    path = Path(args.stations)
    stations = json.loads(path.read_text(encoding="utf-8"))

    tesla_stations = [
        s
        for s in stations
        if s.get("source") == "teslaSupercharger" and s.get("teslaUrl")
    ]
    if args.limit > 0:
        tesla_stations = tesla_stations[: args.limit]

    success = 0
    failures: list[str] = []

    for index, station in enumerate(tesla_stations, start=1):
        url = station["teslaUrl"]
        try:
            page = fetch_html(url)
            payload = extract_next_data(page)
            update_station(station, payload)
            success += 1
            print(f"[{index}/{len(tesla_stations)}] OK {station.get('name')}")
        except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{station.get('name')}: {exc}")
            print(f"[{index}/{len(tesla_stations)}] ERREUR {station.get('name')}: {exc}", file=sys.stderr)
        time.sleep(max(0.0, args.delay))

    path.write_text(json.dumps(stations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata_path = path.parent / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        metadata = {}
    metadata["teslaUpdated"] = date.today().isoformat()
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Mises à jour réussies : {success}/{len(tesla_stations)}")
    if failures:
        print("Échecs :", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)

    # Do not fail the entire workflow if only a small subset is unavailable.
    return 0 if success > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

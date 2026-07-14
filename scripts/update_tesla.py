#!/usr/bin/env python3
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

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

NEXT_DATA_RE = re.compile(
    r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

def extract_next_data(page_html: str) -> dict[str, Any]:
    match = NEXT_DATA_RE.search(page_html)
    if not match:
        raise ValueError("__NEXT_DATA__ introuvable")
    return json.loads(html_lib.unescape(match.group(1)))

def days_object(twenty_four_seven: bool, regular_hours: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if twenty_four_seven:
        return {str(i): {"open": True, "start": "00:00", "end": "24:00"} for i in range(7)}
    result = {str(i): {"open": False, "start": "00:00", "end": "00:00"} for i in range(7)}
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
        p for p in pricebooks or []
        if p.get("vehicleMakeType") == "TSLA"
        and p.get("isMemberPricebook") is True
        and p.get("feeType") == "CHARGING"
    ]
    base = next((p for p in charging if not p.get("isTou")), None)
    tou = [p for p in charging if p.get("isTou")]

    if base:
        uom = str(base.get("uom", "")).lower()
        rules.append({
            "scope": "allDay",
            "billing": "kwh" if uom == "kwh" else "minute",
            "currency": base.get("currencyCode") or "EUR",
            "pricePerKwh": float(base.get("rateBase") or 0) if uom == "kwh" else 0,
            "chargePerMinute": float(base.get("rateBase") or 0) if uom != "kwh" else 0,
            "connectionFee": 0,
            "idlePerMinute": 0,
        })

    for item in tou:
        uom = str(item.get("uom", "")).lower()
        rules.append({
            "scope": "timeWindow",
            "start": item.get("startTime") or "00:00",
            "end": item.get("endTime") or "24:00",
            "billing": "kwh" if uom == "kwh" else "minute",
            "currency": item.get("currencyCode") or "EUR",
            "pricePerKwh": float(item.get("rateBase") or 0) if uom == "kwh" else 0,
            "chargePerMinute": float(item.get("rateBase") or 0) if uom != "kwh" else 0,
            "connectionFee": 0,
            "idlePerMinute": 0,
        })

    congestion = next(
        (p for p in pricebooks or []
         if p.get("vehicleMakeType") == "TSLA"
         and p.get("isMemberPricebook") is True
         and p.get("feeType") == "CONGESTION"),
        None,
    )
    if congestion:
        congestion_fee = float(congestion.get("rateBase") or 0)
    return rules, congestion_fee

def update_station(station: dict[str, Any], payload: dict[str, Any]) -> None:
    page_props = payload.get("props", {}).get("pageProps", {})
    formatted = page_props.get("formattedData", {})
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

    status = (
        page_props.get("locationData", {})
        .get("key_data", {})
        .get("status", {})
        .get("name")
    )
    if status:
        station["status"] = status

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
        "afterCloseMode": "exit_allowed" if nearest_entrance else "must_stop",
        "afterCloseNote": nearest_entrance or (
            "Accessible 24 h/24." if twenty_four_seven else "Respecter les horaires d’accès du site."
        ),
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stations", default="data/tesla_stations.json")
    parser.add_argument("--delay", type=float, default=1.2)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--headed", action="store_true", help="Affiche le navigateur")
    args = parser.parse_args()

    path = Path(args.stations)
    stations = json.loads(path.read_text(encoding="utf-8"))
    tesla_stations = [s for s in stations if s.get("source") == "teslaSupercharger" and s.get("teslaUrl")]
    if args.limit > 0:
        tesla_stations = tesla_stations[:args.limit]

    success = 0
    failures: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            locale="fr-FR",
            timezone_id="Europe/Paris",
            viewport={"width": 1440, "height": 1000},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.7",
                "DNT": "1",
            },
        )
        page = context.new_page()

        for index, station in enumerate(tesla_stations, start=1):
            try:
                page.goto(station["teslaUrl"], wait_until="domcontentloaded", timeout=45000)
                page.wait_for_selector("#__NEXT_DATA__", timeout=20000)
                payload_text = page.locator("#__NEXT_DATA__").text_content()
                if not payload_text:
                    raise ValueError("__NEXT_DATA__ vide")
                payload = json.loads(payload_text)
                update_station(station, payload)
                success += 1
                print(f"[{index}/{len(tesla_stations)}] OK {station.get('name')}")
            except (PlaywrightTimeoutError, ValueError, json.JSONDecodeError) as exc:
                message = f"{station.get('name')}: {exc}"
                failures.append(message)
                print(f"[{index}/{len(tesla_stations)}] ERREUR {message}", file=sys.stderr)
            except Exception as exc:
                message = f"{station.get('name')}: {type(exc).__name__}: {exc}"
                failures.append(message)
                print(f"[{index}/{len(tesla_stations)}] ERREUR {message}", file=sys.stderr)
            time.sleep(max(0.0, args.delay))

        browser.close()

    if success > 0:
        path.write_text(json.dumps(stations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        metadata_path = path.parent / "metadata.json"
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            metadata = {}
        metadata["teslaUpdated"] = date.today().isoformat()
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary_path = path.parent / "tesla_update_summary.json"
    summary_path.write_text(
        json.dumps({
            "date": date.today().isoformat(),
            "attempted": len(tesla_stations),
            "success": success,
            "failed": len(failures),
            "failures": failures[:100],
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Mises à jour réussies : {success}/{len(tesla_stations)}")
    return 0 if success > 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())

import os
import json
import time
import requests
import pandas as pd

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "umkm-success-prediction/0.1 (student project; contact: your-email@example.com)",
    "Referer": "https://github.com/vikaarn94/umkm-success-prediction",
    "Accept": "application/json",
    "Content-Type": "text/plain; charset=utf-8",
}

def build_query():
    return """
    [out:json][timeout:60];
    area["name"="Surabaya"]["boundary"="administrative"]->.searchArea;
    (
      node["amenity"="restaurant"]["name"](area.searchArea);
      way["amenity"="restaurant"]["name"](area.searchArea);
      relation["amenity"="restaurant"]["name"](area.searchArea);

      node["amenity"="fast_food"]["name"](area.searchArea);
      way["amenity"="fast_food"]["name"](area.searchArea);
      relation["amenity"="fast_food"]["name"](area.searchArea);

      node["amenity"="cafe"]["name"](area.searchArea);
      way["amenity"="cafe"]["name"](area.searchArea);
      relation["amenity"="cafe"]["name"](area.searchArea);
    );
    out center tags;
    """

def fetch_surabaya_poi():
    query = build_query()

    response = requests.post(
        OVERPASS_URL,
        data=query.encode("utf-8"),
        headers=HEADERS,
        timeout=120
    )

    print("STATUS CODE:", response.status_code)
    print("CONTENT-TYPE:", response.headers.get("content-type"))
    print("RESPONSE SAMPLE:", response.text[:500])

    response.raise_for_status()
    return response.json()

def transform_overpass(data: dict) -> pd.DataFrame:
    rows = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})

        lat = el.get("lat")
        lon = el.get("lon")

        if lat is None and "center" in el:
            lat = el["center"].get("lat")
            lon = el["center"].get("lon")

        rows.append({
            "osm_id": el.get("id"),
            "osm_type": el.get("type"),
            "name_osm": tags.get("name"),
            "amenity": tags.get("amenity"),
            "cuisine": tags.get("cuisine"),
            "opening_hours": tags.get("opening_hours"),
            "phone": tags.get("phone"),
            "website": tags.get("website"),
            "delivery": tags.get("delivery"),
            "takeaway": tags.get("takeaway"),
            "lat": lat,
            "lon": lon
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    os.makedirs("data/external/overpass/raw_responses", exist_ok=True)
    os.makedirs("data/interim", exist_ok=True)

    raw_data = fetch_surabaya_poi()

    with open(
        "data/external/overpass/raw_responses/overpass_surabaya_raw.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    df = transform_overpass(raw_data)
    df.to_csv("data/interim/overpass_places_cleaned.csv", index=False)

    print(df.head())
    print("Jumlah baris:", len(df))
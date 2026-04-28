import pandas as pd

def clean_overpass_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # rapikan nama kolom
    df.columns = [c.strip().lower() for c in df.columns]

    # buang baris yang tidak punya nama tempat
    df = df[df["name_osm"].notna()].copy()

    # rapikan kolom teks
    text_cols = [
        "name_osm", "amenity", "cuisine",
        "opening_hours", "phone", "website",
        "delivery", "takeaway"
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # buang duplikasi sederhana
    df = df.drop_duplicates(subset=["name_osm", "lat", "lon"]).reset_index(drop=True)

    # buat fitur turunan sederhana
    df["has_opening_hours"] = (df["opening_hours"] != "").astype(int)
    df["has_phone"] = (df["phone"] != "").astype(int)
    df["has_website"] = (df["website"] != "").astype(int)
    df["has_delivery"] = df["delivery"].str.lower().eq("yes").astype(int)
    df["has_takeaway"] = df["takeaway"].str.lower().eq("yes").astype(int)

    # skor kelengkapan data sederhana
    df["data_completeness_score"] = (
        df["has_opening_hours"] +
        df["has_phone"] +
        df["has_website"] +
        df["has_delivery"] +
        df["has_takeaway"]
    )

    return df


if __name__ == "__main__":
    input_path = "data/interim/overpass_places_cleaned.csv"
    output_path = "data/interim/overpass_places_ready.csv"

    df = clean_overpass_data(input_path)
    df.to_csv(output_path, index=False)

    print(df.head())
    print("Jumlah baris setelah cleaning:", len(df))
    print("Kolom akhir:", df.columns.tolist())
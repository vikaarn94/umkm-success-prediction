import pandas as pd

def load_main_dataset(path: str = "data/raw/utama/usaha_kuliner_surabaya.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def load_bps_context(path: str = "data/interim/bps_jatim_context.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def prepare_main_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # tambahkan informasi wilayah tetap
    df["provinsi"] = "Jawa Timur"
    df["kota"] = "Surabaya"

    # rapikan beberapa kolom boolean / indikator jika ada
    indicator_cols = [
        "ada_nama", "ada_telepon", "ada_website", "ada_email",
        "ada_instagram", "ada_jam_buka", "ada_menu", "ada_wifi",
        "ada_parkir", "ada_ac", "ada_toilet", "halal", "vegetarian",
        "takeaway", "delivery", "drive_through", "outdoor_seating",
        "reservasi", "bayar_kartu_kredit", "bayar_qris", "bayar_tunai",
        "buka_24jam", "buka_hari_libur", "jam_buka_lengkap",
        "ada_media_sosial", "ada_digital_payment", "ada_layanan_modern",
        "ada_rating"
    ]

    for col in indicator_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # buang duplikasi sederhana berdasarkan osm_id jika ada
    if "osm_id" in df.columns:
        df = df.drop_duplicates(subset=["osm_id"]).reset_index(drop=True)

    return df

def merge_with_bps(main_df: pd.DataFrame, bps_df: pd.DataFrame) -> pd.DataFrame:
    # karena BPS Jatim hanya 1 baris dan semua data utama adalah Surabaya/Jatim,
    # kita lakukan cross join sederhana
    main_df["_merge_key"] = 1
    bps_df["_merge_key"] = 1

    merged = main_df.merge(bps_df, on="_merge_key", how="left")
    merged = merged.drop(columns=["_merge_key"])

    return merged

if __name__ == "__main__":
    main_df = load_main_dataset()
    bps_df = load_bps_context()

    main_df = prepare_main_dataset(main_df)
    master_df = merge_with_bps(main_df, bps_df)

    output_path = "data/processed/master_dataset.csv"
    master_df.to_csv(output_path, index=False)

    print(master_df.head())
    print("Jumlah baris master:", len(master_df))
    print("Jumlah kolom master:", len(master_df.columns))
    print("File tersimpan di:", output_path)
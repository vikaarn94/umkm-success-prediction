import pandas as pd

def load_bps_jatim(path: str = "data/raw/bps/data_bps.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    if "provinsi" in df.columns:
        df["provinsi"] = df["provinsi"].astype(str).str.strip()
        out = df[df["provinsi"].str.lower() == "jawa timur"].copy()
    elif "provinsi_name" in df.columns:
        df["provinsi_name"] = df["provinsi_name"].astype(str).str.strip()
        out = df[df["provinsi_name"].str.lower() == "jawa timur"].copy()
    else:
        raise ValueError("Kolom provinsi / provinsi_name tidak ditemukan.")

    return out

if __name__ == "__main__":
    df = load_bps_jatim()
    df.to_csv("data/interim/bps_jatim_context.csv", index=False)
    print(df.head())
    print("Jumlah baris BPS Jatim:", len(df))
    print("Kolom:", df.columns.tolist())
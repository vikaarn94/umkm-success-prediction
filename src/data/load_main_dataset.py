import pandas as pd

def load_main_dataset(path: str = "data/raw/utama/usaha_kuliner_surabaya.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

if __name__ == "__main__":
    df = load_main_dataset()
    print(df.head())
    print("Jumlah baris:", len(df))
    print("Kolom:", df.columns.tolist())
# load_db.py
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "food_wastage.db"
DATA_DIR = Path("D:\\local_food_wastage\\data\\Clean")
SCHEMA_FILE = Path("D:\\local_food_wastage\\sql\\schema.sql")

def apply_schema(conn):
    with open(SCHEMA_FILE, "r") as f:
        conn.executescript(f.read())
    print("Schema applied successfully")

def load_table(conn, csv_name, table_name):
    path = DATA_DIR / csv_name
    if not path.exists():
        print(f"Missing: {path}")
        return
    df = pd.read_csv(path)
    if "Expiry_Date" in df.columns:
        df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df.to_sql(table_name, conn, if_exists="append", index=False)
    print(f" Loaded {table_name} from {csv_name} ({len(df)} rows)")

def main():
    conn = sqlite3.connect(DB_PATH)
    apply_schema(conn)  # Apply schema from file
    load_table(conn, "providers_clean.csv", "Providers")
    load_table(conn, "receivers_clean.csv", "Receivers")
    load_table(conn, "food_listings_clean.csv", "Food_Listings")
    load_table(conn, "claims_clean.csv", "Claims")
    conn.close()
    print(f"🎉 Database created successfully at {DB_PATH}")

if __name__ == "__main__":
    main()

import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "krishinetra.db"))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(market_prices)")
cols = [c[1] for c in cursor.fetchall()]

needed = [
    ("commodity", "VARCHAR(100)"),
    ("variety", "VARCHAR(100)"),
    ("state", "VARCHAR(100) DEFAULT 'Gujarat'"),
    ("district", "VARCHAR(100) DEFAULT 'Rajkot'"),
    ("min_price", "FLOAT DEFAULT 0.0"),
    ("max_price", "FLOAT DEFAULT 0.0"),
    ("modal_price", "FLOAT DEFAULT 0.0"),
    ("arrival_quantity", "VARCHAR(100) DEFAULT ''")
]

for col_name, col_type in needed:
    if col_name not in cols:
        cursor.execute(f"ALTER TABLE market_prices ADD COLUMN {col_name} {col_type}")
        print(f"Added column {col_name}")

conn.commit()
conn.close()
print("Market prices migration completed successfully.")

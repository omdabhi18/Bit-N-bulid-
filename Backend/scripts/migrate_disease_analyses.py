import sqlite3
import os

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "krishinetra.db"))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(disease_analyses)")
cols = [c[1] for c in cursor.fetchall()]

needed = [
    ("storage_provider", "VARCHAR(50) DEFAULT 'cloudinary'"),
    ("public_id", "VARCHAR(255) DEFAULT ''"),
    ("image_metadata", "JSON DEFAULT '{}'")
]

for col_name, col_type in needed:
    if col_name not in cols:
        cursor.execute(f"ALTER TABLE disease_analyses ADD COLUMN {col_name} {col_type}")
        print(f"Added column {col_name}")

conn.commit()
conn.close()
print("Disease analyses migration completed successfully.")

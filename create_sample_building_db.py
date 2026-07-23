import sqlite3
from pathlib import Path

out = Path("db_test.sqlite3")
if out.exists():
    out.unlink()

conn = sqlite3.connect(out)
cur = conn.cursor()

cur.execute("""
CREATE TABLE energy_monthly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    kwh REAL NOT NULL
)
""")

cur.execute("""
CREATE TABLE energy_breakdown (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT,
    category TEXT NOT NULL,
    kwh REAL NOT NULL
)
""")

this_year = [12000, 11850, 12120, 11900, 12340, 12780, 13220, 13510, 12990, 12660, 12240, 11880]
last_year = [11200, 10980, 11150, 11020, 11540, 11980, 12440, 12690, 12130, 11850, 11490, 11110]

for i, v in enumerate(this_year, start=1):
    cur.execute(
        "INSERT INTO energy_monthly (building_name, year, month, kwh) VALUES (?, ?, ?, ?)",
        ("Sample Tower", 2026, i, v)
    )

for i, v in enumerate(last_year, start=1):
    cur.execute(
        "INSERT INTO energy_monthly (building_name, year, month, kwh) VALUES (?, ?, ?, ?)",
        ("Sample Tower", 2025, i, v)
    )

for cat, val in [("HVAC", 78000), ("Lighting", 28500), ("Other", 19600)]:
    cur.execute(
        "INSERT INTO energy_breakdown (building_name, category, kwh) VALUES (?, ?, ?)",
        ("Sample Tower", cat, val)
    )

conn.commit()
conn.close()

print(f"Created {out.resolve()}")
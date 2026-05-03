"""
Quick schema explorer for the Open Khipu Repository SQLite database.
Run this first to understand the data structure before building the MDP script.
"""
import sqlite3

DB_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\open-khipu-repository-master\data\khipu.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# List all tables
print("=" * 70)
print("KHIPU DATABASE SCHEMA EXPLORER")
print("=" * 70)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]
print(f"\nTables ({len(tables)}):")
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM [{t}]")
    count = cursor.fetchone()[0]
    print(f"  {t}: {count} rows")

# For key tables, show columns and sample data
key_tables = ["primary_cord", "cord", "cord_color", "knot", "cord_value",
              "khipu_main", "archive_dc", "cord_cluster",
              "urton_khipu_type", "cord_type_dc", "structure_dc",
              "fiber_dc", "termination_dc", "color_dc"]

for table in key_tables:
    if table not in tables:
        # Try without exact match
        matches = [t for t in tables if table.lower() in t.lower()]
        if matches:
            table = matches[0]
        else:
            continue

    print(f"\n{'='*70}")
    print(f"TABLE: {table}")
    print(f"{'='*70}")

    cursor.execute(f"PRAGMA table_info([{table}])")
    columns = cursor.fetchall()
    col_names = [c[1] for c in columns]
    print(f"  Columns: {', '.join(col_names)}")

    cursor.execute(f"SELECT * FROM [{table}] LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(f"  {row}")

# Specifically explore cord colors
print(f"\n{'='*70}")
print("CORD COLOR DISTRIBUTION")
print(f"{'='*70}")

# Find the right color column
for t in tables:
    cursor.execute(f"PRAGMA table_info([{t}])")
    cols = [c[1] for c in cursor.fetchall()]
    color_cols = [c for c in cols if 'color' in c.lower()]
    if color_cols:
        print(f"\n  Table '{t}' has color columns: {color_cols}")

# Try to get color distribution from cord table
try:
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name LIKE '%cord%'
    """)
    cord_tables = [r[0] for r in cursor.fetchall()]
    print(f"\n  Cord-related tables: {cord_tables}")

    for ct in cord_tables:
        cursor.execute(f"PRAGMA table_info([{ct}])")
        cols = cursor.fetchall()
        print(f"\n  {ct} columns:")
        for c in cols:
            print(f"    {c[1]} ({c[2]})")
except Exception as e:
    print(f"  Error: {e}")

# Try to find knot data
print(f"\n{'='*70}")
print("KNOT DATA SAMPLE")
print(f"{'='*70}")

for t in tables:
    if 'knot' in t.lower():
        cursor.execute(f"PRAGMA table_info([{t}])")
        cols = cursor.fetchall()
        print(f"\n  {t} columns:")
        for c in cols:
            print(f"    {c[1]} ({c[2]})")
        cursor.execute(f"SELECT * FROM [{t}] LIMIT 10")
        for row in cursor.fetchall():
            print(f"  {row}")

# Get khipu-level summary
print(f"\n{'='*70}")
print("KHIPU-LEVEL SUMMARY")
print(f"{'='*70}")

for t in tables:
    if 'khipu' in t.lower() and 'type' not in t.lower():
        cursor.execute(f"PRAGMA table_info([{t}])")
        cols = cursor.fetchall()
        col_names = [c[1] for c in cols]
        print(f"\n  {t}: {col_names}")
        cursor.execute(f"SELECT * FROM [{t}] LIMIT 3")
        for row in cursor.fetchall():
            print(f"  {row}")

# Provenance / archive distribution
print(f"\n{'='*70}")
print("PROVENANCE DISTRIBUTION")
print(f"{'='*70}")

for t in tables:
    if 'archive' in t.lower() or 'provenance' in t.lower():
        cursor.execute(f"SELECT * FROM [{t}] LIMIT 20")
        for row in cursor.fetchall():
            print(f"  {row}")

# Urton khipu type
print(f"\n{'='*70}")
print("KHIPU TYPE CATEGORIES")
print(f"{'='*70}")

for t in tables:
    if 'type' in t.lower() and 'khipu' in t.lower():
        cursor.execute(f"SELECT * FROM [{t}] LIMIT 20")
        for row in cursor.fetchall():
            print(f"  {row}")

# Color dictionary
print(f"\n{'='*70}")
print("COLOR DICTIONARY")
print(f"{'='*70}")

for t in tables:
    if 'color' in t.lower() and 'dc' in t.lower():
        cursor.execute(f"SELECT * FROM [{t}] LIMIT 30")
        for row in cursor.fetchall():
            print(f"  {row}")

conn.close()
print(f"\n{'='*70}")
print("SCHEMA EXPLORATION COMPLETE")
print(f"{'='*70}")

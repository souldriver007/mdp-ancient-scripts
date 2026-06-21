"""
=============================================================================
OKR DATABASE AUDIT — WHAT DATA HAVEN'T WE USED YET?
=============================================================================
Comprehensive scan of every table, column, and data pattern in the OKR.
Identifies unexploited variables for v3 analysis.
=============================================================================
"""

import sqlite3
from collections import Counter

DB_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\open-khipu-repository-master\data\khipu.db"
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

print("=" * 80)
print("OKR DATABASE AUDIT — FULL SCHEMA + UNEXPLOITED VARIABLES")
print("=" * 80)

# ═══════════════════════════════════════════════════════
# PART 1: EVERY TABLE, EVERY COLUMN, ROW COUNTS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 1: COMPLETE SCHEMA")
print("=" * 80)

cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM [{table}]")
    count = cur.fetchone()[0]
    
    cur.execute(f"PRAGMA table_info([{table}])")
    columns = cur.fetchall()
    
    print(f"\n  TABLE: {table} ({count} rows)")
    print(f"  " + "-" * 70)
    for col in columns:
        col_id, name, dtype, notnull, default, pk = col
        print(f"    {name:<30} {dtype:<15} {'PK' if pk else ''}")
    
    # Sample 3 rows
    col_names = [c[1] for c in columns]
    cur.execute(f"SELECT * FROM [{table}] LIMIT 3")
    rows = cur.fetchall()
    if rows:
        print(f"  Sample rows:")
        for row in rows:
            # Truncate long values
            parts = []
            for i, val in enumerate(row):
                s = str(val)[:40]
                parts.append(f"{col_names[i]}={s}")
            print(f"    {', '.join(parts)}")

# ═══════════════════════════════════════════════════════
# PART 2: CORD TABLE — EVERY COLUMN PROFILED
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 2: CORD TABLE — FULL COLUMN PROFILING")
print("=" * 80)

cur.execute("PRAGMA table_info(cord)")
cord_cols = [c[1] for c in cur.fetchall()]
print(f"\n  Cord columns: {cord_cols}")

for col in cord_cols:
    # Count non-null, distinct values
    cur.execute(f"SELECT COUNT(*) FROM cord WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    non_null = cur.fetchone()[0]
    
    cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM cord WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    distinct = cur.fetchone()[0]
    
    print(f"\n  {col}: {non_null} non-null ({non_null/54403*100:.0f}%), {distinct} distinct values")
    
    # Show value distribution for categorical columns
    if distinct > 0 and distinct <= 50:
        cur.execute(f"""
            SELECT [{col}], COUNT(*) as cnt 
            FROM cord 
            WHERE [{col}] IS NOT NULL AND [{col}] != ''
            GROUP BY [{col}] 
            ORDER BY cnt DESC 
            LIMIT 20
        """)
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]}")
    elif distinct > 50:
        # Numerical — show stats
        try:
            cur.execute(f"SELECT MIN([{col}]), AVG([{col}]), MAX([{col}]) FROM cord WHERE [{col}] IS NOT NULL AND [{col}] != '' AND [{col}] != 0")
            mn, avg, mx = cur.fetchone()
            if mn is not None:
                print(f"    Range: {mn} to {mx}, avg={avg:.2f}" if avg else f"    Range: {mn} to {mx}")
        except:
            pass

# ═══════════════════════════════════════════════════════
# PART 3: KNOT TABLE — EVERY COLUMN PROFILED
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 3: KNOT TABLE — FULL COLUMN PROFILING")
print("=" * 80)

cur.execute("PRAGMA table_info(knot)")
knot_cols = [c[1] for c in cur.fetchall()]
print(f"\n  Knot columns: {knot_cols}")

for col in knot_cols:
    cur.execute(f"SELECT COUNT(*) FROM knot WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    non_null = cur.fetchone()[0]
    
    cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM knot WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    distinct = cur.fetchone()[0]
    
    print(f"\n  {col}: {non_null} non-null ({non_null/110677*100:.0f}%), {distinct} distinct values")
    
    if distinct > 0 and distinct <= 50:
        cur.execute(f"""
            SELECT [{col}], COUNT(*) as cnt 
            FROM knot 
            WHERE [{col}] IS NOT NULL AND [{col}] != ''
            GROUP BY [{col}] 
            ORDER BY cnt DESC 
            LIMIT 20
        """)
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]}")
    elif distinct > 50:
        try:
            cur.execute(f"SELECT MIN([{col}]), AVG([{col}]), MAX([{col}]) FROM knot WHERE [{col}] IS NOT NULL AND [{col}] != '' AND [{col}] != 0")
            mn, avg, mx = cur.fetchone()
            if mn is not None:
                print(f"    Range: {mn} to {mx}, avg={avg:.2f}" if avg else f"    Range: {mn} to {mx}")
        except:
            pass

# ═══════════════════════════════════════════════════════
# PART 4: KHIPU_MAIN — EVERY COLUMN PROFILED
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 4: KHIPU_MAIN — FULL COLUMN PROFILING")
print("=" * 80)

cur.execute("PRAGMA table_info(khipu_main)")
km_cols = [c[1] for c in cur.fetchall()]
print(f"\n  Khipu_main columns: {km_cols}")

for col in km_cols:
    cur.execute(f"SELECT COUNT(*) FROM khipu_main WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    non_null = cur.fetchone()[0]
    
    cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM khipu_main WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    distinct = cur.fetchone()[0]
    
    print(f"\n  {col}: {non_null} non-null ({non_null/619*100:.0f}%), {distinct} distinct values")
    
    if distinct > 0 and distinct <= 50:
        cur.execute(f"""
            SELECT [{col}], COUNT(*) as cnt 
            FROM khipu_main 
            WHERE [{col}] IS NOT NULL AND [{col}] != ''
            GROUP BY [{col}] 
            ORDER BY cnt DESC 
            LIMIT 20
        """)
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]}")
    elif distinct > 50:
        try:
            cur.execute(f"SELECT MIN([{col}]), AVG([{col}]), MAX([{col}]) FROM khipu_main WHERE [{col}] IS NOT NULL AND [{col}] != '' AND [{col}] != 0")
            mn, avg, mx = cur.fetchone()
            if mn is not None:
                print(f"    Range: {mn} to {mx}, avg={avg:.2f}" if avg else f"    Range: {mn} to {mx}")
        except:
            pass

# ═══════════════════════════════════════════════════════
# PART 5: COLOUR TABLES — FULL PROFILE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 5: COLOUR TABLES")
print("=" * 80)

for t in tables:
    if 'color' in t.lower() or 'colour' in t.lower():
        cur.execute(f"PRAGMA table_info([{t}])")
        cols = [c[1] for c in cur.fetchall()]
        cur.execute(f"SELECT COUNT(*) FROM [{t}]")
        n = cur.fetchone()[0]
        print(f"\n  TABLE: {t} ({n} rows)")
        print(f"  Columns: {cols}")
        
        for col in cols:
            cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM [{t}] WHERE [{col}] IS NOT NULL AND [{col}] != ''")
            distinct = cur.fetchone()[0]
            print(f"    {col}: {distinct} distinct values")

# ═══════════════════════════════════════════════════════
# PART 6: CORD_CLUSTER TABLE — FULL PROFILE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 6: CORD_CLUSTER TABLE")
print("=" * 80)

cur.execute("PRAGMA table_info(cord_cluster)")
cc_cols = [c[1] for c in cur.fetchall()]
print(f"\n  Columns: {cc_cols}")

for col in cc_cols:
    cur.execute(f"SELECT COUNT(*) FROM cord_cluster WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    non_null = cur.fetchone()[0]
    
    cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM cord_cluster WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    distinct = cur.fetchone()[0]
    
    print(f"\n  {col}: {non_null} non-null, {distinct} distinct")
    
    if distinct > 0 and distinct <= 30:
        cur.execute(f"""
            SELECT [{col}], COUNT(*) as cnt 
            FROM cord_cluster 
            WHERE [{col}] IS NOT NULL AND [{col}] != ''
            GROUP BY [{col}] 
            ORDER BY cnt DESC
        """)
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]}")
    elif distinct > 30:
        try:
            cur.execute(f"SELECT MIN([{col}]), AVG([{col}]), MAX([{col}]) FROM cord_cluster WHERE [{col}] IS NOT NULL AND [{col}] != '' AND [{col}] != 0")
            mn, avg, mx = cur.fetchone()
            if mn is not None:
                print(f"    Range: {mn} to {mx}, avg={avg:.2f}" if avg else f"    Range: {mn} to {mx}")
        except:
            pass

# ═══════════════════════════════════════════════════════
# PART 7: PRIMARY_CORD TABLE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 7: PRIMARY_CORD TABLE")
print("=" * 80)

cur.execute("PRAGMA table_info(primary_cord)")
pc_cols = [c[1] for c in cur.fetchall()]
print(f"\n  Columns: {pc_cols}")

for col in pc_cols:
    cur.execute(f"SELECT COUNT(*) FROM primary_cord WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    non_null = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(DISTINCT [{col}]) FROM primary_cord WHERE [{col}] IS NOT NULL AND [{col}] != ''")
    distinct = cur.fetchone()[0]
    print(f"  {col}: {non_null} non-null, {distinct} distinct")
    
    if distinct <= 30 and distinct > 0:
        cur.execute(f"SELECT [{col}], COUNT(*) as cnt FROM primary_cord WHERE [{col}] IS NOT NULL AND [{col}] != '' GROUP BY [{col}] ORDER BY cnt DESC")
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]}")
    elif distinct > 30:
        try:
            cur.execute(f"SELECT MIN([{col}]), AVG([{col}]), MAX([{col}]) FROM primary_cord WHERE [{col}] IS NOT NULL AND [{col}] != '' AND [{col}] != 0")
            mn, avg, mx = cur.fetchone()
            if mn is not None:
                print(f"    Range: {mn} to {mx}, avg={avg:.2f}" if avg else f"    Range: {mn} to {mx}")
        except:
            pass

# ═══════════════════════════════════════════════════════
# PART 8: ANY TABLES WE HAVEN'T LOOKED AT?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 8: DICTIONARY/REFERENCE TABLES")
print("=" * 80)

for t in tables:
    if '_dc' in t.lower() or 'type' in t.lower() or 'structure' in t.lower():
        cur.execute(f"PRAGMA table_info([{t}])")
        cols = [c[1] for c in cur.fetchall()]
        cur.execute(f"SELECT COUNT(*) FROM [{t}]")
        n = cur.fetchone()[0]
        print(f"\n  TABLE: {t} ({n} rows, cols: {cols})")
        cur.execute(f"SELECT * FROM [{t}]")
        for row in cur.fetchall():
            print(f"    {row}")

# ═══════════════════════════════════════════════════════
# PART 9: CORD_VALUE TABLE — PRE-COMPUTED VALUES?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 9: CORD_VALUE TABLE (if exists)")
print("=" * 80)

if 'cord_value' in tables:
    cur.execute("PRAGMA table_info(cord_value)")
    cols = [c[1] for c in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM cord_value")
    n = cur.fetchone()[0]
    print(f"\n  Columns: {cols}")
    print(f"  Rows: {n}")
    cur.execute("SELECT * FROM cord_value LIMIT 10")
    for row in cur.fetchall():
        print(f"    {row}")
else:
    print(f"\n  cord_value table does not exist")

# ═══════════════════════════════════════════════════════
# PART 10: VARIABLES USED vs UNUSED SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("PART 10: USED vs UNUSED VARIABLE SUMMARY")
print("=" * 80)

used_cord = ["KHIPU_ID", "CORD_ID", "CORD_ORDINAL", "TWIST", "FIBER",
             "CORD_LENGTH", "ATTACHMENT_TYPE", "PENDANT_FROM", "CLUSTER_ID"]
used_knot = ["CORD_ID", "TYPE_CODE", "knot_value_type", "NUM_TURNS", "DIRECTION"]
used_color = ["CORD_ID", "FULL_COLOR", "COLOR_CD_1", "PCORD_FLAG"]
used_khipu = ["KHIPU_ID", "PROVENANCE", "REGION"]

print(f"\n  CORD table — used columns: {used_cord}")
unused_cord = [c for c in cord_cols if c not in used_cord]
print(f"  CORD table — UNUSED columns: {unused_cord}")

print(f"\n  KNOT table — used columns: {used_knot}")
unused_knot = [c for c in knot_cols if c not in used_knot]
print(f"  KNOT table — UNUSED columns: {unused_knot}")

print(f"\n  KHIPU_MAIN — used columns: {used_khipu}")
unused_km = [c for c in km_cols if c not in used_khipu]
print(f"  KHIPU_MAIN — UNUSED columns: {unused_km}")

conn.close()
print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)

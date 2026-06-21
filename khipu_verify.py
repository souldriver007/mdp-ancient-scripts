"""
=============================================================================
MDP V2 VERIFICATION — CROSS-CHECK ALL KEY FINDINGS
=============================================================================
Author: Adrian Sharman, SoulDriver Research
Date: June 2026

Verifies v2 findings against raw SQL queries and adds controls.
If there's a bug in the algorithm, this will catch it.
=============================================================================
"""

import sqlite3
import random
import math
from collections import Counter, defaultdict

DB_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\open-khipu-repository-master\data\khipu.db"
conn = sqlite3.connect(DB_FILE)

print("=" * 80)
print("MDP V2 VERIFICATION SUITE")
print("=" * 80)

# ═══════════════════════════════════════════════════════
# CHECK 1: HUAYCÁN — DOES IT EXIST IN THE DATABASE?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 1: HUAYCÁN PROVENANCE SEARCH")
print("  Dumping ALL unique provenance values to find any Huaycán variant")
print("=" * 80)

cur = conn.cursor()
cur.execute("SELECT DISTINCT PROVENANCE FROM khipu_main ORDER BY PROVENANCE")
all_provs = [row[0] for row in cur.fetchall()]

print(f"\n  Total unique provenance values: {len(all_provs)}")

# Search for anything resembling Huaycán or Cieneguilla
huaycan_matches = [p for p in all_provs if p and 
                   any(term in p.lower() for term in 
                       ["huayc", "cieneg", "huayk", "wayc", "wayk"])]

print(f"\n  Matches for 'huayc/cieneg/wayc': {len(huaycan_matches)}")
if huaycan_matches:
    for m in huaycan_matches:
        cur.execute("SELECT COUNT(*) FROM khipu_main WHERE PROVENANCE = ?", (m,))
        n = cur.fetchone()[0]
        print(f"    '{m}': {n} khipus")
else:
    print(f"    >>> NO MATCH FOUND — Huaycán is NOT in the OKR database <<<")

# Also check REGION field
cur.execute("SELECT DISTINCT REGION FROM khipu_main ORDER BY REGION")
all_regions = [row[0] for row in cur.fetchall()]
region_matches = [r for r in all_regions if r and 
                  any(term in r.lower() for term in ["huayc", "cieneg"])]
print(f"\n  Region field matches: {len(region_matches)}")
if region_matches:
    for m in region_matches:
        print(f"    '{m}'")

# Dump ALL provenance values for reference
print(f"\n  FULL PROVENANCE LIST ({len(all_provs)} entries):")
for p in all_provs:
    if p and p.strip():
        cur.execute("SELECT COUNT(*) FROM khipu_main WHERE PROVENANCE = ?", (p,))
        n = cur.fetchone()[0]
        print(f"    [{n:>3}] {p}")


# ═══════════════════════════════════════════════════════
# CHECK 2: FIBER × COLOUR — RAW SQL VERIFICATION
# Is cotton AB really mean=294 vs camelid AB mean=7?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 2: FIBER × COLOUR — RAW SQL VERIFICATION")
print("  Testing: Cotton AB mean=294 vs Camelid AB mean=7")
print("=" * 80)

# Direct SQL: compute cord values for AB cords on cotton vs camelid
# First get cord IDs for AB cotton and AB camelid
for fiber_code, fiber_name in [("CN", "Cotton"), ("CL", "Camelid")]:
    cur.execute("""
        SELECT c.CORD_ID, c.FIBER
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        WHERE acc.COLOR_CD_1 = 'AB' AND c.FIBER = ?
    """, (fiber_code,))
    cord_ids = [row[0] for row in cur.fetchall()]
    
    # Now compute values for these cords from knots
    values = []
    for cid in cord_ids:
        cur.execute("""
            SELECT TYPE_CODE, knot_value_type, NUM_TURNS 
            FROM knot WHERE CORD_ID = ?
        """, (cid,))
        total = 0
        for kr in cur.fetchall():
            kt, pv, nt = kr
            if kt == 'L': total += int(nt or 0)
            elif kt == 'E': total += 1
            elif kt == 'S': total += (pv or 0)
        if total > 0:
            values.append(total)
    
    if values:
        values.sort()
        med = values[len(values)//2]
        mean = sum(values)/len(values)
        print(f"\n  AB on {fiber_name} ({fiber_code}):")
        print(f"    Cords with colour: {len(cord_ids)}")
        print(f"    Cords with values: {len(values)}")
        print(f"    Median: {med}")
        print(f"    Mean: {mean:.1f}")
        print(f"    Max: {max(values)}")
        print(f"    Sample values (first 20): {values[:20]}")
    else:
        print(f"\n  AB on {fiber_name}: no values found")


# ═══════════════════════════════════════════════════════
# CHECK 3: LK KNOT TYPE — RAW SQL VERIFICATION
# Is LK really 79.5% L-type?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 3: LK KNOT TYPE INVERSION — RAW SQL")
print("=" * 80)

cur.execute("""
    SELECT k.TYPE_CODE, COUNT(*) as cnt
    FROM knot k
    JOIN cord c ON k.CORD_ID = c.CORD_ID
    JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
    WHERE acc.COLOR_CD_1 = 'LK'
    GROUP BY k.TYPE_CODE
    ORDER BY cnt DESC
""")
print(f"\n  LK knot types (raw SQL):")
lk_total_sql = 0
lk_knots_sql = {}
for row in cur.fetchall():
    print(f"    {row[0]}: {row[1]}")
    lk_knots_sql[row[0]] = row[1]
    lk_total_sql += row[1]

if lk_total_sql > 0:
    l_pct = lk_knots_sql.get('L', 0) / lk_total_sql * 100
    s_pct = lk_knots_sql.get('S', 0) / lk_total_sql * 100
    print(f"    L-type: {l_pct:.1f}%, S-type: {s_pct:.1f}%")
    print(f"    v2 reported: L=79.5%, S=16.3%")
    print(f"    >>> {'VERIFIED ✓' if abs(l_pct - 79.5) < 2 else 'MISMATCH ✗'}")

# Same for non-LK
cur.execute("""
    SELECT k.TYPE_CODE, COUNT(*) as cnt
    FROM knot k
    JOIN cord c ON k.CORD_ID = c.CORD_ID
    JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
    WHERE acc.COLOR_CD_1 != 'LK' AND acc.COLOR_CD_1 IS NOT NULL AND acc.COLOR_CD_1 != ''
    GROUP BY k.TYPE_CODE
    ORDER BY cnt DESC
""")
print(f"\n  Non-LK knot types (raw SQL):")
other_total_sql = 0
other_knots_sql = {}
for row in cur.fetchall():
    print(f"    {row[0]}: {row[1]}")
    other_knots_sql[row[0]] = row[1]
    other_total_sql += row[1]
if other_total_sql > 0:
    l_pct = other_knots_sql.get('L', 0) / other_total_sql * 100
    s_pct = other_knots_sql.get('S', 0) / other_total_sql * 100
    print(f"    L-type: {l_pct:.1f}%, S-type: {s_pct:.1f}%")


# ═══════════════════════════════════════════════════════
# CHECK 4: SUBSIDIARY DEPTH — VERIFY CALCULATION
# Spot-check a specific khipu's hierarchy
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 4: SUBSIDIARY DEPTH — SPOT CHECK")
print("=" * 80)

# Find a khipu with known subsidiaries
cur.execute("""
    SELECT c.KHIPU_ID, COUNT(*) as sub_count
    FROM cord c
    WHERE c.PENDANT_FROM IS NOT NULL 
      AND c.PENDANT_FROM NOT IN (SELECT PCORD_ID FROM primary_cord)
    GROUP BY c.KHIPU_ID
    ORDER BY sub_count DESC
    LIMIT 5
""")
top_sub = cur.fetchall()
print(f"\n  Top 5 khipus by subsidiary count:")
for row in top_sub:
    print(f"    Khipu {row[0]}: {row[1]} subsidiaries")

if top_sub:
    test_khipu = top_sub[0][0]
    print(f"\n  Tracing hierarchy for khipu {test_khipu}:")
    
    # Get primary cord
    cur.execute("SELECT PCORD_ID FROM primary_cord WHERE KHIPU_ID = ?", (test_khipu,))
    pc = cur.fetchone()
    pcord_id = pc[0] if pc else None
    print(f"    Primary cord: {pcord_id}")
    
    # Get all cords
    cur.execute("""
        SELECT CORD_ID, PENDANT_FROM, CORD_ORDINAL 
        FROM cord WHERE KHIPU_ID = ? 
        ORDER BY CORD_ORDINAL
    """, (test_khipu,))
    all_cords = cur.fetchall()
    
    # Trace depths manually
    depth_map = {}
    for cid, pf, ordinal in all_cords:
        if pf == pcord_id:
            depth_map[cid] = 0
        elif pf in depth_map:
            depth_map[cid] = depth_map[pf] + 1
        else:
            # Check if pendant_from is another cord
            if pf and pf != pcord_id:
                # It's subsidiary, but parent might not be processed yet
                # Simple BFS
                pass
    
    # BFS approach
    depth_map = {}
    queue = []
    for cid, pf, ordinal in all_cords:
        if pf == pcord_id:
            depth_map[cid] = 0
            queue.append(cid)
    
    while queue:
        parent = queue.pop(0)
        for cid, pf, ordinal in all_cords:
            if pf == parent and cid not in depth_map:
                depth_map[cid] = depth_map[parent] + 1
                queue.append(cid)
    
    depth_dist = Counter(depth_map.values())
    print(f"    Depth distribution (manual BFS):")
    for d in sorted(depth_dist.keys()):
        print(f"      Depth {d}: {depth_dist[d]} cords")
    print(f"    Total cords in hierarchy: {len(depth_map)}")
    print(f"    Total cords in khipu: {len(all_cords)}")


# ═══════════════════════════════════════════════════════
# CHECK 5: BARBERPOLE DOMAIN SHIFT — RAW SQL
# Is solid W really mean=403 vs barberpole W mean=148?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 5: BARBERPOLE DOMAIN SHIFT — RAW SQL")
print("=" * 80)

for label, where_clause in [
    ("Solid W (FULL_COLOR = 'W')", "acc.FULL_COLOR = 'W'"),
    ("Barberpole W:* or *:W", "(acc.FULL_COLOR LIKE 'W:%' OR acc.FULL_COLOR LIKE '%:W')")
]:
    cur.execute(f"""
        SELECT c.CORD_ID
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        WHERE {where_clause}
    """)
    cord_ids = [row[0] for row in cur.fetchall()]
    
    values = []
    for cid in cord_ids:
        cur.execute("SELECT TYPE_CODE, knot_value_type, NUM_TURNS FROM knot WHERE CORD_ID = ?", (cid,))
        total = 0
        for kr in cur.fetchall():
            kt, pv, nt = kr
            if kt == 'L': total += int(nt or 0)
            elif kt == 'E': total += 1
            elif kt == 'S': total += (pv or 0)
        if total > 0:
            values.append(total)
    
    if values:
        values.sort()
        print(f"\n  {label}:")
        print(f"    Cords: {len(cord_ids)}, with values: {len(values)}")
        print(f"    Median: {values[len(values)//2]}, Mean: {sum(values)/len(values):.0f}")


# ═══════════════════════════════════════════════════════
# CHECK 6: ZIPF CONTROL — RANDOM COUNTING SEQUENCES
# Does ANY set of small integers produce a Zipfian slope?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 6: ZIPF'S LAW CONTROL — RANDOM COUNTING SEQUENCES")
print("  Testing whether the 0.77 slope is genuine or arithmetic artifact")
print("=" * 80)

random.seed(42)

# Generate random "khipu-like" counting sequences
# Use the same value distribution as the real corpus
real_values = []
cur.execute("""
    SELECT k.TYPE_CODE, k.knot_value_type, k.NUM_TURNS, c.CORD_ID
    FROM knot k
    JOIN cord c ON k.CORD_ID = c.CORD_ID
""")
cord_vals_sql = defaultdict(int)
for row in cur.fetchall():
    kt, pv, nt, cid = row
    if kt == 'L': cord_vals_sql[cid] += int(nt or 0)
    elif kt == 'E': cord_vals_sql[cid] += 1
    elif kt == 'S': cord_vals_sql[cid] += (pv or 0)

real_nonzero = [v for v in cord_vals_sql.values() if v > 0]
print(f"\n  Real corpus: {len(real_nonzero)} cords with values")
print(f"  Value distribution: min={min(real_nonzero)}, median={sorted(real_nonzero)[len(real_nonzero)//2]}, "
      f"mean={sum(real_nonzero)/len(real_nonzero):.0f}, max={max(real_nonzero)}")

# Control 1: Random sequences drawn from the SAME value distribution
control_bigrams_1 = Counter()
for _ in range(3560):  # Same number of non-summing clusters
    seq_len = random.randint(3, 8)  # Typical cluster size
    seq = random.choices(real_nonzero, k=seq_len)
    for i in range(len(seq) - 1):
        control_bigrams_1[(seq[i], seq[i+1])] += 1

ctrl1_freqs = sorted(control_bigrams_1.values(), reverse=True)
if len(ctrl1_freqs) >= 10 and ctrl1_freqs[0] > 0 and ctrl1_freqs[9] > 0:
    slope1 = -(math.log(ctrl1_freqs[9]) - math.log(ctrl1_freqs[0])) / (math.log(10) - math.log(1))
    print(f"\n  CONTROL 1 (random draw from real value distribution):")
    print(f"    Unique bigrams: {len(control_bigrams_1)}")
    print(f"    Top 5: {ctrl1_freqs[:5]}")
    print(f"    Zipf slope: {slope1:.2f}")

# Control 2: Uniform random small integers (1-100)
control_bigrams_2 = Counter()
for _ in range(3560):
    seq_len = random.randint(3, 8)
    seq = [random.randint(1, 100) for _ in range(seq_len)]
    for i in range(len(seq) - 1):
        control_bigrams_2[(seq[i], seq[i+1])] += 1

ctrl2_freqs = sorted(control_bigrams_2.values(), reverse=True)
if len(ctrl2_freqs) >= 10 and ctrl2_freqs[0] > 0 and ctrl2_freqs[9] > 0:
    slope2 = -(math.log(ctrl2_freqs[9]) - math.log(ctrl2_freqs[0])) / (math.log(10) - math.log(1))
    print(f"\n  CONTROL 2 (uniform random 1-100):")
    print(f"    Unique bigrams: {len(control_bigrams_2)}")
    print(f"    Top 5: {ctrl2_freqs[:5]}")
    print(f"    Zipf slope: {slope2:.2f}")

# Control 3: Random draw from ONLY the small values (1-20, matching khipu bias)
control_bigrams_3 = Counter()
small_vals = [v for v in real_nonzero if v <= 20]
for _ in range(3560):
    seq_len = random.randint(3, 8)
    seq = random.choices(small_vals, k=seq_len)
    for i in range(len(seq) - 1):
        control_bigrams_3[(seq[i], seq[i+1])] += 1

ctrl3_freqs = sorted(control_bigrams_3.values(), reverse=True)
if len(ctrl3_freqs) >= 10 and ctrl3_freqs[0] > 0 and ctrl3_freqs[9] > 0:
    slope3 = -(math.log(ctrl3_freqs[9]) - math.log(ctrl3_freqs[0])) / (math.log(10) - math.log(1))
    print(f"\n  CONTROL 3 (random from small values 1-20 only):")
    print(f"    Unique bigrams: {len(control_bigrams_3)}")
    print(f"    Top 5: {ctrl3_freqs[:5]}")
    print(f"    Zipf slope: {slope3:.2f}")

# REAL corpus slope for comparison
print(f"\n  REAL KHIPU CORPUS:")
print(f"    Zipf slope: 0.77 (from v2 analysis)")

print(f"\n  INTERPRETATION:")
print(f"    If controls produce similar slopes → Zipf finding is arithmetic artifact")
print(f"    If real corpus slope is HIGHER than controls → genuine structural signal")


# ═══════════════════════════════════════════════════════
# CHECK 7: CORD LENGTH — VERIFY UNITS
# Are lengths in cm? What does the raw data look like?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 7: CORD LENGTH — RAW DATA SAMPLE")
print("=" * 80)

cur.execute("""
    SELECT CORD_ID, CORD_LENGTH, KHIPU_ID 
    FROM cord 
    WHERE CORD_LENGTH > 0 AND CORD_LENGTH IS NOT NULL
    ORDER BY CORD_LENGTH DESC
    LIMIT 20
""")
print(f"\n  Top 20 longest cords (raw values — what units?):")
for row in cur.fetchall():
    print(f"    Cord {row[0]}: length={row[1]}, khipu={row[2]}")

cur.execute("""
    SELECT MIN(CORD_LENGTH), AVG(CORD_LENGTH), MAX(CORD_LENGTH), COUNT(*)
    FROM cord 
    WHERE CORD_LENGTH > 0
""")
row = cur.fetchone()
print(f"\n  Length stats: min={row[0]}, avg={row[1]:.1f}, max={row[2]}, n={row[3]}")


# ═══════════════════════════════════════════════════════
# CHECK 8: DEPTH 0 vs SUBSIDIARY — VERIFY PENDANT_FROM LOGIC
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("CHECK 8: PENDANT_FROM LOGIC VERIFICATION")
print("=" * 80)

# How many cords have PENDANT_FROM = a primary cord ID?
cur.execute("SELECT COUNT(*) FROM cord WHERE PENDANT_FROM IN (SELECT PCORD_ID FROM primary_cord)")
n_from_primary = cur.fetchone()[0]

# How many cords have PENDANT_FROM = another cord ID (subsidiary)?
cur.execute("""
    SELECT COUNT(*) FROM cord 
    WHERE PENDANT_FROM IS NOT NULL 
      AND PENDANT_FROM NOT IN (SELECT PCORD_ID FROM primary_cord)
""")
n_from_cord = cur.fetchone()[0]

# How many cords have NULL PENDANT_FROM?
cur.execute("SELECT COUNT(*) FROM cord WHERE PENDANT_FROM IS NULL")
n_null = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM cord")
n_total = cur.fetchone()[0]

print(f"\n  PENDANT_FROM breakdown:")
print(f"    From primary cord (depth 0): {n_from_primary}")
print(f"    From another cord (subsidiary): {n_from_cord}")
print(f"    NULL (primary cords themselves?): {n_null}")
print(f"    Total: {n_total}")
print(f"    v2 reported: pendant={39006 + n_subsidiary - n_subsidiary}, subsidiary={15397 if True else 0}")
print(f"    >>> {'VERIFIED ✓' if abs(n_from_cord - 15397) < 100 else 'CHECK — numbers differ'}")


# ═══════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
print(f"""
  CHECK 1: Huaycán provenance — does it exist in OKR?
  CHECK 2: Fiber × colour (Cotton AB vs Camelid AB) — raw SQL
  CHECK 3: LK knot inversion (79.5% L-type) — raw SQL
  CHECK 4: Subsidiary depth — manual BFS spot-check
  CHECK 5: Barberpole domain shift (W solid vs W barberpole) — raw SQL
  CHECK 6: Zipf control — 3 randomised baselines
  CHECK 7: Cord length units — raw data inspection
  CHECK 8: Pendant_from logic — count verification
""")

conn.close()

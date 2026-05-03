"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) — INCA KHIPU APPLICATION
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026
Methodology: Cord-Colour Domain Profiling

DESCRIPTION:
This script applies MDP to the Inca Khipu corpus — the first application of
MDP to a non-written, non-clay medium. Khipus are knotted cord devices used
by the Inca Empire (~1400-1532 CE) for administrative record-keeping.

The MDP mapping:
  - Each KHIPU = one administrative document (like a tablet)
  - Each PENDANT CORD = one line entry
  - CORD COLOUR = the "commodity sign" (what is being counted)
  - KNOT VALUE = the numeral (base-10 decimal system)
  - KNOT TYPE = measurement system indicator (S=single, L=long, E=figure-8)
  - PLY DIRECTION = potential domain marker (S-twist vs Z-twist)
  - PROVENANCE = findspot (administrative archive)

If MDP successfully clusters cord colours into distinct numerical domains,
it proves that the same mathematical law of administrative organisation
operates across clay tablets AND knotted cords, across four continents,
and across 4,700 years of human history.

DATA SOURCES:
- Open Khipu Repository (khipu.db SQLite database)
  DOI: 10.5281/zenodo.18025748
  619 khipus, 54,403 cords, 110,677 knots

LICENSE: MIT License
=============================================================================
"""

import sqlite3
import os
from collections import Counter, defaultdict

# ═══════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════
DB_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\open-khipu-repository-master\data\khipu.db"

# ═══════════════════════════════════════════════════════
# CONNECT AND LOAD
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("METROLOGICAL DOMAIN PROFILING — INCA KHIPU")
print("Four continents. Clay, stone, string. 3200 BCE to 1532 CE. One method.")
print("=" * 75)

conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ═══════════════════════════════════════════════════════
# STEP 1: CORPUS OVERVIEW
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 1: CORPUS OVERVIEW")
print("=" * 75)

cursor.execute("SELECT COUNT(*) FROM khipu_main")
n_khipus = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM cord")
n_cords = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM knot")
n_knots = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ascher_cord_color")
n_colors = cursor.fetchone()[0]

print(f"\n  Khipus: {n_khipus}")
print(f"  Cords: {n_cords}")
print(f"  Knots: {n_knots}")
print(f"  Colour records: {n_colors}")

# Provenance distribution
cursor.execute("""
    SELECT PROVENANCE, COUNT(*) as cnt 
    FROM khipu_main 
    WHERE PROVENANCE != '' 
    GROUP BY PROVENANCE 
    ORDER BY cnt DESC
    LIMIT 20
""")
print(f"\n  Provenance distribution:")
for row in cursor.fetchall():
    print(f"    {row['PROVENANCE']}: {row['cnt']}")

# Region distribution
cursor.execute("""
    SELECT REGION, COUNT(*) as cnt 
    FROM khipu_main 
    WHERE REGION != '' 
    GROUP BY REGION 
    ORDER BY cnt DESC
""")
print(f"\n  Region distribution:")
for row in cursor.fetchall():
    print(f"    {row['REGION']}: {row['cnt']}")

# Fiber distribution
cursor.execute("""
    SELECT FIBER, COUNT(*) as cnt 
    FROM cord 
    WHERE FIBER != '' 
    GROUP BY FIBER 
    ORDER BY cnt DESC
""")
print(f"\n  Fiber distribution:")
fiber_dc = {"CN": "cotton", "A": "alpaca", "L": "llama", "W": "sheep wool",
            "V": "vegetal", "CL": "camelid"}
for row in cursor.fetchall():
    desc = fiber_dc.get(row['FIBER'], row['FIBER'])
    print(f"    {row['FIBER']} ({desc}): {row['cnt']}")

# ═══════════════════════════════════════════════════════
# STEP 2: CORD COLOUR DISTRIBUTION
# The "commodity signs" of the khipu
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 2: CORD COLOUR DISTRIBUTION (The 'Commodity Signs')")
print("=" * 75)

# Load colour dictionary
color_dict = {}
cursor.execute("SELECT AS_COLOR_CD, COLOR_DESCR, COLOR, INTENSITY FROM ascher_color_dc")
for row in cursor.fetchall():
    color_dict[row['AS_COLOR_CD']] = {
        "desc": row['COLOR_DESCR'],
        "hue": row['COLOR'],
        "intensity": row['INTENSITY']
    }

# Get FULL_COLOR distribution (primary colour of each cord)
cursor.execute("""
    SELECT FULL_COLOR, COUNT(*) as cnt 
    FROM ascher_cord_color 
    WHERE PCORD_FLAG = 0 AND FULL_COLOR != ''
    GROUP BY FULL_COLOR 
    ORDER BY cnt DESC
    LIMIT 40
""")

print(f"\n  Top 40 cord colours (pendant cords only):")
print(f"  {'Code':<12} {'Count':>6} {'Description':<35} {'Hue'}")
print(f"  " + "-" * 65)

color_counts = {}
for row in cursor.fetchall():
    code = row['FULL_COLOR']
    count = row['cnt']
    color_counts[code] = count
    info = color_dict.get(code, {"desc": "compound/special", "hue": "?"})
    # Handle compound colours (e.g., "AB:W" = light brown barberpole white)
    if len(code) <= 3 and code in color_dict:
        desc = info['desc']
        hue = info['hue']
    else:
        desc = f"compound ({code})"
        hue = "multi"
    print(f"  {code:<12} {count:>6} {desc:<35} {hue}")

# ═══════════════════════════════════════════════════════
# STEP 3: COMPUTE CORD VALUES FROM KNOTS
# Each cord's total numerical value from its knots
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 3: COMPUTING CORD VALUES FROM KNOTS")
print("=" * 75)

# For each cord, sum up its knot values
# knot_value_type encodes the place value: 1=units, 10=tens, 100=hundreds...
# TYPE_CODE: S=single (tens+), L=long (units), E=figure-eight (1)
# For L knots: value = NUM_TURNS
# For S knots: value = 1 × place value
# For E knots: value = 1

cursor.execute("""
    SELECT c.KHIPU_ID, c.CORD_ID, c.CORD_ORDINAL, c.TWIST, c.FIBER,
           c.CORD_LENGTH, c.ATTACHMENT_TYPE,
           acc.FULL_COLOR, acc.COLOR_CD_1,
           k.TYPE_CODE, k.knot_value_type, k.NUM_TURNS, k.DIRECTION
    FROM cord c
    LEFT JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
    LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
    WHERE c.PENDANT_FROM IN (SELECT PCORD_ID FROM primary_cord)
    ORDER BY c.KHIPU_ID, c.CORD_ORDINAL
""")

# Build cord-level records
cord_data = defaultdict(lambda: {
    "khipu_id": None, "color": None, "color1": None,
    "twist": None, "fiber": None, "ordinal": 0,
    "length": 0, "attachment": None,
    "knots": [], "total_value": 0,
    "knot_types": Counter(), "knot_directions": Counter()
})

for row in cursor.fetchall():
    cid = row['CORD_ID']
    cd = cord_data[cid]
    cd["khipu_id"] = row['KHIPU_ID']
    cd["color"] = row['FULL_COLOR'] or ""
    cd["color1"] = row['COLOR_CD_1'] or ""
    cd["twist"] = row['TWIST'] or ""
    cd["fiber"] = row['FIBER'] or ""
    cd["ordinal"] = row['CORD_ORDINAL'] or 0
    cd["length"] = row['CORD_LENGTH'] or 0
    cd["attachment"] = row['ATTACHMENT_TYPE'] or ""

    if row['TYPE_CODE']:
        knot_type = row['TYPE_CODE']
        place_value = row['knot_value_type'] or 0
        num_turns = row['NUM_TURNS'] or 0
        direction = row['DIRECTION'] or ""

        cd["knot_types"][knot_type] += 1
        cd["knot_directions"][direction] += 1

        # Calculate knot value
        if knot_type == 'L':  # Long knot = units digit (value = num_turns)
            cd["total_value"] += int(num_turns)
        elif knot_type == 'E':  # Figure-eight = 1 in units position
            cd["total_value"] += 1
        elif knot_type == 'S':  # Single knot = 1 × place value
            cd["total_value"] += place_value

print(f"\n  Pendant cords with data: {len(cord_data)}")

# Count cords with non-zero values
cords_with_value = sum(1 for cd in cord_data.values() if cd["total_value"] > 0)
cords_with_color = sum(1 for cd in cord_data.values() if cd["color"])
print(f"  Cords with knot values > 0: {cords_with_value}")
print(f"  Cords with colour data: {cords_with_color}")

# Value distribution
all_values = [cd["total_value"] for cd in cord_data.values() if cd["total_value"] > 0]
if all_values:
    all_values.sort()
    print(f"\n  Value distribution:")
    print(f"    Min: {min(all_values)}")
    print(f"    Median: {all_values[len(all_values)//2]}")
    print(f"    Mean: {sum(all_values)/len(all_values):.1f}")
    print(f"    Max: {max(all_values)}")
    print(f"    Total knot value across corpus: {sum(all_values):,}")

# ═══════════════════════════════════════════════════════
# STEP 4: CORE MDP — COLOUR-VALUE DOMAIN PROFILING
# Profile each cord colour by its numerical behaviour
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 4: CORE MDP — CORD COLOUR DOMAIN PROFILING")
print("=" * 75)

# For each colour: count occurrences, median/mean value, value range,
# which khipus it appears on, twist distribution, knot type distribution
color_profiles = defaultdict(lambda: {
    "count": 0, "values": [], "khipus": set(),
    "twists": Counter(), "knot_types": Counter(),
    "fibers": Counter(), "positions": [],
    "knot_directions": Counter()
})

for cid, cd in cord_data.items():
    color = cd["color"]
    if not color:
        continue

    # Use primary colour code (first component)
    primary = cd["color1"] if cd["color1"] else color.split(":")[0].split("-")[0]

    cp = color_profiles[primary]
    cp["count"] += 1
    if cd["total_value"] > 0:
        cp["values"].append(cd["total_value"])
    cp["khipus"].add(cd["khipu_id"])
    if cd["twist"]:
        cp["twists"][cd["twist"]] += 1
    for kt, kc in cd["knot_types"].items():
        cp["knot_types"][kt] += kc
    if cd["fiber"]:
        cp["fibers"][cd["fiber"]] += 1
    cp["positions"].append(cd["ordinal"])
    for kd, kc in cd["knot_directions"].items():
        cp["knot_directions"][kd] += kc

# Print profiles
print(f"\n  {'Colour':<8} {'Desc':<30} {'Cords':>6} {'Khipus':>7} {'WithVal':>7} "
      f"{'Median':>7} {'Mean':>7} {'Max':>7} {'S-twist%':>8} {'S-knot%':>8}")
print(f"  " + "-" * 115)

color_domains = {}
for color in sorted(color_profiles.keys(),
                     key=lambda c: -color_profiles[c]["count"]):
    cp = color_profiles[color]
    if cp["count"] < 10:
        continue

    vals = cp["values"]
    n_vals = len(vals)
    if vals:
        vals.sort()
        median = vals[len(vals)//2]
        mean = sum(vals)/len(vals)
        maxv = max(vals)
    else:
        median = mean = maxv = 0

    n_khipus = len(cp["khipus"])
    twist_total = sum(cp["twists"].values())
    s_twist_pct = cp["twists"].get("S", 0) / twist_total * 100 if twist_total > 0 else 0

    knot_total = sum(cp["knot_types"].values())
    s_knot_pct = cp["knot_types"].get("S", 0) / knot_total * 100 if knot_total > 0 else 0

    info = color_dict.get(color, {"desc": "?", "hue": "?"})
    desc = info["desc"][:28] if isinstance(info, dict) else "?"

    print(f"  {color:<8} {desc:<30} {cp['count']:>6} {n_khipus:>7} {n_vals:>7} "
          f"{median:>7} {mean:>7.0f} {maxv:>7} {s_twist_pct:>7.0f}% {s_knot_pct:>7.0f}%")

    # Classify by value range
    if n_vals > 0:
        if mean > 100:
            domain = "HIGH_VALUE"
        elif mean > 20:
            domain = "MED_VALUE"
        elif mean > 5:
            domain = "LOW_VALUE"
        else:
            domain = "MINIMAL"
    else:
        domain = "NO_KNOTS"

    color_domains[color] = {
        "domain": domain, "count": cp["count"], "mean": mean,
        "median": median, "n_khipus": n_khipus
    }

# ═══════════════════════════════════════════════════════
# STEP 5: COLOUR CO-OCCURRENCE ON SAME KHIPU
# Which colours appear together? (like word co-occurrence)
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 5: COLOUR CO-OCCURRENCE (Which colours appear together?)")
print("=" * 75)

# Build khipu → set of primary colours
khipu_colors = defaultdict(Counter)
for cid, cd in cord_data.items():
    if cd["color1"]:
        khipu_colors[cd["khipu_id"]][cd["color1"]] += 1

# Compute co-occurrence matrix for top colours
top_colors = [c for c, cp in sorted(color_profiles.items(),
              key=lambda x: -x[1]["count"]) if cp["count"] >= 20][:15]

cooccurrence = defaultdict(Counter)
for khipu_id, colors in khipu_colors.items():
    present = [c for c in top_colors if c in colors]
    for i, c1 in enumerate(present):
        for c2 in present[i+1:]:
            cooccurrence[c1][c2] += 1
            cooccurrence[c2][c1] += 1

print(f"\n  Colour pairs that most frequently appear on the SAME khipu:")
pairs = []
for c1 in top_colors:
    for c2 in top_colors:
        if c1 < c2:
            pairs.append((c1, c2, cooccurrence[c1][c2]))

for c1, c2, count in sorted(pairs, key=lambda x: -x[2])[:20]:
    d1 = color_dict.get(c1, {"desc": "?"})["desc"][:20] if c1 in color_dict else "?"
    d2 = color_dict.get(c2, {"desc": "?"})["desc"][:20] if c2 in color_dict else "?"
    print(f"    {c1} ({d1}) + {c2} ({d2}): {count} khipus")


# ═══════════════════════════════════════════════════════
# STEP 6: TWIST DIRECTION ANALYSIS
# S-twist vs Z-twist — does this encode domain info?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 6: TWIST DIRECTION AS DOMAIN MARKER")
print("=" * 75)

# Overall twist distribution
twist_counts = Counter()
twist_values = defaultdict(list)
for cd in cord_data.values():
    if cd["twist"]:
        twist_counts[cd["twist"]] += 1
        if cd["total_value"] > 0:
            twist_values[cd["twist"]].append(cd["total_value"])

print(f"\n  Overall twist distribution:")
for twist, count in twist_counts.most_common():
    vals = twist_values.get(twist, [])
    if vals:
        vals.sort()
        med = vals[len(vals)//2]
        mean = sum(vals)/len(vals)
        print(f"    {twist}-twist: {count} cords, median value={med}, mean={mean:.0f}")
    else:
        print(f"    {twist}-twist: {count} cords (no knot values)")


# ═══════════════════════════════════════════════════════
# STEP 7: KNOT TYPE AS METROLOGICAL INDICATOR
# Do different knot types correlate with different colours?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 7: KNOT TYPE × COLOUR CORRELATION")
print("=" * 75)

print(f"\n  Do certain colours preferentially use certain knot types?")
print(f"  (S=single/tens+, L=long/units, E=figure-eight/one)\n")

for color in top_colors[:12]:
    cp = color_profiles[color]
    kt = cp["knot_types"]
    total_kt = sum(kt.values())
    if total_kt < 5:
        continue
    desc = color_dict.get(color, {"desc": "?"})["desc"][:25] if color in color_dict else "?"
    kt_str = ", ".join(f"{t}={c}({c/total_kt*100:.0f}%)" for t, c in kt.most_common())
    print(f"  {color} ({desc}): {kt_str}")


# ═══════════════════════════════════════════════════════
# STEP 8: PROVENANCE ANALYSIS
# Do different archives use different colour palettes?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 8: PROVENANCE × COLOUR PALETTE")
print("=" * 75)

# Build provenance → colour distribution
prov_colors = defaultdict(Counter)
prov_values = defaultdict(list)

cursor.execute("SELECT KHIPU_ID, PROVENANCE FROM khipu_main WHERE PROVENANCE != ''")
khipu_prov = {}
for row in cursor.fetchall():
    khipu_prov[row['KHIPU_ID']] = row['PROVENANCE']

for cid, cd in cord_data.items():
    prov = khipu_prov.get(cd["khipu_id"], "")
    if prov and cd["color1"]:
        prov_colors[prov][cd["color1"]] += 1
    if prov and cd["total_value"] > 0:
        prov_values[prov].append(cd["total_value"])

print(f"\n  Top colour palette by provenance:")
for prov in sorted(prov_colors.keys(),
                    key=lambda p: -sum(prov_colors[p].values())):
    colors = prov_colors[prov]
    total = sum(colors.values())
    if total < 50:
        continue
    vals = prov_values.get(prov, [])
    val_str = f"  med={sorted(vals)[len(vals)//2]}, mean={sum(vals)/len(vals):.0f}" if vals else ""
    top5 = ", ".join(f"{c}={n}" for c, n in colors.most_common(5))
    print(f"\n  {prov} ({total} cords{val_str}):")
    print(f"    {top5}")


# ═══════════════════════════════════════════════════════
# STEP 9: SUMMATION CHECKING
# Do subsidiary cords sum to match top cords?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 9: SUMMATION CHECKING — Do cord groups sum correctly?")
print("=" * 75)

# Group cords by cluster within each khipu
# Check if any cord's value equals the sum of its cluster mates
cursor.execute("""
    SELECT cc.KHIPU_ID, cc.CLUSTER_ID, cc.NUM_CORDS,
           c.CORD_ID, c.CORD_ORDINAL
    FROM cord_cluster cc
    JOIN cord c ON cc.KHIPU_ID = c.KHIPU_ID 
                AND c.CLUSTER_ID = cc.CLUSTER_ID
    WHERE cc.NUM_CORDS >= 3
    ORDER BY cc.KHIPU_ID, cc.CLUSTER_ID, c.CORD_ORDINAL
""")

cluster_cords = defaultdict(list)
for row in cursor.fetchall():
    key = (row['KHIPU_ID'], row['CLUSTER_ID'])
    cid = row['CORD_ID']
    val = cord_data[cid]["total_value"] if cid in cord_data else 0
    cluster_cords[key].append((cid, val))

# Check for summation patterns (last cord = sum of others?)
exact_sums = 0
close_sums = 0
total_checked = 0

for (khipu_id, cluster_id), cords in cluster_cords.items():
    if len(cords) < 3:
        continue
    values = [v for _, v in cords if v > 0]
    if len(values) < 3:
        continue

    total_checked += 1
    # Check if last value = sum of others
    last_val = values[-1]
    others_sum = sum(values[:-1])

    if others_sum > 0 and last_val == others_sum:
        exact_sums += 1
    elif others_sum > 0 and abs(last_val - others_sum) <= 2:
        close_sums += 1

print(f"\n  Clusters checked (3+ cords with values): {total_checked}")
print(f"  Last cord = sum of others (exact): {exact_sums}")
print(f"  Close matches (±2): {close_sums}")
if total_checked > 0:
    print(f"  Sum match rate: {(exact_sums + close_sums)/total_checked*100:.1f}%")


# ═══════════════════════════════════════════════════════
# STEP 10: COLOUR DOMAIN CLASSIFICATION SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 10: COLOUR DOMAIN CLASSIFICATION SUMMARY")
print("=" * 75)

# Group by hue family
hue_families = defaultdict(list)
for color, profile in color_profiles.items():
    if profile["count"] < 10:
        continue
    info = color_dict.get(color, {"hue": "?", "desc": "?"})
    hue = info.get("hue", "?") if isinstance(info, dict) else "?"
    hue_families[hue].append((color, profile))

hue_names = {"B": "BROWN", "W": "WHITE", "G": "GREEN", "M": "GREY",
             "Z": "BLACK", "Y": "YELLOW", "N": "ORANGE", "H": "BLUE",
             "R": "RED", "L": "OLIVE", "?": "COMPOUND/SPECIAL"}

print(f"\n  Colours grouped by hue family:")
for hue in sorted(hue_families.keys()):
    family = hue_families[hue]
    total_cords = sum(cp["count"] for _, cp in family)
    all_vals = []
    for _, cp in family:
        all_vals.extend(cp["values"])

    if all_vals:
        all_vals.sort()
        med = all_vals[len(all_vals)//2]
        mean = sum(all_vals)/len(all_vals)
        val_str = f"  median={med}, mean={mean:.0f}, max={max(all_vals)}"
    else:
        val_str = "  (no values)"

    hue_name = hue_names.get(hue, hue)
    print(f"\n  {hue_name} ({hue}) — {total_cords} cords, {len(family)} shades{val_str}")
    for color, cp in sorted(family, key=lambda x: -x[1]["count"])[:5]:
        desc = color_dict.get(color, {"desc": "?"})
        desc = desc["desc"][:30] if isinstance(desc, dict) else "?"
        n_vals = len(cp["values"])
        cp_mean = sum(cp["values"])/n_vals if n_vals > 0 else 0
        print(f"    {color}: {cp['count']} cords, {n_vals} with values, mean={cp_mean:.0f}")


# ═══════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("INCA KHIPU MDP ANALYSIS — COMPLETE")
print("=" * 75)

print(f"\n  CORPUS:")
print(f"    Khipus: {n_khipus}")
print(f"    Pendant cords: {len(cord_data)}")
print(f"    Knots: {n_knots}")
print(f"    Cord colours profiled: {len([c for c in color_profiles if color_profiles[c]['count'] >= 10])}")

print(f"\n  KEY QUESTION: Do cord colours cluster into distinct numerical domains?")

# Check if colours have significantly different value distributions
high_val_colors = [c for c, d in color_domains.items() if d["domain"] == "HIGH_VALUE"]
med_val_colors = [c for c, d in color_domains.items() if d["domain"] == "MED_VALUE"]
low_val_colors = [c for c, d in color_domains.items() if d["domain"] == "LOW_VALUE"]
no_knot_colors = [c for c, d in color_domains.items() if d["domain"] == "NO_KNOTS"]

print(f"\n  HIGH VALUE colours (mean > 100): {len(high_val_colors)}")
for c in high_val_colors[:5]:
    d = color_domains[c]
    desc = color_dict.get(c, {"desc": "?"})
    desc = desc["desc"][:30] if isinstance(desc, dict) else "?"
    print(f"    {c} ({desc}): mean={d['mean']:.0f}, {d['count']} cords")

print(f"\n  MED VALUE colours (mean 20-100): {len(med_val_colors)}")
for c in med_val_colors[:5]:
    d = color_domains[c]
    desc = color_dict.get(c, {"desc": "?"})
    desc = desc["desc"][:30] if isinstance(desc, dict) else "?"
    print(f"    {c} ({desc}): mean={d['mean']:.0f}, {d['count']} cords")

print(f"\n  LOW VALUE colours (mean 5-20): {len(low_val_colors)}")
for c in low_val_colors[:5]:
    d = color_domains[c]
    desc = color_dict.get(c, {"desc": "?"})
    desc = desc["desc"][:30] if isinstance(desc, dict) else "?"
    print(f"    {c} ({desc}): mean={d['mean']:.0f}, {d['count']} cords")

print(f"\n  NO KNOTS colours: {len(no_knot_colors)}")

print(f"\n  If different colours carry systematically different value ranges,")
print(f"  this proves colour encodes commodity/category information —")
print(f"  the same metrological domain separation found on clay tablets")
print(f"  in Mesopotamia, Iran, South Asia, and the Aegean.")

conn.close()
print()

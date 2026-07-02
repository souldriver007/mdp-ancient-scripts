#!/usr/bin/env python3
"""
MDP KHIPU CORE ALGORITHM 2: System Classification + Value Distribution
========================================================================
Peer-review-ready implementation of the dual-system classifier and
value-distribution shape analysis described in Paper IV §2.5–2.6.

PURPOSE:
  Classify each khipu in the OKR corpus into one of three administrative
  systems (A, B, or Mixed) using a composite score across 6-8 dimensions,
  then characterise its value distribution shape (Arithmetic, Gaussian,
  Zipfian, Binary, Low-range).

CLASSIFICATION MODEL:
  Each dimension produces a score from -1.0 (strong System A) to +1.0
  (strong System B). The composite score is the arithmetic mean of all
  applicable dimensions. Optional dimensions (LK marker, canutos) are
  only included when their trigger condition is met, which changes the
  denominator — this means a khipu with 8 dimensions is scored on a
  different scale than one with 6, intentionally weighting rare System B
  markers more heavily when present.

  Thresholds:
    composite >= 0.5   → System B, HIGH confidence
    composite >= 0.3   → System B, MEDIUM confidence
    composite <= -0.5  → System A, HIGH confidence
    composite <= -0.3  → System A, MEDIUM confidence
    otherwise          → Mixed / Unclassified

DIMENSION SCORING RUBRIC:

  1. FIBER (cotton vs camelid)
     Rationale: System A uses coastal cotton; System B uses highland camelid.
     CL (camelid) > 80%:  +1.0  |  CL any:  +0.5
     CN (cotton) > 80%:   -1.0  |  CN any:  -0.5
     Other/unknown:        0.0

  2. TOPOLOGY (hierarchical vs flat)
     Rationale: System A is deeply hierarchical (4-5 levels of subsidiaries);
     System B is completely flat (zero subsidiaries).
     0 subsidiaries, depth ≤ 1:  +1.0  (flat — System B signature)
     Sub rate < 5%:              +0.5  (near-flat)
     Sub rate > 30%:             -1.0  (deeply hierarchical — System A)
     Sub rate > 10%:             -0.5  (hierarchical)
     Otherwise:                   0.0

  3. KNOT SYNTAX (L-type vs S-type vs E-type)
     Rationale: System B uses L-type (long) knots for tactile ridge-counting;
     System A uses S-type for positional decimal arithmetic.
     L-type ≥ 90%:  +1.0  (3.9σ above corpus mean of 23% — definitive)
     L-type ≥ 70%:  +0.7  (elevated)
     S-type ≥ 70%:  -1.0  (standard arithmetic)
     S-type ≥ 50%:  -0.5
     E-type ≥ 90%:  +0.3  (binary checklist — distinct type)
     Otherwise:      0.0

  4. COLOUR DIVERSITY (polychrome vs monochrome)
     Rationale: System A uses polychrome colour matrices; System B is
     monochrome (single-colour data, no structural formatting via colour).
     ≤ 2 colours:  +0.5  (monochrome)
     ≤ 4 colours:  +0.2
     ≥ 8 colours:  -0.5  (polychrome)
     Otherwise:    -0.2

  5. VALUE RANGE (arithmetic scale vs demographic scale)
     Rationale: System B counts people (mean ~15, max ~50); System A
     counts warehouse quantities (means in hundreds, max in thousands).
     max ≤ 50 AND 5 ≤ mean ≤ 30:  +0.5  (demographic range)
     max > 1000:                   -0.5  (warehouse range)
     Otherwise:                     0.0

  6. BEGINNING TYPE (primary cord construction)
     Rationale: System B documents have braided/doubled beginnings
     (authentication markers); System A uses simple twisted beginnings.
     NB/B/D (braided/doubled):  +0.3
     T (twisted):               -0.2
     Otherwise:                  0.0

  7. LK MARKER (optional — only scored if LK > 20%)
     Rationale: LK (black) is the governance marker absent from
     warehouses (0% at Incahuasi) but enriched on System B (58-72%).
     LK > 20%:  +0.5 (dimension added to score)

  8. CANUTOS (optional — only scored if detected)
     Rationale: Canuto thread wrappings are authentication seals found
     predominantly on System B governance documents.
     Detected:  +0.3 (dimension added to score)

VALUE DISTRIBUTION SHAPE CLASSIFIER:
  After computing cord values (L-type: NUM_TURNS; S-type: knot_value_type;
  E-type: 1), the distribution is classified:
    n < 10:                              'Too few values'
    max ≤ 2:                             'Binary' (presence/absence)
    σ < 0.5μ AND μ > 5 AND max < 60:     'Gaussian' (demographic bell curve)
    max > 10μ:                            'Zipfian' (power-law / categorical)
    σ < 3 AND μ < 5:                      'Low-range' (micro-counts)
    otherwise:                            'Arithmetic' (standard decimal)

REPRODUCING THIS ANALYSIS:
  1. Download the OKR SQLite database
  2. Run: python mdp_classifier.py [path_to_khipu.db]
  3. No dependencies beyond Python 3.8+ standard library

Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: July 2026
Paper: MDP IV — The Colour Alphabet of the Inca Empire
"""

import sqlite3
import sys
import os
import math
import csv
from collections import defaultdict

DEFAULT_DB = r"C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\data\khipu.db"

# Classification thresholds
SYSTEM_B_HIGH = 0.5
SYSTEM_B_MEDIUM = 0.3
SYSTEM_A_HIGH = -0.5
SYSTEM_A_MEDIUM = -0.3

# Cache for primary cord IDs (avoids subsidiary miscount)
_pc_ids = None

def _get_pc_ids(conn):
    global _pc_ids
    if _pc_ids is None:
        _pc_ids = set(
            r[0] for r in conn.execute('SELECT PCORD_ID FROM primary_cord').fetchall()
        )
    return _pc_ids

def connect(db_path):
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ════════════════════════════════════════════════════
# CLASSIFY SYSTEM
# ════════════════════════════════════════════════════

def classify_system(conn, khipu_id):
    """
    Score a single khipu across 6-8 dimensions.
    Returns dict with classification, score, per-dimension breakdown.
    Returns None if khipu has no cord data.
    """
    rows = conn.execute("""
        SELECT c.CORD_ID, c.CORD_LEVEL, c.TWIST, c.FIBER, c.PENDANT_FROM,
               acc.COLOR_CD_1,
               k.TYPE_CODE, k.NUM_TURNS, k.knot_value_type
        FROM cord c
        LEFT JOIN ascher_cord_color acc
            ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        LEFT JOIN knot k
            ON c.CORD_ID = k.CORD_ID
        WHERE c.KHIPU_ID = ?
    """, (khipu_id,)).fetchall()

    if not rows:
        return None

    pc_row = conn.execute(
        'SELECT BEGINNING FROM primary_cord WHERE KHIPU_ID = ?', (khipu_id,)
    ).fetchone()
    beginning = (pc_row['BEGINNING'] or '').upper() if pc_row else ''

    # ── Aggregate cord-level statistics ──
    seen = set()
    fibers, knot_types, colors = defaultdict(int), defaultdict(int), defaultdict(int)
    n_subs, n_pendants, max_depth = 0, 0, 0
    cord_vals = defaultdict(int)

    for r in rows:
        cid = r['CORD_ID']
        if cid not in seen:
            seen.add(cid)
            if r['FIBER']: fibers[r['FIBER']] += 1
            if r['COLOR_CD_1']: colors[r['COLOR_CD_1']] += 1
            lvl = r['CORD_LEVEL'] or 0
            if lvl == 1: n_pendants += 1
            if lvl > 1: n_subs += 1
            if lvl > max_depth: max_depth = lvl

        if r['TYPE_CODE']: knot_types[r['TYPE_CODE']] += 1

        # Value computation: same formula as OKR standard
        if r['TYPE_CODE'] == 'L': cord_vals[cid] += (r['NUM_TURNS'] or 0)
        elif r['TYPE_CODE'] == 'E': cord_vals[cid] += 1
        elif r['TYPE_CODE'] == 'S': cord_vals[cid] += (r['knot_value_type'] or 0)

    values = [v for v in cord_vals.values() if v > 0]
    total = len(seen)
    if total == 0: return None

    kt = sum(knot_types.values()) or 1
    s_pct = knot_types.get('S', 0) / kt * 100
    l_pct = knot_types.get('L', 0) / kt * 100
    e_pct = knot_types.get('E', 0) / kt * 100
    n_col = len(colors)
    sub_rate = n_subs / total
    dom = max(fibers.items(), key=lambda x: x[1]) if fibers else ('', 0)
    fiber, fiber_pct = dom[0], dom[1] / total * 100
    mean_v = sum(values) / len(values) if values else 0
    max_v = max(values) if values else 0

    # ── Score each dimension ──
    dims = {}

    # 1. FIBER
    if fiber == 'CL' and fiber_pct > 80: dims['fiber'] = 1.0
    elif fiber == 'CL': dims['fiber'] = 0.5
    elif fiber == 'CN' and fiber_pct > 80: dims['fiber'] = -1.0
    elif fiber == 'CN': dims['fiber'] = -0.5
    else: dims['fiber'] = 0.0

    # 2. TOPOLOGY
    if n_subs == 0 and max_depth <= 1: dims['topology'] = 1.0
    elif sub_rate < 0.05: dims['topology'] = 0.5
    elif sub_rate > 0.3: dims['topology'] = -1.0
    elif sub_rate > 0.1: dims['topology'] = -0.5
    else: dims['topology'] = 0.0

    # 3. KNOT SYNTAX
    if l_pct >= 90: dims['knot_syntax'] = 1.0
    elif l_pct >= 70: dims['knot_syntax'] = 0.7
    elif s_pct >= 70: dims['knot_syntax'] = -1.0
    elif s_pct >= 50: dims['knot_syntax'] = -0.5
    elif e_pct >= 90: dims['knot_syntax'] = 0.3
    else: dims['knot_syntax'] = 0.0

    # 4. COLOUR DIVERSITY
    if n_col <= 2: dims['colour'] = 0.5
    elif n_col <= 4: dims['colour'] = 0.2
    elif n_col >= 8: dims['colour'] = -0.5
    else: dims['colour'] = -0.2

    # 5. VALUE RANGE
    if max_v <= 50 and 5 <= mean_v <= 30: dims['value_range'] = 0.5
    elif max_v > 1000: dims['value_range'] = -0.5
    else: dims['value_range'] = 0.0

    # 6. BEGINNING TYPE
    if beginning in ('NB', 'B', 'D'): dims['beginning'] = 0.3
    elif beginning == 'T': dims['beginning'] = -0.2
    else: dims['beginning'] = 0.0

    # 7. LK MARKER (optional)
    lk_pct = colors.get('LK', 0) / total * 100
    if lk_pct > 20: dims['lk_marker'] = 0.5

    # 8. CANUTOS (optional)
    can = conn.execute("""
        SELECT COUNT(*) as n FROM cord
        WHERE KHIPU_ID = ? AND CORD_LEVEL > 1
          AND CORD_LENGTH < 3 AND CORD_LENGTH > 0
    """, (khipu_id,)).fetchone()
    if can['n'] > 0: dims['canutos'] = 0.3

    # ── Composite score = mean of all active dimensions ──
    score = round(sum(dims.values()) / len(dims), 2) if dims else 0

    if score >= SYSTEM_B_HIGH: cls, conf = 'System_B', 'HIGH'
    elif score >= SYSTEM_B_MEDIUM: cls, conf = 'System_B', 'MEDIUM'
    elif score <= SYSTEM_A_HIGH: cls, conf = 'System_A', 'HIGH'
    elif score <= SYSTEM_A_MEDIUM: cls, conf = 'System_A', 'MEDIUM'
    else: cls, conf = 'Mixed', 'LOW'

    return {
        'khipu_id': khipu_id, 'classification': cls, 'confidence': conf,
        'score': score, 'n_dims': len(dims), 'dimensions': dims,
        'cords': total, 'pendants': n_pendants, 'subs': n_subs,
        'max_depth': max_depth, 'n_colors': n_col,
        'fiber': fiber, 'fiber_pct': round(fiber_pct, 1),
        's_pct': round(s_pct, 1), 'l_pct': round(l_pct, 1), 'e_pct': round(e_pct, 1),
        'mean_val': round(mean_v, 1), 'max_val': max_v, 'lk_pct': round(lk_pct, 1),
    }


# ════════════════════════════════════════════════════
# VALUE DISTRIBUTION SHAPE
# ════════════════════════════════════════════════════

def classify_shape(conn, khipu_id):
    """
    Classify the value distribution of a khipu's pendant cords.
    Returns shape label and key statistics.
    """
    rows = conn.execute("""
        SELECT c.CORD_ID, k.TYPE_CODE, k.NUM_TURNS, k.knot_value_type
        FROM cord c
        LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
        WHERE c.KHIPU_ID = ? AND c.CORD_LEVEL = 1
    """, (khipu_id,)).fetchall()

    vals = defaultdict(int)
    for r in rows:
        cid = r['CORD_ID']
        if r['TYPE_CODE'] == 'L': vals[cid] += (r['NUM_TURNS'] or 0)
        elif r['TYPE_CODE'] == 'E': vals[cid] += 1
        elif r['TYPE_CODE'] == 'S': vals[cid] += (r['knot_value_type'] or 0)

    raw = sorted(vals.values())
    n = len(raw)
    if n == 0: return 'No values', {}

    mean = sum(raw) / n
    mx = raw[-1]
    sd = math.sqrt(sum((v - mean) ** 2 for v in raw) / (n - 1)) if n > 1 else 0

    if n < 10: shape = 'Too few values'
    elif mx <= 2: shape = 'Binary'
    elif sd < mean * 0.5 and mean > 5 and mx < 60: shape = 'Gaussian'
    elif mean > 0 and mx > mean * 10: shape = 'Zipfian'
    elif sd < 3 and mean < 5: shape = 'Low-range'
    else: shape = 'Arithmetic'

    return shape, {'mean': round(mean, 1), 'max': mx, 'std': round(sd, 1), 'n': n}


# ════════════════════════════════════════════════════
# CLEAN SUMMATION — strip formatting noise before testing arithmetic
# ════════════════════════════════════════════════════

def clean_summation(conn, khipu_id, auto_detect_spacers=True):
    """
    Test summation after removing formatting cords (zeros, spacers,
    structural colours). Returns cluster and subsidiary match rates.

    Spacer detection: a cord with value exactly V is a spacer if V appears
    ≥5 times AND accounts for ≥10% of pendants. Default test values: 10, 15, 47
    (documented Inca administrative units in the OKR).
    """
    rows = conn.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL, c.CLUSTER_ID, c.CORD_LEVEL,
               c.PENDANT_FROM, acc.COLOR_CD_1,
               k.TYPE_CODE, k.knot_value_type, k.NUM_TURNS
        FROM cord c
        LEFT JOIN ascher_cord_color acc
            ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
        WHERE c.KHIPU_ID = ?
        ORDER BY c.CORD_LEVEL, c.CORD_ORDINAL
    """, (khipu_id,)).fetchall()

    pc_ids = _get_pc_ids(conn)
    cord_data = {}
    for r in rows:
        cid = r['CORD_ID']
        if cid not in cord_data:
            cord_data[cid] = {
                'cluster': r['CLUSTER_ID'], 'value': 0, 'ordinal': r['CORD_ORDINAL'],
                'level': r['CORD_LEVEL'], 'colour': r['COLOR_CD_1'] or '',
                'pendant_from': r['PENDANT_FROM']
            }
        if r['TYPE_CODE'] == 'L': cord_data[cid]['value'] += (r['NUM_TURNS'] or 0)
        elif r['TYPE_CODE'] == 'E': cord_data[cid]['value'] += 1
        elif r['TYPE_CODE'] == 'S': cord_data[cid]['value'] += (r['knot_value_type'] or 0)

    pendants = {cid: c for cid, c in cord_data.items() if c['level'] == 1}

    # Spacer detection
    spacers = set()
    if auto_detect_spacers:
        for test_val in [10, 15, 47]:
            count = sum(1 for c in pendants.values() if c['value'] == test_val)
            if count >= 5 and count / len(pendants) >= 0.10:
                spacers.add(test_val)

    # Build exclusion set
    excluded = set()
    for cid, c in cord_data.items():
        if c['value'] == 0 or c['value'] in spacers:
            excluded.add(cid)

    # Cluster summation (level 1, cleaned)
    clusters = defaultdict(list)
    for cid, c in pendants.items():
        if cid not in excluded:
            clusters[c['cluster']].append(c)

    cl_tested, cl_first, cl_last = 0, 0, 0
    for cvs in clusters.values():
        cvs.sort(key=lambda x: x['ordinal'])
        vals = [c['value'] for c in cvs if c['value'] > 0]
        if len(vals) < 3: continue
        cl_tested += 1
        if abs(vals[0] - sum(vals[1:])) <= 2: cl_first += 1
        if abs(vals[-1] - sum(vals[:-1])) <= 2: cl_last += 1

    # Subsidiary summation (all levels, cleaned)
    children = defaultdict(list)
    for cid, c in cord_data.items():
        if c['pendant_from'] and c['pendant_from'] not in pc_ids:
            children[c['pendant_from']].append(cid)

    sub_tested, sub_exact, sub_close = 0, 0, 0
    for pid, child_ids in children.items():
        clean_kids = [c for c in child_ids if c not in excluded]
        if len(clean_kids) < 2: continue
        parent = cord_data.get(pid)
        if not parent or parent['value'] == 0 or pid in excluded: continue
        child_sum = sum(cord_data[c]['value'] for c in clean_kids)
        if child_sum == 0: continue
        sub_tested += 1
        if parent['value'] == child_sum: sub_exact += 1
        elif abs(parent['value'] - child_sum) <= 2: sub_close += 1

    return {
        'khipu_id': khipu_id,
        'spacers_detected': list(spacers),
        'excluded': len(excluded),
        'cluster': {
            'tested': cl_tested,
            'first_match': cl_first,
            'last_match': cl_last,
            'first_rate': f"{cl_first/cl_tested*100:.0f}%" if cl_tested else "N/A",
            'last_rate': f"{cl_last/cl_tested*100:.0f}%" if cl_tested else "N/A",
        },
        'subsidiary': {
            'tested': sub_tested,
            'exact': sub_exact,
            'close': sub_close,
            'rate': f"{(sub_exact+sub_close)/sub_tested*100:.0f}%" if sub_tested else "N/A",
        }
    }


# ════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════

def main():
    db_path = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_DB
    conn = connect(db_path)

    khipus = conn.execute("""
        SELECT k.KHIPU_ID, k.OKR_NUM, k.PROVENANCE
        FROM khipu_main k ORDER BY k.KHIPU_ID
    """).fetchall()

    print(f"{'='*70}")
    print(f"CORPUS-WIDE SYSTEM CLASSIFICATION + SHAPE ANALYSIS")
    print(f"Khipus: {len(khipus)} | Method: 6-8 dimension composite scoring")
    print(f"{'='*70}\n")

    results = []
    for i, kh in enumerate(khipus):
        r = classify_system(conn, kh['KHIPU_ID'])
        if r is None: continue
        shape, stats = classify_shape(conn, kh['KHIPU_ID'])
        r['shape'] = shape
        r['okr'] = kh['OKR_NUM'] or ''
        r['provenance'] = kh['PROVENANCE'] or ''
        results.append(r)
        if (i + 1) % 50 == 0:
            print(f"  [{i+1}/{len(khipus)}]...")

    # Summary
    a = [r for r in results if r['classification'] == 'System_A']
    b = [r for r in results if r['classification'] == 'System_B']
    m = [r for r in results if r['classification'] == 'Mixed']
    c = [r for r in m if r['shape'] == 'Zipfian']

    print(f"\n  CLASSIFICATION:")
    print(f"    System A:  {len(a):>4}  ({len(a)/len(results)*100:.1f}%)")
    print(f"    System B:  {len(b):>4}  ({len(b)/len(results)*100:.1f}%)")
    print(f"    System C:  {len(c):>4}  ({len(c)/len(results)*100:.1f}%)  [Mixed + Zipfian]")
    print(f"    Mixed:     {len(m)-len(c):>4}  ({(len(m)-len(c))/len(results)*100:.1f}%)")
    print(f"    Total:     {len(results):>4}")

    # Save
    try:
        out_dir = os.path.dirname(os.path.dirname(os.path.abspath(db_path)))
        if not os.path.isdir(out_dir): out_dir = '.'
    except:
        out_dir = '.'

    csv_path = os.path.join(out_dir, 'classifier_results.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[
            'khipu_id', 'okr', 'classification', 'confidence', 'score',
            'shape', 'n_dims', 'cords', 'pendants', 'subs', 'max_depth',
            'n_colors', 'fiber', 'fiber_pct', 's_pct', 'l_pct', 'e_pct',
            'mean_val', 'max_val', 'lk_pct', 'provenance'
        ], extrasaction='ignore')
        w.writeheader()
        for r in results: w.writerow(r)

    print(f"\n  CSV: {csv_path}")
    print(f"{'='*70}")
    conn.close()


if __name__ == '__main__':
    main()

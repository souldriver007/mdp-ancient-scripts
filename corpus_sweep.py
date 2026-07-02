#!/usr/bin/env python3
"""
CORPUS-WIDE SYSTEM CLASSIFICATION SWEEP
========================================
Faithful Python port of KARP Khipu Graph MCP v1.2.0 classifySystem() + valueTransitions()
from server/khipu.js.

Runs classify_system on ALL 619 khipus, then value_transitions on Mixed specimens
to identify System C (Zipfian) distribution.

Usage:
    python corpus_sweep.py

Output:
    - Console summary with counts
    - corpus_sweep_results.csv  (full results, every khipu)
    - corpus_sweep_summary.md   (Paper IV-ready summary table)

Author: Adrian Sharman / SoulDriver Research / Claude (port)
Date: 2 July 2026
"""

import sqlite3
import sys
import os
import math
from collections import defaultdict
import csv

# Default database path
DEFAULT_DB = r"C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\data\khipu.db"

def connect(db_path):
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found at {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

_pc_ids_cache = None

def _get_pc_ids(conn):
    global _pc_ids_cache
    if _pc_ids_cache is None:
        _pc_ids_cache = set(
            r['PCORD_ID'] for r in
            conn.execute('SELECT PCORD_ID FROM primary_cord').fetchall()
        )
    return _pc_ids_cache

def classify_system(conn, khipu_id):
    pc_ids = _get_pc_ids(conn)
    rows = conn.execute("""
        SELECT c.CORD_ID, c.CORD_LEVEL, c.TWIST, c.FIBER, c.PENDANT_FROM,
               acc.COLOR_CD_1,
               k.TYPE_CODE, k.NUM_TURNS, k.knot_value_type
        FROM cord c
        LEFT JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
        WHERE c.KHIPU_ID = ?
    """, (khipu_id,)).fetchall()

    if not rows:
        return None

    pc_row = conn.execute(
        'SELECT BEGINNING, FIBER, STRUCTURE FROM primary_cord WHERE KHIPU_ID = ?',
        (khipu_id,)
    ).fetchone()
    pc_beginning = (pc_row['BEGINNING'] or '').upper() if pc_row else ''

    seen_cords = set()
    fibers = defaultdict(int)
    knot_types = defaultdict(int)
    colors = defaultdict(int)
    n_subs = 0
    n_pendants = 0
    max_depth = 0
    cord_vals = defaultdict(int)

    for r in rows:
        cid = r['CORD_ID']
        if cid not in seen_cords:
            seen_cords.add(cid)
            if r['FIBER']:
                fibers[r['FIBER']] += 1
            if r['COLOR_CD_1']:
                colors[r['COLOR_CD_1']] += 1
            level = r['CORD_LEVEL'] or 0
            if level == 1:
                n_pendants += 1
            if level > 1:
                n_subs += 1
            if level > max_depth:
                max_depth = level

        if r['TYPE_CODE']:
            knot_types[r['TYPE_CODE']] += 1

        if r['TYPE_CODE'] == 'L':
            cord_vals[cid] += (r['NUM_TURNS'] or 0)
        elif r['TYPE_CODE'] == 'E':
            cord_vals[cid] += 1
        elif r['TYPE_CODE'] == 'S':
            cord_vals[cid] += (r['knot_value_type'] or 0)

    values = [v for v in cord_vals.values() if v > 0]
    total_cords = len(seen_cords)
    if total_cords == 0:
        return None

    kt_total = sum(knot_types.values()) or 1
    s_pct = (knot_types.get('S', 0) / kt_total) * 100
    l_pct = (knot_types.get('L', 0) / kt_total) * 100
    e_pct = (knot_types.get('E', 0) / kt_total) * 100
    n_colors = len(colors)
    sub_rate = n_subs / total_cords if total_cords > 0 else 0

    dom_fiber = max(fibers.items(), key=lambda x: x[1]) if fibers else ('', 0)
    fiber_code = dom_fiber[0]
    fiber_pct = (dom_fiber[1] / total_cords * 100) if total_cords > 0 else 0

    mean_val = sum(values) / len(values) if values else 0
    max_val = max(values) if values else 0

    dimensions = {}

    # 1. FIBER
    if fiber_code == 'CL' and fiber_pct > 80:
        dimensions['fiber'] = 1.0
    elif fiber_code == 'CL':
        dimensions['fiber'] = 0.5
    elif fiber_code == 'CN' and fiber_pct > 80:
        dimensions['fiber'] = -1.0
    elif fiber_code == 'CN':
        dimensions['fiber'] = -0.5
    else:
        dimensions['fiber'] = 0.0

    # 2. TOPOLOGY
    if n_subs == 0 and max_depth <= 1:
        dimensions['topology'] = 1.0
    elif sub_rate < 0.05:
        dimensions['topology'] = 0.5
    elif sub_rate > 0.3:
        dimensions['topology'] = -1.0
    elif sub_rate > 0.1:
        dimensions['topology'] = -0.5
    else:
        dimensions['topology'] = 0.0

    # 3. KNOT SYNTAX
    if l_pct >= 90:
        dimensions['knot_syntax'] = 1.0
    elif l_pct >= 70:
        dimensions['knot_syntax'] = 0.7
    elif s_pct >= 70:
        dimensions['knot_syntax'] = -1.0
    elif s_pct >= 50:
        dimensions['knot_syntax'] = -0.5
    elif e_pct >= 90:
        dimensions['knot_syntax'] = 0.3
    else:
        dimensions['knot_syntax'] = 0.0

    # 4. COLOUR DIVERSITY
    if n_colors <= 2:
        dimensions['colour'] = 0.5
    elif n_colors <= 4:
        dimensions['colour'] = 0.2
    elif n_colors >= 8:
        dimensions['colour'] = -0.5
    else:
        dimensions['colour'] = -0.2

    # 5. VALUE RANGE
    if max_val <= 50 and 5 <= mean_val <= 30:
        dimensions['value_range'] = 0.5
    elif max_val > 1000:
        dimensions['value_range'] = -0.5
    else:
        dimensions['value_range'] = 0.0

    # 6. BEGINNING TYPE
    if pc_beginning in ('NB', 'B', 'D'):
        dimensions['beginning'] = 0.3
    elif pc_beginning == 'T':
        dimensions['beginning'] = -0.2
    else:
        dimensions['beginning'] = 0.0

    # 7. LK COLOUR MARKER (optional — only added if LK > 20%)
    lk_count = colors.get('LK', 0)
    lk_pct = (lk_count / total_cords * 100) if total_cords > 0 else 0
    if lk_pct > 20:
        dimensions['lk_marker'] = 0.5

    # 8. CANUTO CHECK (optional — only added if detected)
    canuto_row = conn.execute("""
        SELECT COUNT(*) as n FROM cord c
        WHERE c.KHIPU_ID = ? AND c.CORD_LEVEL > 1
          AND c.CORD_LENGTH < 3 AND c.CORD_LENGTH > 0
    """, (khipu_id,)).fetchone()
    n_canutos = canuto_row['n'] if canuto_row else 0
    if n_canutos > 0:
        dimensions['canutos'] = 0.3

    scores = list(dimensions.values())
    total_score = sum(scores) / len(scores) if scores else 0
    total_score = round(total_score, 2)

    if total_score >= 0.5:
        classification = 'System_B'
        confidence = 'HIGH'
    elif total_score >= 0.3:
        classification = 'System_B'
        confidence = 'MEDIUM'
    elif total_score <= -0.5:
        classification = 'System_A'
        confidence = 'HIGH'
    elif total_score <= -0.3:
        classification = 'System_A'
        confidence = 'MEDIUM'
    else:
        classification = 'Mixed'
        confidence = 'LOW'

    flags = []
    if e_pct >= 90: flags.append('BINARY_CHECKLIST')
    if not values or all(v == 0 for v in values): flags.append('BLANK_TEMPLATE')
    if l_pct >= 70 and n_subs == 0 and fiber_code == 'CL': flags.append('CEDAR_BOX_PATTERN')
    if n_colors <= 1 and total_cords > 50: flags.append('MONOCHROME_LARGE')
    if lk_pct > 20: flags.append(f'LK_ENRICHED_{round(lk_pct)}%')
    if n_canutos > 0: flags.append('POSSIBLE_CANUTOS')

    return {
        'khipu_id': khipu_id, 'classification': classification,
        'confidence': confidence, 'score': total_score, 'n_dims': len(dimensions),
        'cords': total_cords, 'pendants': n_pendants, 'subs': n_subs,
        'max_depth': max_depth, 'n_colors': n_colors,
        'fiber': fiber_code, 'fiber_pct': round(fiber_pct, 1),
        's_pct': round(s_pct, 1), 'l_pct': round(l_pct, 1), 'e_pct': round(e_pct, 1),
        'mean_val': round(mean_val, 1), 'max_val': max_val, 'lk_pct': round(lk_pct, 1),
        'flags': '|'.join(flags) if flags else 'NONE',
        'dim_fiber': dimensions.get('fiber', 0), 'dim_topology': dimensions.get('topology', 0),
        'dim_knot': dimensions.get('knot_syntax', 0), 'dim_colour': dimensions.get('colour', 0),
        'dim_value': dimensions.get('value_range', 0), 'dim_beginning': dimensions.get('beginning', 0),
    }


def value_transitions_shape(conn, khipu_id):
    rows = conn.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL,
               k.TYPE_CODE, k.NUM_TURNS, k.knot_value_type
        FROM cord c
        LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
        WHERE c.KHIPU_ID = ? AND c.CORD_LEVEL = 1
        ORDER BY c.CORD_ORDINAL
    """, (khipu_id,)).fetchall()

    cord_vals = {}
    for r in rows:
        cid = r['CORD_ID']
        if cid not in cord_vals:
            cord_vals[cid] = {'ordinal': r['CORD_ORDINAL'], 'value': 0}
        if r['TYPE_CODE'] == 'L':
            cord_vals[cid]['value'] += (r['NUM_TURNS'] or 0)
        elif r['TYPE_CODE'] == 'E':
            cord_vals[cid]['value'] += 1
        elif r['TYPE_CODE'] == 'S':
            cord_vals[cid]['value'] += (r['knot_value_type'] or 0)

    raw_values = sorted(cv['value'] for cv in cord_vals.values())
    n = len(raw_values)
    if n == 0:
        return 'No values'

    mean_val = sum(raw_values) / n
    max_val = raw_values[-1]
    std_dev = math.sqrt(sum((v - mean_val) ** 2 for v in raw_values) / (n - 1)) if n > 1 else 0

    if n < 10: return 'Too few values'
    elif max_val <= 2: return 'Binary'
    elif std_dev < mean_val * 0.5 and mean_val > 5 and max_val < 60: return 'Gaussian'
    elif mean_val > 0 and max_val > mean_val * 10: return 'Zipfian'
    elif std_dev < 3 and mean_val < 5: return 'Low-range'
    else: return 'Arithmetic'


def main():
    db_path = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_DB

    print(f"{'=' * 70}")
    print(f"CORPUS-WIDE SYSTEM CLASSIFICATION SWEEP")
    print(f"Database: {db_path}")
    print(f"{'=' * 70}")

    conn = connect(db_path)
    khipus = conn.execute("""
        SELECT k.KHIPU_ID, k.OKR_NUM, k.PROVENANCE, k.MUSEUM_NAME, k.INVESTIGATOR_NUM
        FROM khipu_main k ORDER BY k.KHIPU_ID
    """).fetchall()

    print(f"\nTotal khipus in database: {len(khipus)}")
    print(f"\nClassifying... (this may take 1-2 minutes)\n")

    results = []
    errors = 0
    progress_interval = max(1, len(khipus) // 20)

    for i, kh in enumerate(khipus):
        kid = kh['KHIPU_ID']
        if (i + 1) % progress_interval == 0:
            print(f"  [{i+1}/{len(khipus)}] Processing {kh['OKR_NUM'] or kid}...")

        result = classify_system(conn, kid)
        if result is None:
            errors += 1
            continue

        result['okr_num'] = kh['OKR_NUM'] or ''
        result['provenance'] = kh['PROVENANCE'] or ''
        result['museum'] = kh['MUSEUM_NAME'] or ''
        result['investigator'] = kh['INVESTIGATOR_NUM'] or ''
        results.append(result)

    print(f"\nClassified: {len(results)} | Errors (no cords): {errors}")

    system_a = [r for r in results if r['classification'] == 'System_A']
    system_b = [r for r in results if r['classification'] == 'System_B']
    mixed    = [r for r in results if r['classification'] == 'Mixed']

    a_high = [r for r in system_a if r['confidence'] == 'HIGH']
    a_med  = [r for r in system_a if r['confidence'] == 'MEDIUM']
    b_high = [r for r in system_b if r['confidence'] == 'HIGH']
    b_med  = [r for r in system_b if r['confidence'] == 'MEDIUM']

    print(f"\n{'=' * 70}")
    print(f"PHASE 1: SYSTEM CLASSIFICATION")
    print(f"{'=' * 70}")
    print(f"  System A (Logistical/Warehouse):  {len(system_a):>4}  ({len(system_a)/len(results)*100:.1f}%)")
    print(f"    - HIGH confidence:              {len(a_high):>4}")
    print(f"    - MEDIUM confidence:            {len(a_med):>4}")
    print(f"  System B (Demographic/Governor):  {len(system_b):>4}  ({len(system_b)/len(results)*100:.1f}%)")
    print(f"    - HIGH confidence:              {len(b_high):>4}")
    print(f"    - MEDIUM confidence:            {len(b_med):>4}")
    print(f"  Mixed / Unclassified:             {len(mixed):>4}  ({len(mixed)/len(results)*100:.1f}%)")
    print(f"  {'─' * 40}")
    print(f"  TOTAL CLASSIFIED:                 {len(results):>4}")

    system_b_sorted = sorted(system_b, key=lambda r: r['score'], reverse=True)
    print(f"\n  TOP 15 SYSTEM B SPECIMENS:")
    print(f"  {'OKR':<10} {'Score':>6} {'Conf':<7} {'Fiber':<4} {'L%':>5} {'Colors':>6} {'Cords':>6} {'Provenance'}")
    for r in system_b_sorted[:15]:
        print(f"  {r['okr_num']:<10} {r['score']:>6.2f} {r['confidence']:<7} {r['fiber']:<4} {r['l_pct']:>5.1f} {r['n_colors']:>6} {r['cords']:>6} {r['provenance'][:40]}")

    b_by_prov = defaultdict(list)
    for r in system_b:
        b_by_prov[r['provenance'] or 'Unknown'].append(r)
    print(f"\n  SYSTEM B BY PROVENANCE:")
    for prov, recs in sorted(b_by_prov.items(), key=lambda x: -len(x[1])):
        print(f"    {prov[:50]:<50} {len(recs):>3} specimens")

    flag_counts = defaultdict(int)
    for r in results:
        for f in r['flags'].split('|'):
            if f and f != 'NONE':
                flag_counts[f] += 1
    if flag_counts:
        print(f"\n  FLAGS DETECTED:")
        for flag, count in sorted(flag_counts.items(), key=lambda x: -x[1]):
            print(f"    {flag:<35} {count:>4}")

    # PHASE 2
    print(f"\n{'=' * 70}")
    print(f"PHASE 2: VALUE DISTRIBUTION SHAPES")
    print(f"{'=' * 70}")
    print(f"\nScanning all {len(results)} khipus...\n")

    shape_counts = defaultdict(int)
    zipfian_specimens = []
    gaussian_specimens = []

    for r in results:
        shape = value_transitions_shape(conn, r['khipu_id'])
        r['shape'] = shape
        shape_counts[shape] += 1
        if shape == 'Zipfian': zipfian_specimens.append(r)
        elif shape == 'Gaussian': gaussian_specimens.append(r)

    print(f"  DISTRIBUTION SHAPES:")
    for shape, count in sorted(shape_counts.items(), key=lambda x: -x[1]):
        print(f"    {shape:<25} {count:>4}  ({count/len(results)*100:.1f}%)")

    print(f"\n  SYSTEM C CANDIDATES (Zipfian):")
    print(f"  {'OKR':<10} {'SysClass':<10} {'Score':>6} {'Mean':>8} {'Max':>8} {'Cords':>6} {'Provenance'}")
    for r in sorted(zipfian_specimens, key=lambda x: x['max_val'], reverse=True)[:30]:
        print(f"  {r['okr_num']:<10} {r['classification']:<10} {r['score']:>6.2f} {r['mean_val']:>8.1f} {r['max_val']:>8} {r['cords']:>6} {r['provenance'][:40]}")

    print(f"\n  GAUSSIAN SPECIMENS:")
    print(f"  {'OKR':<10} {'SysClass':<10} {'Score':>6} {'Mean':>8} {'Max':>8} {'L%':>5} {'Fiber':<4} {'Provenance'}")
    for r in sorted(gaussian_specimens, key=lambda x: x['score'], reverse=True)[:15]:
        print(f"  {r['okr_num']:<10} {r['classification']:<10} {r['score']:>6.2f} {r['mean_val']:>8.1f} {r['max_val']:>8} {r['l_pct']:>5.1f} {r['fiber']:<4} {r['provenance'][:40]}")

    # Cross-tabulation
    print(f"\n  CROSS-TABULATION: System x Shape")
    shapes = sorted(shape_counts.keys())
    print(f"  {'':>15}", end='')
    for s in shapes: print(f" {s:>12}", end='')
    print(f" {'TOTAL':>8}")
    for sys_class in ['System_A', 'System_B', 'Mixed']:
        sys_r = [r for r in results if r['classification'] == sys_class]
        print(f"  {sys_class:>15}", end='')
        for s in shapes: print(f" {len([r for r in sys_r if r.get('shape') == s]):>12}", end='')
        print(f" {len(sys_r):>8}")

    # PHASE 3
    system_c = [r for r in results if r['classification'] == 'Mixed' and r.get('shape') == 'Zipfian']
    mixed_non_c = [r for r in mixed if r.get('shape') != 'Zipfian']
    zipf_on_a = [r for r in results if r['classification'] == 'System_A' and r.get('shape') == 'Zipfian']

    print(f"\n{'=' * 70}")
    print(f"PHASE 3: FINAL OKR DEMOGRAPHIC BREAKDOWN")
    print(f"{'=' * 70}")
    print(f"  System A  (Logistical/Warehouse):    {len(system_a):>4}  ({len(system_a)/len(results)*100:.1f}%)")
    print(f"  System B  (Demographic/Governor):     {len(system_b):>4}  ({len(system_b)/len(results)*100:.1f}%)")
    print(f"  System C  (Categorical/Codebook):     {len(system_c):>4}  ({len(system_c)/len(results)*100:.1f}%)  [Mixed + Zipfian]")
    print(f"  Mixed     (unresolved):               {len(mixed_non_c):>4}  ({len(mixed_non_c)/len(results)*100:.1f}%)")
    print(f"  {'─' * 45}")
    print(f"  TOTAL:                                {len(results):>4}")

    if system_c:
        print(f"\n  SYSTEM C SPECIMENS:")
        for r in system_c:
            print(f"    {r['okr_num']:<10} score={r['score']:>5.2f}  mean={r['mean_val']:.0f}  max={r['max_val']}  {r['provenance'][:40]}")

    if zipf_on_a:
        print(f"\n  ZIPFIAN ON SYSTEM A HARDWARE ({len(zipf_on_a)} specimens):")
        for r in sorted(zipf_on_a, key=lambda x: x['max_val'], reverse=True)[:20]:
            print(f"    {r['okr_num']:<10} score={r['score']:>5.2f}  mean={r['mean_val']:.0f}  max={r['max_val']}  fiber={r['fiber']}  {r['provenance'][:40]}")

    # SAVE FILES
    try:
        out_dir = os.path.dirname(os.path.dirname(os.path.abspath(db_path)))
        if not os.path.isdir(out_dir): out_dir = os.path.dirname(os.path.abspath(__file__))
    except:
        out_dir = '.'

    csv_path = os.path.join(out_dir, 'corpus_sweep_results.csv')
    md_path  = os.path.join(out_dir, 'corpus_sweep_summary.md')

    fieldnames = [
        'khipu_id', 'okr_num', 'classification', 'confidence', 'score', 'shape',
        'cords', 'pendants', 'subs', 'max_depth', 'n_colors',
        'fiber', 'fiber_pct', 's_pct', 'l_pct', 'e_pct',
        'mean_val', 'max_val', 'lk_pct', 'flags',
        'provenance', 'museum', 'investigator',
        'dim_fiber', 'dim_topology', 'dim_knot', 'dim_colour', 'dim_value', 'dim_beginning', 'n_dims'
    ]

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in results: writer.writerow(r)
    print(f"\n  CSV saved: {csv_path}")

    import datetime
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Corpus-Wide System Classification - OKR Demographic Census\n\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Corpus:** {len(results)} khipus, OKR SQLite database\n")
        f.write(f"**Method:** KARP Khipu Graph MCP v1.2.0 classifySystem() - Python port\n\n")
        f.write("## Classification Summary\n\n")
        f.write("| System | Count | % | Description |\n")
        f.write("|--------|------:|--:|-------------|\n")
        f.write(f"| System A | {len(system_a)} | {len(system_a)/len(results)*100:.1f}% | Logistical/Warehouse |\n")
        f.write(f"| System B | {len(system_b)} | {len(system_b)/len(results)*100:.1f}% | Demographic/Governor |\n")
        f.write(f"| System C | {len(system_c)} | {len(system_c)/len(results)*100:.1f}% | Categorical/Codebook |\n")
        f.write(f"| Mixed | {len(mixed_non_c)} | {len(mixed_non_c)/len(results)*100:.1f}% | Unresolved |\n")
        f.write(f"| **Total** | **{len(results)}** | **100%** | |\n\n")
        f.write("## Top System B Specimens\n\n")
        f.write("| OKR | Score | Confidence | Fiber | L% | Colors | Provenance |\n")
        f.write("|-----|------:|-----------|-------|---:|-------:|------------|\n")
        for r in system_b_sorted[:20]:
            f.write(f"| {r['okr_num']} | {r['score']:.2f} | {r['confidence']} | {r['fiber']} | {r['l_pct']:.0f}% | {r['n_colors']} | {r['provenance'][:50]} |\n")
        if system_c:
            f.write("\n## System C Specimens\n\n")
            f.write("| OKR | Score | Mean | Max | Provenance |\n")
            f.write("|-----|------:|-----:|----:|------------|\n")
            for r in system_c:
                f.write(f"| {r['okr_num']} | {r['score']:.2f} | {r['mean_val']:.0f} | {r['max_val']} | {r['provenance'][:50]} |\n")
        if zipf_on_a:
            f.write(f"\n## Zipfian on System A Hardware ({len(zipf_on_a)} specimens)\n\n")
            f.write("| OKR | Score | Mean | Max | Fiber | Provenance |\n")
            f.write("|-----|------:|-----:|----:|-------|------------|\n")
            for r in sorted(zipf_on_a, key=lambda x: x['max_val'], reverse=True)[:20]:
                f.write(f"| {r['okr_num']} | {r['score']:.2f} | {r['mean_val']:.0f} | {r['max_val']} | {r['fiber']} | {r['provenance'][:50]} |\n")
    print(f"  Summary saved: {md_path}")

    print(f"\n{'=' * 70}")
    print(f"SWEEP COMPLETE")
    print(f"{'=' * 70}")
    conn.close()

if __name__ == '__main__':
    main()

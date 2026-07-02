#!/usr/bin/env python3
"""
MDP KHIPU CORE ALGORITHM 3: Matched-Pair Network + Monte Carlo Validation
===========================================================================
Peer-review-ready implementation of the cross-site matched-pair detection
and null-hypothesis testing described in Paper IV §2.6–2.7, §3.6.

PURPOSE:
  Identify khipu pairs sharing 5+ sequential value matches at corresponding
  ordinal positions, map the resulting site-connection network, analyse
  formatting-direction (bidirectional data flow), and validate against a
  Monte Carlo null hypothesis (N=1000 random permutations).

MATCHED-PAIR ALGORITHM:
  For each pair of khipus (A, B) with ≥10 non-zero pendant values:
    1. Extract the first 50 non-zero pendant values in ordinal order
    2. Compare value sequences position-by-position
    3. If ≥5 values match at corresponding positions → flagged as a pair
    4. Record the formatting direction:
       - Count distinct colours on each khipu
       - Mono→Poly: fewer-colour khipu sends to richer-colour khipu
       - Poly→Mono: richer-colour khipu sends to fewer-colour khipu
       - Same: equal colour counts

MONTE CARLO NULL HYPOTHESIS (N=1000):
  1. Pool ALL cord values across the entire corpus
  2. For each iteration:
     a. Randomly redistribute pooled values into same-sized khipu containers
     b. Re-run the matched-pair algorithm on the randomised corpus
     c. Record the total number of pairs found
  3. If observed pairs > ALL null iterations → p < 0.001

REPRODUCING THIS ANALYSIS:
  Run: python mdp_matched_pairs.py [path_to_khipu.db]
  WARNING: Monte Carlo with N=1000 takes 10-30 minutes depending on hardware.
  Use --skip-monte-carlo for just the pair detection.

Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: July 2026
Paper: MDP IV — The Colour Alphabet of the Inca Empire
"""

import sqlite3
import sys
import os
import math
import csv
import random
from collections import defaultdict, Counter

DEFAULT_DB = r"C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\data\khipu.db"

# Matched-pair parameters
MIN_NON_ZERO_VALUES = 10   # minimum pendant values to include a khipu
MAX_COMPARE_VALUES = 50     # compare first N non-zero values
MIN_MATCHES = 5             # minimum sequential matches to flag a pair
MONTE_CARLO_N = 1000        # number of null iterations


def connect(db_path):
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def load_khipu_values(conn):
    """
    Load first MAX_COMPARE_VALUES non-zero pendant values per khipu.
    Returns dict: khipu_id → {values: [...], n_colours: int, provenance: str, okr: str}
    """
    rows = conn.execute("""
        SELECT c.KHIPU_ID, c.CORD_ORDINAL,
               COALESCE(cv.value, 0) as value,
               acc.COLOR_CD_1,
               km.PROVENANCE, km.OKR_NUM
        FROM cord c
        JOIN khipu_main km ON c.KHIPU_ID = km.KHIPU_ID
        LEFT JOIN ascher_cord_color acc
            ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        LEFT JOIN (
            SELECT CORD_ID, SUM(CASE
                WHEN TYPE_CODE='S' THEN knot_value_type
                WHEN TYPE_CODE='L' THEN NUM_TURNS
                WHEN TYPE_CODE='E' THEN 1 ELSE 0 END) as value
            FROM knot GROUP BY CORD_ID
        ) cv ON c.CORD_ID = cv.CORD_ID
        WHERE c.CORD_LEVEL = 1
        ORDER BY c.KHIPU_ID, c.CORD_ORDINAL
    """).fetchall()

    khipus = defaultdict(lambda: {'values': [], 'colours': set(), 'prov': '', 'okr': ''})

    for r in rows:
        kid = r['KHIPU_ID']
        val = int(r['value'] or 0)
        khipus[kid]['prov'] = r['PROVENANCE'] or ''
        khipus[kid]['okr'] = r['OKR_NUM'] or ''
        if r['COLOR_CD_1']:
            khipus[kid]['colours'].add(r['COLOR_CD_1'])
        if val > 0 and len(khipus[kid]['values']) < MAX_COMPARE_VALUES:
            khipus[kid]['values'].append(val)

    # Filter to khipus with enough values
    return {
        kid: {
            'values': d['values'],
            'n_colours': len(d['colours']),
            'prov': d['prov'],
            'okr': d['okr']
        }
        for kid, d in khipus.items()
        if len(d['values']) >= MIN_NON_ZERO_VALUES
    }


def find_matched_pairs(khipu_data):
    """
    Compare all khipu pairs for sequential value matches.
    Returns list of matched pairs with metadata.
    """
    kids = list(khipu_data.keys())
    pairs = []

    for i in range(len(kids)):
        for j in range(i + 1, len(kids)):
            a, b = kids[i], kids[j]
            va, vb = khipu_data[a]['values'], khipu_data[b]['values']
            min_len = min(len(va), len(vb))

            matches = sum(1 for k in range(min_len) if va[k] == vb[k])

            if matches >= MIN_MATCHES:
                ca = khipu_data[a]['n_colours']
                cb = khipu_data[b]['n_colours']

                if ca < cb:
                    direction = 'mono_to_poly'
                elif ca > cb:
                    direction = 'poly_to_mono'
                else:
                    direction = 'same'

                pa = khipu_data[a]['prov']
                pb = khipu_data[b]['prov']
                cross_site = pa != pb and pa and pb

                pairs.append({
                    'kid_a': a, 'kid_b': b,
                    'okr_a': khipu_data[a]['okr'], 'okr_b': khipu_data[b]['okr'],
                    'matches': matches, 'compared': min_len,
                    'prov_a': pa, 'prov_b': pb,
                    'cross_site': cross_site,
                    'direction': direction,
                    'colours_a': ca, 'colours_b': cb
                })

    return pairs


def monte_carlo_test(khipu_data, n_iterations=MONTE_CARLO_N):
    """
    Null hypothesis: randomly redistribute all values into same-sized containers.
    Returns observed count, null distribution, and p-value.
    """
    # Pool all values
    all_values = []
    sizes = []
    kids = list(khipu_data.keys())

    for kid in kids:
        vals = khipu_data[kid]['values']
        all_values.extend(vals)
        sizes.append(len(vals))

    observed_pairs = find_matched_pairs(khipu_data)
    observed_count = len(observed_pairs)

    null_counts = []
    for iteration in range(n_iterations):
        if (iteration + 1) % 100 == 0:
            print(f"    Monte Carlo iteration {iteration+1}/{n_iterations}...")

        # Shuffle all values randomly
        shuffled = all_values.copy()
        random.shuffle(shuffled)

        # Redistribute into same-sized containers
        null_data = {}
        offset = 0
        for i, kid in enumerate(kids):
            sz = sizes[i]
            null_data[kid] = {
                'values': shuffled[offset:offset + sz],
                'n_colours': khipu_data[kid]['n_colours'],
                'prov': khipu_data[kid]['prov'],
                'okr': khipu_data[kid]['okr']
            }
            offset += sz

        null_pairs = find_matched_pairs(null_data)
        null_counts.append(len(null_pairs))

    null_mean = sum(null_counts) / len(null_counts)
    null_max = max(null_counts)
    exceeds = sum(1 for nc in null_counts if nc >= observed_count)
    p_value = exceeds / n_iterations

    return {
        'observed': observed_count,
        'null_mean': round(null_mean, 1),
        'null_max': null_max,
        'ratio': round(observed_count / null_mean, 1) if null_mean > 0 else float('inf'),
        'p_value': p_value,
        'p_string': f"{p_value:.4f}" if p_value > 0 else "<0.001",
        'n_iterations': n_iterations,
        'exceeds_observed': exceeds
    }


def main():
    db_path = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_DB
    skip_mc = '--skip-monte-carlo' in sys.argv

    conn = connect(db_path)

    print(f"{'='*70}")
    print(f"MATCHED-PAIR NETWORK + MONTE CARLO VALIDATION")
    print(f"{'='*70}\n")

    # Load data
    print(f"  Loading khipu values...")
    data = load_khipu_values(conn)
    print(f"  Khipus with ≥{MIN_NON_ZERO_VALUES} non-zero values: {len(data)}")

    # Find pairs
    print(f"  Finding matched pairs (≥{MIN_MATCHES} sequential matches)...")
    pairs = find_matched_pairs(data)

    total = len(pairs)
    cross = sum(1 for p in pairs if p['cross_site'])
    same = total - cross

    print(f"\n  MATCHED PAIRS: {total}")
    print(f"    Cross-site: {cross}")
    print(f"    Same-site:  {same}")

    # Direction analysis
    dirs = Counter(p['direction'] for p in pairs)
    m2p = dirs.get('mono_to_poly', 0)
    p2m = dirs.get('poly_to_mono', 0)
    same_fmt = dirs.get('same', 0)

    print(f"\n  FORMATTING DIRECTION:")
    print(f"    Mono→Poly (receipts UP):     {m2p}")
    print(f"    Poly→Mono (quotas DOWN):     {p2m}")
    print(f"    Same formatting:             {same_fmt}")

    # Top routes
    routes = Counter()
    for p in pairs:
        if p['cross_site']:
            route = tuple(sorted([p['prov_a'], p['prov_b']]))
            routes[route] += 1

    print(f"\n  TOP CROSS-SITE ROUTES:")
    for route, count in routes.most_common(15):
        print(f"    {route[0][:25]:<25s} ↔ {route[1][:25]:<25s}  {count:>4} pairs")

    # Hub analysis
    hubs = Counter()
    for p in pairs:
        if p['cross_site']:
            if p['prov_a']: hubs[p['prov_a']] += 1
            if p['prov_b']: hubs[p['prov_b']] += 1

    print(f"\n  HUB SITES (most cross-site connections):")
    for site, count in hubs.most_common(10):
        print(f"    {site[:40]:<40s}  {count:>4} connections")

    # Monte Carlo
    if not skip_mc:
        print(f"\n  MONTE CARLO VALIDATION (N={MONTE_CARLO_N})...")
        mc = monte_carlo_test(data)
        print(f"\n  RESULTS:")
        print(f"    Observed pairs:   {mc['observed']}")
        print(f"    Null mean:        {mc['null_mean']}")
        print(f"    Null max:         {mc['null_max']}")
        print(f"    Ratio:            {mc['ratio']}×")
        print(f"    Exceeds observed: {mc['exceeds_observed']}/{mc['n_iterations']}")
        print(f"    p-value:          {mc['p_string']}")
    else:
        print(f"\n  Monte Carlo skipped (use without --skip-monte-carlo to run)")

    # Save
    try:
        out_dir = os.path.dirname(os.path.dirname(os.path.abspath(db_path)))
        if not os.path.isdir(out_dir): out_dir = '.'
    except:
        out_dir = '.'

    csv_path = os.path.join(out_dir, 'matched_pairs.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=[
            'okr_a', 'okr_b', 'matches', 'compared',
            'prov_a', 'prov_b', 'cross_site', 'direction',
            'colours_a', 'colours_b'
        ], extrasaction='ignore')
        w.writeheader()
        for p in pairs: w.writerow(p)

    print(f"\n  CSV: {csv_path}")
    print(f"{'='*70}")
    conn.close()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
MDP KHIPU CORE ALGORITHM 1: Shannon Entropy Colour Analysis
=============================================================
Peer-review-ready implementation of the colour entropy hierarchy
described in Paper IV §3.1.

PURPOSE:
  Quantify the information content of each colour in the OKR corpus,
  demonstrate the three-tier vowel/consonant hierarchy, and measure
  the information loss caused by the standard practice of collapsing
  compound colours to their primary component (COLOR_CD_1).

MATHEMATICAL FRAMEWORK:
  Given a corpus of N pendant cords, each assigned one of K distinct
  colours, the probability of colour c_i is:

      p(c_i) = count(c_i) / N

  The self-information (surprise) of a single occurrence of c_i is:

      I(c_i) = -log_2(p(c_i))  [bits]

  The corpus Shannon entropy is:

      H = -SUM_i  p(c_i) * log_2(p(c_i))  [bits]

  The maximum possible entropy for K colours is:

      H_max = log_2(K)  [bits]  (achieved when all colours are equally frequent)

  The entropy ratio H / H_max measures how evenly the palette is used.

  Information loss from collapsing compound colours:

      Delta_H = H(FULL_COLOR) - H(COLOR_CD_1)

TIER CLASSIFICATION THRESHOLDS:
  Vowel:        I(c) < 4 bits   — high-frequency structural colours
  Semi-vowel:   4 <= I(c) < 7   — moderate-frequency domain markers
  Consonant:    7 <= I(c) < 10  — low-frequency identifiers
  Rare consonant: I(c) >= 10    — maximum identifying power per occurrence

  Justification: These boundaries are empirical, chosen at natural gaps
  in the information-content distribution. The 4-bit boundary separates
  colours appearing on >1% of cords (W, AB, MB) from the rest. The 7-bit
  boundary separates colours with 50+ occurrences from those with <50.
  The 10-bit boundary isolates colours with <20 occurrences.

REPRODUCING THIS ANALYSIS:
  1. Download the OKR SQLite database from https://doi.org/10.5281/zenodo.18025748
  2. Place it at the path specified by OKR_PATH below (or pass as argument)
  3. Run: python mdp_entropy.py [path_to_khipu.db]
  4. No dependencies beyond Python 3.8+ standard library (sqlite3, math, csv)

Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: July 2026
Paper: MDP IV — The Colour Alphabet of the Inca Empire
"""

import sqlite3
import sys
import os
import math
import csv
from collections import defaultdict, Counter

# ════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════

DEFAULT_DB = r"C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\data\khipu.db"

# Tier boundaries (bits of information per occurrence)
TIER_VOWEL_MAX = 4.0       # < 4 bits = vowel
TIER_SEMIVOWEL_MAX = 7.0   # 4-7 bits = semi-vowel
TIER_CONSONANT_MAX = 10.0  # 7-10 bits = consonant
                            # >= 10 bits = rare consonant

# Motif search parameters
MIN_MOTIF_KHIPUS = 3        # minimum distinct khipus for a motif to qualify
MIN_ENTROPY_WEIGHT = 15.0   # minimum total entropy bits for name candidates
MIN_SITE_CONCENTRATION = 0.5  # >50% at one site = geographic cluster
MIN_VALUE_VARIANCE = 0.6    # >60% unique value tuples = categorical, not formulaic


def connect(db_path):
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ════════════════════════════════════════════════════
# MODULE 1: CORPUS ENTROPY COMPUTATION
# ════════════════════════════════════════════════════
# Computes Shannon entropy for both FULL_COLOR and COLOR_CD_1 palettes
# and quantifies the information loss from the standard collapse.

def compute_entropy(conn):
    """
    Returns:
        full_entropy: dict with corpus stats for FULL_COLOR palette
        cd1_entropy:  dict with corpus stats for COLOR_CD_1 palette
        colour_info:  dict mapping each FULL_COLOR to its information stats
    """
    # ── Count all pendant colours using FULL_COLOR ──
    # FULL_COLOR preserves compound notation:
    #   Barberpole (twisted): AB:W  = light brown twisted with white
    #   Stripe:               MB-KB = medium brown striped with dark brown
    #   Complex:              W*SR:SY:0G = multi-colour construction
    # COLOR_CD_1 collapses these to just the first component (AB, MB, W)

    rows = conn.execute("""
        SELECT acc.FULL_COLOR, COUNT(*) as n
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        WHERE c.CORD_LEVEL = 1
          AND acc.FULL_COLOR IS NOT NULL AND acc.FULL_COLOR != ''
        GROUP BY acc.FULL_COLOR
        ORDER BY n DESC
    """).fetchall()

    full_counts = {r['FULL_COLOR']: r['n'] for r in rows}
    full_total = sum(full_counts.values())
    n_full_colours = len(full_counts)

    # ── Shannon entropy: H = -SUM p(c) * log2(p(c)) ──
    full_H = -sum(
        (count / full_total) * math.log2(count / full_total)
        for count in full_counts.values()
    )
    full_H_max = math.log2(n_full_colours)

    # ── Per-colour information content ──
    colour_info = {}
    for colour, count in full_counts.items():
        p = count / full_total
        info_bits = -math.log2(p)

        if info_bits < TIER_VOWEL_MAX:
            tier = 'vowel'
        elif info_bits < TIER_SEMIVOWEL_MAX:
            tier = 'semi-vowel'
        elif info_bits < TIER_CONSONANT_MAX:
            tier = 'consonant'
        else:
            tier = 'rare-consonant'

        colour_info[colour] = {
            'count': count,
            'probability': p,
            'info_bits': info_bits,
            'tier': tier
        }

    # ── Repeat for COLOR_CD_1 ──
    rows_cd1 = conn.execute("""
        SELECT acc.COLOR_CD_1, COUNT(*) as n
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        WHERE c.CORD_LEVEL = 1
          AND acc.COLOR_CD_1 IS NOT NULL AND acc.COLOR_CD_1 != ''
        GROUP BY acc.COLOR_CD_1
        ORDER BY n DESC
    """).fetchall()

    cd1_counts = {r['COLOR_CD_1']: r['n'] for r in rows_cd1}
    cd1_total = sum(cd1_counts.values())
    n_cd1_colours = len(cd1_counts)

    cd1_H = -sum(
        (count / cd1_total) * math.log2(count / cd1_total)
        for count in cd1_counts.values()
    )
    cd1_H_max = math.log2(n_cd1_colours)

    # ── Information loss ──
    delta_H = full_H - cd1_H
    pct_loss = (delta_H / cd1_H) * 100  # as percentage of primary entropy

    full_entropy = {
        'total_cords': full_total,
        'n_colours': n_full_colours,
        'entropy': round(full_H, 3),
        'max_entropy': round(full_H_max, 3),
        'ratio': round(full_H / full_H_max * 100, 1)
    }

    cd1_entropy = {
        'total_cords': cd1_total,
        'n_colours': n_cd1_colours,
        'entropy': round(cd1_H, 3),
        'max_entropy': round(cd1_H_max, 3),
        'ratio': round(cd1_H / cd1_H_max * 100, 1)
    }

    return full_entropy, cd1_entropy, delta_H, pct_loss, colour_info


# ════════════════════════════════════════════════════
# MODULE 2: COLOUR-VALUE FUNCTIONAL TAXONOMY
# ════════════════════════════════════════════════════
# Tests whether each colour carries a characteristic value distribution,
# distinguishing formatting (100% zero), category labels (any value),
# and domain identifiers (bounded value ranges).

def colour_value_taxonomy(conn):
    """
    Returns list of dicts with per-colour value statistics.
    """
    rows = conn.execute("""
        SELECT acc.COLOR_CD_1,
               COALESCE(cv.value, 0) as value
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        LEFT JOIN (
            SELECT CORD_ID, SUM(CASE
                WHEN TYPE_CODE='S' THEN knot_value_type
                WHEN TYPE_CODE='L' THEN NUM_TURNS
                WHEN TYPE_CODE='E' THEN 1 ELSE 0 END) as value
            FROM knot GROUP BY CORD_ID
        ) cv ON c.CORD_ID = cv.CORD_ID
        WHERE c.CORD_LEVEL = 1
          AND acc.COLOR_CD_1 IS NOT NULL AND acc.COLOR_CD_1 != ''
    """).fetchall()

    colour_values = defaultdict(list)
    for r in rows:
        colour_values[r['COLOR_CD_1']].append(float(r['value']))

    results = []
    for colour, values in sorted(colour_values.items(), key=lambda x: len(x[1]), reverse=True):
        if len(values) < 20:
            continue

        non_zero = [v for v in values if v > 0]
        zero_pct = (len(values) - len(non_zero)) / len(values) * 100

        if non_zero:
            mean_val = sum(non_zero) / len(non_zero)
            sorted_nz = sorted(non_zero)
            median_val = sorted_nz[len(sorted_nz) // 2]
            max_val = sorted_nz[-1]
            std_val = math.sqrt(sum((v - mean_val) ** 2 for v in non_zero) / len(non_zero))
        else:
            mean_val = median_val = max_val = std_val = 0

        # Functional classification
        #   Formatting:  >85% zero-value — structural delimiters
        #   Domain ID:   characteristic bounded value range
        #   Category:    full range, high variance — column labels
        if zero_pct > 85:
            function = 'FORMATTING'
        elif mean_val > 500:
            function = 'COMMODITY'
        elif mean_val > 10 and max_val < 500:
            function = 'DEMOGRAPHIC'
        else:
            function = 'CATEGORY'

        results.append({
            'colour': colour, 'count': len(values),
            'zero_pct': round(zero_pct, 1),
            'mean': round(mean_val, 1), 'median': median_val,
            'max': max_val, 'std': round(std_val, 1),
            'function': function
        })

    return results


# ════════════════════════════════════════════════════
# MODULE 3: SITE-SPECIFIC COLOUR SIGNATURES
# ════════════════════════════════════════════════════
# Identifies colour n-grams that cluster geographically,
# weighted by entropy (information content).

def site_signatures(conn, colour_info):
    """
    Returns list of name candidate motifs with geographic concentration.
    """
    # Load pendant sequences with FULL_COLOR and values
    rows = conn.execute("""
        SELECT c.KHIPU_ID, km.OKR_NUM, km.PROVENANCE,
               c.CORD_ORDINAL, acc.FULL_COLOR,
               COALESCE(cv.value, 0) as value
        FROM cord c
        JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
        JOIN khipu_main km ON c.KHIPU_ID = km.KHIPU_ID
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

    # Group by khipu
    khipu_cords = defaultdict(list)
    khipu_meta = {}
    for r in rows:
        khipu_cords[r['KHIPU_ID']].append(
            (r['CORD_ORDINAL'], r['FULL_COLOR'] or '', float(r['value']))
        )
        khipu_meta[r['KHIPU_ID']] = (r['OKR_NUM'] or '', r['PROVENANCE'] or '')

    # Extract 3-gram and 4-gram motifs
    motif_instances = defaultdict(list)

    for kid, cords in khipu_cords.items():
        colours = [c[1] for c in cords]
        okr, prov = khipu_meta[kid]

        for n in [3, 4]:
            for i in range(len(colours) - n + 1):
                motif = tuple(colours[i:i + n])
                if '' in motif:
                    continue
                # Skip all-same vowel motifs (AB-AB-AB etc.)
                primaries = set(c.split(':')[0].split('-')[0] for c in motif)
                if len(primaries) == 1 and list(primaries)[0] in ('AB', 'MB', 'W'):
                    continue

                values = [cords[i + j][2] for j in range(n)]
                motif_instances[motif].append({
                    'kid': kid, 'okr': okr, 'prov': prov,
                    'ordinal': cords[i][0], 'values': values
                })

    # Score motifs
    name_candidates = []

    for motif, instances in motif_instances.items():
        unique_khipus = set(inst['kid'] for inst in instances)
        if len(unique_khipus) < MIN_MOTIF_KHIPUS:
            continue

        # Entropy weight = sum of per-colour information bits
        entropy_weight = sum(
            colour_info[c]['info_bits'] if c in colour_info else 12.0
            for c in motif
        )

        if entropy_weight < MIN_ENTROPY_WEIGHT:
            continue

        # Value variance ratio (unique tuples / total instances)
        value_tuples = [tuple(int(v) for v in inst['values']) for inst in instances]
        value_variance = len(set(value_tuples)) / len(instances)

        if value_variance < MIN_VALUE_VARIANCE:
            continue

        # Geographic concentration
        prov_counter = Counter(
            inst['prov'] for inst in instances if inst['prov']
        )
        if not prov_counter:
            continue

        top_site, top_count = prov_counter.most_common(1)[0]
        known = sum(1 for inst in instances if inst['prov'])
        concentration = top_count / known if known > 0 else 0

        if concentration >= MIN_SITE_CONCENTRATION:
            name_candidates.append({
                'motif': motif,
                'n_instances': len(instances),
                'n_khipus': len(unique_khipus),
                'entropy_weight': round(entropy_weight, 1),
                'value_variance': round(value_variance, 2),
                'top_site': top_site,
                'concentration': round(concentration * 100, 1),
            })

    name_candidates.sort(key=lambda x: x['entropy_weight'] * x['concentration'] / 100, reverse=True)
    return name_candidates


# ════════════════════════════════════════════════════
# MAIN — RUN ALL ANALYSES
# ════════════════════════════════════════════════════

def main():
    db_path = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_DB
    conn = connect(db_path)

    # ── ANALYSIS 1: Corpus Entropy ──
    print("=" * 70)
    print("ANALYSIS 1: SHANNON ENTROPY — COLOUR INFORMATION HIERARCHY")
    print("=" * 70)

    full_e, cd1_e, delta_H, pct_loss, colour_info = compute_entropy(conn)

    print(f"\n  FULL_COLOR palette:")
    print(f"    Pendant cords:     {full_e['total_cords']:,}")
    print(f"    Unique colours:    {full_e['n_colours']}")
    print(f"    Shannon entropy:   {full_e['entropy']:.3f} bits")
    print(f"    Max entropy:       {full_e['max_entropy']:.3f} bits")
    print(f"    Utilisation:       {full_e['ratio']:.1f}%")

    print(f"\n  COLOR_CD_1 palette (standard practice):")
    print(f"    Unique colours:    {cd1_e['n_colours']}")
    print(f"    Shannon entropy:   {cd1_e['entropy']:.3f} bits")

    print(f"\n  INFORMATION LOSS from collapsing compounds:")
    print(f"    Delta H:           {delta_H:.3f} bits")
    print(f"    Percentage lost:   {pct_loss:.1f}% of primary entropy")

    # Tier counts
    tiers = Counter(ci['tier'] for ci in colour_info.values())
    print(f"\n  TIER DISTRIBUTION ({full_e['n_colours']} colours):")
    for tier in ['vowel', 'semi-vowel', 'consonant', 'rare-consonant']:
        count = tiers.get(tier, 0)
        print(f"    {tier:<18s} {count:>4} colours")

    # Top colours per tier
    print(f"\n  {'Colour':<20s} {'Count':>7s} {'Prob':>7s} {'I(bits)':>8s} {'Tier':<15s}")
    print(f"  {'-'*62}")
    for colour, info in sorted(colour_info.items(), key=lambda x: x[1]['info_bits']):
        if info['count'] >= 5:
            print(f"  {colour:<20s} {info['count']:>7,} {info['probability']:>6.4f} "
                  f"{info['info_bits']:>7.2f}  {info['tier']:<15s}")

    # ── ANALYSIS 2: Colour-Value Taxonomy ──
    print(f"\n{'=' * 70}")
    print("ANALYSIS 2: COLOUR-VALUE FUNCTIONAL TAXONOMY")
    print("=" * 70)

    taxonomy = colour_value_taxonomy(conn)
    print(f"\n  {'Colour':<10s} {'Count':>7s} {'Zero%':>6s} {'Mean':>8s} {'Median':>8s} "
          f"{'Max':>8s} {'StdDev':>8s} {'Function':<12s}")
    print(f"  {'-'*78}")
    for t in taxonomy:
        print(f"  {t['colour']:<10s} {t['count']:>7,} {t['zero_pct']:>5.1f}% {t['mean']:>7.1f} "
              f"{t['median']:>7.0f} {t['max']:>7.0f} {t['std']:>7.1f}  {t['function']:<12s}")

    funcs = Counter(t['function'] for t in taxonomy)
    print(f"\n  FUNCTIONAL SUMMARY:")
    for func, count in funcs.most_common():
        colours = [t['colour'] for t in taxonomy if t['function'] == func]
        print(f"    {func}: {count} colours — {', '.join(colours[:8])}")

    # ── ANALYSIS 3: Site Signatures ──
    print(f"\n{'=' * 70}")
    print("ANALYSIS 3: SITE-SPECIFIC COLOUR SIGNATURES")
    print("=" * 70)

    candidates = site_signatures(conn, colour_info)
    print(f"\n  Name candidates (>{MIN_SITE_CONCENTRATION*100:.0f}% single-site, "
          f">{MIN_VALUE_VARIANCE*100:.0f}% value variance, "
          f">{MIN_ENTROPY_WEIGHT:.0f} bits entropy): {len(candidates)}")

    print(f"\n  {'Motif':<45s} {'Khipus':>6s} {'Entropy':>8s} {'ValVar':>6s} "
          f"{'Site':<25s} {'Conc%':>5s}")
    print(f"  {'-'*100}")
    for nc in candidates[:30]:
        motif_str = '-'.join(nc['motif'])
        print(f"  {motif_str:<45s} {nc['n_khipus']:>6} {nc['entropy_weight']:>7.1f} "
              f"{nc['value_variance']:>5.2f}  {nc['top_site'][:25]:<25s} {nc['concentration']:>4.0f}%")

    # ── Save Results ──
    try:
        out_dir = os.path.dirname(os.path.dirname(os.path.abspath(db_path)))
        if not os.path.isdir(out_dir):
            out_dir = os.path.dirname(os.path.abspath(__file__))
    except:
        out_dir = '.'

    # Entropy table CSV
    csv_path = os.path.join(out_dir, 'entropy_colour_table.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'colour', 'count', 'probability', 'info_bits', 'tier'
        ])
        writer.writeheader()
        for colour, info in sorted(colour_info.items(), key=lambda x: x[1]['info_bits']):
            writer.writerow({
                'colour': colour, 'count': info['count'],
                'probability': round(info['probability'], 6),
                'info_bits': round(info['info_bits'], 3),
                'tier': info['tier']
            })
    print(f"\n  Entropy table saved: {csv_path}")

    # Summary stats
    print(f"\n{'=' * 70}")
    print(f"PAPER IV KEY STATISTICS:")
    print(f"  Corpus entropy (FULL_COLOR):  {full_e['entropy']:.3f} bits")
    print(f"  Corpus entropy (COLOR_CD_1):  {cd1_e['entropy']:.3f} bits")
    print(f"  Information loss:             {delta_H:.3f} bits ({pct_loss:.1f}%)")
    print(f"  Unique FULL_COLORs:           {full_e['n_colours']}")
    print(f"  Unique COLOR_CD_1s:           {cd1_e['n_colours']}")
    print(f"  Site-specific name candidates: {len(candidates)}")
    print(f"{'=' * 70}")

    conn.close()


if __name__ == '__main__':
    main()

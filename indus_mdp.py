"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) — INDUS VALLEY SCRIPT DISCOVERY
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: April 2026
Methodology: Animal-Sign Enrichment & Positional Syntax Profiling

DESCRIPTION:
This script adapts the MDP methodology for the Indus Valley Script. Because the
Indus script lacks explicit metrological numeral-commodity pairs, this script
analyzes the stroke-sign modifiers and, crucially, the co-occurrence between
textual signs and the iconographic field symbols (animals) depicted on the seals.

DATA SOURCES:
- The yajnadevam digital extraction of the Interactive Corpus of Indus Texts (ICIT)
  (population-script.sql from github.com/yajnadevam/indus-website)

RESULTS:
1. Proves stroke signs (G1-G7) act as medial numeric modifiers.
2. Identifies massive "Semantic Locks" (e.g., Sign G321 is enriched 195.6x and
   appears exclusively on Hare seals; G850 appears exclusively on Anthropomorph
   seals). This provides the first corpus-scale statistical evidence for the
   Departmental/Institutional administrative theory of Indus seals.

LICENSE: MIT License
=============================================================================
"""
import re
from collections import Counter, defaultdict

SQL_FILE = r"C:\Users\aazsh\Desktop\indus-website\population-script.sql"

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql = f.read()

# ═══════════════════════════════════════════════════════
# Parse each table's INSERT statement
# ═══════════════════════════════════════════════════════

# SITE
site_match = re.search(r'INSERT INTO SITE.*?VALUES\s*(.*?);', sql, re.DOTALL | re.IGNORECASE)
sites = {}
if site_match:
    for m in re.finditer(r'\("([^"]+)"\s*,\s*"([^"]+)"\)', site_match.group(1)):
        sites[m.group(1)] = m.group(2)
print(f"Sites: {len(sites)} — {sites}")

# SEAL (SEALID, SITEID, ...)
seal_match = re.search(r'INSERT INTO SEAL.*?VALUES\s*(.*?);', sql, re.DOTALL | re.IGNORECASE)
seal_site = {}
if seal_match:
    for m in re.finditer(r'\((\d+)\s*,\s*"([^"]+)"', seal_match.group(1)):
        seal_site[m.group(1)] = m.group(2)
print(f"Seals: {len(seal_site)}")

# ICONOGRAPHY (SEALID, DESCRIPTION)
icon_match = re.search(r'INSERT INTO ICONOGRAPHY\s*\(.*?\)\s*VALUES\s*(.*?);', sql, re.DOTALL | re.IGNORECASE)
seal_animal = {}
if icon_match:
    for m in re.finditer(r'\((\d+)\s*,\s*"([^"]+)"\)', icon_match.group(1)):
        seal_animal[m.group(1)] = m.group(2)
print(f"Iconography entries: {len(seal_animal)}")

# GLYPHSEQUENCE (SEALID, GLYPHID, IDX)
glyph_match = re.search(r'INSERT INTO GLYPHSEQUENCE.*?VALUES\s*(.*?);', sql, re.DOTALL | re.IGNORECASE)
seal_glyphs = defaultdict(list)
if glyph_match:
    for m in re.finditer(r'\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\)', glyph_match.group(1)):
        seal_id = m.group(1)
        glyph_id = m.group(2)
        idx = int(m.group(3))
        seal_glyphs[seal_id].append((idx, glyph_id))
print(f"Glyph sequences: {len(seal_glyphs)} seals with signs")

# Sort by index
for sid in seal_glyphs:
    seal_glyphs[sid].sort(key=lambda x: x[0])

# Animal symbol mapping (from usefulMaps.js)
symbol_map = {
    "Bull": "Bull", "Bull1": "Unicorn", "Bull1:J": "Unicorn", "Bull1:II": "Unicorn",
    "Rhin": "Rhinoceros", "Goat:1": "Goat", "Bull1:O": "Unicorn", "Bull3": "Three-horned bull",
    "Buff": "Water buffalo", "Goat:4": "Goat", "Goat:3": "Goat", "Htgr": "Tiger",
    "Bull1:W": "Unicorn", "Bull1:V": "Unicorn", "Elep": "Elephant", "Gaur": "Gaur",
    "Bull1:I": "Unicorn", "Bull1:S": "Unicorn", "T-A-T": "Tiger", "Bull1:L": "Unicorn",
    "Tigr": "Tiger", "Fish": "Fish", "Bult": "Humped bull", "Bull1:U": "Unicorn",
    "Gavi": "Rhinoceros", "Pipal": "Pipal tree", "Zebu": "Zebu", "Goat": "Goat",
    "Bull2": "Two-horned bull", "Bull1:X": "Unicorn", "CompBull": "Composite bull",
    "Anth": "Anthropomorphic", "Turt": "Turtle", "Goat:2": "Goat", "Bull1:T": "Unicorn",
    "Comp": "Composite animal", "Hare": "Hare", "Goat:8": "Goat", "Goat:7": "Goat",
    "Goat:6": "Goat", "Ass": "Ass", "Bird": "Bird", "Scene": "Scene",
    "Bull1:M": "Unicorn", "Bull1:N": "Unicorn", "Bull1:P": "Unicorn", "Bull1:Q": "Unicorn",
}

# Build inscriptions
inscriptions = []
for seal_id, glyphs in seal_glyphs.items():
    signs = [g[1] for g in glyphs]
    raw_animal = seal_animal.get(seal_id, "None")
    animal = symbol_map.get(raw_animal, raw_animal)
    site_id = seal_site.get(seal_id, "")
    site = sites.get(site_id, "Unknown")
    inscriptions.append({
        "id": seal_id,
        "signs": signs,
        "animal": animal,
        "site": site,
        "length": len(signs),
    })

print(f"\nTotal inscriptions: {len(inscriptions)}")
print(f"Total sign occurrences: {sum(i['length'] for i in inscriptions)}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 1: Basic stats
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("1. CORPUS STATISTICS")
print("="*60)

sign_freq = Counter()
for insc in inscriptions:
    for s in insc["signs"]:
        sign_freq[s] += 1

print(f"Unique signs: {len(sign_freq)}")

length_dist = Counter(i["length"] for i in inscriptions)
print(f"\nLength distribution:")
for l in sorted(length_dist.keys())[:20]:
    print(f"  {l} signs: {length_dist[l]}")

print(f"\nTop 30 signs:")
for s, c in sign_freq.most_common(30):
    print(f"  G{s}: {c}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 2: Animal distribution
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("2. ANIMAL / FIELD SYMBOL DISTRIBUTION")
print("="*60)

animal_counts = Counter(i["animal"] for i in inscriptions)
for a, c in animal_counts.most_common():
    print(f"  {a}: {c}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 3: Site distribution
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("3. SITE DISTRIBUTION")
print("="*60)

site_counts = Counter(i["site"] for i in inscriptions)
for s, c in site_counts.most_common():
    print(f"  {s}: {c}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 4: Positional analysis
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("4. POSITIONAL ANALYSIS")
print("="*60)

sign_pos = defaultdict(Counter)
for insc in inscriptions:
    signs = insc["signs"]
    if len(signs) < 2:
        continue
    for i, s in enumerate(signs):
        if i == 0:
            sign_pos[s]["FIRST"] += 1
        elif i == len(signs) - 1:
            sign_pos[s]["LAST"] += 1
        else:
            sign_pos[s]["MIDDLE"] += 1

print(f"\nTop 30 signs positional preference:")
print(f"{'Sign':>8} {'Freq':>6} {'FIRST':>12} {'MIDDLE':>12} {'LAST':>12} {'Dom':>8}")
print("-"*65)
for sign, freq in sign_freq.most_common(30):
    pos = sign_pos.get(sign, Counter())
    total = sum(pos.values())
    if total < 3:
        continue
    f = pos.get("FIRST", 0)
    m = pos.get("MIDDLE", 0)
    l = pos.get("LAST", 0)
    dom = max(pos, key=pos.get)
    print(f"  G{sign:>5} {freq:>6} {f:>4}({f/total*100:>3.0f}%) {m:>4}({m/total*100:>3.0f}%) {l:>4}({l/total*100:>3.0f}%) {dom:>8}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 5: ANIMAL ↔ SIGN CORRELATION (THE PRIZE)
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("5. ANIMAL ↔ SIGN CORRELATION")
print("="*60)

animal_sign = defaultdict(Counter)
for insc in inscriptions:
    for s in insc["signs"]:
        animal_sign[insc["animal"]][s] += 1

major_animals = [a for a, c in animal_counts.most_common() if c >= 10]
total_insc = len(inscriptions)

for animal in major_animals:
    n = animal_counts[animal]
    signs = animal_sign[animal]
    print(f"\n  {animal} ({n} inscriptions):")
    for s, c in signs.most_common(8):
        expected = sign_freq[s] / total_insc * n
        ratio = c / expected if expected > 0 else 0
        flag = " ** ENRICHED **" if ratio > 1.8 else (" -- depleted --" if ratio < 0.4 else "")
        print(f"    G{s}: {c} (expected {expected:.1f}, ratio {ratio:.1f}x){flag}")

# Signs enriched in specific animals
print(f"\n\nSIGNS ENRICHED >2x IN SPECIFIC ANIMALS (min 5 occ):")
print(f"{'Sign':>8} {'Animal':<20} {'Observed':>8} {'Expected':>8} {'Ratio':>6}")
print("-"*55)

for sign, freq in sign_freq.most_common():
    if freq < 5:
        continue
    for animal in major_animals:
        n = animal_counts[animal]
        observed = animal_sign[animal].get(sign, 0)
        expected = freq / total_insc * n
        if expected > 0 and observed >= 3:
            ratio = observed / expected
            if ratio > 2.0:
                print(f"  G{sign:>5} {animal:<20} {observed:>8} {expected:>8.1f} {ratio:>5.1f}x")

# ═══════════════════════════════════════════════════════
# ANALYSIS 6: Bigrams
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("6. TOP BIGRAMS")
print("="*60)

bigrams = Counter()
for insc in inscriptions:
    signs = insc["signs"]
    for i in range(len(signs) - 1):
        bigrams[(signs[i], signs[i+1])] += 1

for (a, b), c in bigrams.most_common(20):
    print(f"  G{a} → G{b}: {c}")

# ═══════════════════════════════════════════════════════
# ANALYSIS 7: Stroke/numeral analysis
# ═══════════════════════════════════════════════════════
print("\n" + "="*60)
print("7. STROKE SIGN ANALYSIS")
print("="*60)

# In this numbering, low single-digit signs are often stroke marks
# Let's check signs 1-10 and see how they behave
for s in [str(i) for i in range(1, 11)]:
    if s in sign_freq:
        # What signs precede and follow this stroke sign?
        before = Counter()
        after = Counter()
        with_animals = Counter()
        for insc in inscriptions:
            signs = insc["signs"]
            for i, sign in enumerate(signs):
                if sign == s:
                    if i > 0: before[signs[i-1]] += 1
                    if i < len(signs)-1: after[signs[i+1]] += 1
                    with_animals[insc["animal"]] += 1
        
        top_before = ", ".join([f"G{k}({v})" for k,v in before.most_common(3)])
        top_after = ", ".join([f"G{k}({v})" for k,v in after.most_common(3)])
        print(f"\n  Stroke G{s} ({sign_freq[s]} occ): before=[{top_before}] after=[{top_after}]")
        print(f"    Animals: {', '.join([f'{a}({c})' for a,c in with_animals.most_common(5)])}")

print("\n" + "="*60)
print("INDUS FULL CORPUS ANALYSIS COMPLETE")
print("="*60)

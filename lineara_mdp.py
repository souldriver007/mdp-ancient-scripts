"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) — LINEAR A APPLICATION
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026
Methodology: Commodity-Ideogram Domain Profiling

DESCRIPTION:
This script applies the MDP methodology to the undeciphered Minoan Linear A
script. Unlike Proto-Elamite (which uses dedicated numeral system codes per
commodity domain) or Proto-Cuneiform (which requires subtractive sieve logic),
Linear A possesses explicit COMMODITY IDEOGRAMS — logograms like GRA (grain),
OLE (olive oil), VIN (wine), OLIV (olives), and FIC (figs) — that directly
label the commodity being counted. These ideograms function as domain anchors.

The MDP algorithm profiles every syllabic word (personal names, place names,
administrative terms) by which commodity ideograms it co-occurs with on the
same inscription. Words that appear exclusively or predominantly alongside
a specific commodity ideogram are classified into that commodity's administrative
domain.

Additionally, the script analyses:
- Fraction co-occurrence per commodity (Linear A's fractional system)
- Positional syntax (which words appear first/last on tablets)
- Site distribution (Hagia Triada vs other sites)
- Scribe attribution patterns
- Known administrative terms (KI-RO = deficit, KU-RO = total)

DATA SOURCES:
- LinearAInscriptions.js from the lineara.xyz corpus (mwenge/lineara.xyz)
  Based on GORILA (Godart & Olivier, Recueil des inscriptions en Linéaire A)
  and George Douros' tabulation.

LICENSE: MIT License
=============================================================================
"""

import json
import re
import os
from collections import Counter, defaultdict

# ═══════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════
JS_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\lineara.xyz-master\LinearAInscriptions.js"
OUT_DIR = r"C:\Users\aazsh\Desktop\Latest_MDP_research"

# ═══════════════════════════════════════════════════════
# COMMODITY IDEOGRAM DEFINITIONS
# Known Linear A logograms for commodities
# ═══════════════════════════════════════════════════════
COMMODITY_IDEOGRAMS = {
    # Primary commodities
    "GRA": "GRAIN",
    "OLE": "OLIVE_OIL",
    "VIN": "WINE",
    "OLIV": "OLIVES",
    "FIC": "FIGS",       # *120B sometimes identified as figs
    "AROM": "AROMATICS",
    "CYP": "CYPRESS/CONTAINER",
    "GAL": "GAL_MEASURE",
    "HIDE": "HIDES/LEATHER",
    "TELA": "TEXTILES",
    "CAP": "CAPRID/GOAT",
    # Person ideograms
    "VIR": "PERSON/MAN",
    "*21F": "WOMAN",
    "*22F": "WOMAN_2",
    "*21M": "MAN_TYPE",
    "*22M": "MAN_TYPE_2",
    "*23M": "MAN_TYPE_3",
}

# Compound commodity variants (OLE+A, OLE+U, VIN+SA, GRA+PA, etc.)
# These are sub-types of the parent commodity
COMMODITY_PARENT = {}  # Will be populated during parsing

# Known administrative terms
KNOWN_TERMS = {
    "KI-RO": "deficit/owed",
    "KU-RO": "total/sum",
    "PO-TO-KU-RO": "grand total",
    "KI-RE-TA-NA": "unknown (recurrent)",
    "KI-RE-TA₂-NA": "unknown (recurrent)",
    "A-DU": "unknown (recurrent)",
    "A-KA-RU": "unknown (recurrent)",
    "PA-I-TO": "Phaistos (place name)",
    "KU-DO-NI": "Kydonia (place name)",
    "SU-KI-RI-TA": "unknown (place name?)",
}

# ═══════════════════════════════════════════════════════
# STEP 1: PARSE LinearAInscriptions.js
# ═══════════════════════════════════════════════════════
print("=" * 70)
print("METROLOGICAL DOMAIN PROFILING — LINEAR A")
print("=" * 70)

print("\nStep 1: Parsing LinearAInscriptions.js...")

# The JS file is a Map constructor: var inscriptions = new Map([...])
# We need to extract the JSON-like array content
with open(JS_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

# Strip the JS wrapper to get the array of [key, value] pairs
# Remove 'var inscriptions = new Map(' prefix and ');' suffix
match = re.search(r'new Map\(\s*\[(.*)\]\s*\)\s*;?\s*$', raw, re.DOTALL)
if not match:
    print("ERROR: Could not parse JS Map structure")
    exit(1)

inner = match.group(1)

# Parse each inscription entry
# Format: ["ID", { ... }], ["ID", { ... }], ...
inscriptions = {}
# Use a robust approach: find each ["...",{ pattern
entry_pattern = re.compile(r'\["([^"]+)"\s*,\s*\{', re.DOTALL)
positions = [(m.start(), m.group(1)) for m in entry_pattern.finditer(raw)]

for i, (pos, name) in enumerate(positions):
    # Find the matching closing }]
    # Start from the opening brace
    brace_start = raw.index('{', pos)
    depth = 0
    j = brace_start
    while j < len(raw):
        if raw[j] == '{':
            depth += 1
        elif raw[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1

    obj_str = raw[brace_start:j + 1]
    try:
        obj = json.loads(obj_str)
        inscriptions[name] = obj
    except json.JSONDecodeError:
        # Try fixing common JS→JSON issues
        fixed = obj_str.replace("'", '"')
        try:
            obj = json.loads(fixed)
            inscriptions[name] = obj
        except:
            pass  # Skip unparseable entries

print(f"  Inscriptions parsed: {len(inscriptions)}")

# Count by site
site_counts = Counter()
support_counts = Counter()
for name, data in inscriptions.items():
    site_counts[data.get("site", "unknown")] += 1
    support_counts[data.get("support", "unknown")] += 1

print(f"\n  Inscriptions by site:")
for site, count in site_counts.most_common(15):
    print(f"    {site}: {count}")

print(f"\n  Inscriptions by support type:")
for sup, count in support_counts.most_common():
    print(f"    {sup}: {count}")

# ═══════════════════════════════════════════════════════
# STEP 2: TOKEN CLASSIFICATION
# Classify each token as WORD, NUMERAL, IDEOGRAM, FRACTION, or SEPARATOR
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 2: TOKEN CLASSIFICATION")
print("=" * 70)

def is_numeral(token):
    """Check if token is a pure number."""
    try:
        int(token)
        return True
    except ValueError:
        return False

def classify_token(token):
    """Classify a transliterated token."""
    if token == "\n":
        return "NEWLINE"
    if token in ("𐄁", "𐄀", "𐄂"):
        return "SEPARATOR"  # word dividers
    if is_numeral(token):
        return "NUMERAL"

    # Check for commodity ideograms (including compound forms)
    upper = token.upper()

    # Direct match
    if upper in COMMODITY_IDEOGRAMS:
        return "COMMODITY"

    # Compound commodity (e.g., OLE+U, OLE+A, VIN+SA, GRA+PA)
    if "+" in token:
        base = token.split("+")[0]
        if base.upper() in COMMODITY_IDEOGRAMS:
            return "COMMODITY"
        # Check if it's a known compound ideogram starting with commodity
        for key in COMMODITY_IDEOGRAMS:
            if token.upper().startswith(key + "+"):
                return "COMMODITY"

    # Fraction indicators
    if token in ("¹⁄₃", "¹⁄₂", "¹⁄₄", "¹⁄₅", "¹⁄₈", "¹⁄₆", "¹⁄₁₆",
                 "³⁄₄", "³⁄₈", "⅝", "6/10", "≈¹⁄₆", "≈¹⁄₄",
                 "B", "D", "E", "F", "H", "J", "K", "L", "L2", "L3",
                 "L4", "L6", "W", "X", "Y", "Ω",
                 "BB", "DD", "EE", "EF", "JE", "JB", "JF", "JH",
                 "JJ", "JK", "JL2", "KL2", "LL", "LL2", "L2L4",
                 "EB", "EJ", "EL2", "EL4", "EL6", "FK", "FL", "HK",
                 "BL6", "DDDD", "EYYY"):
        return "FRACTION"

    # Asterisk signs (*301, *304, etc.) - undeciphered ideograms
    if token.startswith("*"):
        return "IDEOGRAM_UNKNOWN"

    # Quoted translations like "owed", "olive oil" etc.
    if token.startswith('"') and token.endswith('"'):
        return "TRANSLATION"

    # Syllabic words (personal names, place names, admin terms)
    # These contain hyphens: A-KA-RU, KI-RO, QE-RA₂-U
    if "-" in token or token.replace("₂", "").replace("₃", "").isalpha():
        return "WORD"

    # Single syllabograms without hyphens
    if len(token) <= 4 and token.replace("₂", "").replace("₃", "").isalpha():
        return "WORD"

    return "OTHER"

def get_commodity_domain(token):
    """Extract the commodity domain from a commodity ideogram token."""
    upper = token.upper()
    if upper in COMMODITY_IDEOGRAMS:
        return COMMODITY_IDEOGRAMS[upper]

    # Compound: OLE+U → OLIVE_OIL, VIN+SA → WINE, GRA+PA → GRAIN
    if "+" in token:
        base = token.split("+")[0].upper()
        if base in COMMODITY_IDEOGRAMS:
            return COMMODITY_IDEOGRAMS[base]
    return "UNKNOWN"

# Process all inscriptions
all_words = Counter()
all_commodities = Counter()
all_fractions = Counter()
all_numerals = []
word_commodity_cooccurrence = defaultdict(Counter)  # word → {commodity_domain: count}
word_tablets = defaultdict(set)                      # word → set of tablet IDs
word_sites = defaultdict(Counter)                    # word → {site: count}
word_positions = defaultdict(Counter)                # word → {FIRST/LAST/MIDDLE: count}
word_numeral_adjacency = defaultdict(lambda: {"total": 0, "with_num": 0})
word_fraction_types = defaultdict(Counter)           # word → {fraction: count}
tablet_commodities = defaultdict(set)                # tablet → set of commodity domains
tablet_words = defaultdict(set)                      # tablet → set of words
commodity_numeral_values = defaultdict(list)          # commodity → [numeral values]
commodity_fraction_types = defaultdict(Counter)       # commodity → {fraction: count}
scribe_commodities = defaultdict(Counter)             # scribe → {commodity: count}

total_tokens = 0
tablets_with_data = 0

for tab_name, data in inscriptions.items():
    # Use transliteratedWords as primary data source
    tokens = data.get("transliteratedWords", [])
    if not tokens:
        continue

    tablets_with_data += 1
    site = data.get("site", "unknown")
    scribe = data.get("scribe", "")

    # Classify all tokens on this tablet
    words_on_tablet = []
    commodities_on_tablet = []
    numerals_on_tablet = []
    fractions_on_tablet = []
    lines = [[]]  # Track per-line tokens

    for token in tokens:
        if token == "\n":
            lines.append([])
            continue

        total_tokens += 1
        ttype = classify_token(token)

        if ttype == "WORD":
            words_on_tablet.append(token)
            lines[-1].append(("WORD", token))
            all_words[token] += 1
            word_tablets[token].add(tab_name)
            word_sites[token][site] += 1

        elif ttype == "COMMODITY":
            domain = get_commodity_domain(token)
            commodities_on_tablet.append(domain)
            all_commodities[token] += 1
            tablet_commodities[tab_name].add(domain)
            lines[-1].append(("COMMODITY", token, domain))
            if scribe:
                scribe_commodities[scribe][domain] += 1

        elif ttype == "NUMERAL":
            val = int(token)
            numerals_on_tablet.append(val)
            all_numerals.append(val)
            lines[-1].append(("NUMERAL", val))

        elif ttype == "FRACTION":
            fractions_on_tablet.append(token)
            all_fractions[token] += 1
            lines[-1].append(("FRACTION", token))

        elif ttype == "IDEOGRAM_UNKNOWN":
            lines[-1].append(("IDEOGRAM", token))

    # Record co-occurrences: which words appear on tablets with which commodities
    unique_commodities = set(commodities_on_tablet)
    unique_words = set(words_on_tablet)

    for word in unique_words:
        tablet_words[tab_name].add(word)
        has_num = len(numerals_on_tablet) > 0
        word_numeral_adjacency[word]["total"] += 1
        if has_num:
            word_numeral_adjacency[word]["with_num"] += 1

        for commodity in unique_commodities:
            word_commodity_cooccurrence[word][commodity] += 1

    # Record commodity → numeral associations (per line)
    for line_tokens in lines:
        line_commodities = [t[2] for t in line_tokens if t[0] == "COMMODITY"]
        line_numerals = [t[1] for t in line_tokens if t[0] == "NUMERAL"]
        line_fractions = [t[1] for t in line_tokens if t[0] == "FRACTION"]

        for com in set(line_commodities):
            for val in line_numerals:
                commodity_numeral_values[com].append(val)
            for frac in line_fractions:
                commodity_fraction_types[com][frac] += 1

    # Positional analysis (per line: first and last word)
    for line_tokens in lines:
        line_words = [t[1] for t in line_tokens if t[0] == "WORD"]
        if len(line_words) >= 2:
            word_positions[line_words[0]]["FIRST"] += 1
            word_positions[line_words[-1]]["LAST"] += 1
            for w in line_words[1:-1]:
                word_positions[w]["MIDDLE"] += 1
        elif len(line_words) == 1:
            word_positions[line_words[0]]["SOLE"] += 1

print(f"\n  Tablets with transliterated data: {tablets_with_data}")
print(f"  Total tokens processed: {total_tokens}")
print(f"  Unique syllabic words: {len(all_words)}")
print(f"  Unique commodity tokens: {len(all_commodities)}")
print(f"  Total numeral tokens: {len(all_numerals)}")
print(f"  Unique fractions: {len(all_fractions)}")

print(f"\n  Top 20 commodity ideograms:")
for com, count in all_commodities.most_common(20):
    print(f"    {com}: {count}")

print(f"\n  Top 20 syllabic words:")
for word, count in all_words.most_common(20):
    known = KNOWN_TERMS.get(word, "")
    marker = f" ← {known}" if known else ""
    print(f"    {word}: {count}{marker}")

# ═══════════════════════════════════════════════════════
# STEP 3: COMMODITY DOMAIN PROFILING
# The core MDP analysis — which words belong to which commodity domain
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 3: COMMODITY DOMAIN PROFILING (Core MDP)")
print("=" * 70)

print(f"\n{'Word':<22} {'Freq':>5} {'Tabs':>5} {'NumAdj%':>8} "
      f"{'GRAIN':>6} {'OIL':>6} {'WINE':>6} {'OLIV':>5} {'PERS':>5} {'Domain':<20}")
print("-" * 105)

domain_classifications = {}

for word, freq in all_words.most_common(150):
    if freq < 2:
        continue

    cooc = word_commodity_cooccurrence.get(word, Counter())
    n_tabs = len(word_tablets.get(word, set()))
    adj = word_numeral_adjacency.get(word, {"total": 0, "with_num": 0})
    adj_pct = adj["with_num"] / adj["total"] * 100 if adj["total"] > 0 else 0

    grain_ct = cooc.get("GRAIN", 0)
    oil_ct = cooc.get("OLIVE_OIL", 0)
    wine_ct = cooc.get("WINE", 0)
    olive_ct = cooc.get("OLIVES", 0)
    person_ct = cooc.get("PERSON/MAN", 0)

    total_cooc = sum(cooc.values())

    # Classification logic
    domain = "UNCLASSIFIED"

    if total_cooc == 0:
        # No commodity co-occurrence — pure syllabic (possibly header/admin)
        domain = "NO_COMMODITY_SIGNAL"
    else:
        # Calculate domain percentages
        grain_pct = grain_ct / total_cooc * 100 if total_cooc > 0 else 0
        oil_pct = oil_ct / total_cooc * 100 if total_cooc > 0 else 0
        wine_pct = wine_ct / total_cooc * 100 if total_cooc > 0 else 0
        olive_pct = olive_ct / total_cooc * 100 if total_cooc > 0 else 0
        person_pct = person_ct / total_cooc * 100 if total_cooc > 0 else 0

        # Dominant domain (>50% of co-occurrences)
        if grain_pct > 50:
            domain = "GRAIN_ADMIN"
        elif oil_pct > 50:
            domain = "OIL_ADMIN"
        elif wine_pct > 50:
            domain = "WINE_ADMIN"
        elif olive_pct > 50:
            domain = "OLIVE_ADMIN"
        elif person_pct > 50:
            domain = "PERSONNEL"
        elif total_cooc >= 3 and max(grain_pct, oil_pct, wine_pct, olive_pct) < 40:
            domain = "CROSS-COMMODITY"
        else:
            # Weak signal
            top_domain = max(cooc, key=cooc.get) if cooc else "?"
            domain = f"WEAK_{top_domain}"

    domain_classifications[word] = domain
    known = KNOWN_TERMS.get(word, "")
    marker = f" [{known}]" if known else ""

    print(f"  {word:<20} {freq:>5} {n_tabs:>5} {adj_pct:>7.0f}% "
          f"{grain_ct:>6} {oil_ct:>6} {wine_ct:>6} {olive_ct:>5} {person_ct:>5} {domain:<20}{marker}")

# ═══════════════════════════════════════════════════════
# STEP 4: COMMODITY ECONOMIC PARAMETERS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 4: COMMODITY ECONOMIC PARAMETERS")
print("=" * 70)

print(f"\n{'Commodity':<20} {'Count':>6} {'Median':>7} {'Mean':>7} {'Max':>6} {'Frac Types'}")
print("-" * 70)

for domain in ["GRAIN", "OLIVE_OIL", "WINE", "OLIVES", "PERSON/MAN",
                "AROMATICS", "CYPRESS/CONTAINER", "HIDES/LEATHER"]:
    vals = commodity_numeral_values.get(domain, [])
    fracs = commodity_fraction_types.get(domain, Counter())
    if vals:
        vals.sort()
        median = vals[len(vals) // 2]
        mean = sum(vals) / len(vals)
        frac_str = ", ".join(f"{f}:{c}" for f, c in fracs.most_common(5))
        print(f"  {domain:<18} {len(vals):>6} {median:>7} {mean:>7.1f} {max(vals):>6} {frac_str}")
    elif fracs:
        frac_str = ", ".join(f"{f}:{c}" for f, c in fracs.most_common(5))
        print(f"  {domain:<18}      0       -       -      - {frac_str}")

# ═══════════════════════════════════════════════════════
# STEP 5: POSITIONAL SYNTAX
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 5: POSITIONAL SYNTAX ANALYSIS")
print("=" * 70)

print(f"\nWords strongly preferring FIRST position (>50%, min 5 occ):")
for word in sorted(word_positions.keys(), key=lambda w: -all_words.get(w, 0)):
    pos = word_positions[word]
    total = sum(pos.values())
    if total >= 5 and pos.get("FIRST", 0) / total > 0.5:
        pct = pos["FIRST"] / total * 100
        known = KNOWN_TERMS.get(word, "")
        marker = f" ← {known}" if known else ""
        print(f"  {word}: {pos['FIRST']}/{total} ({pct:.0f}%) FIRST{marker}")

print(f"\nWords strongly preferring LAST position (>50%, min 5 occ):")
for word in sorted(word_positions.keys(), key=lambda w: -all_words.get(w, 0)):
    pos = word_positions[word]
    total = sum(pos.values())
    if total >= 5 and pos.get("LAST", 0) / total > 0.5:
        pct = pos["LAST"] / total * 100
        known = KNOWN_TERMS.get(word, "")
        marker = f" ← {known}" if known else ""
        print(f"  {word}: {pos['LAST']}/{total} ({pct:.0f}%) LAST{marker}")

# ═══════════════════════════════════════════════════════
# STEP 6: SCRIBE SPECIALISATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 6: SCRIBE COMMODITY SPECIALISATION")
print("=" * 70)

for scribe, commodities in sorted(scribe_commodities.items(),
                                    key=lambda x: -sum(x[1].values())):
    if not scribe or sum(commodities.values()) < 3:
        continue
    total = sum(commodities.values())
    top_commodity = max(commodities, key=commodities.get)
    top_pct = commodities[top_commodity] / total * 100

    specialisation = ""
    if top_pct > 70:
        specialisation = f"SPECIALIST: {top_commodity}"
    elif top_pct > 50:
        specialisation = f"LEANING: {top_commodity}"
    else:
        specialisation = "GENERALIST"

    com_str = ", ".join(f"{c}={n}" for c, n in commodities.most_common(4))
    print(f"  {scribe}: {total} records — {com_str} → {specialisation}")

# ═══════════════════════════════════════════════════════
# STEP 7: SITE DISTRIBUTION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 7: SITE-SPECIFIC VOCABULARY")
print("=" * 70)

# Words that appear predominantly at one site
print(f"\nWords appearing at 3+ tablets, >80% at a single site:")
for word in sorted(word_sites.keys(), key=lambda w: -all_words.get(w, 0)):
    sites = word_sites[word]
    total_tabs = len(word_tablets.get(word, set()))
    if total_tabs < 3:
        continue
    top_site = max(sites, key=sites.get)
    top_pct = sites[top_site] / sum(sites.values()) * 100
    if top_pct > 80:
        known = KNOWN_TERMS.get(word, "")
        marker = f" ← {known}" if known else ""
        print(f"  {word}: {sum(sites.values())} occ, {top_pct:.0f}% at {top_site}{marker}")

# ═══════════════════════════════════════════════════════
# STEP 8: FRACTION SYSTEM ANALYSIS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 8: FRACTION SYSTEM BY COMMODITY DOMAIN")
print("=" * 70)

print(f"\nDo different commodities use different fractional systems?")
print(f"(This is the Linear A equivalent of PE's metrological domain separation)\n")

for domain in ["GRAIN", "OLIVE_OIL", "WINE", "OLIVES", "AROMATICS"]:
    fracs = commodity_fraction_types.get(domain, Counter())
    if fracs:
        total_fracs = sum(fracs.values())
        print(f"  {domain} ({total_fracs} fractions):")
        for frac, count in fracs.most_common(10):
            print(f"    {frac}: {count} ({count/total_fracs*100:.0f}%)")
        print()

# ═══════════════════════════════════════════════════════
# STEP 9: DOMAIN SUMMARY & VALIDATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 9: DOMAIN CLASSIFICATION SUMMARY")
print("=" * 70)

domain_groups = defaultdict(list)
for word, domain in domain_classifications.items():
    domain_groups[domain].append((word, all_words[word]))

for domain in sorted(domain_groups.keys()):
    words = sorted(domain_groups[domain], key=lambda x: -x[1])
    print(f"\n  {domain} ({len(words)} words):")
    for w, f in words[:15]:
        known = KNOWN_TERMS.get(w, "")
        marker = f" [{known}]" if known else ""
        print(f"    {w}: {f}{marker}")

# ═══════════════════════════════════════════════════════
# STEP 10: VALIDATION AGAINST KNOWN TERMS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Step 10: VALIDATION — Known Linear A Administrative Terms")
print("=" * 70)

print(f"\n{'Term':<22} {'Meaning':<25} {'Domain Classification':<25} {'Co-occurs with'}")
print("-" * 90)

for term, meaning in KNOWN_TERMS.items():
    domain = domain_classifications.get(term, "NOT IN TOP 150")
    cooc = word_commodity_cooccurrence.get(term, Counter())
    cooc_str = ", ".join(f"{c}={n}" for c, n in cooc.most_common(4)) if cooc else "none"
    print(f"  {term:<20} {meaning:<25} {domain:<25} {cooc_str}")

# Final stats
print("\n" + "=" * 70)
print("LINEAR A MDP ANALYSIS COMPLETE")
print("=" * 70)
print(f"\n  Inscriptions analysed: {tablets_with_data}")
print(f"  Unique syllabic words: {len(all_words)}")
print(f"  Words classified: {len(domain_classifications)}")
print(f"  Domain breakdown:")
domain_summary = Counter(domain_classifications.values())
for d, c in domain_summary.most_common():
    print(f"    {d}: {c}")
print()

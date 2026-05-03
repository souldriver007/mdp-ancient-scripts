"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) — CRETAN HIEROGLYPHIC
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026
Methodology: Commodity-Ideogram Domain Profiling

DESCRIPTION:
Cretan Hieroglyphic (~2100-1700 BCE) is the grandmother of Linear A and
the great-grandmother of Linear B. It is completely undeciphered. This
script completes the Aegean Trilogy: Cretan Hieroglyphic → Linear A → Linear B.

The corpus is small (~317 inscriptions) but contains commodity ideograms
shared with Linear A (GRA, OLE, VIN, OVIS, LANA, AES) and numerals
(units, tens, hundreds, thousands). MDP should detect the same metrological
domain separation found in its descendants.

DATA SOURCES:
- CretanHieroInscriptions.js from linear0.xyz (mwenge/linear0.xyz)
  Based on CHIC (Corpus Hieroglyphicarum Inscriptionum Cretae, Olivier & Godart 1996)
- simpledictionary.js — lexicon with commodity translations

LICENSE: MIT License
=============================================================================
"""

import json
import re
from collections import Counter, defaultdict

# ═══════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════
JS_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\linear0.xyz-master\CretanHieroInscriptions.js"

# ═══════════════════════════════════════════════════════
# COMMODITY IDEOGRAM DEFINITIONS — Cretan Hieroglyphic
# Shared with Linear A / Linear B system
# ═══════════════════════════════════════════════════════
COMMODITY_MAP = {
    # Grain & agricultural
    "GRA": "GRAIN", "HORD": "GRAIN",
    "FAR": "FLOUR", "NI": "FIGS",
    # Olive/oil
    "OLE": "OIL", "OLIV": "OLIVES",
    # Wine
    "VIN": "WINE",
    # Livestock
    "OVIS": "LIVESTOCK", "OVIS:M": "LIVESTOCK", "OVIS:F": "LIVESTOCK",
    "OVIS:X": "LIVESTOCK", "OVIS+TA": "LIVESTOCK",
    "CAP": "LIVESTOCK", "CAP:M": "LIVESTOCK", "CAP:F": "LIVESTOCK",
    "CAP:X": "LIVESTOCK",
    "SUS": "LIVESTOCK", "SUS:M": "LIVESTOCK", "SUS:F": "LIVESTOCK",
    "SUS:X": "LIVESTOCK", "SUS+KA": "LIVESTOCK", "SUS+SI": "LIVESTOCK",
    "BOS": "LIVESTOCK", "BOS:M": "LIVESTOCK", "BOS:F": "LIVESTOCK",
    "BOS:X": "LIVESTOCK", "BOS+SI": "LIVESTOCK",
    "EQU": "LIVESTOCK", "EQU:M": "LIVESTOCK", "EQU:F": "LIVESTOCK",
    "CERV": "LIVESTOCK",
    # Wool & textiles
    "LANA": "WOOL",
    "TELA": "TEXTILES",
    # Metals
    "AES": "BRONZE", "AUR": "GOLD",
    # Spices & aromatics
    "CROC": "SPICE", "AROM": "SPICE", "KANAKO": "SPICE",
    "CYP": "SPICE", "PYC": "SPICE",
    # People
    "VIR": "PERSON", "MUL": "WOMAN",
    # Vessels & equipment
    "ROTA": "WHEEL", "BIG": "CHARIOT", "CUR": "CHARIOT",
    "CAPS": "CHARIOT",
    # Weapons
    "HAS": "WEAPON", "SAG": "WEAPON", "PUG": "WEAPON",
    # Vessels
    "TUN": "GARMENT",
    # Misc
    "CORN": "GRAIN", "LUNA": "CALENDAR",
    "ARB": "TREE", "ARM": "ARMOUR",
}

# Also catch compound commodities (TELA;1, OLE+A, etc.)
def get_domain(t):
    if t in COMMODITY_MAP:
        return COMMODITY_MAP[t]
    # Strip modifiers
    base = t.split("+")[0].split(":")[0].split(";")[0]
    if base in COMMODITY_MAP:
        return COMMODITY_MAP[base]
    # Check if starts with known commodity
    for key in COMMODITY_MAP:
        if t.startswith(key):
            return COMMODITY_MAP[key]
    return None

# Measure subunits
MEASURE_SUBUNITS = {"T": "DRY", "V": "DRY_2", "Z": "DRY_3",
                     "S": "LIQUID", "M": "WEIGHT", "N": "WEIGHT_2",
                     "P": "WEIGHT_3", "Q": "WEIGHT_4", "L": "WEIGHT_BASE"}

# Undeciphered ideograms (numbered signs like *155, *156, etc.)
# These are the Cretan Hieroglyphic equivalent of unknown signs

SKIP_TOKENS = {"X", "[", "]", "/", "\\n", "\n", "\r", "\r\n",
               "vacat", "vac.", "vest.", "deest", "VACAT", "DEEST",
               "⌜", "⌝", ".", ":", "|", "Α", "Β", "Γ", "Δ",
               "α", "β", "γ", "δ", "Λ", "ΛΔ", "ΛΘ", "Θ",
               "SIGILLUM", "SUPRA", "INFRA", "", "QS", "qs",
               "GRAFFITO", "FRAGMENTUM", "ANGUSTUM",
               "INF.", "SUP.", "LAT.", "SIN.", "DEX.",
               "PARS", "SINE", "REGULIS", "RELIQUA", "PRIOR",
               "SEPARATUM", "BIS", "DEEST?", "MUT.", "MUT",
               "MUTILA", "VEST.", "VESTIGIA", "DT"}

# ═══════════════════════════════════════════════════════
# PARSE CORPUS
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("METROLOGICAL DOMAIN PROFILING — CRETAN HIEROGLYPHIC")
print("The Grandmother of Linear A. The Aegean Trilogy Complete.")
print("=" * 75)

print("\nStep 0: Parsing corpus...")

with open(JS_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

entry_pattern = re.compile(r'\["([^"]+)",\s*\{', re.DOTALL)
positions_list = [(m.start(), m.group(1)) for m in entry_pattern.finditer(raw)]

inscriptions = {}
for i, (pos, name) in enumerate(positions_list):
    brace_start = raw.index('{', pos)
    depth = 0
    j = brace_start
    while j < len(raw):
        if raw[j] == '{': depth += 1
        elif raw[j] == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    try:
        obj = json.loads(raw[brace_start:j + 1])
        inscriptions[name] = obj
    except:
        pass

print(f"  Total inscriptions: {len(inscriptions)}")

# Count by site
site_counts = Counter()
for name, data in inscriptions.items():
    site_counts[data.get("site", "") or "unknown"] += 1
print(f"\n  Inscriptions by site:")
for site, count in site_counts.most_common(10):
    print(f"    {site}: {count}")

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def is_numeral(t):
    t = t.strip().rstrip("'").rstrip("?")
    try: int(t); return True
    except: return False

def get_numeral(t):
    t = t.strip().rstrip("'").rstrip("?")
    try: return int(t)
    except: return 0

def is_commodity(t):
    return get_domain(t) is not None

def is_measure(t):
    return t in MEASURE_SUBUNITS

def is_skip(t):
    if not t or not t.strip(): return True
    t = t.strip()
    if t in SKIP_TOKENS: return True
    if t.startswith("SIGILLUM"): return True
    if t in ("VAC.", "VAC..", "VEST.?", "V.", "V.→", "V.↓",
             "V.↗", "V.↓?", "INF.?", "SUP.?", "MUT.?",
             "VEST.??", "VESTIGIA?"): return True
    return False

def is_word(t):
    if not t or not t.strip(): return False
    t = t.strip()
    if is_numeral(t) or is_commodity(t) or is_measure(t) or is_skip(t):
        return False
    # Cretan Hieroglyphic signs: uppercase syllables with hyphens or numbered signs
    # Words: sequences like "RA₃-TA-RO", "KO-RO₃", "*152", etc.
    if t.startswith("*") and any(c.isdigit() for c in t):
        return True  # Undeciphered numbered sign
    if any(c.isalpha() for c in t) and t[0] != "\n":
        return True
    return False

def split_lines(tokens):
    lines = [[]]
    for t in tokens:
        if t in ("\n", "\r\n", "\r"):
            lines.append([])
        else:
            lines[-1].append(t)
    return [l for l in lines if l]

# ═══════════════════════════════════════════════════════
# STEP 1: TOKEN CLASSIFICATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 1: TOKEN CLASSIFICATION")
print("=" * 75)

word_freq = Counter()
commodity_freq = Counter()
measure_freq = Counter()
numeral_count = 0
word_commodity = defaultdict(Counter)
word_tablets = defaultdict(set)
word_numadj = defaultdict(lambda: {"total": 0, "with_num": 0})
commodity_numerals = defaultdict(list)
commodity_measures = defaultdict(Counter)
tablet_words = defaultdict(set)
tablet_comms = defaultdict(set)
total_tokens = 0
tablets_with_commodities = 0
tablets_with_numerals = 0

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    if not tokens: continue

    site = data.get("site", "") or "unknown"
    lines = split_lines(tokens)
    tab_has_comm = False
    tab_has_num = False
    tab_w = set()
    tab_c = set()

    for line in lines:
        line_words = []
        line_comms = []
        line_nums = []
        line_measures = []

        for t in line:
            if not t: continue
            t = t.strip()
            if not t: continue
            total_tokens += 1

            if is_numeral(t):
                numeral_count += 1
                line_nums.append(get_numeral(t))
                tab_has_num = True
            elif is_commodity(t):
                domain = get_domain(t)
                commodity_freq[t] += 1
                line_comms.append(domain)
                tab_c.add(domain)
                tab_has_comm = True
            elif is_measure(t):
                measure_freq[t] += 1
                line_measures.append(t)
            elif is_word(t):
                word_freq[t] += 1
                word_tablets[t].add(tab_name)
                line_words.append(t)
                tab_w.add(t)

        has_num = len(line_nums) > 0
        for w in set(line_words):
            word_numadj[w]["total"] += 1
            if has_num:
                word_numadj[w]["with_num"] += 1

        for com in set(line_comms):
            for val in line_nums:
                commodity_numerals[com].append(val)
            for ms in line_measures:
                commodity_measures[com][ms] += 1

    for w in tab_w:
        for c in tab_c:
            word_commodity[w][c] += 1
    tablet_words[tab_name] = tab_w
    tablet_comms[tab_name] = tab_c

    if tab_has_comm: tablets_with_commodities += 1
    if tab_has_num: tablets_with_numerals += 1

print(f"\n  Total tokens: {total_tokens}")
print(f"  Unique words/signs: {len(word_freq)}")
print(f"  Numeral tokens: {numeral_count}")
print(f"  Commodity tokens: {sum(commodity_freq.values())}")
print(f"  Tablets with commodities: {tablets_with_commodities}/{len(inscriptions)}")
print(f"  Tablets with numerals: {tablets_with_numerals}/{len(inscriptions)}")

print(f"\n  Top 20 commodity ideograms:")
for com, count in commodity_freq.most_common(20):
    domain = get_domain(com)
    print(f"    {com}: {count} → {domain}")

print(f"\n  Top 30 words/signs:")
for word, count in word_freq.most_common(30):
    n_tabs = len(word_tablets.get(word, set()))
    adj = word_numadj.get(word, {"total": 0, "with_num": 0})
    adj_pct = adj["with_num"] / adj["total"] * 100 if adj["total"] > 0 else 0
    print(f"    {word}: {count} (tabs={n_tabs}, numAdj={adj_pct:.0f}%)")

print(f"\n  Measure subunits:")
for m, count in measure_freq.most_common():
    print(f"    {m}: {count}")

# ═══════════════════════════════════════════════════════
# STEP 2: CORE MDP — COMMODITY DOMAIN PROFILING
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 2: CORE MDP — SIGN-COMMODITY DOMAIN PROFILING")
print("=" * 75)

print(f"\n  {'Sign':<30} {'Freq':>4} {'Tabs':>4} {'NumA%':>5} "
      f"{'GRA':>4} {'OIL':>4} {'LIV':>4} {'WOL':>4} {'WNE':>4} {'PER':>4} {'BRZ':>4} {'Domain'}")
print("  " + "-" * 105)

domain_classifications = {}

for word, freq in word_freq.most_common(100):
    if freq < 2: continue

    cooc = word_commodity.get(word, Counter())
    n_tabs = len(word_tablets.get(word, set()))
    adj = word_numadj.get(word, {"total": 0, "with_num": 0})
    adj_pct = adj["with_num"] / adj["total"] * 100 if adj["total"] > 0 else 0

    grain = cooc.get("GRAIN", 0)
    oil = cooc.get("OIL", 0)
    livestock = cooc.get("LIVESTOCK", 0)
    wool = cooc.get("WOOL", 0)
    wine = cooc.get("WINE", 0)
    person = cooc.get("PERSON", 0)
    bronze = cooc.get("BRONZE", 0)

    total_cooc = sum(cooc.values())
    domain = "UNCLASSIFIED"
    if total_cooc == 0:
        domain = "NO_COMMODITY"
    else:
        pcts = {k: v / total_cooc * 100 for k, v in cooc.items()}
        top_domain = max(cooc, key=cooc.get)
        top_pct = pcts[top_domain]
        if top_pct > 60:
            domain = top_domain
        elif top_pct > 40:
            domain = f"LEANING_{top_domain}"
        elif total_cooc >= 3 and top_pct < 35:
            domain = "CROSS-COMMODITY"
        else:
            domain = f"WEAK_{top_domain}"

    domain_classifications[word] = domain

    print(f"  {word:<28} {freq:>4} {n_tabs:>4} {adj_pct:>4.0f}% "
          f"{grain:>4} {oil:>4} {livestock:>4} {wool:>4} {wine:>4} {person:>4} {bronze:>4} {domain}")

# ═══════════════════════════════════════════════════════
# STEP 3: COMMODITY ECONOMIC PARAMETERS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 3: COMMODITY ECONOMIC PARAMETERS")
print("=" * 75)

print(f"\n  {'Domain':<16} {'Count':>6} {'Median':>7} {'Mean':>7} {'Max':>7} {'Measures'}")
print("  " + "-" * 65)

for domain in ["GRAIN", "OIL", "WINE", "OLIVES", "LIVESTOCK", "WOOL",
                "TEXTILES", "BRONZE", "GOLD", "SPICE", "FLOUR",
                "PERSON", "WOMAN", "GARMENT", "WEAPON", "CHARIOT"]:
    vals = commodity_numerals.get(domain, [])
    measures = commodity_measures.get(domain, Counter())
    if vals:
        vals.sort()
        med = vals[len(vals)//2]
        mean = sum(vals)/len(vals)
        m_str = ", ".join(f"{m}:{c}" for m, c in measures.most_common(5))
        print(f"  {domain:<14} {len(vals):>6} {med:>7} {mean:>7.1f} {max(vals):>7} {m_str}")
    elif measures:
        m_str = ", ".join(f"{m}:{c}" for m, c in measures.most_common(5))
        print(f"  {domain:<14}      0       -       -       - {m_str}")

# ═══════════════════════════════════════════════════════
# STEP 4: MEASURE SUBUNIT DOMAIN DIVERGENCE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 4: MEASURE SUBUNIT DOMAIN DIVERGENCE")
print("=" * 75)

print(f"\n  Do Cretan Hieroglyphic commodities use different measurement systems?")
print(f"  (Same question asked of Linear A and Linear B — does the pattern hold?)\n")

for domain in ["GRAIN", "OIL", "WINE", "LIVESTOCK", "WOOL", "TEXTILES",
                "BRONZE", "GOLD", "SPICE", "FLOUR"]:
    measures = commodity_measures.get(domain, Counter())
    if not measures: continue
    total_m = sum(measures.values())
    print(f"  {domain} ({total_m} measure tokens):")
    for m, count in measures.most_common(8):
        bar = "█" * int(count / total_m * 30)
        print(f"    {m:<4} {count:>4} ({count/total_m*100:>4.0f}%) {bar}")
    print()

# ═══════════════════════════════════════════════════════
# STEP 5: UNDECIPHERED NUMBERED SIGNS (*NNN)
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("STEP 5: UNDECIPHERED NUMBERED SIGNS (*NNN)")
print("=" * 75)

star_signs = {w: f for w, f in word_freq.items()
              if w.startswith("*") and any(c.isdigit() for c in w)}

print(f"\n  Numbered signs (undeciphered ideograms): {len(star_signs)}")
for sign in sorted(star_signs.keys(), key=lambda s: -star_signs[s]):
    freq = star_signs[sign]
    cooc = word_commodity.get(sign, Counter())
    adj = word_numadj.get(sign, {"total": 0, "with_num": 0})
    adj_pct = adj["with_num"] / adj["total"] * 100 if adj["total"] > 0 else 0
    domain = domain_classifications.get(sign, "?")

    cooc_str = ", ".join(f"{d}={n}" for d, n in cooc.most_common(3)) if cooc else "none"
    print(f"  {sign:<12} freq={freq:>3}, numAdj={adj_pct:>3.0f}%, "
          f"co-occurs: {cooc_str} → {domain}")

# ═══════════════════════════════════════════════════════
# STEP 6: LINEAR A COGNATE COMPARISON
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 6: LINEAR A COGNATE COMPARISON")
print("=" * 75)

# Words that appear in both Cretan Hieroglyphic AND Linear A
linear_a_top_words = {
    "A-TA-I-*301-WA-JA": "libation formula",
    "KU-RO": "total (Linear A)",
    "PO-TO-KU-RO": "grand total (Linear A)",
    "A-KA-RU": "heading sign (Linear A)",
    "KI-RO": "deficit (Linear A)",
    "SA-RO": "? (Linear A)",
    "JA": "frequent sign",
    "A-JA": "? (Linear A)",
    "KO": "? (Linear A)",
    "TA": "? (Linear A)",
    "RO": "? (Linear A)",
}

print(f"\n  Signs shared with Linear A (potential cognates):")
for word, la_note in linear_a_top_words.items():
    ch_freq = word_freq.get(word, 0)
    if ch_freq > 0:
        domain = domain_classifications.get(word, "?")
        print(f"    {word}: CH freq={ch_freq}, LA note='{la_note}', CH domain={domain}")

# Check for any overlapping vocabulary
ch_words = set(word_freq.keys())
la_vocab = {"JA", "SA", "RO", "RI", "NA", "TI", "RE", "MA", "KU", "KO",
            "WA", "TA", "RU", "RA", "KI", "ZE", "TU", "TE", "QE", "DE",
            "WI", "SI", "NE", "MI", "KA", "DO", "AI", "A", "I", "NWA"}
shared = ch_words & la_vocab
print(f"\n  Syllabic signs shared with Linear A: {len(shared)}")
print(f"    {', '.join(sorted(shared))}")

# ═══════════════════════════════════════════════════════
# STEP 7: SUMMATION CHECKING
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 7: SUMMATION CHECKING")
print("=" * 75)

exact_sums = 0
close_sums = 0
checked = 0

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    lines = split_lines(tokens)

    # Collect all numerals per line
    line_values = []
    for line in lines:
        nums = [get_numeral(t) for t in line if is_numeral(t.strip())]
        if nums:
            line_values.append(sum(nums))

    if len(line_values) >= 3:
        checked += 1
        last = line_values[-1]
        others = sum(line_values[:-1])
        if others > 0 and last == others:
            exact_sums += 1
        elif others > 0 and abs(last - others) <= 2:
            close_sums += 1

print(f"\n  Tablets with 3+ lines of numerals: {checked}")
print(f"  Last line = sum of others (exact): {exact_sums}")
print(f"  Close matches (±2): {close_sums}")
if checked > 0:
    print(f"  Sum match rate: {(exact_sums + close_sums)/checked*100:.1f}%")

# ═══════════════════════════════════════════════════════
# STEP 8: DOMAIN CLASSIFICATION SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 8: DOMAIN CLASSIFICATION SUMMARY")
print("=" * 75)

domain_groups = defaultdict(list)
for word, domain in domain_classifications.items():
    domain_groups[domain].append((word, word_freq[word]))

for domain in sorted(domain_groups.keys(), key=lambda d: -len(domain_groups[d])):
    words = sorted(domain_groups[domain], key=lambda x: -x[1])
    print(f"\n  {domain} ({len(words)} signs):")
    for w, f in words[:8]:
        print(f"    {w}: {f}")

# ═══════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("CRETAN HIEROGLYPHIC MDP ANALYSIS — COMPLETE")
print("=" * 75)

print(f"\n  CORPUS:")
print(f"    Inscriptions: {len(inscriptions)}")
print(f"    With commodities: {tablets_with_commodities}")
print(f"    With numerals: {tablets_with_numerals}")
print(f"    Unique signs: {len(word_freq)}")
print(f"    Commodity types found: {len(commodity_freq)}")

print(f"\n  MDP RESULTS:")
print(f"    Signs classified: {len(domain_classifications)}")
domain_summary = Counter(domain_classifications.values())
for d, c in domain_summary.most_common():
    print(f"      {d}: {c}")

print(f"\n  AEGEAN TRILOGY STATUS:")
print(f"    Cretan Hieroglyphic (~2100 BCE) ← YOU ARE HERE")
print(f"    Linear A (~1800 BCE) ← Done (120 words classified)")
print(f"    Linear B (~1400 BCE) ← Done (functional ontology proof)")
print(f"\n  Three generations. One method. One universal principle.")
print()

"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) — LINEAR B CONTROL VALIDATION
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026
Methodology: Commodity-Ideogram Domain Profiling (Deciphered Control)

DESCRIPTION:
This script applies the identical MDP methodology used on Linear A to the
DECIPHERED Linear B corpus. Because Linear B is Mycenaean Greek (deciphered
1952 by Michael Ventris), every word has a known translation. This provides
the ultimate validation: if MDP classifies 'si-to' into GRAIN, we verify
that sitos = Greek for wheat/grain. If it classifies 'e-ra-wo' into OIL,
we verify elaiwon = olive oil.

The corpus also has pre-tagged tablet categories (Lists of Personnel,
Livestock, Agricultural Produce) from the groups.js file, providing a
second ground-truth validation layer.

DATA FORMAT:
Linear B uses the same JS Map format as Linear A (same developer, Rob Hogan).
Key differences:
- translatedWords contains English translations of Mycenaean Greek
- Commodity ideograms: GRA (wheat), HORD (barley), OLE (oil), VIN (wine),
  OLIV (olives), LANA (wool), OVIS (sheep), BOS (ox), EQU (horse),
  AES (bronze), AUR (gold), FAR (flour), CROC (saffron), AROM (spice)
- Measure subunits: T, V, Z (dry), S (liquid) appear as separate tokens
- Damage markers: [ ] for lacunae
- Tablet series letters encode content type (D=livestock, E=land/grain,
  F=oil, G=spice, K=vessels, L=textiles, etc.)

DATA SOURCES:
- LinearBInscriptions.js from linearb.xyz (mwenge/linearb.xyz)
  Based on CALIBRA (Cambridge) and Younger/Douros tabulations.
- groups.js — pre-tagged tablet categories for validation.

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
JS_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\linearb.xyz-master\LinearBInscriptions.js"
GROUPS_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\linearb.xyz-master\groups.js"
LEXICON_FILE = r"C:\Users\aazsh\Desktop\Latest_MDP_research\linearb.xyz-master\lexicon.js"

# ═══════════════════════════════════════════════════════
# COMMODITY IDEOGRAM DEFINITIONS — Linear B
# These appear in the transliteratedWords field
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
    "OVIS": "LIVESTOCK", "OVIS:m": "LIVESTOCK", "OVIS:f": "LIVESTOCK",
    "OVIS:x": "LIVESTOCK",
    "CAP": "LIVESTOCK", "CAP:m": "LIVESTOCK", "CAP:f": "LIVESTOCK",
    "SUS": "LIVESTOCK", "SUS:m": "LIVESTOCK", "SUS:f": "LIVESTOCK",
    "BOS": "LIVESTOCK", "BOS:m": "LIVESTOCK", "BOS:f": "LIVESTOCK",
    "EQU": "LIVESTOCK", "EQU:m": "LIVESTOCK", "EQU:f": "LIVESTOCK",
    # Wool & textiles
    "LANA": "WOOL", "TELA": "TEXTILES",
    # Metals
    "AES": "BRONZE", "AUR": "GOLD",
    # Spices & aromatics
    "CROC": "SPICE", "AROM": "SPICE",
    # People
    "VIR": "PERSON", "MUL": "WOMAN",
    # Vessels & equipment
    "CYP": "VESSEL", "PYC": "VESSEL",
    # Military / transport
    "ROTA": "WHEEL", "ROTA+TE": "WHEEL",
    "CAPSUS": "CHARIOT_BODY",
    # Misc commodities
    "MERI": "HONEY", "AREPA": "UNGUENT",
}

# Known Linear B words with their Mycenaean Greek meaning
# These are our validation targets
KNOWN_WORDS = {
    "si-to": ("sitos", "wheat/grain"),
    "si-to-po-ti-ni-ja": ("sitopotnia", "grain goddess"),
    "ki-ri-ta": ("kritha", "barley"),
    "e-ra-wo": ("elaiwon", "olive oil"),
    "e-ra-wa": ("elaia", "olive"),
    "wo-no": ("woinos", "wine"),
    "me-ri": ("meli", "honey"),
    "ka-ko": ("khalkos", "bronze"),
    "ku-ru-so": ("khrusos", "gold"),
    "ko-wo": ("korwos", "boy/youth"),
    "ko-wa": ("korwa", "girl/youth"),
    "pa-te": ("pater", "father"),
    "do-e-ro": ("doelos", "slave/servant"),
    "do-e-ra": ("doela", "female slave"),
    "po-me": ("poimen", "shepherd"),
    "su-qo-ta": ("subotas", "swineherd"),
    "a-re-pa": ("aleiphar", "unguent/oil"),
    "to-so": ("toson", "so much/total"),
    "to-sa": ("tosa", "so much (fem.)"),
    "o-pe-ro": ("ophelos", "deficit/owed"),
    "pa-ro": ("paro", "from/at (the place of)"),
    "o-pi": ("opi", "over/for"),
    "re-u-ko": ("leukos", "white"),
    "e-re-pa-te": ("elephanteios", "of ivory"),
    "ka-na-pe-u": ("knapheus", "fuller"),
    "ke-ra-me-u": ("kerameus", "potter"),
    "ka-ke-u": ("khalkeus", "bronze-smith"),
    "to-ko-do-mo": ("toikhodomoi", "builders"),
    "pi-ri-e-te-re": ("pristeres", "sawyers"),
    "i-je-re-ja": ("hiereia", "priestess"),
    "wa-na-ka": ("wanax", "king"),
    "ra-wa-ke-ta": ("lawagetas", "army leader"),
    "te-re-ta": ("telestai", "land holders"),
    "ko-re-te": ("koreter", "mayor/governor"),
    "po-ro-ko-re-te": ("prokoreter", "deputy governor"),
    "da-mo": ("damos", "district/people"),
    "pa-i-to": ("Phaistos", "Phaistos"),
    "ko-no-so": ("Knossos", "Knossos"),
    "pu-ro": ("Pylos", "Pylos"),
    "a-mi-ni-so": ("Amnisos", "Amnisos"),
}

# Measure subunits — these indicate the fractional measurement system
MEASURE_SUBUNITS = {
    # Dry measures
    "T": "DRY_1", "V": "DRY_2", "Z": "DRY_3",
    # Liquid measures
    "S": "LIQUID_1",
    # Weight measures
    "M": "WEIGHT_1", "N": "WEIGHT_2", "P": "WEIGHT_3", "Q": "WEIGHT_4",
}

# Damage/structural markers to skip
SKIP_TOKENS = {"[", "]", "/", "vacat", "vac.", "vest.", "mut.", "deest",
               "VACAT", "DEEST", "SUPRA", "INFRA", "SIGILLUM",
               "⌜", "⌝", "Α", "Β", "α", "β", "γ", "δ",
               "\r", "\r\n", "qs", "QS"}

# ═══════════════════════════════════════════════════════
# PARSE CORPUS
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("METROLOGICAL DOMAIN PROFILING — LINEAR B CONTROL VALIDATION")
print("=" * 75)

print("\nStep 0: Parsing corpus...")

with open(JS_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

entry_pattern = re.compile(r'\[\s*"([^"]+)"\s*,\s*\{', re.DOTALL)
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
        inscriptions[name] = json.loads(raw[brace_start:j + 1])
    except:
        pass

print(f"  Total inscriptions: {len(inscriptions)}")

# Parse groups.js for ground-truth categories
ground_truth = {}
try:
    with open(GROUPS_FILE, "r", encoding="utf-8") as f:
        groups_raw = f.read()
    for m in re.finditer(r'\["([^"]+)",\s*"([^"]+)"\]', groups_raw):
        ground_truth[m.group(1)] = m.group(2)
    print(f"  Ground truth categories loaded: {len(ground_truth)}")
except:
    print("  WARNING: groups.js not found — no ground truth validation")

# Count by site
site_counts = Counter()
for name, data in inscriptions.items():
    site_counts[data.get("site", "unknown")] += 1
print(f"\n  Inscriptions by site:")
for site, count in site_counts.most_common(10):
    print(f"    {site}: {count}")

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def is_numeral(t):
    try: int(t); return True
    except: return False

def is_commodity(t):
    if not t: return False
    # Check direct match
    if t in COMMODITY_MAP: return True
    # Check compound (OLIV+A, OVIS:m, etc.)
    base = t.split("+")[0].split(":")[0]
    return base in COMMODITY_MAP

def get_domain(t):
    if t in COMMODITY_MAP: return COMMODITY_MAP[t]
    base = t.split("+")[0].split(":")[0]
    return COMMODITY_MAP.get(base, "UNKNOWN")

def is_measure(t):
    return t in MEASURE_SUBUNITS

def is_skip(t):
    if not t: return True
    if t in SKIP_TOKENS: return True
    if t.startswith("*") and len(t) < 6 and not "-" in t: return True
    return False

def is_word(t):
    if not t or t in ("\n", "\r", "\r\n"): return False
    if is_numeral(t) or is_commodity(t) or is_measure(t) or is_skip(t): return False
    # Linear B words are lowercase with hyphens: si-to, e-ra-wo, pa-i-to
    if t[0].islower() or (t[0] == "-" and len(t) > 1):
        return True
    return False

def split_lines(tokens):
    lines = [[]]
    for t in tokens:
        if t in ("\n", "\r\n"):
            lines.append([])
        else:
            lines[-1].append(t)
    return [l for l in lines if l]

# ═══════════════════════════════════════════════════════
# STEP 1: TOKEN CLASSIFICATION & CORPUS STATISTICS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 1: CORPUS STATISTICS")
print("=" * 75)

word_freq = Counter()
commodity_freq = Counter()
measure_freq = Counter()
word_commodity = defaultdict(Counter)
word_tablets = defaultdict(set)
word_sites = defaultdict(Counter)
word_numadj = defaultdict(lambda: {"total": 0, "with_num": 0})
word_measures = defaultdict(Counter)
commodity_numerals = defaultdict(list)
commodity_measures = defaultdict(Counter)
scribe_commodities = defaultdict(Counter)
tablet_words = defaultdict(set)
tablet_comms = defaultdict(set)

total_tokens = 0
tablets_with_data = 0

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    if not tokens: continue
    tablets_with_data += 1

    site = data.get("site", "unknown")
    scribe = data.get("scribe", "")
    lines = split_lines(tokens)

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

            if is_word(t):
                word_freq[t] += 1
                word_tablets[t].add(tab_name)
                word_sites[t][site] += 1
                line_words.append(t)
                tab_w.add(t)

            elif is_commodity(t):
                domain = get_domain(t)
                commodity_freq[t] += 1
                line_comms.append(domain)
                tab_c.add(domain)
                if scribe:
                    scribe_commodities[scribe][domain] += 1

            elif is_numeral(t):
                line_nums.append(int(t))

            elif is_measure(t):
                line_measures.append(t)
                measure_freq[t] += 1

        has_num = len(line_nums) > 0
        for w in set(line_words):
            word_numadj[w]["total"] += 1
            if has_num:
                word_numadj[w]["with_num"] += 1

        # Commodity → numeral / measure recording
        for com in set(line_comms):
            for val in line_nums:
                commodity_numerals[com].append(val)
            for ms in line_measures:
                commodity_measures[com][ms] += 1

    # Tablet-level co-occurrence
    for w in tab_w:
        for c in tab_c:
            word_commodity[w][c] += 1
    tablet_words[tab_name] = tab_w
    tablet_comms[tab_name] = tab_c

print(f"\n  Tablets with data: {tablets_with_data}")
print(f"  Total tokens: {total_tokens}")
print(f"  Unique words: {len(word_freq)}")
print(f"  Unique commodity tokens: {len(commodity_freq)}")

print(f"\n  Top 25 commodity ideograms:")
for com, count in commodity_freq.most_common(25):
    domain = get_domain(com)
    print(f"    {com}: {count} → {domain}")

print(f"\n  Top 30 words:")
for word, count in word_freq.most_common(30):
    known = KNOWN_WORDS.get(word, None)
    marker = f" ← {known[0]} ({known[1]})" if known else ""
    print(f"    {word}: {count}{marker}")

# ═══════════════════════════════════════════════════════
# STEP 2: CORE MDP — COMMODITY DOMAIN PROFILING
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 2: CORE MDP — COMMODITY DOMAIN PROFILING")
print("=" * 75)

print(f"\n  {'Word':<24} {'Freq':>5} {'Tabs':>4} {'NumA%':>6} "
      f"{'GRA':>4} {'OIL':>4} {'LIV':>4} {'WOL':>4} {'WNE':>4} {'PER':>4} {'BRZ':>4} {'Domain':<20} {'Validation'}")
print("  " + "-" * 125)

domain_classifications = {}

for word, freq in word_freq.most_common(200):
    if freq < 3: continue

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

    # Classification
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
        elif total_cooc >= 5 and top_pct < 35:
            domain = "CROSS-COMMODITY"
        else:
            domain = f"WEAK_{top_domain}"

    domain_classifications[word] = domain

    # Validation against known Greek
    known = KNOWN_WORDS.get(word, None)
    if known:
        greek, meaning = known
        # Check if MDP domain matches known meaning
        if "grain" in meaning.lower() or "wheat" in meaning.lower() or "barley" in meaning.lower():
            expected = "GRAIN"
        elif "oil" in meaning.lower() or "olive" in meaning.lower() or "unguent" in meaning.lower():
            expected = "OIL"
        elif "wine" in meaning.lower():
            expected = "WINE"
        elif "bronze" in meaning.lower():
            expected = "BRONZE"
        elif "gold" in meaning.lower():
            expected = "GOLD"
        elif "shepherd" in meaning.lower() or "swineherd" in meaning.lower():
            expected = "LIVESTOCK"
        elif "slave" in meaning.lower() or "boy" in meaning.lower() or "girl" in meaning.lower():
            expected = "PERSON"
        elif "total" in meaning.lower() or "deficit" in meaning.lower():
            expected = "CROSS-COMMODITY"
        elif "builder" in meaning.lower() or "potter" in meaning.lower() or "fuller" in meaning.lower() or "smith" in meaning.lower():
            expected = "TRADES"
        else:
            expected = "?"

        match = "✓" if expected in domain or domain in expected else "~" if expected == "?" else "✗"
        validation = f"{match} {greek}={meaning} (exp:{expected})"
    else:
        validation = ""

    print(f"  {word:<22} {freq:>5} {n_tabs:>4} {adj_pct:>5.0f}% "
          f"{grain:>4} {oil:>4} {livestock:>4} {wool:>4} {wine:>4} {person:>4} {bronze:>4} "
          f"{domain:<20} {validation}")


# ═══════════════════════════════════════════════════════
# STEP 3: GROUND TRUTH VALIDATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 3: GROUND TRUTH VALIDATION (groups.js categories)")
print("=" * 75)

# For each ground-truth category, check what MDP domains the tablet's words got
category_domain_matches = defaultdict(Counter)
category_counts = Counter()

for tab_name, category in ground_truth.items():
    if tab_name not in tablet_words: continue
    category_counts[category] += 1
    for word in tablet_words[tab_name]:
        dom = domain_classifications.get(word, None)
        if dom:
            category_domain_matches[category][dom] += 1

print(f"\n  Do MDP domain classifications match pre-tagged tablet categories?\n")
for category in sorted(category_counts.keys(), key=lambda c: -category_counts[c]):
    count = category_counts[category]
    domains = category_domain_matches[category]
    total_d = sum(domains.values())
    top3 = ", ".join(f"{d}={n}" for d, n in domains.most_common(5))
    print(f"  {category} ({count} tablets): {top3}")


# ═══════════════════════════════════════════════════════
# STEP 4: COMMODITY ECONOMIC PARAMETERS
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 4: COMMODITY ECONOMIC PARAMETERS")
print("=" * 75)

print(f"\n  {'Domain':<20} {'Count':>6} {'Median':>7} {'Mean':>7} {'Max':>7} {'Measures'}")
print("  " + "-" * 70)

for domain in ["GRAIN", "OIL", "WINE", "OLIVES", "LIVESTOCK", "WOOL",
                "BRONZE", "GOLD", "SPICE", "FLOUR", "PERSON", "WOMAN"]:
    vals = commodity_numerals.get(domain, [])
    measures = commodity_measures.get(domain, Counter())
    if vals:
        vals.sort()
        med = vals[len(vals)//2]
        mean = sum(vals)/len(vals)
        m_str = ", ".join(f"{m}:{c}" for m, c in measures.most_common(5))
        print(f"  {domain:<18} {len(vals):>6} {med:>7} {mean:>7.1f} {max(vals):>7} {m_str}")

# ═══════════════════════════════════════════════════════
# STEP 5: MEASURE SUBUNIT DOMAIN DIVERGENCE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 5: MEASURE SUBUNIT DOMAIN DIVERGENCE")
print("=" * 75)

print(f"\n  Do different commodities use different measurement subunits?")
print(f"  (T/V/Z = dry measures, S = liquid, M/N/P = weight)\n")

for domain in ["GRAIN", "OIL", "WINE", "OLIVES", "LIVESTOCK", "WOOL",
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
# STEP 6: KNOWN WORDS VALIDATION SUMMARY
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("STEP 6: KNOWN MYCENAEAN GREEK WORDS — VALIDATION")
print("=" * 75)

matches = 0
mismatches = 0
not_found = 0

print(f"\n  {'Word':<22} {'Greek':<16} {'Meaning':<22} {'MDP Domain':<22} {'Match'}")
print("  " + "-" * 95)

for word, (greek, meaning) in sorted(KNOWN_WORDS.items(), key=lambda x: -word_freq.get(x[0], 0)):
    domain = domain_classifications.get(word, "NOT CLASSIFIED")

    # Determine expected domain
    ml = meaning.lower()
    if any(w in ml for w in ["wheat", "grain", "barley"]):
        expected = "GRAIN"
    elif any(w in ml for w in ["oil", "olive", "unguent"]):
        expected = "OIL"
    elif "wine" in ml:
        expected = "WINE"
    elif "bronze" in ml:
        expected = "BRONZE"
    elif "gold" in ml:
        expected = "GOLD"
    elif any(w in ml for w in ["shepherd", "swineherd"]):
        expected = "LIVESTOCK"
    elif any(w in ml for w in ["slave", "servant", "boy", "girl"]):
        expected = "PERSON"
    elif any(w in ml for w in ["total", "deficit", "from", "over"]):
        expected = "CROSS-COMMODITY"
    elif any(w in ml for w in ["builder", "sawyer", "potter", "fuller", "smith"]):
        expected = "TRADES"
    elif any(w in ml for w in ["priestess", "goddess", "king", "leader"]):
        expected = "ADMIN/RELIGIOUS"
    elif any(w in ml for w in ["place", "phaistos", "knossos", "pylos", "amnisos"]):
        expected = "PLACE_NAME"
    else:
        expected = "?"

    if domain == "NOT CLASSIFIED":
        match = "— (not in top 200)"
        not_found += 1
    elif expected == "?":
        match = "? (no clear expected)"
    elif expected in domain or domain.replace("LEANING_", "").replace("WEAK_", "") == expected:
        match = "✓ CORRECT"
        matches += 1
    elif domain == "CROSS-COMMODITY" and expected in ("CROSS-COMMODITY", "ADMIN/RELIGIOUS", "PLACE_NAME"):
        match = "✓ CORRECT (admin)"
        matches += 1
    else:
        match = f"✗ (expected {expected})"
        mismatches += 1

    print(f"  {word:<20} {greek:<16} {meaning:<22} {domain:<22} {match}")

total_tested = matches + mismatches
accuracy = matches / total_tested * 100 if total_tested > 0 else 0
print(f"\n  VALIDATION: {matches}/{total_tested} correct ({accuracy:.0f}%)")
print(f"  Not in top 200 words: {not_found}")


# ═══════════════════════════════════════════════════════
# STEP 7: SCRIBE SPECIALISATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 7: SCRIBE SPECIALISATION")
print("=" * 75)

for scribe, comms in sorted(scribe_commodities.items(), key=lambda x: -sum(x[1].values())):
    if not scribe or sum(comms.values()) < 5: continue
    total = sum(comms.values())
    top = comms.most_common(1)[0]
    top_pct = top[1] / total * 100

    if top_pct > 70: spec = f"SPECIALIST: {top[0]}"
    elif top_pct > 50: spec = f"LEANING: {top[0]}"
    else: spec = "GENERALIST"

    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(5))
    print(f"  {scribe}: {total} records — {comm_str} → {spec}")


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
    print(f"\n  {domain} ({len(words)} words):")
    for w, f in words[:10]:
        known = KNOWN_WORDS.get(w, None)
        marker = f" ← {known[0]} ({known[1]})" if known else ""
        print(f"    {w}: {f}{marker}")


# ═══════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("LINEAR B MDP CONTROL VALIDATION — COMPLETE")
print("=" * 75)
print(f"\n  CORPUS:")
print(f"    Inscriptions: {len(inscriptions)}")
print(f"    With data: {tablets_with_data}")
print(f"    Unique words: {len(word_freq)}")
print(f"    Commodity tokens: {len(commodity_freq)}")
print(f"\n  MDP RESULTS:")
print(f"    Words classified: {len(domain_classifications)}")
domain_summary = Counter(domain_classifications.values())
for d, c in domain_summary.most_common():
    print(f"      {d}: {c}")
print(f"\n  VALIDATION:")
print(f"    Known Greek words tested: {matches + mismatches}")
print(f"    Correct: {matches} ({accuracy:.0f}%)")
print(f"    Mismatched: {mismatches}")
print(f"    Not in top 200: {not_found}")
print()

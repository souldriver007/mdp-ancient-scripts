"""
=============================================================================
METROLOGICAL DOMAIN PROFILING (MDP) V2 — LINEAR A MASTER ANALYSIS
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026
Methodology: Commodity-Ideogram Domain Profiling (Tablet-Filtered)

DESCRIPTION:
Master V2 analysis of the Minoan Linear A corpus. Incorporates all findings
from the initial MDP pass and the Deep Snoop exploration:

KEY V2 IMPROVEMENTS:
1. REGISTER SEPARATION: Splits corpus into Tablets (ledgers), Nodules (cargo
   stamps), Roundels, and Ritual (stone vessels). Only Tablets are used for
   the core MDP commodity profiling — nodule data contaminated V1.
2. TABLET-LEVEL POSITION: Checks whether KU-RO/KI-RO appear on LAST line
   (summation position) vs middle (section subtotals).
3. SUMMATION VERIFICATION: Mathematically validates accounting by checking
   whether line items sum to KU-RO values.
4. LEDGER LINE GRAMMAR: Extracts the syntactic template of each line
   (WORD→COMMODITY→NUMBER patterns).
5. COMMODITY SUB-TYPE PROFILING: OLE+U vs OLE+MI vs OLE+DI — different oil
   types with different quantity ranges and different administrative personnel.
6. ROOM/FINDSPOT SPECIALISATION: Maps commodity domains to physical rooms.
7. SCRIBE SPECIALISATION: Which scribes handle which commodities.
8. FRACTION DOMAIN DIVERGENCE: Proves different commodities use different
   fractional systems (the Linear A equivalent of PE's metrological separation).
9. NODULE STAMP ANALYSIS: Separate analysis of single-syllable cargo stamps.
10. CHRONOLOGICAL PROFILING: LMIA vs LMIB commodity shifts.

DATA SOURCES:
- LinearAInscriptions.js from the lineara.xyz corpus (mwenge/lineara.xyz)
  Based on GORILA (Godart & Olivier) and George Douros' tabulation.

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
# COMMODITY / CLASSIFICATION DEFINITIONS
# ═══════════════════════════════════════════════════════
COMMODITY_BASES = {
    "GRA": "GRAIN", "OLE": "OLIVE_OIL", "VIN": "WINE", "OLIV": "OLIVES",
    "FIC": "FIGS", "AROM": "AROMATICS", "CYP": "CYPRESS/CONTAINER",
    "GAL": "GAL_MEASURE", "HIDE": "HIDES/LEATHER", "TELA": "TEXTILES",
    "CAP": "CAPRID/GOAT", "VIR": "PERSON/MAN",
    "*21F": "WOMAN", "*22F": "WOMAN_2", "*21M": "MAN_TYPE",
    "*22M": "MAN_TYPE_2", "*23M": "MAN_TYPE_3",
}

KNOWN_TERMS = {
    "KI-RO": "deficit/owed", "KU-RO": "total/sum",
    "PO-TO-KU-RO": "grand total",
    "KI-RE-TA-NA": "recurrent (place?)", "KI-RE-TA₂-NA": "recurrent",
    "A-DU": "recurrent", "A-KA-RU": "recurrent (heading?)",
    "PA-I-TO": "Phaistos (place)", "KU-DO-NI": "Kydonia (place)",
    "SU-KI-RI-TA": "place name?", "SA-RA₂": "recurrent",
    "DA-ME": "grain admin", "MI-NU-TE": "grain admin",
    "KU-NI-SU": "grain admin", "DI-NA-U": "wine admin",
    "JE-DI": "oil admin", "DA-RE": "personnel",
    "A-TA-I-*301-WA-JA": "libation formula",
    "JA-SA-SA-RA-ME": "libation formula",
    "I-PI-NA-MA": "libation formula", "SI-RU-TE": "libation formula",
}

FRACTION_TOKENS = {
    "¹⁄₃", "¹⁄₂", "¹⁄₄", "¹⁄₅", "¹⁄₈", "¹⁄₆", "¹⁄₁₆",
    "³⁄₄", "³⁄₈", "⅝", "6/10", "≈¹⁄₆", "≈¹⁄₄",
    "B", "D", "E", "F", "H", "J", "K", "L", "L2", "L3",
    "L4", "L6", "W", "X", "Y", "Ω",
    "BB", "DD", "EE", "EF", "JE", "JB", "JF", "JH",
    "JJ", "JK", "JL2", "KL2", "LL", "LL2", "L2L4",
    "EB", "EJ", "EL2", "EL4", "EL6", "FK", "FL", "HK",
    "BL6", "DDDD", "EYYY",
}

# ═══════════════════════════════════════════════════════
# PARSE LinearAInscriptions.js
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("METROLOGICAL DOMAIN PROFILING V2 — LINEAR A MASTER ANALYSIS")
print("=" * 75)

print("\nStep 0: Parsing corpus...")

with open(JS_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

entry_pattern = re.compile(r'\["([^"]+)"\s*,\s*\{', re.DOTALL)
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
        try:
            inscriptions[name] = json.loads(raw[brace_start:j + 1].replace("'", '"'))
        except:
            pass

print(f"  Total inscriptions: {len(inscriptions)}")

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
def is_numeral(t):
    try: int(t); return True
    except: return False

def is_commodity(t):
    if not t: return False
    u = t.upper()
    if u in COMMODITY_BASES: return True
    if "+" in t:
        base = t.split("+")[0].upper()
        return base in COMMODITY_BASES
    return False

def get_commodity_domain(t):
    u = t.upper()
    if u in COMMODITY_BASES: return COMMODITY_BASES[u]
    if "+" in t:
        base = t.split("+")[0].upper()
        if base in COMMODITY_BASES: return COMMODITY_BASES[base]
    return "UNKNOWN"

def is_fraction(t):
    return t in FRACTION_TOKENS

def is_separator(t):
    return t in ("𐄁", "𐄀", "𐄂")

def is_word(t):
    if not t or t == "\n": return False
    if is_numeral(t) or is_commodity(t) or is_fraction(t) or is_separator(t): return False
    if t.startswith("*") and "-" not in t: return False
    if t.startswith('"'): return False
    if t == "𐝫": return False
    return True

def split_lines(tokens):
    lines = [[]]
    for t in tokens:
        if t == "\n": lines.append([])
        else: lines[-1].append(t)
    return [l for l in lines if l]

# ═══════════════════════════════════════════════════════
# STEP 1: REGISTER SEPARATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 1: REGISTER SEPARATION")
print("=" * 75)

register_map = {
    "Tablet": "LEDGER", "Lames (short thin tablet)": "LEDGER",
    "3-sided bar": "LEDGER", "4-sided bar": "LEDGER",
    "Nodule": "NODULE", "Sealing": "NODULE",
    "Roundel": "ROUNDEL",
    "Stone vessel": "RITUAL", "Metal object": "RITUAL",
    "Stone object": "RITUAL", "Clay vessel": "RITUAL",
    "Inked inscription": "OTHER", "Architecture": "OTHER",
    "Graffito": "OTHER", "Label": "OTHER",
}

registers = defaultdict(list)
for name, data in inscriptions.items():
    support = data.get("support", "unknown")
    register = register_map.get(support, "OTHER")
    registers[register].append(name)

for reg, tabs in sorted(registers.items(), key=lambda x: -len(x[1])):
    print(f"  {reg}: {len(tabs)} inscriptions")

tablets = {name: inscriptions[name] for name in registers["LEDGER"]}
nodules = {name: inscriptions[name] for name in registers["NODULE"]}
roundels = {name: inscriptions[name] for name in registers["ROUNDEL"]}
ritual = {name: inscriptions[name] for name in registers["RITUAL"]}

print(f"\n  → Using {len(tablets)} LEDGER inscriptions for MDP profiling")
print(f"  → {len(nodules)} NODULE inscriptions analysed separately (Stamp Analysis)")

# ═══════════════════════════════════════════════════════
# STEP 2: CORE MDP — TABLET-ONLY COMMODITY DOMAIN PROFILING
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 2: CORE MDP — TABLET-ONLY COMMODITY DOMAIN PROFILING")
print("=" * 75)

word_freq = Counter()
word_commodity = defaultdict(Counter)
word_tablets = defaultdict(set)
word_sites = defaultdict(Counter)
word_numadj = defaultdict(lambda: {"total": 0, "with_num": 0})
word_positions_line = defaultdict(Counter)
word_positions_tablet = defaultdict(Counter)  # FIRST_LINE / LAST_LINE / MIDDLE
commodity_freq = Counter()
commodity_numerals = defaultdict(list)
commodity_fractions = defaultdict(Counter)
tablet_commodities_map = defaultdict(set)
scribe_commodities = defaultdict(Counter)

for tab_name, data in tablets.items():
    tokens = data.get("transliteratedWords", [])
    if not tokens: continue

    site = data.get("site", "unknown")
    scribe = data.get("scribe", "")
    lines = split_lines(tokens)

    tab_words = set()
    tab_comms = set()

    for li, line in enumerate(lines):
        line_words = []
        line_comms = []
        line_nums = []
        line_fracs = []

        for t in line:
            if is_word(t):
                line_words.append(t)
                word_freq[t] += 1
                word_tablets[t].add(tab_name)
                word_sites[t][site] += 1
                tab_words.add(t)
            elif is_commodity(t):
                domain = get_commodity_domain(t)
                line_comms.append(domain)
                commodity_freq[t] += 1
                tab_comms.add(domain)
                if scribe:
                    scribe_commodities[scribe][domain] += 1
            elif is_numeral(t):
                line_nums.append(int(t))
            elif is_fraction(t):
                line_fracs.append(t)

        # Numeral adjacency for words on this line
        has_num = len(line_nums) > 0
        for w in set(line_words):
            word_numadj[w]["total"] += 1
            if has_num:
                word_numadj[w]["with_num"] += 1

        # Line-level positional (first/last word on line)
        if len(line_words) >= 2:
            word_positions_line[line_words[0]]["FIRST"] += 1
            word_positions_line[line_words[-1]]["LAST"] += 1
            for w in line_words[1:-1]:
                word_positions_line[w]["MIDDLE"] += 1
        elif len(line_words) == 1:
            word_positions_line[line_words[0]]["SOLE"] += 1

        # Tablet-level positional (first/last LINE of tablet)
        for w in set(line_words):
            if li == 0 and len(lines) > 1:
                word_positions_tablet[w]["FIRST_LINE"] += 1
            elif li == len(lines) - 1 and len(lines) > 1:
                word_positions_tablet[w]["LAST_LINE"] += 1
            elif len(lines) == 1:
                word_positions_tablet[w]["SOLE_LINE"] += 1
            else:
                word_positions_tablet[w]["MIDDLE_LINE"] += 1

        # Commodity → numeral / fraction recording
        for com in set(line_comms):
            for val in line_nums:
                commodity_numerals[com].append(val)
            for frac in line_fracs:
                commodity_fractions[com][frac] += 1

    # Tablet-level co-occurrence
    for w in tab_words:
        for c in tab_comms:
            word_commodity[w][c] += 1
        tablet_commodities_map[tab_name] = tab_comms

print(f"\n  Unique words on tablets: {len(word_freq)}")
print(f"  Total word occurrences: {sum(word_freq.values())}")
print(f"  Unique commodity tokens: {len(commodity_freq)}")

# Print the classification table
print(f"\n  {'Word':<24} {'Freq':>5} {'Tabs':>4} {'NumA%':>6} "
      f"{'GRA':>4} {'OLE':>4} {'VIN':>4} {'OLV':>4} {'PER':>4} {'CYP':>4} {'Domain':<22} {'Known'}")
print("  " + "-" * 115)

domain_classifications = {}

for word, freq in word_freq.most_common(120):
    if freq < 2: continue
    cooc = word_commodity.get(word, Counter())
    n_tabs = len(word_tablets.get(word, set()))
    adj = word_numadj.get(word, {"total": 0, "with_num": 0})
    adj_pct = adj["with_num"] / adj["total"] * 100 if adj["total"] > 0 else 0

    grain = cooc.get("GRAIN", 0)
    oil = cooc.get("OLIVE_OIL", 0)
    wine = cooc.get("WINE", 0)
    olive = cooc.get("OLIVES", 0)
    person = cooc.get("PERSON/MAN", 0)
    cyp = cooc.get("CYPRESS/CONTAINER", 0)

    total_cooc = sum(cooc.values())

    # Classification
    domain = "UNCLASSIFIED"
    if total_cooc == 0:
        domain = "NO_COMMODITY"
    else:
        pcts = {}
        for key, val in cooc.items():
            pcts[key] = val / total_cooc * 100

        top_domain = max(cooc, key=cooc.get)
        top_pct = pcts[top_domain]

        if top_pct > 60:
            domain = f"{top_domain}"
        elif top_pct > 40:
            domain = f"LEANING_{top_domain}"
        elif total_cooc >= 3 and top_pct < 35:
            domain = "CROSS-COMMODITY"
        else:
            domain = f"WEAK_{top_domain}"

    domain_classifications[word] = domain
    known = KNOWN_TERMS.get(word, "")
    print(f"  {word:<22} {freq:>5} {n_tabs:>4} {adj_pct:>5.0f}% "
          f"{grain:>4} {oil:>4} {wine:>4} {olive:>4} {person:>4} {cyp:>4} "
          f"{domain:<22} {known}")


# ═══════════════════════════════════════════════════════
# STEP 3: SUMMATION VERIFICATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 3: SUMMATION VERIFICATION")
print("=" * 75)

exact_count = 0
close_count = 0  # within ±2
total_checked = 0

print(f"\n  {'Tablet':<15} {'Lines':>5} {'Items∑':>8} {'KU-RO':>8} {'Δ':>6} {'Status'}")
print("  " + "-" * 55)

for tab_name, data in tablets.items():
    tokens = data.get("transliteratedWords", [])
    if "KU-RO" not in tokens: continue

    lines = split_lines(tokens)
    kuro_value = None
    item_values = []

    for line in lines:
        line_nums = [int(t) for t in line if is_numeral(t)]
        if "KU-RO" in line and line_nums:
            kuro_value = sum(line_nums)
        elif "KU-RO" not in line and "PO-TO-KU-RO" not in line and line_nums:
            item_values.extend(line_nums)

    if kuro_value is not None and item_values:
        items_sum = sum(item_values)
        diff = kuro_value - items_sum
        total_checked += 1
        if diff == 0:
            exact_count += 1
            status = "✓ EXACT"
        elif abs(diff) <= 2:
            close_count += 1
            status = f"~ CLOSE (Δ={diff})"
        else:
            status = f"✗ Δ={diff}"
        print(f"  {tab_name:<15} {len(lines):>5} {items_sum:>8} {kuro_value:>8} {diff:>6} {status}")

print(f"\n  Results: {exact_count} exact, {close_count} close (±2), "
      f"{total_checked - exact_count - close_count} mismatched out of {total_checked} checked")
if total_checked > 0:
    print(f"  Exact match rate: {exact_count/total_checked*100:.0f}%")
    print(f"  Close match rate: {(exact_count+close_count)/total_checked*100:.0f}%")

# ═══════════════════════════════════════════════════════
# STEP 4: LEDGER LINE GRAMMAR
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 4: LEDGER LINE GRAMMAR (Tablet-only)")
print("=" * 75)

line_patterns = Counter()
for tab_name, data in tablets.items():
    tokens = data.get("transliteratedWords", [])
    for line in split_lines(tokens):
        parts = []
        for t in line:
            if is_word(t): parts.append("W")
            elif is_commodity(t): parts.append("C")
            elif is_numeral(t): parts.append("N")
            elif is_fraction(t): parts.append("F")
            elif is_separator(t): parts.append("|")
            else: parts.append("?")
        line_patterns["-".join(parts)] += 1

print(f"\n  Top 20 tablet line patterns:")
for pattern, count in line_patterns.most_common(20):
    print(f"    {pattern}: {count}")


# ═══════════════════════════════════════════════════════
# STEP 5: COMMODITY SUB-TYPE PROFILING
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 5: COMMODITY SUB-TYPE PROFILING (Tablet-only)")
print("=" * 75)

variant_data = defaultdict(lambda: {"count": 0, "numerals": [], "cowords": Counter()})

for tab_name, data in tablets.items():
    tokens = data.get("transliteratedWords", [])
    tab_words = [t for t in tokens if is_word(t)]

    for idx, t in enumerate(tokens):
        if is_commodity(t):
            vd = variant_data[t]
            vd["count"] += 1
            for w in tab_words:
                vd["cowords"][w] += 1
            # Adjacent numeral
            for offset in range(1, 3):
                if idx + offset < len(tokens) and is_numeral(tokens[idx + offset]):
                    vd["numerals"].append(int(tokens[idx + offset]))
                    break

# Group by base commodity
bases = defaultdict(list)
for variant, vd in variant_data.items():
    base = variant.split("+")[0] if "+" in variant else variant
    bases[base].append((variant, vd))

for base in sorted(bases.keys(), key=lambda b: -sum(vd["count"] for _, vd in bases[b])):
    variants = bases[base]
    total = sum(vd["count"] for _, vd in variants)
    if total < 3: continue

    print(f"\n  {base} ({total} total on tablets):")
    for variant, vd in sorted(variants, key=lambda x: -x[1]["count"]):
        nums = vd["numerals"]
        if nums:
            nums.sort()
            med = nums[len(nums)//2]
            mean = sum(nums)/len(nums)
            n_str = f"  med={med}, mean={mean:.0f}, max={max(nums)}, n={len(nums)}"
        else:
            n_str = "  (no numerals)"
        top3 = ", ".join(f"{w}({c})" for w, c in vd["cowords"].most_common(3))
        print(f"    {variant}: {vd['count']}{n_str}")
        print(f"      co-words: {top3}")


# ═══════════════════════════════════════════════════════
# STEP 6: FRACTION DOMAIN DIVERGENCE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 6: FRACTION DOMAIN DIVERGENCE")
print("=" * 75)

print(f"\n  Do different commodities use different fractional measurement systems?")
print(f"  (Linear A equivalent of Proto-Elamite's metrological domain separation)\n")

for domain in ["GRAIN", "OLIVE_OIL", "WINE", "OLIVES", "CYPRESS/CONTAINER",
                "PERSON/MAN", "HIDES/LEATHER", "AROMATICS"]:
    fracs = commodity_fractions.get(domain, Counter())
    if not fracs: continue
    total_f = sum(fracs.values())
    print(f"  {domain} ({total_f} fraction instances):")
    for frac, count in fracs.most_common(8):
        bar = "█" * int(count / total_f * 30)
        print(f"    {frac:<8} {count:>3} ({count/total_f*100:>4.0f}%) {bar}")
    print()


# ═══════════════════════════════════════════════════════
# STEP 7: TABLET-LEVEL POSITION (KU-RO / PO-TO-KU-RO)
# ═══════════════════════════════════════════════════════
print("=" * 75)
print("STEP 7: TABLET-LEVEL SUMMATION POSITION")
print("=" * 75)

for target in ["KU-RO", "KI-RO", "PO-TO-KU-RO"]:
    pos_counter = Counter()
    for tab_name, data in tablets.items():
        tokens = data.get("transliteratedWords", [])
        if target not in tokens: continue
        lines = split_lines(tokens)
        for i, line in enumerate(lines):
            if target in line:
                if len(lines) == 1:
                    pos_counter["SOLE_LINE"] += 1
                elif i == 0:
                    pos_counter["FIRST_LINE"] += 1
                elif i == len(lines) - 1:
                    pos_counter["LAST_LINE"] += 1
                else:
                    pos_counter["MIDDLE_LINE"] += 1

    total = sum(pos_counter.values())
    if total == 0: continue
    print(f"\n  {target} ({total} occurrences on tablets):")
    for pos, count in pos_counter.most_common():
        bar = "█" * int(count / total * 30)
        print(f"    {pos:<15} {count:>3}/{total} ({count/total*100:>4.0f}%) {bar}")


# ═══════════════════════════════════════════════════════
# STEP 8: SCRIBE SPECIALISATION
# ═══════════════════════════════════════════════════════
print("\n\n" + "=" * 75)
print("STEP 8: SCRIBE SPECIALISATION (Tablet-only)")
print("=" * 75)

for scribe, comms in sorted(scribe_commodities.items(), key=lambda x: -sum(x[1].values())):
    if not scribe or sum(comms.values()) < 3: continue
    total = sum(comms.values())
    top = comms.most_common(1)[0]
    top_pct = top[1] / total * 100

    if top_pct > 70: spec = f"SPECIALIST: {top[0]}"
    elif top_pct > 50: spec = f"LEANING: {top[0]}"
    else: spec = "GENERALIST"

    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(4))
    print(f"  {scribe}: {total} records — {comm_str} → {spec}")


# ═══════════════════════════════════════════════════════
# STEP 9: ROOM / FINDSPOT SPECIALISATION
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 9: ROOM / FINDSPOT SPECIALISATION (Tablet-only)")
print("=" * 75)

findspot_comms = defaultdict(Counter)
findspot_count = Counter()

for tab_name, data in tablets.items():
    fs = data.get("findspot", "")
    if not fs: continue
    findspot_count[fs] += 1
    tokens = data.get("transliteratedWords", [])
    for t in tokens:
        if is_commodity(t):
            base = t.split("+")[0] if "+" in t else t
            findspot_comms[fs][base] += 1

print(f"\n  Findspots with 3+ tablets and commodity data:")
for fs in sorted(findspot_count.keys(), key=lambda f: -findspot_count[f]):
    count = findspot_count[fs]
    comms = findspot_comms.get(fs, Counter())
    if count < 3 or not comms: continue
    total_c = sum(comms.values())
    top = comms.most_common(1)[0]
    top_pct = top[1] / total_c * 100 if total_c > 0 else 0
    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(5))
    spec = f" ← {top[0]} SPECIALIST" if top_pct > 60 else ""
    print(f"  {fs}: {count} tablets, {total_c} commodity refs")
    print(f"    {comm_str}{spec}")


# ═══════════════════════════════════════════════════════
# STEP 10: NODULE STAMP ANALYSIS (Separate register)
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 10: NODULE STAMP ANALYSIS")
print("=" * 75)

nodule_words = Counter()
nodule_word_combos = Counter()

for name, data in nodules.items():
    tokens = data.get("transliteratedWords", [])
    words = [t for t in tokens if is_word(t)]
    for w in words:
        nodule_words[w] += 1
    if len(words) >= 2:
        nodule_word_combos[tuple(sorted(words))] += 1
    elif len(words) == 1:
        nodule_word_combos[(words[0],)] += 1

print(f"\n  Total nodules: {len(nodules)}")
print(f"  Unique stamps: {len(nodule_words)}")
print(f"\n  Top 20 nodule stamps:")
for w, c in nodule_words.most_common(20):
    # Check if this word ALSO appears on tablets
    tab_count = word_freq.get(w, 0)
    ratio_str = f"  (also on {tab_count} tablet lines)" if tab_count > 0 else "  (NODULE-ONLY)"
    print(f"    {w}: {c}{ratio_str}")

print(f"\n  Top 15 stamp combinations (multi-word nodules):")
for combo, count in nodule_word_combos.most_common(15):
    if len(combo) > 1:
        print(f"    {' + '.join(combo)}: {count}")


# ═══════════════════════════════════════════════════════
# STEP 11: WORD BIGRAMS (Tablet-only)
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 11: WORD BIGRAMS — Administrative Phrases (Tablet-only)")
print("=" * 75)

bigrams = Counter()
for tab_name, data in tablets.items():
    tokens = data.get("transliteratedWords", [])
    words = [t for t in tokens if is_word(t)]
    for i in range(len(words) - 1):
        bigrams[(words[i], words[i+1])] += 1

print(f"\n  Top 20 tablet word bigrams:")
for (a, b), count in bigrams.most_common(20):
    known_a = KNOWN_TERMS.get(a, "")
    known_b = KNOWN_TERMS.get(b, "")
    notes = ""
    if known_a: notes += f" [{a}={known_a}]"
    if known_b: notes += f" [{b}={known_b}]"
    print(f"    {a} → {b}: {count}{notes}")


# ═══════════════════════════════════════════════════════
# STEP 12: CHRONOLOGICAL PROFILE
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 12: CHRONOLOGICAL COMMODITY PROFILE")
print("=" * 75)

context_comms = defaultdict(Counter)
context_count = Counter()

for tab_name, data in tablets.items():
    ctx = data.get("context", "")
    if not ctx: continue
    context_count[ctx] += 1
    tokens = data.get("transliteratedWords", [])
    for t in tokens:
        if is_commodity(t):
            base = t.split("+")[0] if "+" in t else t
            context_comms[ctx][base] += 1

print(f"\n  {'Period':<12} {'Tablets':>7} {'Commodities'}")
print("  " + "-" * 60)
for ctx in sorted(context_count.keys(), key=lambda c: -context_count[c]):
    comms = context_comms.get(ctx, Counter())
    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(6))
    print(f"  {ctx:<12} {context_count[ctx]:>7} {comm_str}")


# ═══════════════════════════════════════════════════════
# STEP 13: DOMAIN CLASSIFICATION SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 13: DOMAIN CLASSIFICATION SUMMARY (Tablet-only)")
print("=" * 75)

domain_groups = defaultdict(list)
for word, domain in domain_classifications.items():
    domain_groups[domain].append((word, word_freq[word]))

for domain in sorted(domain_groups.keys(), key=lambda d: -len(domain_groups[d])):
    words = sorted(domain_groups[domain], key=lambda x: -x[1])
    print(f"\n  {domain} ({len(words)} words):")
    for w, f in words[:12]:
        known = KNOWN_TERMS.get(w, "")
        pos_info = ""
        tpos = word_positions_tablet.get(w, Counter())
        if tpos:
            top_pos = max(tpos, key=tpos.get)
            top_pos_pct = tpos[top_pos] / sum(tpos.values()) * 100
            if top_pos_pct > 60:
                pos_info = f" [{top_pos} {top_pos_pct:.0f}%]"
        marker = f" ← {known}" if known else ""
        print(f"    {w}: {f}{pos_info}{marker}")


# ═══════════════════════════════════════════════════════
# STEP 14: VALIDATION — Known Terms Check
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("STEP 14: VALIDATION — Known Terms")
print("=" * 75)

print(f"\n  {'Term':<24} {'Meaning':<22} {'Domain':<22} {'Commodity Co-occ'}")
print("  " + "-" * 95)

for term, meaning in KNOWN_TERMS.items():
    domain = domain_classifications.get(term, "NOT IN TOP 120")
    cooc = word_commodity.get(term, Counter())
    cooc_str = ", ".join(f"{c}={n}" for c, n in cooc.most_common(4)) if cooc else "-"
    print(f"  {term:<22} {meaning:<22} {domain:<22} {cooc_str}")


# ═══════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 75)
print("LINEAR A MDP V2 — MASTER ANALYSIS COMPLETE")
print("=" * 75)
print(f"\n  CORPUS:")
print(f"    Total inscriptions: {len(inscriptions)}")
print(f"    Ledger tablets analysed: {len(tablets)}")
print(f"    Nodule stamps analysed: {len(nodules)}")
print(f"    Roundels: {len(roundels)}")
print(f"    Ritual/votive: {len(ritual)}")
print(f"\n  MDP RESULTS (Tablet-only):")
print(f"    Unique words profiled: {len(word_freq)}")
print(f"    Words classified: {len(domain_classifications)}")
domain_summary = Counter(domain_classifications.values())
for d, c in domain_summary.most_common():
    print(f"      {d}: {c}")
print(f"\n  SUMMATION:")
print(f"    Tablets with KU-RO checked: {total_checked}")
print(f"    Exact matches: {exact_count} ({exact_count/total_checked*100:.0f}%)" if total_checked else "")
print(f"    Close matches (±2): {exact_count+close_count}" if total_checked else "")
print()

"""
=============================================================================
LINEAR A DEEP SNOOP — Corpus Structure Discovery
=============================================================================
Author: Adrian Sharman, SoulDriver Research (souldriver.com.au)
Date: May 2026

DESCRIPTION:
Deep exploration script that tears through the Linear A corpus looking for
hidden structure the initial MDP pass didn't catch. Specifically targets:

1. TABLET-LEVEL POSITION: Does KU-RO appear on the LAST line of tablets?
2. LEDGER STRUCTURE: Name → Commodity → Number patterns per line
3. SUMMATION CHECKING: Do numeral totals on tablets add up?
4. WORD BIGRAMS: Sequential word pairs revealing administrative syntax
5. TABLET TEMPLATES: Cluster tablets by their structural fingerprint
6. FINDSPOT CORRELATION: Do rooms in the same building handle same commodities?
7. COMMODITY SUB-TYPE PROFILING: OLE+U vs OLE+A vs OLE+KI — different oils?
8. SINGLE-SYLLABLE SIGN EXPLOSION: KU/KA/SI/RO — are these words or fragments?
9. NODULE vs TABLET ANALYSIS: Different inscription patterns by support type?
10. CROSS-VALIDATION: Check tagged tablets (Libation Formula, Wrong Total)

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

# ═══════════════════════════════════════════════════════
# PARSE DATA (same parser as lineara_mdp.py)
# ═══════════════════════════════════════════════════════
print("=" * 70)
print("LINEAR A DEEP SNOOP — CORPUS STRUCTURE DISCOVERY")
print("=" * 70)

with open(JS_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

entry_pattern = re.compile(r'\["([^"]+)"\s*,\s*\{', re.DOTALL)
positions = [(m.start(), m.group(1)) for m in entry_pattern.finditer(raw)]

inscriptions = {}
for i, (pos, name) in enumerate(positions):
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
        inscriptions[name] = json.loads(obj_str)
    except:
        try:
            inscriptions[name] = json.loads(obj_str.replace("'", '"'))
        except:
            pass

print(f"\nParsed {len(inscriptions)} inscriptions")

# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════
COMMODITY_KEYWORDS = {
    "GRA", "OLE", "VIN", "OLIV", "FIC", "AROM", "CYP", "GAL",
    "HIDE", "TELA", "CAP", "VIR", "*21F", "*22F", "*21M", "*22M", "*23M",
}

def is_numeral(token):
    try:
        int(token)
        return True
    except:
        return False

def is_commodity(token):
    if not token:
        return False
    upper = token.upper()
    if upper in COMMODITY_KEYWORDS:
        return True
    if "+" in token:
        base = token.split("+")[0].upper()
        return base in COMMODITY_KEYWORDS
    return False

def is_fraction(token):
    frac_chars = {"¹", "²", "³", "⁄", "₂", "₃", "₄", "₅", "₈", "₁₆",
                  "≈", "½", "¼", "¾", "⅝"}
    if any(c in token for c in frac_chars):
        return True
    if token in ("B", "D", "E", "F", "H", "J", "K", "L", "L2", "L3",
                 "L4", "L6", "W", "X", "Y", "Ω", "BB", "DD", "EE",
                 "JE", "JB", "JF", "JH", "JJ", "JK", "JL2", "KL2",
                 "LL", "LL2", "L2L4", "EB", "EJ", "EL2", "EL4",
                 "EL6", "FK", "FL", "HK", "BL6", "DDDD", "EYYY",
                 "EF"):
        return True
    return False

def is_separator(token):
    return token in ("𐄁", "𐄀", "𐄂")

def is_word(token):
    if token == "\n" or not token:
        return False
    if is_numeral(token) or is_commodity(token) or is_fraction(token) or is_separator(token):
        return False
    if token.startswith("*") and not "-" in token:
        return False
    if token.startswith('"'):
        return False
    if token == "𐝫":  # damage marker
        return False
    return True


# ═══════════════════════════════════════════════════════
# SNOOP 1: TABLET-LEVEL POSITION OF KU-RO / KI-RO
# Does the "total" word appear on the LAST line?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 1: TABLET-LEVEL POSITION — Where does KU-RO appear?")
print("=" * 70)

target_words = ["KU-RO", "KI-RO", "PO-TO-KU-RO"]

for target in target_words:
    positions_found = Counter()  # "FIRST_LINE", "LAST_LINE", "MIDDLE_LINE"
    examples = []

    for tab_name, data in inscriptions.items():
        tokens = data.get("transliteratedWords", [])
        if target not in tokens:
            continue

        # Split into lines
        lines = [[]]
        for t in tokens:
            if t == "\n":
                lines.append([])
            else:
                lines[-1].append(t)

        # Remove empty lines
        lines = [l for l in lines if l]
        if not lines:
            continue

        # Find which line(s) contain the target
        for i, line in enumerate(lines):
            if target in line:
                if i == 0 and len(lines) == 1:
                    positions_found["SOLE_LINE"] += 1
                elif i == 0:
                    positions_found["FIRST_LINE"] += 1
                elif i == len(lines) - 1:
                    positions_found["LAST_LINE"] += 1
                else:
                    positions_found["MIDDLE_LINE"] += 1

                if len(examples) < 3:
                    examples.append(f"    {tab_name} line {i+1}/{len(lines)}: {' '.join(line)}")

    print(f"\n  {target}:")
    total = sum(positions_found.values())
    for pos, count in positions_found.most_common():
        print(f"    {pos}: {count}/{total} ({count/total*100:.0f}%)")
    for ex in examples:
        print(ex)


# ═══════════════════════════════════════════════════════
# SNOOP 2: LINE-LEVEL LEDGER STRUCTURE
# What's the typical pattern on a single line?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 2: LINE-LEVEL LEDGER STRUCTURE")
print("=" * 70)

line_patterns = Counter()
line_examples = defaultdict(list)

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    lines = [[]]
    for t in tokens:
        if t == "\n":
            lines.append([])
        else:
            lines[-1].append(t)

    for line in lines:
        if not line:
            continue
        # Build pattern string
        pattern_parts = []
        for token in line:
            if is_word(token):
                pattern_parts.append("W")
            elif is_commodity(token):
                pattern_parts.append("C")
            elif is_numeral(token):
                pattern_parts.append("N")
            elif is_fraction(token):
                pattern_parts.append("F")
            elif is_separator(token):
                pattern_parts.append("|")
            else:
                pattern_parts.append("?")

        pattern = "-".join(pattern_parts)
        line_patterns[pattern] += 1
        if len(line_examples[pattern]) < 2:
            line_examples[pattern].append(f"{tab_name}: {' '.join(line)}")

print(f"\nTop 30 line patterns (W=word, C=commodity, N=numeral, F=fraction, |=separator):")
for pattern, count in line_patterns.most_common(30):
    print(f"  {pattern}: {count}")
    for ex in line_examples[pattern]:
        print(f"    ex: {ex}")


# ═══════════════════════════════════════════════════════
# SNOOP 3: SUMMATION CHECKING
# Do the line-by-line numerals add up to the total on KU-RO tablets?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 3: SUMMATION CHECKING — Do the numbers add up?")
print("=" * 70)

checks = []
for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    if "KU-RO" not in tokens:
        continue

    # Split into lines
    lines = [[]]
    for t in tokens:
        if t == "\n":
            lines.append([])
        else:
            lines[-1].append(t)
    lines = [l for l in lines if l]

    # Find the KU-RO line and extract its numeral
    kuro_value = None
    item_values = []
    kuro_line_idx = -1

    for i, line in enumerate(lines):
        line_nums = [int(t) for t in line if is_numeral(t)]
        has_kuro = "KU-RO" in line

        if has_kuro and line_nums:
            kuro_value = sum(line_nums)
            kuro_line_idx = i
        elif not has_kuro and line_nums:
            item_values.extend(line_nums)

    if kuro_value is not None and item_values:
        items_sum = sum(item_values)
        diff = kuro_value - items_sum
        match = "✓ EXACT" if diff == 0 else f"Δ={diff}"
        checks.append((tab_name, items_sum, kuro_value, diff, match))

print(f"\n  {'Tablet':<15} {'Items∑':>8} {'KU-RO':>8} {'Diff':>8} {'Status'}")
print("  " + "-" * 50)

exact = 0
for tab, items, kuro, diff, match in sorted(checks, key=lambda x: abs(x[3])):
    print(f"  {tab:<15} {items:>8} {kuro:>8} {diff:>8} {match}")
    if diff == 0:
        exact += 1

print(f"\n  Exact matches: {exact}/{len(checks)} ({exact/len(checks)*100:.0f}% if checks)")


# ═══════════════════════════════════════════════════════
# SNOOP 4: WORD BIGRAMS — Sequential pairs
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 4: WORD BIGRAMS (sequential word pairs)")
print("=" * 70)

bigrams = Counter()
bigram_examples = defaultdict(list)

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    # Get just the words (skip numerals, commodities, newlines)
    words_only = [t for t in tokens if is_word(t)]

    for i in range(len(words_only) - 1):
        bigram = (words_only[i], words_only[i + 1])
        bigrams[bigram] += 1
        if len(bigram_examples[bigram]) < 2:
            bigram_examples[bigram].append(tab_name)

print(f"\nTop 25 word bigrams:")
for (a, b), count in bigrams.most_common(25):
    tabs = ", ".join(bigram_examples[(a, b)])
    print(f"  {a} → {b}: {count}  (e.g. {tabs})")


# ═══════════════════════════════════════════════════════
# SNOOP 5: TABLET TEMPLATES — Structural fingerprints
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 5: TABLET TEMPLATES — Structural fingerprints")
print("=" * 70)

templates = Counter()
template_examples = defaultdict(list)

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    if not tokens:
        continue

    # Build per-line type sequence
    lines = [[]]
    for t in tokens:
        if t == "\n":
            lines.append([])
        else:
            lines[-1].append(t)
    lines = [l for l in lines if l]

    line_types = []
    for line in lines:
        has_word = any(is_word(t) for t in line)
        has_commodity = any(is_commodity(t) for t in line)
        has_numeral = any(is_numeral(t) for t in line)
        has_kuro = "KU-RO" in line
        has_kiro = "KI-RO" in line

        if has_kuro:
            line_types.append("TOTAL")
        elif has_kiro:
            line_types.append("DEFICIT")
        elif has_word and has_commodity and has_numeral:
            line_types.append("FULL")  # Name + Commodity + Number
        elif has_word and has_numeral:
            line_types.append("W+N")  # Name + Number (no commodity)
        elif has_commodity and has_numeral:
            line_types.append("C+N")  # Commodity + Number
        elif has_word and has_commodity:
            line_types.append("W+C")  # Name + Commodity
        elif has_word:
            line_types.append("W")  # Word only (header?)
        elif has_numeral:
            line_types.append("N")  # Number only
        else:
            line_types.append("?")

    template = " → ".join(line_types)
    templates[template] += 1
    if len(template_examples[template]) < 3:
        template_examples[template].append(tab_name)

print(f"\nTop 25 tablet templates:")
for template, count in templates.most_common(25):
    examples = ", ".join(template_examples[template])
    print(f"  [{count:>4}] {template}")
    print(f"         e.g. {examples}")


# ═══════════════════════════════════════════════════════
# SNOOP 6: SUPPORT TYPE vs CONTENT
# Do Nodules, Tablets, and Roundels carry different content?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 6: SUPPORT TYPE vs CONTENT ANALYSIS")
print("=" * 70)

support_stats = defaultdict(lambda: {
    "count": 0, "has_commodity": 0, "has_numeral": 0, "has_word": 0,
    "avg_tokens": [], "commodities": Counter(), "has_kuro": 0
})

for tab_name, data in inscriptions.items():
    support = data.get("support", "unknown")
    tokens = data.get("transliteratedWords", [])
    tokens_clean = [t for t in tokens if t != "\n"]

    stats = support_stats[support]
    stats["count"] += 1
    stats["avg_tokens"].append(len(tokens_clean))

    has_com = False
    has_num = False
    has_w = False

    for t in tokens_clean:
        if is_commodity(t):
            has_com = True
            stats["commodities"][t.split("+")[0] if "+" in t else t] += 1
        elif is_numeral(t):
            has_num = True
        elif is_word(t):
            has_w = True

    if has_com:
        stats["has_commodity"] += 1
    if has_num:
        stats["has_numeral"] += 1
    if has_w:
        stats["has_word"] += 1
    if "KU-RO" in tokens:
        stats["has_kuro"] += 1

print(f"\n{'Support':<25} {'Count':>6} {'Words%':>7} {'Comm%':>7} {'Nums%':>7} {'KU-RO%':>7} {'AvgTok':>7} {'Top Commodity'}")
print("-" * 95)

for support in sorted(support_stats.keys(), key=lambda s: -support_stats[s]["count"]):
    s = support_stats[support]
    n = s["count"]
    avg_tok = sum(s["avg_tokens"]) / len(s["avg_tokens"]) if s["avg_tokens"] else 0
    top_com = s["commodities"].most_common(1)[0][0] if s["commodities"] else "-"
    print(f"  {support:<23} {n:>6} {s['has_word']/n*100:>6.0f}% {s['has_commodity']/n*100:>6.0f}% "
          f"{s['has_numeral']/n*100:>6.0f}% {s['has_kuro']/n*100:>6.0f}% {avg_tok:>6.1f} {top_com}")


# ═══════════════════════════════════════════════════════
# SNOOP 7: COMMODITY SUB-TYPES — OLE+U vs OLE+A vs OLE+KI
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 7: COMMODITY SUB-TYPE PROFILING")
print("=" * 70)

# Group all commodity variants by base
commodity_variants = defaultdict(Counter)
commodity_variant_numerals = defaultdict(list)
commodity_variant_cowords = defaultdict(Counter)

for tab_name, data in inscriptions.items():
    tokens = data.get("transliteratedWords", [])
    tab_words = [t for t in tokens if is_word(t)]

    for t in tokens:
        if is_commodity(t):
            base = t.split("+")[0] if "+" in t else t
            variant = t
            commodity_variants[base][variant] += 1

            # Find numerals adjacent (within 2 tokens)
            idx = tokens.index(t)
            for offset in range(1, 3):
                if idx + offset < len(tokens) and is_numeral(tokens[idx + offset]):
                    commodity_variant_numerals[variant].append(int(tokens[idx + offset]))
                    break

            # Co-occurring words on same tablet
            for w in tab_words:
                commodity_variant_cowords[variant][w] += 1

for base in sorted(commodity_variants.keys(), key=lambda b: -sum(commodity_variants[b].values())):
    variants = commodity_variants[base]
    if sum(variants.values()) < 5:
        continue
    print(f"\n  {base} ({sum(variants.values())} total):")
    for variant, count in variants.most_common():
        nums = commodity_variant_numerals.get(variant, [])
        if nums:
            nums.sort()
            median = nums[len(nums) // 2]
            mean = sum(nums) / len(nums)
            num_str = f"  median={median}, mean={mean:.0f}, max={max(nums)}"
        else:
            num_str = ""
        # Top co-occurring words
        cowords = commodity_variant_cowords.get(variant, Counter())
        top_words = ", ".join(f"{w}({c})" for w, c in cowords.most_common(3))
        print(f"    {variant}: {count}{num_str}  words: {top_words}")


# ═══════════════════════════════════════════════════════
# SNOOP 8: SINGLE-SYLLABLE EXPLOSION
# KU=170, KA=169, SI=118 — are these really standalone words?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 8: SINGLE-SYLLABLE SIGN ANALYSIS")
print("=" * 70)

print("\nAre the high-frequency single syllables (KU, KA, SI, RO, NI) standalone words")
print("or fragments from damaged/broken multi-syllable words?\n")

single_syllables = ["KU", "KA", "SI", "RO", "NI", "TE", "ZE", "I", "TA",
                     "A", "KI", "O", "DI", "PA", "RE", "NA"]

for syl in single_syllables:
    # Check how many times this syllable appears as part of a LONGER word
    as_prefix = sum(c for w, c in all_words_global.items() if w.startswith(syl + "-") and w != syl) if 'all_words_global' in dir() else 0
    as_suffix = sum(c for w, c in all_words_global.items() if w.endswith("-" + syl) and w != syl) if 'all_words_global' in dir() else 0

# Actually, let's check on the support type — nodules only have 1-2 signs
single_on_nodule = Counter()
single_on_tablet = Counter()
single_on_roundel = Counter()

for tab_name, data in inscriptions.items():
    support = data.get("support", "")
    tokens = data.get("transliteratedWords", [])
    words = [t for t in tokens if is_word(t)]

    for w in words:
        if len(w) <= 3 and w.isalpha():  # single syllable
            if support == "Nodule":
                single_on_nodule[w] += 1
            elif support == "Tablet":
                single_on_tablet[w] += 1
            elif support == "Roundel":
                single_on_roundel[w] += 1

print(f"{'Syllable':<8} {'Nodule':>8} {'Tablet':>8} {'Roundel':>8} {'Nodule%':>8}")
print("-" * 45)
for syl in single_syllables:
    nod = single_on_nodule.get(syl, 0)
    tab = single_on_tablet.get(syl, 0)
    rnd = single_on_roundel.get(syl, 0)
    total = nod + tab + rnd
    nod_pct = nod / total * 100 if total > 0 else 0
    if total > 0:
        print(f"  {syl:<6} {nod:>8} {tab:>8} {rnd:>8} {nod_pct:>7.0f}%")


# ═══════════════════════════════════════════════════════
# SNOOP 9: FINDSPOT CORRELATION
# Do rooms cluster by commodity?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 9: FINDSPOT / ROOM CORRELATION")
print("=" * 70)

findspot_commodities = defaultdict(Counter)
findspot_count = Counter()

for tab_name, data in inscriptions.items():
    findspot = data.get("findspot", "")
    if not findspot:
        continue
    findspot_count[findspot] += 1
    tokens = data.get("transliteratedWords", [])
    for t in tokens:
        if is_commodity(t):
            base = t.split("+")[0] if "+" in t else t
            findspot_commodities[findspot][base] += 1

print(f"\nFindspots with 5+ inscriptions and commodity data:")
for findspot in sorted(findspot_count.keys(), key=lambda f: -findspot_count[f]):
    count = findspot_count[findspot]
    comms = findspot_commodities.get(findspot, Counter())
    if count < 5 or not comms:
        continue
    total_comms = sum(comms.values())
    top_comm = comms.most_common(1)[0] if comms else ("-", 0)
    top_pct = top_comm[1] / total_comms * 100 if total_comms > 0 else 0
    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(5))

    specialisation = ""
    if top_pct > 60:
        specialisation = f" ← {top_comm[0]} SPECIALIST"

    print(f"  {findspot}: {count} inscriptions, {total_comms} commodity refs")
    print(f"    {comm_str}{specialisation}")


# ═══════════════════════════════════════════════════════
# SNOOP 10: CONTEXT (DATING) vs CONTENT
# LMIA vs LMIB — did commodity profiles change over time?
# ═══════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("SNOOP 10: CHRONOLOGICAL ANALYSIS — LMIA vs LMIB")
print("=" * 70)

context_commodities = defaultdict(Counter)
context_count = Counter()

for tab_name, data in inscriptions.items():
    context = data.get("context", "")
    if not context:
        continue
    context_count[context] += 1
    tokens = data.get("transliteratedWords", [])
    for t in tokens:
        if is_commodity(t):
            base = t.split("+")[0] if "+" in t else t
            context_commodities[context][base] += 1

print(f"\n{'Context/Date':<15} {'Count':>6} {'Commodities'}")
print("-" * 70)
for ctx in sorted(context_count.keys(), key=lambda c: -context_count[c]):
    count = context_count[ctx]
    comms = context_commodities.get(ctx, Counter())
    comm_str = ", ".join(f"{c}={n}" for c, n in comms.most_common(8))
    print(f"  {ctx:<13} {count:>6} {comm_str}")


print("\n" + "=" * 70)
print("DEEP SNOOP COMPLETE")
print("=" * 70)

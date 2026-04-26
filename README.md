# Metrological Domain Profiling (MDP)
## A Computational Method for Classifying Signs in Undeciphered Administrative Scripts

**Author:** Adrian Sharman, SoulDriver Research ([souldriver.com.au](https://souldriver.com.au))

**Paper:** *Metrological Domain Profiling: A Computational Approach to Administrative Architectures in Proto-Cuneiform, Proto-Elamite, and the Indus Valley Script* (Sharman, April 2026)

---

### Overview

This repository contains the complete code and methodology for **Metrological Domain Profiling (MDP)**, a novel computational method that classifies signs in ancient administrative scripts by analysing their statistical co-occurrence with metrological numeral systems. The method requires no linguistic assumptions, no phonetic hypotheses, and no prior knowledge of sign meanings.

### Key Results

| Script | Period | Corpus Size | Method | Accuracy / Finding |
|--------|--------|------------|--------|-------------------|
| **Proto-Cuneiform** | c. 3350–3000 BCE | 31,191 signs, 6,819 tablets | Subtractive MDP | **100% accuracy** on 28-sign validation set |
| **Proto-Elamite** | c. 3100–2900 BCE | 14,716 records | Standard MDP | **79 signs classified**, 64% corpus coverage |
| **Indus Valley** | c. 2600–1900 BCE | 11,280 signs, 2,543 inscriptions | Animal-Sign Enrichment | **Semantic locks discovered** (G321→Hare: 195.6× enrichment) |

---

### Repository Contents

| File | Description |
|------|-------------|
| `protocuneiform_mdp.py` | **Study 1:** Validates Subtractive MDP on proto-cuneiform (Uruk IV/III). Achieves 100% on 28 known signs. |
| `protoelamite_mdp.py` | **Study 2:** Applies MDP to Proto-Elamite. Classifies 79 signs, reveals syntax and seal specialisation. |
| `indus_mdp.py` | **Study 3:** Adapts methodology for the Indus Valley Script. Discovers animal-sign semantic locks. |
| `Indus_scripts_terminal_output.md` | Full terminal output from the Indus analysis run. |
| `README.md` | This file. |

---

### Data Sources & Reproduction Instructions

This repository does not include the source datasets due to size constraints. All data is freely available from the following sources:

#### 1. CDLI Bulk Data (Proto-Cuneiform & Proto-Elamite)

Both `protocuneiform_mdp.py` and `protoelamite_mdp.py` require two files from the **Cuneiform Digital Library Initiative (CDLI)**:

| File | Description | Approx. Size |
|------|-------------|-------------|
| `cdliatf_unblocked.atf` | Bulk ATF transliteration dump — contains transliterations of ~135,000 cuneiform tablets | ~83 MB |
| `cdli_cat.csv` | Catalogue with metadata (period, provenience, language) for each tablet | ~148 MB |

**How to obtain:**
1. Visit [https://cdli.earth/](https://cdli.earth/) (or [https://github.com/cdli-gh/data](https://github.com/cdli-gh/data))
2. Download the bulk ATF transliteration file and the catalogue CSV
3. Place both files in a local directory (e.g., `C:\Users\you\cdli-data\`)
4. Update the `ATF_FILE` and `CAT_FILE` path variables at the top of each script

The CDLI data is open-access and freely available for research purposes.

#### 2. Yajnadevam Indus Corpus (Indus Valley Script)

`indus_mdp.py` requires the SQL population script from the **yajnadevam/indus-website** repository, which contains a structured digital extraction of the Interactive Corpus of Indus Texts (ICIT; Wells & Fuls 2015).

| File | Description | Approx. Size |
|------|-------------|-------------|
| `population-script.sql` | MySQL dump containing 2,543 inscriptions with sign sequences, iconographic descriptions, and site provenance | ~430 KB |

**How to obtain:**
1. Clone or download [https://github.com/yajnadevam/indus-website](https://github.com/yajnadevam/indus-website)
2. The file `population-script.sql` is in the repository root
3. Update the `SQL_FILE` path variable at the top of `indus_mdp.py`

Note: The script parses the SQL file directly using regex — no MySQL installation is required.

#### 3. Alternative Indus Corpus (Smaller, JSON format)

For a smaller Indus corpus (179 Mohenjo-daro unicorn seals in JSON format), see [https://github.com/mayig/indus-valley-script-corpus](https://github.com/mayig/indus-valley-script-corpus). This corpus was used for initial testing but lacks the multi-site, multi-animal coverage needed for the semantic lock analysis.

---

### Requirements

- Python 3.8+
- No external dependencies — uses only `re`, `csv`, `os`, `json`, and `collections` from the Python standard library
- Each script runs in under 60 seconds on a standard laptop

### Usage

```bash
# 1. Download the data sources listed above
# 2. Update file paths in each script to point to your local data files
# 3. Run:

python protocuneiform_mdp.py    # Study 1: Proto-Cuneiform Validation (expect: 28/28 = 100%)
python protoelamite_mdp.py      # Study 2: Proto-Elamite Application
python indus_mdp.py             # Study 3: Indus Valley Discovery
```

---

### Methodology: Subtractive Metrological Domain Profiling

Ancient administrative scripts pair commodity signs with numeral notations drawn from specific metrological systems. Grain is measured in capacity units (with fractional subdivisions), livestock is counted in discrete integers, and land is measured in area units. MDP exploits these metrological signatures to classify signs by commodity domain.

#### The Polyvalency Problem

Proto-cuneiform uses **polyvalent** numeral signs — the same grapheme (N14) represents different values in different metrological systems. As Englund (2011) describes: *"the sign N14 can represent ten clay pots of butter oil, a measure of grain corresponding to about 150 litres of barley, or a field of about 6 hectares."* Standard numeral co-occurrence analysis fails because the numeral codes are domain-ambiguous.

Proto-Elamite, by contrast, evolved **dedicated** numeral codes per domain (N39B exclusively for grain capacity, N23/N51 exclusively for the decimal/animate system). This architectural difference — shared vs dedicated numeral codes — is itself a finding about how the two contemporary writing systems diverged in encoding metrological information.

#### The Subtractive Solution

**Subtractive MDP** overcomes the polyvalency barrier with a three-step sieve:

1. **Total Numeral Adjacency:** Is the sign counted at all? (Uses all numerals including polyvalent N01/N14/N34)
2. **System-Specific Anchor Check:** Does it co-occur with fractional anchors unique to a specific system?
   - N39A, N24 → Grain capacity (ŠE system)
   - N51, N54 → Bisexagesimal rations
   - N50, N47, N08 → Area/land (GAN₂ system)
3. **Subtractive Deduction:** If counted but no system-specific anchors → sexagesimal discrete (livestock, textiles, metals, people)

#### Development Trajectory

The final 100% accuracy was achieved through iterative refinement:

| Version | Accuracy | Key Change |
|---------|----------|------------|
| v1 | 16% (3/19) | Hard-coded Proto-Elamite numeral systems — wrong for proto-cuneiform |
| v2 | 22% (4/18) | Data-driven anchor discovery — no livestock discriminators found |
| v3 | 55% (6/11) | Subtractive method introduced — grain failed due to anchor rarity |
| v4 | 94% (15/16) | Data normalisation fixes (tilde stripping, lowercase purge, compounds) |
| v4 expanded | **100% (28/28)** | Corrected validation dictionary + expanded test set |

---

### The Indus Discovery

By adapting MDP to analyse **sign–animal co-occurrence** instead of sign–numeral co-occurrence, we discovered that specific Indus signs are statistically **locked** to specific seal animals:

| Sign | Animal | Enrichment | Exclusivity |
|------|--------|------------|-------------|
| G321 | Hare | **195.6×** | 12/12 (100%) |
| G850 | Anthropomorphic | **60.5×** | 10/10 (100%) |
| G845 | Hare | **63.6×** | Shared with Anthropomorphic |
| G407 | Hare | **50.9×** | Primary hare, shared |
| G48 | Elephant | **35.6×** | Near-exclusive |
| G318 | Rhinoceros | **37.0×** | Near-exclusive |
| G436 | Rhinoceros | **31.7×** | Near-exclusive |
| G923 | Elephant | **14.8×** | Exclusive |

Each animal type possesses a **unique sign vocabulary** — a set of enriched signs that collectively distinguish its inscriptions from all others. This provides the first corpus-scale statistical evidence that Indus seal animals encode **institutional/departmental identity**, paralleling the commodity-specific seal ownership discovered in Proto-Elamite.

---

### Research Infrastructure

This research was conducted using **KARP** (Knowledge Acquisition Research Protocol), a multi-agent AI deliberation system developed by SoulDriver Research that orchestrates Claude (Anthropic), GPT, Gemini (Google), and Grok through structured adversarial research sessions.

The initial hypothesis — that Proto-Elamite's dedicated numeral codes could serve as a computational anchor for unsupervised sign classification — emerged from KARP council sessions on undeciphered ancient scripts. The Subtractive MDP variant was proposed during a Gemini review that identified the polyvalency barrier. Three critical data-normalisation fixes were likewise identified through external AI review.

The complete research trajectory — from initial hypothesis through five algorithm iterations to the final 100% validation, plus the Indus semantic lock discovery — was conducted in a single research session, demonstrating the potential of structured multi-agent AI deliberation for accelerating computational humanities research.

For more on KARP and SoulDriver Research, visit [souldriver.com.au](https://souldriver.com.au).

---

### License

MIT License — see [LICENSE](LICENSE) for details.

### Citation

If you use this code or methodology, please cite:

```
Sharman, A. (2026). Metrological Domain Profiling: A Computational Approach to
Administrative Architectures in Proto-Cuneiform, Proto-Elamite, and the Indus Valley
Script. SoulDriver Research. https://souldriver.com.au
```

### Acknowledgements

- **CDLI** (Cuneiform Digital Library Initiative) for open-access cuneiform data
- **Bryan K. Wells and Andreas Fuls** for the Interactive Corpus of Indus Texts (ICIT)
- **yajnadevam** for the digital ICIT extraction
- **mayig** for the Indus Valley script corpus (JSON format)
- **Robert K. Englund and Peter Damerow** for the foundational work on proto-cuneiform numeral systems
- **Jacob L. Dahl** for Proto-Elamite sign identifications

# Metrological Domain Profiling (MDP)
## A Computational Method for Classifying Signs in Undeciphered Administrative Scripts

**Author:** Adrian Sharman, SoulDriver Research ([souldriver.com.au](https://souldriver.com.au))

**Paper IV:** *Metrological Domain Profiling IV: Dual Systems, Redundant Channels, and the Imperial Data Network of the Inca Khipu* (Sharman, July 2026) — DOI: [10.17613/2d7r8-26m93](https://doi.org/10.17613/2d7r8-26m93)

**Paper III:** *Metrological Domain Profiling III: Reconstructing the 3D Tactile Grammar of the Inca Khipu* (Sharman, June 2026) — DOI: [10.17613/c97d4-pgs78](https://doi.org/10.17613/c97d4-pgs78)

**Paper II:** *Metrological Domain Profiling II: Functional Economic Ontologies from the Aegean Bronze Age to the Inca Empire* (Sharman, May 2026) — DOI: [10.17613/q536f-0wa13](https://doi.org/10.17613/q536f-0wa13)

**Paper I:** *Metrological Domain Profiling: A Computational Approach to Administrative Architectures in Proto-Cuneiform, Proto-Elamite, and the Indus Valley Script* (Sharman, April 2026) — DOI: [10.17613/mmjdt-ba806](https://doi.org/10.17613/mmjdt-ba806)

---

### Overview

This repository contains the complete code and methodology for **Metrological Domain Profiling (MDP)**, a novel computational method that classifies signs in ancient administrative scripts by analysing their statistical co-occurrence with metrological numeral systems. The method requires no linguistic assumptions, no phonetic hypotheses, and no prior knowledge of sign meanings.

**Update — July 2026:** MDP Paper IV applies Shannon entropy analysis to 720 compound colours across 39,172 pendant cords, revealing a three-tier vowel/consonant information hierarchy and proving that collapsing compound colours (standard practice since the Aschers) discards 27% of the colour signal. Corpus-wide classification of all 612 khipus identifies three co-existing administrative systems: System A (Logistical, 154), System B (Demographic, 28), and System C (Categorical, 63). Cross-site matched-pair analysis maps a continental bidirectional data network (3,512 pairs, 1,747 cross-site, p < 0.001). Evolutionary analysis traces System B through Wari antecedents to a pre-Wari human-hair origin. Collection audits of Santa Valley and Leymebamba prove both contain exclusively state copies, explaining 100 years of the "Spreadsheet Fallacy." Research conducted via Multi-Agent Deliberation Distillation (MADD) using the KARP platform with Claude, Gemini, and Grok. 30 findings, 9 falsifications.

**Update — June 2026:** MDP Paper III extends khipu analysis from 1D colour profiling to **full 3D tactile-spatial ontology**, exploiting fiber type, subsidiary tree depth, colour transition constraints, and canutito metadata across 54,403 cords. Sixteen structural findings identified including forbidden colour sequences, decimal run-length groupings, and an independent canutito metadata layer (98.6% colour-divergent from parent cords). Three hypotheses explicitly tested and falsified (spacing as punctuation, Hanan/Hurin midpoint split, cord thickness).

### Key Results

| # | Script | Period | Region | Corpus Size | Method | Key Finding |
|---|--------|--------|--------|------------|--------|-------------|
| 1 | **Proto-Cuneiform** | 3200 BCE | Mesopotamia | 31,191 signs, 6,819 tablets | Subtractive MDP | **100% accuracy** on 28-sign validation set |
| 2 | **Proto-Elamite** | 3100 BCE | Iran | 14,716 records | Standard MDP | **79 signs classified**, 64% corpus coverage |
| 3 | **Indus Valley** | 2600 BCE | South Asia | 11,280 signs, 2,543 inscriptions | Animal-Sign Enrichment | **Semantic locks** (G321→Hare: 195.6×) |
| 4 | **Cretan Hieroglyphic** | 2100 BCE | Crete | 317 inscriptions | Commodity-Ideogram MDP | **KU-RO cognate confirmed**; numbered signs *155/*156/*161 identified as probable commodity ideograms |
| 5 | **Linear A** | 1800 BCE | Crete | 1,712 inscriptions (419 tablets) | Commodity-Ideogram MDP | **120 Minoan words classified**; register separation; fraction domain divergence; two-tier summation |
| 6 | **Linear B** | 1400 BCE | Greece | 5,832 inscriptions | Control Validation | **Functional ontology proof** — MDP classifies by administrative context, not dictionary meaning |
| 7 | **Inca Khipu** | 1400 CE | South America | 619 khipus, 54,403 cords, 110,677 knots | Cord-Colour Domain Profiling | **Black cord knot inversion**; colour-value domain separation; provenance specialisation |
| 7b | **Inca Khipu (Paper III)** | 1400 CE | South America | 54,403 cords, 619 khipus | 3D Tactile-Spatial MDP | **Forbidden colour transitions**; fiber redefines domains (41×); subsidiary summation (17.4%); canutito independent metadata layer; decimal run-length groupings |

| 7c | **Inca Khipu (Paper IV)** | 1400 CE | South America | 612 khipus, 39,172 pendant cords | Shannon Entropy + System Classification | **720-colour alphabet**; 27% information loss quantified; 3 administrative systems (A/B/C); continental data network (p<0.001); Wari-to-hair evolutionary lineage; survival bias proven |

### The Administrative Segregation Principle

Across all seven scripts, MDP reveals a strong recurring structural pattern:

> *When human societies build administrative systems at scale, they tend to mathematically segregate their counting domains by commodity type — regardless of medium (clay, stone, string), continent, or millennium.*

This principle operates in Sumerian clay tablets (3200 BCE), Proto-Elamite accounting records (3100 BCE), Indus Valley seals (2600 BCE), Cretan Hieroglyphic stamps (2100 BCE), Minoan ledgers (1800 BCE), Mycenaean archives (1400 BCE), and Inca knotted cords (1400 CE).

---

### Repository Contents

#### Paper I Scripts (Published — DOI: [10.17613/mmjdt-ba806](https://doi.org/10.17613/mmjdt-ba806))

| File | Description |
|------|-------------|
| `protocuneiform_mdp.py` | **Study 1:** Validates Subtractive MDP on proto-cuneiform (Uruk IV/III). Achieves 100% on 28 known signs. |
| `protoelamite_mdp.py` | **Study 2:** Applies MDP to Proto-Elamite. Classifies 79 signs, reveals syntax and seal specialisation. |
| `indus_mdp.py` | **Study 3:** Adapts methodology for the Indus Valley Script. Discovers animal-sign semantic locks. |
| `Indus_scripts_terminal_output.md` | Full terminal output from the Indus analysis run. |

#### Paper II Scripts (Published — DOI: [10.17613/q536f-0wa13](https://doi.org/10.17613/q536f-0wa13))

| File | Description |
|------|-------------|
| `lineara_mdp.py` | **Study 4a:** Initial MDP pass on Linear A (all inscriptions). |
| `lineara_snoop.py` | **Study 4b:** Deep exploration script for Linear A (10 snoops). |
| `lineara_mdp_v2.py` | **Study 4c:** Master V2 analysis — tablet-filtered, 14-step analysis with register separation, summation verification, fraction divergence, scribe/room specialisation. |
| `linearb_mdp.py` | **Study 5:** Linear B control validation — 8-step analysis proving functional ontology vs semantic meaning. |
| `khipu_explore.py` | **Study 6a:** Schema explorer for the Open Khipu Repository SQLite database. |
| `khipu_mdp.py` | **Study 6b:** Full MDP analysis of Inca Khipu — 10-step cord-colour domain profiling. |
| `cretan_hieroglyphic_mdp.py` | **Study 7:** Cretan Hieroglyphic MDP — completes the Aegean Trilogy. |

#### Paper III Scripts (June 2026)

| File | Description |
|------|-------------|
| `khipu_mdp_v3_5_final.py` | **Study 6c:** Final 3D tactile-spatial analysis — 16 tests with plain-English explanations covering material metrology, topological syntax, categorical sorting, and hardware metadata. |
| `khipu_verify.py` | **Verification suite:** 8 independent raw SQL cross-checks validating all key findings. Includes Zipf's Law control experiments with 3 randomised baselines. |
| `khipu_audit.py` | **Database audit:** Complete schema scan of the OKR identifying 16+ previously unexploited variables (ATTACH_POS, SPACING, TERMINATION, THICKNESS, CORD_LEVEL, AXIS_ORIENTATION, canutito tables, primary cord metadata). |

#### Paper IV Scripts (July 2026)

| File | Description |
|------|-------------|
| `corpus_sweep.py` | **Corpus-wide census:** Classifies all 612 khipus into System A/B/C/Mixed with confidence scores. Produces the demographic N-counts cited in Paper IV. |
| `mdp_entropy.py` | **Shannon entropy analysis:** Computes information content for all 720 FULL_COLORs, quantifies the 27% information loss from compound collapse, colour-value taxonomy, and site-specific motif search. |
| `mdp_classifier.py` | **System classification:** 6-8 dimension composite scoring with documented thresholds, value distribution shape analysis, and clean summation with spacer auto-detection. |
| `mdp_matched_pairs.py` | **Continental network:** Cross-site matched-pair detection, formatting-direction analysis, and Monte Carlo null-hypothesis validation (N=1,000, p<0.001). |
| `verify_findings.sql` | **Glass Box SQL:** 8 raw SQL queries executable in DB Browser for SQLite against the public OKR database. Zero programming knowledge required. |

#### Papers

| File | Description |
|------|-------------|
| `MDP_Tri_Script_Paper_V1_Sharman_2026.pdf` | Paper I — Proto-Cuneiform, Proto-Elamite, Indus Valley |
| `MDP_Paper_II_v2_Sharman_2026.pdf` | Paper II — Aegean Trilogy + Inca Khipu |
| `MDP_Paper_IV_Sharman_2026.pdf` | Paper IV — Inca Khipu Dual Systems, Colour Alphabet, Continental Network |
| `MDP_Paper_III_Sharman_2026.pdf` | Paper III — Inca Khipu 3D Tactile Grammar |

#### Terminal Outputs

| File | Description |
|------|-------------|
| `lineara_mdp_terminal_output.md` | Full terminal output from Linear A V2 master analysis. |
| `linearb_mdp_terminal_output.md` | Full terminal output from Linear B control validation. |
| `khipu_mdp_terminal_output.md` | Full terminal output from Inca Khipu analysis (Paper II). |
| `cretan_hieroglyphic_mdp_terminal_output.md` | Full terminal output from Cretan Hieroglyphic analysis. |
| `corpus_sweep_output.md` | Full terminal output from the corpus-wide classification sweep (612 khipus). |
| `mdp_entropy_output.md` | Full terminal output from Shannon entropy colour analysis. |
| `mdp_classifier_output.md` | Full terminal output from system classification + shape analysis. |
| `mdp_matched_pairs_output.md` | Full terminal output from matched-pair network + Monte Carlo validation. |
| `khipu_mdp_v3_5_terminal_output.md` | Full terminal output from Paper III 3D tactile-spatial analysis (v3 + v3.5, 16 tests). |

---

### Data Sources & Reproduction Instructions

This repository does not include the source datasets due to size constraints. All data is freely available:

#### Paper I Data

| Source | Files Required | How to Obtain |
|--------|---------------|---------------|
| **CDLI** (Proto-Cuneiform & Proto-Elamite) | `cdliatf_unblocked.atf` (~83 MB), `cdli_cat.csv` (~148 MB) | [cdli.earth](https://cdli.earth/) or [github.com/cdli-gh/data](https://github.com/cdli-gh/data) |
| **Yajnadevam Indus Corpus** | `population-script.sql` (~430 KB) | [github.com/yajnadevam/indus-website](https://github.com/yajnadevam/indus-website) |

#### Paper II Data

| Source | Files Required | How to Obtain |
|--------|---------------|---------------|
| **Linear A Explorer** | `LinearAInscriptions.js` | [github.com/mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz) — download ZIP, extract |
| **Linear B Explorer** | `LinearBInscriptions.js`, `groups.js`, `lexicon.js` | [github.com/mwenge/linearb.xyz](https://github.com/mwenge/linearb.xyz) — download ZIP, extract |
| **Cretan Hieroglyphic Explorer** | `CretanHieroInscriptions.js`, `simpledictionary.js` | [github.com/mwenge/linear0.xyz](https://github.com/mwenge/linear0.xyz) — download ZIP, extract |
| **Open Khipu Repository** | `khipu.db` (37 MB SQLite) | [github.com/khipulab/open-khipu-repository](https://github.com/khipulab/open-khipu-repository) — DOI: [10.5281/zenodo.18025748](https://doi.org/10.5281/zenodo.18025748) |

#### Setup Instructions

```bash
# 1. Clone this repository
git clone https://github.com/souldriver007/mdp-ancient-scripts.git

# 2. Download data sources listed above into your preferred directories

# 3. Update file paths at the top of each script

# 4. Run any script:
python protocuneiform_mdp.py           # Paper I — Proto-Cuneiform (100% validation)
python protoelamite_mdp.py             # Paper I — Proto-Elamite
python indus_mdp.py                    # Paper I — Indus Valley
python lineara_mdp_v2.py               # Paper II — Linear A (master analysis)
python linearb_mdp.py                  # Paper II — Linear B (control validation)
python khipu_mdp.py                    # Paper II — Inca Khipu
python cretan_hieroglyphic_mdp.py      # Paper II — Cretan Hieroglyphic
python khipu_mdp_v3_5_final.py         # Paper III — Inca Khipu 3D ontology (16 tests)
python corpus_sweep.py                  # Paper IV — Corpus-wide system census (612 khipus)
python mdp_entropy.py                   # Paper IV — Shannon entropy colour analysis
python mdp_classifier.py                # Paper IV — System A/B/C classification
python mdp_matched_pairs.py             # Paper IV — Continental network + Monte Carlo
```

### Requirements

- Python 3.8+
- No external dependencies — uses only `re`, `csv`, `os`, `json`, `sqlite3`, and `collections` from the Python standard library
- Each script runs in under 60 seconds on a standard laptop

---

### Methodology Overview

#### The Core Principle

Ancient administrative scripts pair **commodity signs** (what is being counted) with **numerals** (how many). MDP exploits this pairing to classify unknown signs by their statistical co-occurrence with numerals and commodity ideograms.

#### Method Variants by Script

| Script | MDP Variant | Commodity Anchor | Numeral Anchor |
|--------|------------|-----------------|----------------|
| Proto-Cuneiform | Subtractive MDP | System-specific fractional anchors (N39A, N24, N51) | Polyvalent numerals (N01, N14, N34) |
| Proto-Elamite | Standard MDP | Dedicated numeral system codes (N39B, N23) | Domain-specific numerals |
| Indus Valley | Animal-Sign Enrichment | Iconographic field symbols (animals) | Stroke-sign modifiers (G1–G7) |
| Linear A / B / Cretan Hieroglyphic | Commodity-Ideogram MDP | Explicit commodity logograms (GRA, OLE, VIN, OVIS) | Decimal numerals + measure subunits (T, V, S, M, N, P) |
| Inca Khipu | Cord-Colour Domain Profiling | Pendant cord colour (64 Munsell codes) | Knot values (base-10 decimal: S/L/E knot types) |
| Inca Khipu (Paper III) | 3D Tactile-Spatial MDP | Colour + fiber + depth + canutito | Knot values + tree hierarchy + physical construction |

#### The Functional Ontology Discovery (Linear B)

When applied to the fully deciphered Linear B corpus, MDP achieved only 14% agreement with traditional Greek dictionaries — but this "failure" revealed the method's most important theoretical insight. MDP classifies words by their **administrative context** (which department handled them) rather than their **semantic meaning** (what they literally translate to). A slave (`do-e-ro` = *doelos*) is classified as GRAIN because slaves were administered through the grain-ration department. This provides economic historians with a **functional ontology** of ancient economies that pure linguistic translation cannot replicate.

#### The Khipu Cross-Medium Proof

By successfully applying MDP to Inca knotted cords — where cord colour replaces commodity ideograms and knot values replace written numerals — the method proves that the Administrative Segregation Principle operates across recording media. Black cords (LK) show a completely inverted knot-type signature (80% L-type vs 23% for all other colours), demonstrating metrological domain separation on string.

Paper III extends this to demonstrate that the khipu encodes information across six independent channels: cord colour, knot type, fiber material, tree depth, physical construction, and canutito wrapping — each operating independently and each contributing to the administrative ontology of the document.

---

### Development Trajectory

| Version | Date | Scripts | Key Achievement |
|---------|------|---------|----------------|
| v1–v3 | April 2026 | Proto-Cuneiform | Iterative refinement from 16% to 55% accuracy |
| v4 | April 2026 | Proto-Cuneiform | **100% accuracy** (28/28) — data normalisation fixes |
| v4 expanded | April 2026 | + Proto-Elamite, Indus | 79 PE signs classified; Indus semantic locks discovered |
| **Paper I published** | April 2026 | 3 scripts | DOI: [10.17613/mmjdt-ba806](https://doi.org/10.17613/mmjdt-ba806) |
| v5 | May 2026 | + Linear A | 120 Minoan words classified; register separation; fraction divergence |
| v6 | May 2026 | + Linear B | Functional ontology proof; measure subunit divergence confirmed |
| v7 | May 2026 | + Inca Khipu | Cross-medium validation; black cord knot inversion |
| v8 | May 2026 | + Cretan Hieroglyphic | Aegean Trilogy complete; KU-RO cognate confirmed |
| **Paper II published** | May 2026 | **7 scripts total** | DOI: [10.17613/q536f-0wa13](https://doi.org/10.17613/q536f-0wa13) |
| v9 | June 2026 | Inca Khipu (deep) | 3D tactile-spatial MDP: fiber, depth, transitions, canutito |
| **Paper III published** | June 2026 | **Khipu 3D Ontology** | DOI: [10.17613/c97d4-pgs78](https://doi.org/10.17613/c97d4-pgs78) — 16 findings, 3 falsified. "The Spreadsheet Fallacy" |

| v10 | July 2026 | Inca Khipu (deep) | Dual-system ontology, Shannon entropy, colour alphabet, continental network |
| **Paper IV final** | July 2026 | **30 findings, 9 falsifications** | 612 khipus classified; 720 colours; 3,512 matched pairs (p<0.001); hair khipu discovery; MADD methodology |

---

### The Indus Discovery

By adapting MDP to analyse **sign–animal co-occurrence**, we discovered that specific Indus signs are statistically **locked** to specific seal animals:

| Sign | Animal | Enrichment | Exclusivity |
|------|--------|------------|-------------|
| G321 | Hare | **195.6×** | 12/12 (100%) |
| G850 | Anthropomorphic | **60.5×** | 10/10 (100%) |
| G845 | Hare | **63.6×** | Shared with Anthropomorphic |
| G48 | Elephant | **35.6×** | Near-exclusive |
| G318 | Rhinoceros | **37.0×** | Near-exclusive |

This provides the first corpus-scale statistical evidence that Indus seal animals encode **institutional/departmental identity**.

---

### Research Infrastructure

This research was conducted using **KARP** (Knowledge Acquisition Research Protocol), a multi-agent AI deliberation system developed by SoulDriver Research that orchestrates Claude (Anthropic), GPT, Gemini (Google), and Grok (xAI) through structured adversarial research sessions using the **Multi-Agent Deliberation Distillation (MADD)** methodology.

Paper IV was researched and written across three extended sessions totalling approximately 12 hours, producing 30 findings, 9 falsifications, 4 standalone Python scripts, 8 SQL verification queries, and a 22-page publication-ready paper. The KARP Khipu Graph MCP server (25 tools) was hosted via Anthropic's Claude Desktop MCP integration for interactive corpus exploration. All findings were extracted from MCP tools into deterministic scripts for peer-review reproducibility (the "Glass Box" approach).

For more on KARP and SoulDriver Research, visit [souldriver.com.au](https://souldriver.com.au).

---

### License

MIT License — see [LICENSE](LICENSE) for details.

### Citation

If you use this code or methodology, please cite:

```
Sharman, A. (2026). Metrological Domain Profiling: A Computational Approach to
Administrative Architectures in Proto-Cuneiform, Proto-Elamite, and the Indus Valley
Script. SoulDriver Research. DOI: 10.17613/mmjdt-ba806

Sharman, A. (2026). Metrological Domain Profiling II: Functional Economic Ontologies
from the Aegean Bronze Age to the Inca Empire. SoulDriver Research.
DOI: 10.17613/q536f-0wa13

Sharman, A. (2026). Metrological Domain Profiling IV: Dual Systems, Redundant Channels,
and the Imperial Data Network of the Inca Khipu. SoulDriver Research.
DOI: 10.17613/2d7r8-26m93

Sharman, A. (2026). Metrological Domain Profiling III: Reconstructing the 3D Tactile
Grammar of the Inca Khipu. SoulDriver Research. DOI: 10.17613/c97d4-pgs78
```

### Acknowledgements

- **CDLI** (Cuneiform Digital Library Initiative) for open-access cuneiform data
- **Rob Hogan** (mwenge) for the lineara.xyz, linearb.xyz, and linear0.xyz digital corpus explorers
- **Open Khipu Repository** team (Mackinley FitzPatrick, Carrie Brezine, Gary Urton, Jon Clindaniel) for the digitised khipu database
- **Bryan K. Wells and Andreas Fuls** for the Interactive Corpus of Indus Texts (ICIT)
- **yajnadevam** for the digital ICIT extraction
- **Robert K. Englund and Peter Damerow** for foundational work on proto-cuneiform numeral systems
- **Jacob L. Dahl** for Proto-Elamite sign identifications
- **Michael Ventris and John Chadwick** for the decipherment of Linear B
- **Marcia and Robert Ascher** for foundational khipu research and the Code of the Quipu
- **Gary Urton** for the khipu binary coding theory and the Open Khipu Repository

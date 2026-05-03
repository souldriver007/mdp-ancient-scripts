'''
PS C:\Users\aazsh\Desktop\Latest_MDP_research> python cretan_hieroglyphic_mdp.py
===========================================================================
METROLOGICAL DOMAIN PROFILING — CRETAN HIEROGLYPHIC
The Grandmother of Linear A. The Aegean Trilogy Complete.
===========================================================================

Step 0: Parsing corpus...
  Total inscriptions: 317

  Inscriptions by site:
    unknown: 185
    Knossos: 68
    Malia: 63
    Prodromos: 1

===========================================================================
STEP 1: TOKEN CLASSIFICATION
===========================================================================

  Total tokens: 1198
  Unique words/signs: 434
  Numeral tokens: 158
  Commodity tokens: 20
  Tablets with commodities: 17/317
  Tablets with numerals: 46/317

  Top 20 commodity ideograms:
    BOS/MU₂: 9 → LIVESTOCK
    VIR₁: 2 → PERSON
    GRA: 2 → GRAIN
    VIR₂: 2 → PERSON
    VIR₃-: 1 → PERSON
    VIR₄-KU-RO-termination sign: 1 → PERSON
    NI-TI: 1 → FIGS
    BOS/MU₂-RO₃: 1 → LIVESTOCK
    BOS/MU₂-TI: 1 → LIVESTOCK

  Top 30 words/signs:
    KO-RO₃: 64 (tabs=59, numAdj=14%)
    KO-Rv: 32 (tabs=32, numAdj=3%)
    JA-RI-RE: 23 (tabs=23, numAdj=0%)
    JA-RI: 12 (tabs=12, numAdj=0%)
    A: 11 (tabs=10, numAdj=27%)
    A-SA: 11 (tabs=11, numAdj=0%)
    JA: 10 (tabs=10, numAdj=0%)
    RO₃: 10 (tabs=10, numAdj=10%)
    SA₂-RU: 8 (tabs=8, numAdj=0%)
    KI-TA-KU: 7 (tabs=7, numAdj=0%)
    *155: 7 (tabs=7, numAdj=57%)
    SA₂-RU-RE: 7 (tabs=7, numAdj=0%)
    SA: 7 (tabs=7, numAdj=0%)
    *156: 6 (tabs=6, numAdj=67%)
    RO: 6 (tabs=5, numAdj=17%)
    *152: 6 (tabs=4, numAdj=33%)
    Π: 6 (tabs=1, numAdj=100%)
    A-JA: 5 (tabs=5, numAdj=0%)
    *153: 5 (tabs=5, numAdj=20%)
    NA: 5 (tabs=5, numAdj=0%)
    A-KO: 5 (tabs=5, numAdj=0%)
    RI: 5 (tabs=5, numAdj=20%)
    RE: 4 (tabs=4, numAdj=0%)
    KU: 4 (tabs=4, numAdj=0%)
    SA-: 4 (tabs=4, numAdj=0%)
    SA-RA-NE: 4 (tabs=4, numAdj=0%)
    termination sign: 4 (tabs=4, numAdj=25%)
    MA: 4 (tabs=4, numAdj=50%)
    *161: 4 (tabs=3, numAdj=100%)
    KO: 4 (tabs=3, numAdj=25%)

  Measure subunits:

===========================================================================
STEP 2: CORE MDP — SIGN-COMMODITY DOMAIN PROFILING
===========================================================================

  Sign                           Freq Tabs NumA%  GRA  OIL  LIV  WOL  WNE  PER  BRZ Domain
  ---------------------------------------------------------------------------------------------------------
  KO-RO₃                         64   59   14%    0    0    2    0    0    1    0 LIVESTOCK
  KO-Rv                          32   32    3%    0    0    2    0    0    0    0 LIVESTOCK
  JA-RI-RE                       23   23    0%    0    0    1    0    0    0    0 LIVESTOCK
  JA-RI                          12   12    0%    0    0    0    0    0    0    0 NO_COMMODITY
  A                              11   10   27%    0    0    0    0    0    0    0 NO_COMMODITY
  A-SA                           11   11    0%    0    0    0    0    0    0    0 NO_COMMODITY
  JA                             10   10    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RO₃                            10   10   10%    0    0    2    0    0    0    0 LIVESTOCK
  SA₂-RU                          8    8    0%    0    0    0    0    0    1    0 PERSON
  KI-TA-KU                        7    7    0%    0    0    0    0    0    1    0 PERSON
  *155                            7    7   57%    0    0    0    0    0    0    0 NO_COMMODITY
  SA₂-RU-RE                       7    7    0%    0    0    1    0    0    0    0 LIVESTOCK
  SA                              7    7    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *156                            6    6   67%    0    0    0    0    0    0    0 NO_COMMODITY
  RO                              6    5   17%    0    0    0    0    0    0    0 NO_COMMODITY
  *152                            6    4   33%    0    0    1    0    0    0    0 LIVESTOCK
  Π                               6    1  100%    0    0    0    0    0    0    0 NO_COMMODITY
  A-JA                            5    5    0%    0    0    0    0    0    1    0 PERSON
  *153                            5    5   20%    1    0    0    0    0    0    0 GRAIN
  NA                              5    5    0%    0    0    0    0    0    0    0 NO_COMMODITY
  A-KO                            5    5    0%    0    0    0    0    0    1    0 PERSON
  RI                              5    5   20%    0    0    0    0    0    1    0 PERSON
  RE                              4    4    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KU                              4    4    0%    0    0    0    0    0    0    0 NO_COMMODITY
  SA-                             4    4    0%    0    0    1    0    0    0    0 LIVESTOCK
  SA-RA-NE                        4    4    0%    0    0    0    0    0    0    0 NO_COMMODITY
  termination sign                4    4   25%    0    0    0    0    0    0    0 NO_COMMODITY
  MA                              4    4   50%    0    0    0    0    0    0    0 NO_COMMODITY
  *161                            4    3  100%    0    0    0    0    0    0    0 NO_COMMODITY
  KO                              4    3   25%    0    0    0    0    0    0    0 NO_COMMODITY
  TI                              4    4    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KO-                             4    4    0%    0    0    1    0    0    0    0 LIVESTOCK
  SI-KU                           3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RU                              3    3   33%    0    0    0    0    0    0    0 NO_COMMODITY
  KU₄                             3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KA-RO₃                          3    3  100%    0    0    1    0    0    0    0 LIVESTOCK
  I                               3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  A-SA-                           3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  A-                              3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  -RO                             3    3   33%    0    0    0    0    0    0    0 NO_COMMODITY
  KI                              3    3   33%    0    0    0    0    0    0    0 NO_COMMODITY
  WA                              3    3    0%    0    0    1    0    0    0    0 LIVESTOCK
  *309                            3    3   33%    0    0    0    0    0    0    0 NO_COMMODITY
  -SA-                            3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RA                              3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RO₃-                            3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *180                            3    3   67%    0    0    0    0    0    0    0 NO_COMMODITY
  TA                              3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RU₂                             3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  -RO₃                            3    3   67%    0    0    1    0    0    0    0 LIVESTOCK
  Rv                              3    3    0%    0    0    0    0    0    0    0 NO_COMMODITY
  -DE-termination sign            3    1    0%    0    0    0    0    0    0    0 NO_COMMODITY
  A-DE-termination sign           3    3   33%    0    0    0    0    0    1    0 PERSON
  KU₂                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  AU-TI                           2    2    0%    0    0    0    0    0    1    0 PERSON
  NWA-KI-RU                       2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  KI-TU                           2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  TA-KU                           2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  *174                            2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  A₂-RU₂-BOS/MU₂-AI               2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RE-PI-termination sign          2    2    0%    0    0    1    0    0    0    0 LIVESTOCK
  SI-                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RO₂                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  JA-                             2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  DE                              2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  Rv-                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *167                            2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  *307                            2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *302                            2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  -NE                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KU-RO                           2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  SA₂                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  QE                              2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  RU-RE                           2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  RO-RE-SA                        2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  TI-KI                           2    2    0%    0    0    1    0    0    0    0 LIVESTOCK
  -Rv                             2    2    0%    0    0    1    0    0    0    0 LIVESTOCK
  KI-BOS/MU₂-RO₃                  2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  JA-A₃                           2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  Rv-SI-MA                        2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  A₂                              2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  KU-QE-RE                        2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KU₂-RO₃-WA-VIR₃                 2    2    0%    0    0    1    0    0    1    0 LEANING_LIVESTOCK
  *157                            2    2  100%    0    0    0    0    0    0    0 NO_COMMODITY
  -JA                             2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  KU₃                             2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  TE                              2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *181                            2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  TU                              2    2   50%    0    0    0    0    0    1    0 PERSON
  ZE                              2    2   50%    0    0    0    0    0    1    0 PERSON
  SO-RO                           2    2   50%    0    0    0    0    0    0    0 NO_COMMODITY
  *164                            2    1  100%    0    0    0    0    0    0    0 NO_COMMODITY
  *165                            2    1  100%    0    0    0    0    0    0    0 NO_COMMODITY
  NA-RO₂                          2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  -RE                             2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  E?                              2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KO-SA₂-RA₄                      2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  KI-TA-                          2    2    0%    0    0    0    0    0    0    0 NO_COMMODITY
  *160                            2    1  100%    0    0    1    0    0    1    0 LEANING_LIVESTOCK
  *176                            2    1  100%    0    0    1    0    0    1    0 LEANING_LIVESTOCK

===========================================================================
STEP 3: COMMODITY ECONOMIC PARAMETERS
===========================================================================

  Domain            Count  Median    Mean     Max Measures
  -----------------------------------------------------------------
  GRAIN               2     200   116.0     200
  PERSON              3      22    34.0      60

===========================================================================
STEP 4: MEASURE SUBUNIT DOMAIN DIVERGENCE
===========================================================================

  Do Cretan Hieroglyphic commodities use different measurement systems?
  (Same question asked of Linear A and Linear B — does the pattern hold?)

===========================================================================
STEP 5: UNDECIPHERED NUMBERED SIGNS (*NNN)
===========================================================================

  Numbered signs (undeciphered ideograms): 39
  *155         freq=  7, numAdj= 57%, co-occurs: none → NO_COMMODITY
  *156         freq=  6, numAdj= 67%, co-occurs: none → NO_COMMODITY
  *152         freq=  6, numAdj= 33%, co-occurs: LIVESTOCK=1 → LIVESTOCK
  *153         freq=  5, numAdj= 20%, co-occurs: GRAIN=1 → GRAIN
  *161         freq=  4, numAdj=100%, co-occurs: none → NO_COMMODITY
  *309         freq=  3, numAdj= 33%, co-occurs: none → NO_COMMODITY
  *180         freq=  3, numAdj= 67%, co-occurs: none → NO_COMMODITY
  *174         freq=  2, numAdj= 50%, co-occurs: none → NO_COMMODITY
  *167         freq=  2, numAdj= 50%, co-occurs: none → NO_COMMODITY
  *307         freq=  2, numAdj=  0%, co-occurs: none → NO_COMMODITY
  *302         freq=  2, numAdj=  0%, co-occurs: none → NO_COMMODITY
  *157         freq=  2, numAdj=100%, co-occurs: none → NO_COMMODITY
  *181         freq=  2, numAdj=  0%, co-occurs: none → NO_COMMODITY
  *164         freq=  2, numAdj=100%, co-occurs: none → NO_COMMODITY
  *165         freq=  2, numAdj=100%, co-occurs: none → NO_COMMODITY
  *160         freq=  2, numAdj=100%, co-occurs: LIVESTOCK=1, PERSON=1 → LEANING_LIVESTOCK
  *176         freq=  2, numAdj=100%, co-occurs: LIVESTOCK=1, PERSON=1 → LEANING_LIVESTOCK
  *154         freq=  1, numAdj=  0%, co-occurs: none → ?
  *182         freq=  1, numAdj=100%, co-occurs: none → ?
  *163         freq=  1, numAdj=  0%, co-occurs: none → ?
  *308         freq=  1, numAdj=  0%, co-occurs: none → ?
  *159         freq=  1, numAdj=100%, co-occurs: none → ?
  *172         freq=  1, numAdj=100%, co-occurs: none → ?
  *177         freq=  1, numAdj=100%, co-occurs: none → ?
  *173         freq=  1, numAdj=100%, co-occurs: none → ?
  *179         freq=  1, numAdj=100%, co-occurs: none → ?
  *162         freq=  1, numAdj=100%, co-occurs: none → ?
  *171         freq=  1, numAdj=100%, co-occurs: none → ?
  *178         freq=  1, numAdj=100%, co-occurs: none → ?
  *158         freq=  1, numAdj=100%, co-occurs: none → ?
  *175         freq=  1, numAdj=100%, co-occurs: none → ?
  *134         freq=  1, numAdj=  0%, co-occurs: none → ?
  *004         freq=  1, numAdj=  0%, co-occurs: LIVESTOCK=1 → ?
  *169         freq=  1, numAdj=100%, co-occurs: none → ?
  *168         freq=  1, numAdj=100%, co-occurs: none → ?
  *166         freq=  1, numAdj=100%, co-occurs: none → ?
  *159bis      freq=  1, numAdj=  0%, co-occurs: none → ?
  *016         freq=  1, numAdj=100%, co-occurs: none → ?
  *025         freq=  1, numAdj=100%, co-occurs: none → ?

===========================================================================
STEP 6: LINEAR A COGNATE COMPARISON
===========================================================================

  Signs shared with Linear A (potential cognates):
    KU-RO: CH freq=2, LA note='total (Linear A)', CH domain=NO_COMMODITY
    JA: CH freq=10, LA note='frequent sign', CH domain=NO_COMMODITY
    A-JA: CH freq=5, LA note='? (Linear A)', CH domain=PERSON
    KO: CH freq=4, LA note='? (Linear A)', CH domain=NO_COMMODITY
    TA: CH freq=3, LA note='? (Linear A)', CH domain=NO_COMMODITY
    RO: CH freq=6, LA note='? (Linear A)', CH domain=NO_COMMODITY

  Syllabic signs shared with Linear A: 30
    A, AI, DE, DO, I, JA, KA, KI, KO, KU, MA, MI, NA, NE, NWA, QE, RA, RE, RI, RO, RU, SA, SI, TA, TE, TI, TU, WA, WI, ZE

===========================================================================
STEP 7: SUMMATION CHECKING
===========================================================================

  Tablets with 3+ lines of numerals: 16
  Last line = sum of others (exact): 1
  Close matches (±2): 0
  Sum match rate: 6.2%

===========================================================================
STEP 8: DOMAIN CLASSIFICATION SUMMARY
===========================================================================

  NO_COMMODITY (73 signs):
    JA-RI: 12
    A: 11
    A-SA: 11
    JA: 10
    *155: 7
    SA: 7
    *156: 6
    RO: 6

  LIVESTOCK (14 signs):
    KO-RO₃: 64
    KO-Rv: 32
    JA-RI-RE: 23
    RO₃: 10
    SA₂-RU-RE: 7
    *152: 6
    SA-: 4
    KO-: 4

  PERSON (9 signs):
    SA₂-RU: 8
    KI-TA-KU: 7
    A-JA: 5
    A-KO: 5
    RI: 5
    A-DE-termination sign: 3
    AU-TI: 2
    TU: 2

  LEANING_LIVESTOCK (3 signs):
    KU₂-RO₃-WA-VIR₃: 2
    *160: 2
    *176: 2

  GRAIN (1 signs):
    *153: 5

===========================================================================
CRETAN HIEROGLYPHIC MDP ANALYSIS — COMPLETE
===========================================================================

  CORPUS:
    Inscriptions: 317
    With commodities: 17
    With numerals: 46
    Unique signs: 434
    Commodity types found: 9

  MDP RESULTS:
    Signs classified: 100
      NO_COMMODITY: 73
      LIVESTOCK: 14
      PERSON: 9
      LEANING_LIVESTOCK: 3
      GRAIN: 1

  AEGEAN TRILOGY STATUS:
    Cretan Hieroglyphic (~2100 BCE) ← YOU ARE HERE
    Linear A (~1800 BCE) ← Done (120 words classified)
    Linear B (~1400 BCE) ← Done (functional ontology proof)

  Three generations. One method. One universal principle.

PS C:\Users\aazsh\Desktop\Latest_MDP_research>
'''
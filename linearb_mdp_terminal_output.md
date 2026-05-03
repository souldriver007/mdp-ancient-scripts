'''

PS C:\Users\aazsh\Desktop\Latest_MDP_research> python linearb_mdp.py
===========================================================================
METROLOGICAL DOMAIN PROFILING — LINEAR B CONTROL VALIDATION
===========================================================================

Step 0: Parsing corpus...
  Total inscriptions: 5832
  Ground truth categories loaded: 345

  Inscriptions by site:
    Knossos: 4223
    Pylos: 986
    Thebes: 363
    Mycenae: 87
    Vases - Thebes: 61
    Vases - Tiryns: 24
    Tiryns: 24
    Vases - Khania: 23
    Vases - Mycenae: 14
    Khania: 7

===========================================================================
STEP 1: CORPUS STATISTICS
===========================================================================

  Tablets with data: 5832
  Total tokens: 62148
  Unique words: 5823
  Unique commodity tokens: 65

  Top 25 commodity ideograms:
    OVIS:m: 1070 → LIVESTOCK
    VIR: 864 → PERSON
    GRA: 584 → GRAIN
    OVIS:f: 427 → LIVESTOCK
    LANA: 415 → WOOL
    MUL: 247 → WOMAN
    AES: 226 → BRONZE
    HORD: 192 → GRAIN
    OLE: 155 → OIL
    CAP:f: 93 → LIVESTOCK
    EQU: 81 → LIVESTOCK
    NI: 75 → FIGS
    VIN: 74 → WINE
    OVIS: 60 → LIVESTOCK
    ROTA: 56 → WHEEL
    OLIV: 53 → OLIVES
    CAP:m: 51 → LIVESTOCK
    AUR: 44 → GOLD
    AROM: 43 → SPICE
    BOS: 43 → LIVESTOCK
    CROC: 43 → SPICE
    FAR: 42 → FLOUR
    OVIS:x: 42 → LIVESTOCK
    BOS:m: 38 → LIVESTOCK
    SUS:f: 27 → LIVESTOCK

  Top 30 words:
    inf.: 1178
    sup.: 1120
    o: 319
    pa-ro: 272 ← paro (from/at (the place of))
    ko-wo: 218 ← korwos (boy/youth)
    pe-mo: 201
    o-na-to: 187
    e-ke: 173
    to-so-de: 158
    ko-to-na: 151
    ko-wa: 151 ← korwa (girl/youth)
    to-so: 122 ← toson (so much/total)
    v.↓: 114
    pa: 103
    e-ke-qe: 101
    ki: 100
    te-o-jo: 97
    ke-ke-me-na: 94
    supra: 92
    da-mo: 90 ← damos (district/people)
    do-e-ro: 90 ← doelos (slave/servant)
    pe: 89
    jo: 84
    lat.: 75
    ko: 72
    a: 71
    -jo: 69
    do-e-ra: 66 ← doela (female slave)
    ku-ta-to: 66
    a-: 66

===========================================================================
STEP 2: CORE MDP — COMMODITY DOMAIN PROFILING
===========================================================================

  Word                      Freq Tabs  NumA%  GRA  OIL  LIV  WOL  WNE  PER  BRZ Domain               Validation
  -----------------------------------------------------------------------------------------------------------------------------
  inf.                    1178 1143     1%   40    5   81   23    9   37    1 CROSS-COMMODITY
  sup.                    1120 1092     0%   33    7   68   26    4   42    1 CROSS-COMMODITY
  o                        319  271    83%   11    2  169   76    1    7    1 LEANING_LIVESTOCK
  pa-ro                    272  120    77%   73    1   20    2    2    3    0 GRAIN                ~ paro=from/at (the place of) (exp:?)
  ko-wo                    218  176    92%   29    0    1    1    1   44    0 LEANING_WOMAN        ✗ korwos=boy/youth (exp:PERSON)
  pe-mo                    201   69    92%   69    0    0    0    0    1    0 GRAIN
  o-na-to                  187   93    76%   93    0    0    0    0    1    0 GRAIN
  e-ke                     173   74    82%   62    0    2    0    0    2    0 GRAIN
  to-so-de                 158   75    87%   58    0    1    0    1    4   16 GRAIN
  ko-to-na                 151   86    66%   85    0    0    0    0    1    0 GRAIN
  ko-wa                    151  136    89%   28    0    0    0    0    4    0 WOMAN                ✗ korwa=girl/youth (exp:PERSON)
  to-so                    122   64    79%   22    5    2    1    2   18    1 WEAK_GRAIN           ✗ toson=so much/total (exp:CROSS-COMMODITY)
  v.↓                      114  114     0%   10    9   24   12    7    2    0 CROSS-COMMODITY
  pa                       103   92    80%    2    1   75    1    1    0    0 LIVESTOCK
  e-ke-qe                  101   64    52%   62    0    0    0    0    0    0 GRAIN
  ki                       100   88    69%    2    0   74   28    0    1    0 LIVESTOCK
  te-o-jo                   97   34    79%   34    0    0    0    0    1    0 GRAIN
  ke-ke-me-na               94   51    61%   48    0    0    0    0    0    0 GRAIN
  supra                     92   92     2%    2    3   52    1    4    2    1 LIVESTOCK
  da-mo                     90   56    79%   50    0    2    0    1    1    0 GRAIN                ~ damos=district/people (exp:?)
  do-e-ro                   90   49    71%   33    0    4    0    0    6    5 GRAIN                ✗ doelos=slave/servant (exp:PERSON)
  pe                        89   84    91%    3    0   63    2    0    1    0 LIVESTOCK
  jo                        84   83    44%    6    2    7    1    0   10    3 CROSS-COMMODITY
  lat.                      75   75     0%    5    0   10   11    3    6    0 CROSS-COMMODITY
  ko                        72   70    58%   14    0    4    2    3    7    1 CROSS-COMMODITY
  a                         71   69    31%    5    0    9    0    1    7    6 CROSS-COMMODITY
  -jo                       69   66    41%   10    2   16    1    1    8    2 WEAK_LIVESTOCK
  do-e-ra                   66   33    70%   27    0    0    0    0    1    0 GRAIN                ✗ doela=female slave (exp:PERSON)
  ku-ta-to                  66   66    70%    0    0   57   14    0    0    0 LIVESTOCK
  a-                        66   63    52%    3    2    6    0    0    5    1 CROSS-COMMODITY
  do-so-mo                  65   17    92%   15    0    1    0    1    0    0 GRAIN
  pu-ro                     64   52    81%   21    0    3    1    2   21    0 CROSS-COMMODITY      ~ Pylos=Pylos (exp:?)
  ja                        62   61    42%    2    0    8    2    0    1    1 CROSS-COMMODITY
  e                         59   43    37%    3    1    2    1    0    8    1 WEAK_PERSON
  to                        57   55    56%    8    0   10    3    2    9    2 CROSS-COMMODITY
  v.→                       57   57     0%    6    0   14    1    3    6    0 CROSS-COMMODITY
  v.                        56   56     0%    6    0   10    4    2    8    1 CROSS-COMMODITY
  sigillum                  54   54     2%    2    3    5    1    4    2    1 CROSS-COMMODITY
  ko-                       54   51    70%   12    1    1    1    0    3    0 LEANING_GRAIN
  wa                        52   52    44%    6    0    0    0    0    2    1 CROSS-COMMODITY
  ka-ke-we                  52   35    37%    0    1    0    0    0    1   18 BRONZE
  ro                        51   49    65%    9    1   11    0    0    4    0 CROSS-COMMODITY
  de                        50   47    54%   12    6    1    1    2    2    2 WEAK_GRAIN
  -ja                       50   49    44%    4    0    3    2    0    3    2 CROSS-COMMODITY
  o-pe-ro                   48   42    72%    3    0    2    0    0   12    0 LEANING_PERSON       ✗ ophelos=deficit/owed (exp:CROSS-COMMODITY)
  pa-i-to                   47   47    36%    2    0   29    2    0    0    0 LIVESTOCK            ~ Phaistos=Phaistos (exp:?)
  wo                        47   47    43%    5    1   10    0    0    2    2 LEANING_LIVESTOCK
  no                        46   45    35%    3    2    5    4    0    6    0 CROSS-COMMODITY
  da-wo                     44   44    52%    1    0   30    1    0    0    0 LIVESTOCK
  ne                        44   31    75%    2    0    8    6    0    3    0 CROSS-COMMODITY
  e-                        44   43    43%    6    0    3    0    0    1    1 WEAK_GRAIN
  ku                        42   25    59%    2    1    0   13    0    0    0 WOOL
  o-da-a2                   42   23    59%   10    0    1    0    1    2    0 GRAIN
  di                        41   29    83%    0    0    1    0    0    2    1 WOMAN
  ko-re-te                  41    7    97%    0    0    1    0    0    0    1 WEAK_GOLD            ~ koreter=mayor/governor (exp:?)
  e-ra                      40   39    38%    1    1   21    4    1    1    0 LIVESTOCK
  ka                        40   39    28%    6    0    5    2    1    1    0 CROSS-COMMODITY
  e-ko-so                   39   39    67%    1    0   32    1    0    0    0 LIVESTOCK
  da-*22-to                 39   33    77%    1    0   26    1    0    1    0 LIVESTOCK
  o-pi                      39   32    42%    0    1    1    5    0    5    0 WEAK_WOOL            ~ opi=over/for (exp:?)
  qa-ra                     38   35    42%    1    0   19    0    0    1    0 LIVESTOCK
  -to                       37   37    41%    7    0   10    0    0    4    0 LEANING_LIVESTOCK
  ru-ki-to                  37   37    57%    0    1   31    0    0    0    0 LIVESTOCK
  ta                        37   37    35%    1    0    5    1    0    5    1 WEAK_PERSON
  ra                        37   37    43%    3    0    6    2    0    0    0 WEAK_LIVESTOCK
  we-da-ne-wo               35   22    94%   12    0    6    0    0    1    0 GRAIN
  me-zo-e                   34   24    73%    0    0    0    0    0    0    0 WOMAN
  -ro                       33   33    39%    9    0    3    0    1    1    1 LEANING_GRAIN
  ma                        33   20    52%    2    0    3    0    0    1    0 CROSS-COMMODITY
  -ta                       32   31    31%    1    0    3    0    0    4    0 LEANING_PERSON
  ti-ri-to                  32   32    44%    0    0   19    0    0    0    0 LIVESTOCK
  o-                        31   30    42%    7    0    1    0    0    3    0 LEANING_GRAIN
  to-sa                     31   28    61%    2    0    4    2    0    1    0 CROSS-COMMODITY      ~ tosa=so much (fem.) (exp:?)
  ra-to                     31   31    58%    0    0   25    0    0    0    0 LIVESTOCK
  pa-we-a                   30   30    57%    0    0    0    8    0    0    0 WOOL
  ka-                       30   30    20%    4    0    4    2    1    0    1 CROSS-COMMODITY
  ke                        29   26    41%    3    0    1    2    0    3    1 CROSS-COMMODITY
  i                         29   29    45%    7    1    2    0    2    2    0 CROSS-COMMODITY
  te                        29   28    38%    4    1    2    1    0    3    0 CROSS-COMMODITY
  do-ti-ja                  29   29    59%    1    0   20    1    0    0    0 LIVESTOCK
  ri-jo-no                  28   28    86%    0    0   26    1    0    0    0 LIVESTOCK
  vestigia                  28   25    14%    2    0    5    2    0    3    1 CROSS-COMMODITY
  o-pa                      28   27    29%    1    0    9    0    0    1    0 LIVESTOCK
  su-ri-mo                  27   27    63%    0    0   20    2    0    1    0 LIVESTOCK
  to-                       27   24    59%    4    2    1    2    0    2    0 CROSS-COMMODITY
  wo-wo                     27   14    93%    0    0    7    1    0    2    0 LIVESTOCK
  pars                      26   25     0%    6    0    5    3    4    4    0 CROSS-COMMODITY
  sine                      26   25     0%    6    0    5    3    4    4    0 CROSS-COMMODITY
  regulis                   26   25     0%    6    0    5    3    4    4    0 CROSS-COMMODITY
  me-no                     26   26    35%    0    9    0    1    0    1    2 OIL
  a-pu-do-si                26   26    50%    0    4    0    0    0    3    0 LEANING_OIL
  -na                       25   24    32%   10    0    1    0    0    0    0 GRAIN
  sa                        25   23    50%    0    0    7    2    1    1    1 LEANING_LIVESTOCK
  reliqua                   25   24     0%    6    0    4    2    3    4    0 CROSS-COMMODITY
  fragmentum                25   11     0%    2    0    2    1    0    1    0 CROSS-COMMODITY
  po-                       25   24    40%    2    1    3    1    0    1    2 CROSS-COMMODITY
  ki-ti-me-na               24   17    92%   17    0    0    0    0    1    0 GRAIN
  a-ke-o-jo                 24    9    96%    0    0    8    0    0    0    0 LIVESTOCK
  ra-su-to                  24   23    65%    0    0   17    1    0    1    0 LIVESTOCK
  ta-ra-si-ja               24   21     8%    0    0    0    1    0    1   16 BRONZE
  u-ta-jo-jo                24   24    46%    0    0   24    0    0    0    0 LIVESTOCK
  me                        24   22    39%    1    0    0    0    0    1    0 WEAK_WOMAN
  tu-ni-ja                  23   23    65%    0    0   15    2    0    0    0 LIVESTOCK
  ma-ro-pi                  23    4   100%    0    0    4    0    0    0    0 LIVESTOCK
  u-ta-jo                   23   23    39%    0    0   20    0    0    0    0 LIVESTOCK
  we-we-si-jo               23   23    83%    0    0   16    0    0    1    3 LIVESTOCK
  pa-                       23   22    52%    7    0    6    0    0    0    1 LEANING_GRAIN
  ke-ro-si-ja               22    2   100%    0    0    0    1    0    2    0 LEANING_PERSON
  e-ko-te                   21   17     5%    1    0    0    0    0    2   14 BRONZE
  we                        21   20    57%    1    0    6    2    0    2    0 LEANING_LIVESTOCK
  -no                       20   19    25%    2    0    1    0    0    6    1 LEANING_PERSON
  e-ko-si                   20   16    15%    6    0    0    0    0    1    2 GRAIN
  o-no                      20   18    75%    2    5    3    4    1    3    0 CROSS-COMMODITY
  tu-na-no                  20   20    85%    0    0    0   12    0    0    0 WOOL
  ri                        19   18    32%    0    0    1    0    0    0    0 LEANING_SPICE
  me-                       19   19    68%    2    0    1    0    1    1    0 LEANING_WOMAN
  to-sa-de                  19   16    68%    1    0    0    0    0    0    0 LEANING_GRAIN
  ra-ja                     19   19    58%    0    0   15    0    0    1    0 LIVESTOCK
  da-mi-ni-jo               19   19    68%    0    0   15    4    0    1    0 LIVESTOCK
  a-ja-me-no                19    8    82%    0    0    0    0    0    0    0 NO_COMMODITY
  ku-pi-ri-jo               18   18    78%    1    7    2    1    0    0    1 LEANING_OIL
  te-                       18   18    50%    3    0    3    1    0    1    0 CROSS-COMMODITY
  we-we-si-jo-jo            18   18    72%    0    0   13    2    0    0    0 LIVESTOCK
  i-qi-ja                   18   18    39%    0    0    0    0    0    0    0 NO_COMMODITY
  ka-ko                     18   13    89%    0    0    0    0    0    1   12 BRONZE               ✓ khalkos=bronze (exp:BRONZE)
  ko-no                     18   12    76%    1    0    0    0    0    0    1 WEAK_GRAIN
  -so                       18   18    33%    1    0    3    1    0    3    0 WEAK_PERSON
  ku-                       18   18    33%    0    0    4    0    0    1    0 LIVESTOCK
  wo-ka                     18   18   100%    0    0    0    0    0    0    0 WHEEL
  we-je-ke-e                18   18    94%    0    0    0    0    0    0    0 WHEEL
  u-ta-no                   18   17    17%    0    1   10    0    0    0    0 LIVESTOCK
  ka-na-ko                  18    5    92%    0    0    0    0    0    0    0 SPICE
  po-ro-ko-re-te            18    3   100%    0    0    0    0    0    0    1 LEANING_GOLD         ~ prokoreter=deputy governor (exp:?)
  e-qe-ta                   17   11    24%    0    0    0    0    0   10    0 PERSON
  po                        17   17    59%    0    0    1    0    0    6    0 PERSON
  pi                        17   15    47%    0    0    2    0    0    1    0 LEANING_LIVESTOCK
  a-ta-ra-si-jo             17   16    18%    0    0    0    0    0    1   16 BRONZE
  -we                       17   17    53%    0    3    2    1    2    3    1 CROSS-COMMODITY
  da-                       17   16    35%    3    0    5    0    0    0    0 LEANING_LIVESTOCK
  ke-                       17   17    47%    5    0    1    1    0    1    0 GRAIN
  i-je-re-ja                17   12    59%    8    1    1    1    0    1    0 LEANING_GRAIN        ~ hiereia=priestess (exp:?)
  se-to-i-ja                17   17    47%    0    0    6    2    0    3    0 LEANING_LIVESTOCK
  ko-to-no-o-ko             17   11    82%   11    0    0    0    0    0    0 GRAIN
  u                         17   17    47%    0    0    1    0    0    5    2 PERSON
  qe                        17   17    53%    4    0    2    0    1    4    1 CROSS-COMMODITY
  pa-ra-jo                  16    8    81%    1    0    4    0    0    1    0 LIVESTOCK
  a-si-ja-ti-ja             16    8    56%    0    0    3    0    0    1    2 LEANING_LIVESTOCK
  -i                        16   15    62%    3    1    0    0    1    0    0 CROSS-COMMODITY
  o-u-qe                    16   11    43%    3    0    0    0    0    0    0 GRAIN
  e-re-pa-te-jo             16    9    75%    0    0    0    0    0    0    0 NO_COMMODITY
  mo                        16   13    44%    5    0    3    0    0    0    0 LEANING_GRAIN
  po-ni-ki-jo               16   15    56%    0    0    0    0    0    2    0 PERSON
  o-u-di-do-si              16   14   100%    0    0    0    0    0    0    0 NO_COMMODITY
  po-ti-ni-ja               16   16    69%    0    5    1    1    0    2    0 LEANING_OIL
  me-wi-jo-e                16   11   100%    0    0    0    0    0    0    0 WOMAN
  a-ka                      16   16    56%    0    0   11    0    0    1    0 LIVESTOCK
  a-ta-o                    16    4   100%    2    0    0    0    0    2    1 WEAK_GRAIN
  te-o                      16   16    44%    8    1    0    1    0    0    0 GRAIN
  na                        15   15    40%    5    0    1    0    0    0    0 GRAIN
  ki-ri-jo-te               15   15     0%    0    0   15    0    0    0    0 LIVESTOCK
  o-ka                      15   10    27%    3    0    0    0    0    5    0 PERSON
  -qe                       15   14    21%    4    0    2    0    0    2    1 LEANING_GRAIN
  ti                        15   15    33%    0    0    4    0    0    0    0 LIVESTOCK
  da                        15   15    47%    1    0    4    1    0    1    0 LEANING_LIVESTOCK
  so                        15   15    60%    2    2    2    0    0    1    0 CROSS-COMMODITY
  ta-ra-nu                  15    7    79%    0    0    0    0    0    0    0 NO_COMMODITY
  -wo                       15   15    73%    2    0    3    0    0    3    0 CROSS-COMMODITY
  qa                        15   15    13%    2    0    0    1    0    0    0 GRAIN
  po-se-da-o-ne             14   14    93%   10    2    2    2    1    0    0 LEANING_GRAIN
  e-ka-ra-e-we              14   14    71%    0    0   12    0    0    0    0 LIVESTOCK
  ja-                       14   14    21%    0    0    0    0    0    0    0 NO_COMMODITY
  i-                        14   14    21%    0    0    1    1    0    0    0 WEAK_TEXTILES
  si                        14   14    43%    0    1    2    0    1    1    0 CROSS-COMMODITY
  to-jo                     14   14    71%    3    0    0    0    0    0    0 LEANING_FLOUR
  se                        14   14    79%    0    0   10    0    0    2    0 LIVESTOCK
  te-re-ta                  14   13    43%    6    0    0    0    0    4    0 LEANING_GRAIN        ~ telestai=land holders (exp:?)
  me-ta-pa                  14   14    86%    0    0    3    0    0    3    1 WEAK_WOMAN
  ka-ma                     14   10    43%    5    0    0    1    0    1    0 LEANING_GRAIN
  pa-si-te-o-i              14   12    93%    0    7    0    0    0    0    0 OIL
  pi-*82                    14   11    86%    0    0    4    0    0    2    1 LEANING_LIVESTOCK
  mi                        14    7    73%    0    0    0    1    0    1    0 LEANING_TEXTILES
  di-wi-je-we               13   13    92%   12    0    1    0    0    0    0 GRAIN
  o-po-qo                   13   13    38%    0    0    0    0    0    0    0 NO_COMMODITY
  a-nu-to                   13   13    54%    2    0    0    0    0    1    0 LEANING_FLOUR
  me-zo                     13   11    77%    0    0    0    1    0    0    0 LEANING_WOMAN
  -wa                       13   13    62%    2    0    0    1    0    1    0 CROSS-COMMODITY
  -mo                       13   12    46%    5    0    2    0    0    1    0 LEANING_GRAIN
  a-ko-da-mo                13   13    92%    1    0    0    0    0    1    0 OLIVES
  re                        13   13    62%    0    0    1    1    0    0    0 WEAK_SPICE
  ro-u-so                   13   13    46%    2    0    3    0    1    0    2 CROSS-COMMODITY
  -de                       13   13    31%    3    1    0    0    1    0    1 LEANING_GRAIN
  -o                        13   13    46%    1    0    1    1    0    4    0 LEANING_PERSON
  e-ru-ta-ra                13    9    92%    0    0    0    0    0    1    0 SPICE
  pu-so                     13   13    62%    0    0   10    0    0    1    0 LIVESTOCK
  du-ni-jo                  13   12    69%    6    0    1    0    1    3    0 LEANING_GRAIN
  a-ke-re-wa                13   12    77%    1    0    2    0    0    4    3 WEAK_PERSON
  zo-wa                     13   13    69%    4    0    0    0    0    1    0 LEANING_GRAIN
  pe-i                      12    6    25%    0    0    0    0    0    5    0 PERSON
  we-                       12   12    50%    3    0    2    0    0    0    1 LEANING_GRAIN
  o-pi-i-ja-pi              12   12    42%    0    0    0    0    0    0    0 NO_COMMODITY

===========================================================================
STEP 3: GROUND TRUTH VALIDATION (groups.js categories)
===========================================================================

  Do MDP domain classifications match pre-tagged tablet categories?

  Lists of Personnel (71 tablets): CROSS-COMMODITY=62, LEANING_WOMAN=27, WOMAN=23, PERSON=19, LIVESTOCK=17
  Land Tenure (59 tablets): GRAIN=269, CROSS-COMMODITY=40, LEANING_GRAIN=33, WEAK_GRAIN=18, LIVESTOCK=12
  Military Equipment (38 tablets): NO_COMMODITY=21, CROSS-COMMODITY=16, LIVESTOCK=9, WEAK_LIVESTOCK=3, WEAK_TEXTILES=2
  Industrial Production (36 tablets): CROSS-COMMODITY=26, BRONZE=20, WOOL=11, GRAIN=9, LEANING_LIVESTOCK=4
  Taxation (34 tablets): CROSS-COMMODITY=16, GRAIN=12, LEANING_LIVESTOCK=11, NO_COMMODITY=7, BRONZE=7
  Religion and Ritual (27 tablets): CROSS-COMMODITY=32, OIL=12, LEANING_GRAIN=6, LEANING_OIL=4, WEAK_GRAIN=4
  Agricultural Produce (23 tablets): CROSS-COMMODITY=17, SPICE=6, LIVESTOCK=5, LEANING_LIVESTOCK=5, LEANING_OIL=4
  Vessels and Furniture (19 tablets): NO_COMMODITY=18, CROSS-COMMODITY=9, LEANING_LIVESTOCK=2, OIL=1, LEANING_GRAIN=1
  Livestock (17 tablets): LIVESTOCK=29, LEANING_LIVESTOCK=13, GRAIN=3, LEANING_OIL=2, LEANING_GRAIN=1
  Miscellaneous Texts (11 tablets): CROSS-COMMODITY=8, GRAIN=4, WEAK_GOLD=2, WEAK_WOMAN=2, LEANING_GRAIN=2
  Dosmos Tablets (7 tablets): GRAIN=19, CROSS-COMMODITY=6, LEANING_GRAIN=5, WEAK_GRAIN=3, PERSON=2

===========================================================================
STEP 4: COMMODITY ECONOMIC PARAMETERS
===========================================================================

  Domain                Count  Median    Mean     Max Measures
  ----------------------------------------------------------------------
  GRAIN                1070       3    19.4   10300 T:462, V:245, Z:16, S:1
  OIL                   228       2    10.4     339 S:72, V:66, Z:9, T:4
  WINE                  144       2     9.0     168 V:38, S:23, T:9, Z:6
  OLIVES                156       4    25.1     402 T:49, V:25, S:3
  LIVESTOCK            1959      30    90.8   19200 M:15, V:3, T:2, Q:1, S:1
  WOOL                  538       6    26.8    1000 M:50, N:4, S:3, P:3, V:2
  BRONZE                307       2     3.6      30 M:197, N:76, P:2, Q:1
  GOLD                   55       1     2.3       7 P:16, N:10, M:1
  SPICE                  90       4     7.8     100 N:14, P:13, T:11, V:4, M:2
  FLOUR                  77       1     1.7       8 V:50, Z:11, T:10, S:3
  PERSON                761       1     9.5     900 M:3, Z:2, T:1, V:1, N:1
  WOMAN                 523       2     6.7     200 T:21

===========================================================================
STEP 5: MEASURE SUBUNIT DOMAIN DIVERGENCE
===========================================================================

  Do different commodities use different measurement subunits?
  (T/V/Z = dry measures, S = liquid, M/N/P = weight)

  GRAIN (724 measure tokens):
    T     462 (  64%) ███████████████████
    V     245 (  34%) ██████████
    Z      16 (   2%)
    S       1 (   0%)

  OIL (151 measure tokens):
    S      72 (  48%) ██████████████
    V      66 (  44%) █████████████
    Z       9 (   6%) █
    T       4 (   3%)

  WINE (76 measure tokens):
    V      38 (  50%) ███████████████
    S      23 (  30%) █████████
    T       9 (  12%) ███
    Z       6 (   8%) ██

  OLIVES (77 measure tokens):
    T      49 (  64%) ███████████████████
    V      25 (  32%) █████████
    S       3 (   4%) █

  LIVESTOCK (22 measure tokens):
    M      15 (  68%) ████████████████████
    V       3 (  14%) ████
    T       2 (   9%) ██
    Q       1 (   5%) █
    S       1 (   5%) █

  WOOL (63 measure tokens):
    M      50 (  79%) ███████████████████████
    N       4 (   6%) █
    S       3 (   5%) █
    P       3 (   5%) █
    V       2 (   3%)
    Q       1 (   2%)

  BRONZE (276 measure tokens):
    M     197 (  71%) █████████████████████
    N      76 (  28%) ████████
    P       2 (   1%)
    Q       1 (   0%)

  GOLD (27 measure tokens):
    P      16 (  59%) █████████████████
    N      10 (  37%) ███████████
    M       1 (   4%) █

  SPICE (46 measure tokens):
    N      14 (  30%) █████████
    P      13 (  28%) ████████
    T      11 (  24%) ███████
    V       4 (   9%) ██
    M       2 (   4%) █
    S       1 (   2%)
    Q       1 (   2%)

  FLOUR (74 measure tokens):
    V      50 (  68%) ████████████████████
    Z      11 (  15%) ████
    T      10 (  14%) ████
    S       3 (   4%) █

===========================================================================
STEP 6: KNOWN MYCENAEAN GREEK WORDS — VALIDATION
===========================================================================

  Word                   Greek            Meaning                MDP Domain             Match
  -----------------------------------------------------------------------------------------------
  pa-ro                paro             from/at (the place of) GRAIN                  ✗ (expected CROSS-COMMODITY)
  ko-wo                korwos           boy/youth              LEANING_WOMAN          ✗ (expected PERSON)
  ko-wa                korwa            girl/youth             WOMAN                  ✗ (expected PERSON)
  to-so                toson            so much/total          WEAK_GRAIN             ✗ (expected CROSS-COMMODITY)
  do-e-ro              doelos           slave/servant          GRAIN                  ✗ (expected PERSON)
  da-mo                damos            district/people        GRAIN                  ? (no clear expected)
  do-e-ra              doela            female slave           GRAIN                  ✗ (expected PERSON)
  pu-ro                Pylos            Pylos                  CROSS-COMMODITY        ✓ CORRECT (admin)
  o-pe-ro              ophelos          deficit/owed           LEANING_PERSON         ✗ (expected CROSS-COMMODITY)
  pa-i-to              Phaistos         Phaistos               LIVESTOCK              ✗ (expected PLACE_NAME)
  ko-re-te             koreter          mayor/governor         WEAK_GOLD              ✗ (expected CROSS-COMMODITY)
  o-pi                 opi              over/for               WEAK_WOOL              ✗ (expected CROSS-COMMODITY)
  to-sa                tosa             so much (fem.)         CROSS-COMMODITY        ? (no clear expected)
  ka-ko                khalkos          bronze                 BRONZE                 ✓ CORRECT
  po-ro-ko-re-te       prokoreter       deputy governor        LEANING_GOLD           ✗ (expected CROSS-COMMODITY)
  i-je-re-ja           hiereia          priestess              LEANING_GRAIN          ✗ (expected ADMIN/RELIGIOUS)
  te-re-ta             telestai         land holders           LEANING_GRAIN          ? (no clear expected)
  a-mi-ni-so           Amnisos          Amnisos                NOT CLASSIFIED         — (not in top 200)
  ko-no-so             Knossos          Knossos                NOT CLASSIFIED         — (not in top 200)
  si-to                sitos            wheat/grain            NOT CLASSIFIED         — (not in top 200)
  po-me                poimen           shepherd               NOT CLASSIFIED         — (not in top 200)
  e-re-pa-te           elephanteios     of ivory               NOT CLASSIFIED         — (not in top 200)
  me-ri                meli             honey                  NOT CLASSIFIED         — (not in top 200)
  ku-ru-so             khrusos          gold                   NOT CLASSIFIED         — (not in top 200)
  re-u-ko              leukos           white                  NOT CLASSIFIED         — (not in top 200)
  ka-ke-u              khalkeus         bronze-smith           NOT CLASSIFIED         — (not in top 200)
  wo-no                woinos           wine                   NOT CLASSIFIED         — (not in top 200)
  ka-na-pe-u           knapheus         fuller                 NOT CLASSIFIED         — (not in top 200)
  wa-na-ka             wanax            king                   NOT CLASSIFIED         — (not in top 200)
  pa-te                pater            father                 NOT CLASSIFIED         — (not in top 200)
  to-ko-do-mo          toikhodomoi      builders               NOT CLASSIFIED         — (not in top 200)
  ra-wa-ke-ta          lawagetas        army leader            NOT CLASSIFIED         — (not in top 200)
  ki-ri-ta             kritha           barley                 NOT CLASSIFIED         — (not in top 200)
  e-ra-wo              elaiwon          olive oil              NOT CLASSIFIED         — (not in top 200)
  si-to-po-ti-ni-ja    sitopotnia       grain goddess          NOT CLASSIFIED         — (not in top 200)
  e-ra-wa              elaia            olive                  NOT CLASSIFIED         — (not in top 200)
  su-qo-ta             subotas          swineherd              NOT CLASSIFIED         — (not in top 200)
  ke-ra-me-u           kerameus         potter                 NOT CLASSIFIED         — (not in top 200)
  pi-ri-e-te-re        pristeres        sawyers                NOT CLASSIFIED         — (not in top 200)
  a-re-pa              aleiphar         unguent/oil            NOT CLASSIFIED         — (not in top 200)

  VALIDATION: 2/14 correct (14%)
  Not in top 200 words: 23

===========================================================================
STEP 7: SCRIBE SPECIALISATION
===========================================================================
  Scribe 117: 1031 records — LIVESTOCK=1026, WOOL=5 → SPECIALIST: LIVESTOCK
  Scribe 103: 274 records — PERSON=92, WOMAN=83, WOOL=67, TEXTILES=17, GRAIN=9 → GENERALIST
  Scribe 118: 153 records — LIVESTOCK=103, WOOL=50 → LEANING: LIVESTOCK
  Scribe 104: 100 records — PERSON=100 → SPECIALIST: PERSON
  Scribe 101: 86 records — PERSON=86 → SPECIALIST: PERSON
  Scribe 120: 84 records — WOOL=65, LIVESTOCK=19 → SPECIALIST: WOOL
  Scribe 141: 83 records — OIL=83 → SPECIALIST: OIL
  Scribe 124: 63 records — LIVESTOCK=44, GRAIN=7, PERSON=5, OIL=2, OLIVES=2 → LEANING: LIVESTOCK
  Scribe 106: 60 records — LIVESTOCK=50, PERSON=10 → SPECIALIST: LIVESTOCK
  Scribe 139: 59 records — GRAIN=15, FIGS=12, FLOUR=12, WINE=11, OIL=9 → GENERALIST
  Scribe 119: 58 records — WOOL=36, LIVESTOCK=22 → LEANING: WOOL
  Scribe 107: 57 records — LIVESTOCK=46, PERSON=11 → SPECIALIST: LIVESTOCK
  Scribe 111: 30 records — LIVESTOCK=30 → SPECIALIST: LIVESTOCK
  Scribe 124-B: 22 records — LIVESTOCK=19, WOMAN=2, PERSON=1 → SPECIALIST: LIVESTOCK
  Scribe 124-E: 21 records — SPICE=21 → SPECIALIST: SPICE
  Scribe 134: 20 records — SPICE=20 → SPECIALIST: SPICE
  Scribe 138: 19 records — OIL=19 → SPECIALIST: OIL
  Scribe 124-I: 17 records — LIVESTOCK=17 → SPECIALIST: LIVESTOCK
  Scribe 102a: 17 records — GRAIN=7, WOMAN=6, BRONZE=2, PERSON=1, OLIVES=1 → GENERALIST
  Scribe 124-D: 17 records — GRAIN=6, VESSEL=6, OIL=2, WINE=2, OLIVES=1 → GENERALIST
  Scribe 108: 16 records — WOMAN=16 → SPECIALIST: WOMAN
  Scribe 131: 16 records — WHEEL=16 → SPECIALIST: WHEEL
  Scribe 110: 16 records — LIVESTOCK=16 → SPECIALIST: LIVESTOCK
  Scribe 136: 16 records — GRAIN=8, SPICE=7, VESSEL=1 → GENERALIST
  Scribe 113: 15 records — WOOL=13, TEXTILES=2 → SPECIALIST: WOOL
  Scribe 132: 14 records — LIVESTOCK=14 → SPECIALIST: LIVESTOCK
  Scribe 221: 14 records — SPICE=14 → SPECIALIST: SPICE
  Scribe 215: 14 records — WOOL=8, LIVESTOCK=6 → LEANING: WOOL
  Scribe 121: 14 records — LIVESTOCK=14 → SPECIALIST: LIVESTOCK
  Scribe 112: 14 records — LIVESTOCK=14 → SPECIALIST: LIVESTOCK
  Scribe 124-A: 13 records — PERSON=7, WOMAN=6 → LEANING: PERSON
  Scribe 130: 13 records — WHEEL=13 → SPECIALIST: WHEEL
  Scribe 135: 13 records — SPICE=12, VESSEL=1 → SPECIALIST: SPICE
  Scribe 201: 13 records — LIVESTOCK=13 → SPECIALIST: LIVESTOCK
  Scribe 216: 12 records — LIVESTOCK=12 → SPECIALIST: LIVESTOCK
  Scribe 124-G: 12 records — LIVESTOCK=12 → SPECIALIST: LIVESTOCK
  Scribe 124-F: 10 records — LIVESTOCK=10 → SPECIALIST: LIVESTOCK
  Scribe 137: 10 records — PERSON=10 → SPECIALIST: PERSON
  Scribe 124-S: 9 records — LIVESTOCK=9 → SPECIALIST: LIVESTOCK
  Scribe 234: 9 records — OLIVES=4, GRAIN=3, VESSEL=1, FIGS=1 → GENERALIST
  Scribe 205: 9 records — WOMAN=6, GRAIN=3 → LEANING: WOMAN
  Scribe 102b: 9 records — PERSON=9 → SPECIALIST: PERSON
  Scribe 115: 8 records — WOOL=8 → SPECIALIST: WOOL
  Scribe 222: 8 records — OIL=8 → SPECIALIST: OIL
  Scribe 217: 8 records — LIVESTOCK=8 → SPECIALIST: LIVESTOCK
  Scribe 109: 8 records — LIVESTOCK=8 → SPECIALIST: LIVESTOCK
  Scribe 227: 6 records — WOOL=5, WOMAN=1 → SPECIALIST: WOOL
  Scribe 218: 6 records — LIVESTOCK=4, WOOL=2 → LEANING: LIVESTOCK
  Scribe 116: 6 records — TEXTILES=6 → SPECIALIST: TEXTILES
  Scribe 124-C: 6 records — LIVESTOCK=6 → SPECIALIST: LIVESTOCK
  Scribe 105: 5 records — PERSON=5 → SPECIALIST: PERSON

===========================================================================
STEP 8: DOMAIN CLASSIFICATION SUMMARY
===========================================================================

  CROSS-COMMODITY (44 words):
    inf.: 1178
    sup.: 1120
    v.↓: 114
    jo: 84
    lat.: 75
    ko: 72
    a: 71
    a-: 66
    pu-ro: 64 ← Pylos (Pylos)
    ja: 62

  LIVESTOCK (38 words):
    pa: 103
    ki: 100
    supra: 92
    pe: 89
    ku-ta-to: 66
    pa-i-to: 47 ← Phaistos (Phaistos)
    da-wo: 44
    e-ra: 40
    e-ko-so: 39
    da-*22-to: 39

  GRAIN (25 words):
    pa-ro: 272 ← paro (from/at (the place of))
    pe-mo: 201
    o-na-to: 187
    e-ke: 173
    to-so-de: 158
    ko-to-na: 151
    e-ke-qe: 101
    te-o-jo: 97
    ke-ke-me-na: 94
    da-mo: 90 ← damos (district/people)

  LEANING_GRAIN (16 words):
    ko-: 54
    -ro: 33
    o-: 31
    pa-: 23
    to-sa-de: 19
    i-je-re-ja: 17 ← hiereia (priestess)
    mo: 16
    -qe: 15
    po-se-da-o-ne: 14
    te-re-ta: 14 ← telestai (land holders)

  LEANING_LIVESTOCK (11 words):
    o: 319
    wo: 47
    -to: 37
    sa: 25
    we: 21
    pi: 17
    da-: 17
    se-to-i-ja: 17
    a-si-ja-ti-ja: 16
    da: 15

  NO_COMMODITY (8 words):
    a-ja-me-no: 19
    i-qi-ja: 18
    e-re-pa-te-jo: 16
    o-u-di-do-si: 16
    ta-ra-nu: 15
    ja-: 14
    o-po-qo: 13
    o-pi-i-ja-pi: 12

  PERSON (6 words):
    e-qe-ta: 17
    po: 17
    u: 17
    po-ni-ki-jo: 16
    o-ka: 15
    pe-i: 12

  WEAK_GRAIN (5 words):
    to-so: 122 ← toson (so much/total)
    de: 50
    e-: 44
    ko-no: 18
    a-ta-o: 16

  BRONZE (5 words):
    ka-ke-we: 52
    ta-ra-si-ja: 24
    e-ko-te: 21
    ka-ko: 18 ← khalkos (bronze)
    a-ta-ra-si-jo: 17

  LEANING_PERSON (5 words):
    o-pe-ro: 48 ← ophelos (deficit/owed)
    -ta: 32
    ke-ro-si-ja: 22
    -no: 20
    -o: 13

  WOMAN (4 words):
    ko-wa: 151 ← korwa (girl/youth)
    di: 41
    me-zo-e: 34
    me-wi-jo-e: 16

  WEAK_PERSON (4 words):
    e: 59
    ta: 37
    -so: 18
    a-ke-re-wa: 13

  LEANING_WOMAN (3 words):
    ko-wo: 218 ← korwos (boy/youth)
    me-: 19
    me-zo: 13

  WOOL (3 words):
    ku: 42
    pa-we-a: 30
    tu-na-no: 20

  LEANING_OIL (3 words):
    a-pu-do-si: 26
    ku-pi-ri-jo: 18
    po-ti-ni-ja: 16

  WEAK_LIVESTOCK (2 words):
    -jo: 69
    ra: 37

  OIL (2 words):
    me-no: 26
    pa-si-te-o-i: 14

  WEAK_WOMAN (2 words):
    me: 24
    me-ta-pa: 14

  WHEEL (2 words):
    wo-ka: 18
    we-je-ke-e: 18

  SPICE (2 words):
    ka-na-ko: 18
    e-ru-ta-ra: 13

  LEANING_FLOUR (2 words):
    to-jo: 14
    a-nu-to: 13

  WEAK_GOLD (1 words):
    ko-re-te: 41 ← koreter (mayor/governor)

  WEAK_WOOL (1 words):
    o-pi: 39 ← opi (over/for)

  LEANING_SPICE (1 words):
    ri: 19

  LEANING_GOLD (1 words):
    po-ro-ko-re-te: 18 ← prokoreter (deputy governor)

  WEAK_TEXTILES (1 words):
    i-: 14

  LEANING_TEXTILES (1 words):
    mi: 14

  OLIVES (1 words):
    a-ko-da-mo: 13

  WEAK_SPICE (1 words):
    re: 13

===========================================================================
LINEAR B MDP CONTROL VALIDATION — COMPLETE
===========================================================================

  CORPUS:
    Inscriptions: 5832
    With data: 5832
    Unique words: 5823
    Commodity tokens: 65

  MDP RESULTS:
    Words classified: 200
      CROSS-COMMODITY: 44
      LIVESTOCK: 38
      GRAIN: 25
      LEANING_GRAIN: 16
      LEANING_LIVESTOCK: 11
      NO_COMMODITY: 8
      PERSON: 6
      WEAK_GRAIN: 5
      BRONZE: 5
      LEANING_PERSON: 5
      WOMAN: 4
      WEAK_PERSON: 4
      LEANING_WOMAN: 3
      WOOL: 3
      LEANING_OIL: 3
      WEAK_LIVESTOCK: 2
      OIL: 2
      WEAK_WOMAN: 2
      WHEEL: 2
      SPICE: 2
      LEANING_FLOUR: 2
      WEAK_GOLD: 1
      WEAK_WOOL: 1
      LEANING_SPICE: 1
      LEANING_GOLD: 1
      WEAK_TEXTILES: 1
      LEANING_TEXTILES: 1
      OLIVES: 1
      WEAK_SPICE: 1

  VALIDATION:
    Known Greek words tested: 14
    Correct: 2 (14%)
    Mismatched: 12
    Not in top 200: 23

PS C:\Users\aazsh\Desktop\Latest_MDP_research>

'''
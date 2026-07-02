'''

# MDP Entropy Analysis — Output Log
**Date:** 2 July 2026
**Database:** OKR SQLite (619 khipus, 54,403 cords)
**Script:** mdp_entropy.py

PS C:\Users\aazsh\Desktop\Latest_MDP_research> python mdp_entropy.py
======================================================================
ANALYSIS 1: SHANNON ENTROPY — COLOUR INFORMATION HIERARCHY
======================================================================

  FULL_COLOR palette:
    Pendant cords:     39,172
    Unique colours:    720
    Shannon entropy:   4.995 bits
    Max entropy:       9.492 bits
    Utilisation:       52.6%

  COLOR_CD_1 palette (standard practice):
    Unique colours:    65
    Shannon entropy:   3.630 bits

  INFORMATION LOSS from collapsing compounds:
    Delta H:           1.366 bits
    Percentage lost:   37.6% of primary entropy

  TIER DISTRIBUTION (720 colours):
    vowel                 3 colours
    semi-vowel           14 colours
    consonant            60 colours
    rare-consonant      643 colours

  Colour                 Count    Prob  I(bits) Tier
  --------------------------------------------------------------
  W                     10,604 0.2707    1.89  vowel
  AB                     5,338 0.1363    2.88  vowel
  MB                     3,838 0.0980    3.35  vowel
  B                      1,704 0.0435    4.52  semi-vowel
  YB                     1,521 0.0388    4.69  semi-vowel
  KB                       887 0.0226    5.46  semi-vowel
  LB                       872 0.0223    5.49  semi-vowel
  AB:W                     858 0.0219    5.51  semi-vowel
  NB                       657 0.0168    5.90  semi-vowel
  MB:W                     640 0.0163    5.94  semi-vowel
  KB:W                     530 0.0135    6.21  semi-vowel
  HB                       472 0.0120    6.37  semi-vowel
  LK                       437 0.0112    6.49  semi-vowel
  MB:AB                    414 0.0106    6.56  semi-vowel
  RB                       411 0.0105    6.57  semi-vowel
  GG                       355 0.0091    6.79  semi-vowel
  DB                       351 0.0090    6.80  semi-vowel
  RL                       251 0.0064    7.29  consonant
  BG                       204 0.0052    7.59  consonant
  YG                       197 0.0050    7.64  consonant
  GG:AB                    196 0.0050    7.64  consonant
  BB                       192 0.0049    7.67  consonant
  W:MB                     176 0.0045    7.80  consonant
  GG:W                     166 0.0042    7.88  consonant
  CB                       150 0.0038    8.03  consonant
  LB:W                     146 0.0037    8.07  consonant
  BS                       139 0.0035    8.14  consonant
  AB:MB                    133 0.0034    8.20  consonant
  KB:MB                    132 0.0034    8.21  consonant
  G0                       130 0.0033    8.24  consonant
  DB                       126 0.0032    8.28  consonant
  BY                       123 0.0031    8.32  consonant
  KB:AB                    117 0.0030    8.39  consonant
  W:AB                     115 0.0029    8.41  consonant
  G                        110 0.0028    8.48  consonant
  B:W                      110 0.0028    8.48  consonant
  0D                       108 0.0028    8.50  consonant
  MB-W                     104 0.0027    8.56  consonant
  DB :W                    104 0.0027    8.56  consonant
  LG                       100 0.0026    8.61  consonant
  KB-W                      99 0.0025    8.63  consonant
  AB-W                      98 0.0025    8.64  consonant
  MB%W                      96 0.0025    8.67  consonant
  MB:YB                     94 0.0024    8.70  consonant
  BB:W                      90 0.0023    8.77  consonant
  RM                        88 0.0022    8.80  consonant
  LC                        85 0.0022    8.85  consonant
  AB%W                      82 0.0021    8.90  consonant
  PR                        81 0.0021    8.92  consonant
  DB -W                     77 0.0020    8.99  consonant
  BG:W                      73 0.0019    9.07  consonant
  MB-AB                     67 0.0017    9.19  consonant
  FB                        67 0.0017    9.19  consonant
  HB:W                      66 0.0017    9.21  consonant
  LG:AB                     65 0.0017    9.24  consonant
  LK:W                      64 0.0016    9.26  consonant
  GG:MB                     62 0.0016    9.30  consonant
  DB -CB                    60 0.0015    9.35  consonant
  0G                        60 0.0015    9.35  consonant
  W-MB                      59 0.0015    9.37  consonant
  W:KB                      56 0.0014    9.45  consonant
  GL                        51 0.0013    9.59  consonant
  BY-W                      50 0.0013    9.61  consonant
  BL:W                      48 0.0012    9.67  consonant
  BD                        48 0.0012    9.67  consonant
  AB:GG                     48 0.0012    9.67  consonant
  W:NB                      46 0.0012    9.73  consonant
  CB-W                      46 0.0012    9.73  consonant
  CB:W                      44 0.0011    9.80  consonant
  RB:AB                     43 0.0011    9.83  consonant
  GB                        43 0.0011    9.83  consonant
  B-W                       42 0.0011    9.87  consonant
  YB:W                      40 0.0010    9.94  consonant
  BY:W                      40 0.0010    9.94  consonant
  RL:W                      39 0.0010    9.97  consonant
  G:W                       39 0.0010    9.97  consonant
  FB:W                      39 0.0010    9.97  consonant
  YB:0G                     38 0.0010   10.01  rare-consonant
  RB:W                      38 0.0010   10.01  rare-consonant
  DB -YG                    37 0.0009   10.05  rare-consonant
  W:RM                      36 0.0009   10.09  rare-consonant
  W:BL                      36 0.0009   10.09  rare-consonant
  B:BB                      36 0.0009   10.09  rare-consonant
  GG-AB                     34 0.0009   10.17  rare-consonant
  NB:W                      33 0.0008   10.21  rare-consonant
  0B                        33 0.0008   10.21  rare-consonant
  R                         32 0.0008   10.26  rare-consonant
  MB:KB                     31 0.0008   10.30  rare-consonant
  MB-KB                     31 0.0008   10.30  rare-consonant
  AB-MB                     31 0.0008   10.30  rare-consonant
  VR                        30 0.0008   10.35  rare-consonant
  RD                        30 0.0008   10.35  rare-consonant
  KB:AB:W                   28 0.0007   10.45  rare-consonant
  FR                        28 0.0007   10.45  rare-consonant
  BD:W                      28 0.0007   10.45  rare-consonant
  CB:B                      27 0.0007   10.50  rare-consonant
  B:YG                      27 0.0007   10.50  rare-consonant
  AB:LG                     26 0.0007   10.56  rare-consonant
  W-AB                      25 0.0006   10.61  rare-consonant
  GY                        25 0.0006   10.61  rare-consonant
  EB                        25 0.0006   10.61  rare-consonant
  BL                        25 0.0006   10.61  rare-consonant
  B:GG                      25 0.0006   10.61  rare-consonant
  W*SY                      24 0.0006   10.67  rare-consonant
  W*FB                      24 0.0006   10.67  rare-consonant
  W*BS                      24 0.0006   10.67  rare-consonant
  W*0G                      24 0.0006   10.67  rare-consonant
  VB:W                      24 0.0006   10.67  rare-consonant
  MB:GG                     24 0.0006   10.67  rare-consonant
  CB:MB                     24 0.0006   10.67  rare-consonant
  BL:AB                     24 0.0006   10.67  rare-consonant
  BG:MB                     24 0.0006   10.67  rare-consonant
  AB:KB                     24 0.0006   10.67  rare-consonant
  LD                        23 0.0006   10.73  rare-consonant
  LB:YB                     23 0.0006   10.73  rare-consonant
  KB:B                      23 0.0006   10.73  rare-consonant
  DB :YG                    22 0.0006   10.80  rare-consonant
  BS-W                      22 0.0006   10.80  rare-consonant
  PB                        21 0.0005   10.87  rare-consonant
  MB:YG                     21 0.0005   10.87  rare-consonant
  LK:AB                     21 0.0005   10.87  rare-consonant
  LG:W                      21 0.0005   10.87  rare-consonant
  LA                        21 0.0005   10.87  rare-consonant
  YB:B                      20 0.0005   10.94  rare-consonant
  HB:CB                     20 0.0005   10.94  rare-consonant
  HB:AB                     20 0.0005   10.94  rare-consonant
  GY:W                      20 0.0005   10.94  rare-consonant
  W-KB                      19 0.0005   11.01  rare-consonant
  SR                        19 0.0005   11.01  rare-consonant
  LG-W                      19 0.0005   11.01  rare-consonant
  DB :KB                    19 0.0005   11.01  rare-consonant
  W*KB                      18 0.0005   11.09  rare-consonant
  KB:BB:W                   18 0.0005   11.09  rare-consonant
  GG:YB                     18 0.0005   11.09  rare-consonant
  W:BG                      17 0.0004   11.17  rare-consonant
  MG                        17 0.0004   11.17  rare-consonant
  LB:B                      17 0.0004   11.17  rare-consonant
  KB:GG:W                   17 0.0004   11.17  rare-consonant
  G0:AB                     17 0.0004   11.17  rare-consonant
  BG:AB                     17 0.0004   11.17  rare-consonant
  B-BD                      17 0.0004   11.17  rare-consonant
  W-BG                      16 0.0004   11.26  rare-consonant
  MG:W                      16 0.0004   11.26  rare-consonant
  KB-AB                     16 0.0004   11.26  rare-consonant
  FR:W                      16 0.0004   11.26  rare-consonant
  CB:AB                     16 0.0004   11.26  rare-consonant
  BD-W                      16 0.0004   11.26  rare-consonant
  B:BB:GG                   16 0.0004   11.26  rare-consonant
  0D:W                      16 0.0004   11.26  rare-consonant
  PR:RL                     15 0.0004   11.35  rare-consonant
  AB:SY                     15 0.0004   11.35  rare-consonant
  AB:RB                     15 0.0004   11.35  rare-consonant
  W:PG                      14 0.0004   11.45  rare-consonant
  MB:W-W                    14 0.0004   11.45  rare-consonant
  LB:B:GG                   14 0.0004   11.45  rare-consonant
  KB:BB                     14 0.0004   11.45  rare-consonant
  KB-MB                     14 0.0004   11.45  rare-consonant
  GG:AB:MB                  14 0.0004   11.45  rare-consonant
  GG-W                      14 0.0004   11.45  rare-consonant
  DG                        14 0.0004   11.45  rare-consonant
  0L                        14 0.0004   11.45  rare-consonant
  0K:W                      14 0.0004   11.45  rare-consonant
  W:                        13 0.0003   11.56  rare-consonant
  W-NB                      13 0.0003   11.56  rare-consonant
  SB                        13 0.0003   11.56  rare-consonant
  RL-W                      13 0.0003   11.56  rare-consonant
  MB:GG:W                   13 0.0003   11.56  rare-consonant
  MB:AB:W                   13 0.0003   11.56  rare-consonant
  LB-W                      13 0.0003   11.56  rare-consonant
  KB:NB                     13 0.0003   11.56  rare-consonant
  B:LC                      13 0.0003   11.56  rare-consonant
  B:G                       13 0.0003   11.56  rare-consonant
  W*SY*                     12 0.0003   11.67  rare-consonant
  MB:B                      12 0.0003   11.67  rare-consonant
  KG                        12 0.0003   11.67  rare-consonant
  BG-W                      12 0.0003   11.67  rare-consonant
  AB:YB                     12 0.0003   11.67  rare-consonant
  AB-GG                     12 0.0003   11.67  rare-consonant
  W:GG                      11 0.0003   11.80  rare-consonant
  W*VB*                     11 0.0003   11.80  rare-consonant
  W*SR*                     11 0.0003   11.80  rare-consonant
  W*0G*                     11 0.0003   11.80  rare-consonant
  RM-MB                     11 0.0003   11.80  rare-consonant
  RB%AB                     11 0.0003   11.80  rare-consonant
  KB:LC                     11 0.0003   11.80  rare-consonant
  HB:MB                     11 0.0003   11.80  rare-consonant
  HB-AB                     11 0.0003   11.80  rare-consonant
  YG:W                      10 0.0003   11.94  rare-consonant
  R0                        10 0.0003   11.94  rare-consonant
  PG                        10 0.0003   11.94  rare-consonant
  MB:RL:AB                  10 0.0003   11.94  rare-consonant
  KB:W*SR                   10 0.0003   11.94  rare-consonant
  GR                        10 0.0003   11.94  rare-consonant
  BB-W                      10 0.0003   11.94  rare-consonant
  B:CB                      10 0.0003   11.94  rare-consonant
  AB-B                      10 0.0003   11.94  rare-consonant
  0D:LD                     10 0.0003   11.94  rare-consonant
  W*SR:0G                    9 0.0002   12.09  rare-consonant
  W*DB *                     9 0.0002   12.09  rare-consonant
  R:W                        9 0.0002   12.09  rare-consonant
  PR:AB                      9 0.0002   12.09  rare-consonant
  MB:PG                      9 0.0002   12.09  rare-consonant
  MB%AB                      9 0.0002   12.09  rare-consonant
  GG:AB:W                    9 0.0002   12.09  rare-consonant
  FR-YB                      9 0.0002   12.09  rare-consonant
  BB:YG                      9 0.0002   12.09  rare-consonant
  AB:NB                      9 0.0002   12.09  rare-consonant
  YG-B                       8 0.0002   12.26  rare-consonant
  YB:PB:R0                   8 0.0002   12.26  rare-consonant
  W:PB                       8 0.0002   12.26  rare-consonant
  W*GR                       8 0.0002   12.26  rare-consonant
  RL:KB                      8 0.0002   12.26  rare-consonant
  RL:AB                      8 0.0002   12.26  rare-consonant
  RG                         8 0.0002   12.26  rare-consonant
  NB:DG:W                    8 0.0002   12.26  rare-consonant
  MB:BL:W                    8 0.0002   12.26  rare-consonant
  MB-HB                      8 0.0002   12.26  rare-consonant
  LK:YB                      8 0.0002   12.26  rare-consonant
  KB:MB:W                    8 0.0002   12.26  rare-consonant
  GL:AB                      8 0.0002   12.26  rare-consonant
  DB :AB                     8 0.0002   12.26  rare-consonant
  D0                         8 0.0002   12.26  rare-consonant
  BL:RL                      8 0.0002   12.26  rare-consonant
  BL:MB                      8 0.0002   12.26  rare-consonant
  YB:AB                      7 0.0002   12.45  rare-consonant
  W:AB:PB                    7 0.0002   12.45  rare-consonant
  W*SR:VB                    7 0.0002   12.45  rare-consonant
  W*SR:SY:0G                 7 0.0002   12.45  rare-consonant
  W*KB*                      7 0.0002   12.45  rare-consonant
  W*FB:SY                    7 0.0002   12.45  rare-consonant
  W*BS*                      7 0.0002   12.45  rare-consonant
  VG                         7 0.0002   12.45  rare-consonant
  PK:AB                      7 0.0002   12.45  rare-consonant
  NB-W                       7 0.0002   12.45  rare-consonant
  MB:BG                      7 0.0002   12.45  rare-consonant
  MB:AB:GG                   7 0.0002   12.45  rare-consonant
  LC:W                       7 0.0002   12.45  rare-consonant
  LB:BL                      7 0.0002   12.45  rare-consonant
  KB-NB                      7 0.0002   12.45  rare-consonant
  GG-MB                      7 0.0002   12.45  rare-consonant
  GA:W                       7 0.0002   12.45  rare-consonant
  G:AB                       7 0.0002   12.45  rare-consonant
  FB:SY                      7 0.0002   12.45  rare-consonant
  DB :MB                     7 0.0002   12.45  rare-consonant
  CB-B                       7 0.0002   12.45  rare-consonant
  BS*SY*                     7 0.0002   12.45  rare-consonant
  0Y:W                       7 0.0002   12.45  rare-consonant
  YY                         6 0.0002   12.67  rare-consonant
  YB:BL                      6 0.0002   12.67  rare-consonant
  W:TG                       6 0.0002   12.67  rare-consonant
  W:LG                       6 0.0002   12.67  rare-consonant
  W*SR:SY                    6 0.0002   12.67  rare-consonant
  W*HB                       6 0.0002   12.67  rare-consonant
  VB                         6 0.0002   12.67  rare-consonant
  TG                         6 0.0002   12.67  rare-consonant
  RG:W                       6 0.0002   12.67  rare-consonant
  MG:AB:W                    6 0.0002   12.67  rare-consonant
  MB:FB                      6 0.0002   12.67  rare-consonant
  LD:W                       6 0.0002   12.67  rare-consonant
  KB:SY                      6 0.0002   12.67  rare-consonant
  HB-MB                      6 0.0002   12.67  rare-consonant
  GGW                        6 0.0002   12.67  rare-consonant
  BY:BL                      6 0.0002   12.67  rare-consonant
  BS*VB*                     6 0.0002   12.67  rare-consonant
  BS*SR*                     6 0.0002   12.67  rare-consonant
  BS*KB*                     6 0.0002   12.67  rare-consonant
  BS*0G*                     6 0.0002   12.67  rare-consonant
  BG:KB                      6 0.0002   12.67  rare-consonant
  B:VB                       6 0.0002   12.67  rare-consonant
  B:BL                       6 0.0002   12.67  rare-consonant
  0R                         6 0.0002   12.67  rare-consonant
  YG:MB                      5 0.0001   12.94  rare-consonant
  YG-W                       5 0.0001   12.94  rare-consonant
  YB-KB                      5 0.0001   12.94  rare-consonant
  W*DB :KB*                  5 0.0001   12.94  rare-consonant
  W%MB                       5 0.0001   12.94  rare-consonant
  RM:W                       5 0.0001   12.94  rare-consonant
  MB:AB:KB                   5 0.0001   12.94  rare-consonant
  MB-NB                      5 0.0001   12.94  rare-consonant
  LB-BL                      5 0.0001   12.94  rare-consonant
  GG%W                       5 0.0001   12.94  rare-consonant
  FB:B                       5 0.0001   12.94  rare-consonant
  FB*BS                      5 0.0001   12.94  rare-consonant
  DB -GG                     5 0.0001   12.94  rare-consonant
  DB *VB*                    5 0.0001   12.94  rare-consonant
  DB *SY*                    5 0.0001   12.94  rare-consonant
  DB *SR*                    5 0.0001   12.94  rare-consonant
  DB *KB*                    5 0.0001   12.94  rare-consonant
  DB *0G*                    5 0.0001   12.94  rare-consonant
  BS:FB                      5 0.0001   12.94  rare-consonant
  BS:DB                      5 0.0001   12.94  rare-consonant
  BS*DB *                    5 0.0001   12.94  rare-consonant
  B-GG                       5 0.0001   12.94  rare-consonant
  B-BB                       5 0.0001   12.94  rare-consonant
  AB:HB                      5 0.0001   12.94  rare-consonant
  AB-BL                      5 0.0001   12.94  rare-consonant
  :W-W                       5 0.0001   12.94  rare-consonant

======================================================================
ANALYSIS 2: COLOUR-VALUE FUNCTIONAL TAXONOMY
======================================================================

  Colour       Count  Zero%     Mean   Median      Max   StdDev Function
  ------------------------------------------------------------------------------
  W           11,609  37.3%   461.1      20  320535  4532.2  CATEGORY
  AB           6,804  27.8%   354.5      11  245811  4412.1  CATEGORY
  MB           5,554  35.0%   172.8      10   36024  1279.2  CATEGORY
  B            2,050  29.8%   502.3      12   97357  3635.1  COMMODITY
  KB           2,002  52.3%   135.3      10   10188   699.1  CATEGORY
  YB           1,675  40.7%    87.6       8    5730   385.7  CATEGORY
  LB           1,119  45.1%   277.9      10   42760  2083.0  CATEGORY
  GG             908  29.1%   503.3      13   43372  2789.5  COMMODITY
  DB             735  32.2%   190.7      43   11400   794.4  CATEGORY
  NB             719  42.4%   515.7      60   10170  1307.0  COMMODITY
  HB             637  44.4%   164.6      11    8140   619.5  CATEGORY
  LK             540   9.3%    21.2      19     500    28.3  CATEGORY
  RB             515  20.4%    36.2      10     930   101.4  CATEGORY
  BG             345  27.5%   180.0      16   11598  1143.4  CATEGORY
  RL             343  25.4%    69.0      15    1261   154.6  CATEGORY
  CB             320  37.8%   279.2      20   19274  1581.5  CATEGORY
  BB             302  54.6%   324.1      10   18504  1791.9  CATEGORY
  BS             229  59.8%   340.8       7   11544  1456.6  CATEGORY
  YG             226  14.6%   350.3     100   23098  1868.7  CATEGORY
  BY             224  31.2%    61.3      22    2910   252.1  CATEGORY
  LG             220  33.6%   166.8      10    3900   555.4  CATEGORY
  G              164  31.7%    89.6      18    4000   389.7  CATEGORY
  G0             150  21.3%    70.2      10    4741   433.7  CATEGORY
  0D             134  29.1%    40.4      19     300    60.8  DEMOGRAPHIC
  DB             131   6.1%    17.4      15     120    12.8  DEMOGRAPHIC
  FB             131  40.5%    34.9      10    1271   143.9  CATEGORY
  BL             118  16.1%   538.5      32    9681  1818.7  COMMODITY
  PR             109  28.4%    18.3      10     100    21.7  DEMOGRAPHIC
  RM             106  24.5%   226.2      51    6136   703.1  CATEGORY
  LC             102  19.6%    58.0       7     780   145.4  CATEGORY
  BD              93  53.8%   334.8     102    3654   702.1  CATEGORY
  0G              77  49.4%    15.9       4     140    31.4  DEMOGRAPHIC
  GL              69  43.5%   371.1      30    7444  1177.6  CATEGORY
  FR              58  56.9%    31.6      28      71    22.3  DEMOGRAPHIC
  GB              47  76.6%    15.5      10     100    27.0  DEMOGRAPHIC
  GY              45   8.9%   148.5     101     879   184.9  CATEGORY
  R               43  34.9%     7.8       6      30     7.0  CATEGORY
  MG              42  42.9%    70.8       5     802   161.4  CATEGORY
  0B              36  25.0%    82.6      20     573   132.8  CATEGORY
  RD              35  51.4%   170.4      20    2402   559.0  CATEGORY
  VR              31  77.4%     2.7       2      10     3.0  CATEGORY
  VB              30  26.7%    22.5       5     210    46.9  DEMOGRAPHIC
  LD              29  10.3%    23.3       8     130    33.1  DEMOGRAPHIC
  SR              27 100.0%     0.0       0       0     0.0  FORMATTING
  PB              27  48.1%    17.6      10      60    20.7  DEMOGRAPHIC
  EB              25  32.0%   275.6      57    1810   552.6  CATEGORY
  LA              22  18.2%    14.1       5     101    22.9  DEMOGRAPHIC

  FUNCTIONAL SUMMARY:
    CATEGORY: 32 colours — W, AB, MB, KB, YB, LB, DB , HB
    DEMOGRAPHIC: 10 colours — 0D, DB, PR, 0G, FR, GB, VB, LD
    COMMODITY: 4 colours — B, GG, NB, BL
    FORMATTING: 1 colours — SR

======================================================================
ANALYSIS 3: SITE-SPECIFIC COLOUR SIGNATURES
======================================================================

  Name candidates (>50% single-site, >60% value variance, >15 bits entropy): 266

  Motif                                         Khipus  Entropy ValVar Site                      Conc%
  ----------------------------------------------------------------------------------------------------
  LB:W-LB:W-LB:W-LB:W                                4    32.3  0.60  Pachacamac                 100%
  G-G-G-G                                            3    33.9  1.00  Nazca                       95%
  PR-PR-PR-PR                                        4    35.7  0.91  Ica/Pisco                   82%
  RL-RL-RL-RL                                        4    29.1  0.88  Santa                      100%
  B:W-B:W-B:W-B:W                                    4    33.9  0.65  Ica/Pisco                   80%
  AB%W-AB%W-AB%W                                     3    26.7  0.89  Pachacamac                 100%
  DB :W-DB :W-DB :W-DB :W                            3    34.2  0.81  Nazca                       77%
  W-LB:W-LB:W-LB:W                                   3    26.1  0.75  Pachacamac                 100%
  LK-LK-LK-LK                                        7    25.9  1.00  Valle de Pisco              98%
  HB:W-HB:W-HB:W-HB:W                                4    36.9  1.00  Pachacamac                  68%
  LB:W-LB:W-LB:W                                     5    24.2  0.64  Pachacamac                 100%
  W:MB-W-NB-W:AB                                     3    24.0  1.00  Incahuasi                  100%
  NB-NB-NB-NB                                       12    23.6  0.93  Incahuasi                  100%
  G-G-G                                              4    25.4  1.00  Nazca                       88%
  GG:W-GG:W-GG:W-GG:W                                6    31.5  1.00  Pachacamac                  71%
  LK:W-LK:W-LK:W-LK:W                                3    37.0  1.00  near Lima                   60%
  AB-HB-HB-HB                                        3    22.0  1.00  Pachacamac                 100%
  RL-RL-RL                                           5    21.9  0.88  Santa                      100%
  LK-LK-LK-W                                         3    21.3  1.00  unknown                    100%
  NB-NB-NB-MB                                        4    21.0  1.00  Incahuasi                  100%
  MB-NB-NB-NB                                        3    21.0  1.00  Incahuasi                  100%
  NB-MB-NB-NB                                        3    21.0  1.00  Incahuasi                  100%
  NB-NB-MB-NB                                        3    21.0  1.00  Incahuasi                  100%
  AB-NB-NB-NB                                        7    20.6  1.00  Incahuasi                  100%
  NB-NB-NB-AB                                        5    20.6  0.88  Incahuasi                  100%
  NB-NB-AB-NB                                        3    20.6  0.90  Incahuasi                  100%
  NB-AB-NB-NB                                        4    20.6  0.92  Incahuasi                  100%
  PR-PR-PR                                           4    26.8  0.85  Ica/Pisco                   76%
  RB:W-RB:W-RB:W-RB:W                                3    40.0  0.83  Santa                       50%
  NB-YB-YB-YB                                        3    20.0  1.00  Incahuasi                  100%

  Entropy table saved: C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\entropy_colour_table.csv

======================================================================
PAPER IV KEY STATISTICS:
  Corpus entropy (FULL_COLOR):  4.995 bits
  Corpus entropy (COLOR_CD_1):  3.630 bits
  Information loss:             1.366 bits (37.6%)
  Unique FULL_COLORs:           720
  Unique COLOR_CD_1s:           65
  Site-specific name candidates: 266
======================================================================
PS C:\Users\aazsh\Desktop\Latest_MDP_research>

'''
'''
PS C:\Users\aazsh\Desktop\Latest_MDP_research> python khipu_mdp.py
===========================================================================
METROLOGICAL DOMAIN PROFILING — INCA KHIPU
Four continents. Clay, stone, string. 3200 BCE to 1532 CE. One method.
===========================================================================

===========================================================================
STEP 1: CORPUS OVERVIEW
===========================================================================

  Khipus: 619
  Cords: 54403
  Knots: 110677
  Colour records: 56306

  Provenance distribution:
    Pachacamac: 90
    Incahuasi: 52
    Ica: 49
    unknown: 46
    Leymebamba: 22
    Huaquerones: 19
    Nazca: 13
    Armatambo, Huaca San Pedro: 11
    Valle de Ica Hacienda Callango Ocucaje: 8
    Between Ica and Pisco: 8
    Paracas: 7
    Hacienda Ullujalla y Callengo: 7
    near Lima: 6
    Santa: 6
    Marquez: 6
    Huacho: 6
    Atarco: 6
    Peru: 5
    "Playa Miller #6, Arica, Chile": 5
    "Chancay, Central Coast": 5

  Region distribution:
    "Central Coast, Peru": 27
    Puruchuco: 24
    Chachapoyas: 22
    "South Coast, Peru": 19
    "Inka, Late Horizon": 18
    unknown: 14
    Nazca: 6
    "North-Central Coast, Peru": 2
    near Lima: 1
    "Inka, Playa Miller": 1
     : 1

  Fiber distribution:
    CN (cotton): 28895
    CL (camelid): 1373
    W (sheep wool): 666
    H (H): 226
    CC (CC): 106
    V (vegetal): 91
    AH (AH): 45

===========================================================================
STEP 2: CORD COLOUR DISTRIBUTION (The 'Commodity Signs')
===========================================================================

  Top 40 cord colours (pendant cords only):
  Code          Count Description                         Hue
  -----------------------------------------------------------------
  W             13608 white                               A
  AB             7459 light brown                         B
  MB             5607 moderate brown                      B
  B              2130 moderate yellowish brown            B
  KB             1845 dark brown                          B
  YB             1841 light yellowish brown               B
  AB:W           1280 compound (AB:W)                     multi
  LB             1152 deep yellowish brown                B
  MB:W           1064 compound (MB:W)                     multi
  NB             1004 strong yellowish brown              B
  KB:W            842 compound (KB:W)                     multi
  HB              736 grayish brown                       B
  GG              626 grayish green                       G
  DB              570 deep brown                          B
  MB:AB           559 compound (MB:AB)                    multi
  RB              516 moderate reddish brown              B
  LK              475 black                               Z
  RL              377 light reddish brown                 B
  BG              370 grayish blue                        H
  BB              310 dark yellowish brown                B
  W:MB            280 compound (W:MB)                     multi
  YG              253 dark grayish green                  G
  CB              251 dark grayish brown                  B
  GG:AB           245 compound (GG:AB)                    multi
  GG:W            243 compound (GG:W)                     multi
  AB-W            240 compound (AB-W)                     multi
  KB:AB           236 compound (KB:AB)                    multi
  KB-W            236 compound (KB-W)                     multi
  BS              205 strong brown                        B
  BG:W            201 compound (BG:W)                     multi
  KB:MB           197 compound (KB:MB)                    multi
  AB:MB           192 compound (AB:MB)                    multi
  DB -W           188 compound (DB -W)                    multi
  LB:W            186 compound (LB:W)                     multi
  B:W             184 compound (B:W)                      multi
  G0              175 grayish olive                       L
  DB :W           168 compound (DB :W)                    multi
  PR              162 deep reddish brown                  B
  MB-W            150 compound (MB-W)                     multi
  LG              141 light greenish gray                 M

===========================================================================
STEP 3: COMPUTING CORD VALUES FROM KNOTS
===========================================================================

  Pendant cords with data: 38736
  Cords with knot values > 0: 24545
  Cords with colour data: 37388

  Value distribution:
    Min: 1
    Median: 15
    Mean: 327.5
    Max: 320535
    Total knot value across corpus: 8,038,367

===========================================================================
STEP 4: CORE MDP — CORD COLOUR DOMAIN PROFILING
===========================================================================

  Colour   Desc                            Cords  Khipus WithVal  Median    Mean     Max S-twist%  S-knot%
  -------------------------------------------------------------------------------------------------------------------
  W        white                           11106     442    7066      20     483  320535      66%      74%
  AB       light brown                      6436     325    4660      12     372  245811      92%      71%
  MB       moderate brown                   5267     305    3406      10     177   36024      88%      67%
  B        moderate yellowish brown         1979      91    1384      12     417   97357      62%      72%
  KB       dark brown                       1881     193     890      10     145   10188      80%      67%
  YB       light yellowish brown            1671     110     993       8      95   11460      74%      65%
  LB       deep yellowish brown             1109      62     609      10     420   85520      50%      77%
  GG       grayish green                     893     133     633      15     513   43372      94%      77%
  DB       deep brown                        734      47     498      45     192   22800      64%      81%
  NB       strong yellowish brown            714      36     410      60     507   10170      83%      82%
  HB       grayish brown                     587      81     326      13     203   16280      92%      71%
  LK       black                             529      29     483      19      20     500      73%       9%
  RB       moderate reddish brown            500      50     399      10      36     930      90%      60%
  RL       light reddish brown               327      60     246      15      74    1320      93%      71%
  BG       grayish blue                      313      60     221      20     165   11598      69%      77%
  CB       dark grayish brown                291      33     186      20     525   38548      87%      82%
  BB       dark yellowish brown              285      26     124      10     357   18504      78%      68%
  YG       dark grayish green                226      22     193     100     350   23098      93%      87%
  BY       light grayish yellowish brow      220      21     152      22      56    2910      70%      70%
  LG       light greenish gray               217      32     144      10     169    3900      71%      69%
  BS       strong brown                      188      16      83       6     370   11544      36%      66%
  G        grayish olive green               164      25     112      18      90    4000      71%      72%
  G0       grayish olive                     133      20     106      20      84    4741      74%      77%
  DB       ?                                 128       6     121      15      18     120       7%       9%
  0D       dark grayish olive green          116       6      84      19      40     300      74%      68%
  BL       pale blue                         111      20      92      32     573    9681      93%      79%
  FB       brownish black                    111      13      75      10      36    1271      35%      45%
  PR       deep reddish brown                105      14      74      10      19     120      99%      51%
  LC       dark grayish blue                  98      19      78       7      57     780      81%      55%
  BD       dark grayish yellowish brown       93       2      43     102     335    3654      12%      81%
  RM       moderate red                       85      19      64      41     276    6136      89%      82%
  0G       light grayish olive                70      18      37       4      17     140      94%      51%
  GL       moderate greenish blue             66      22      38      40     381    7444      48%      81%
  FR       strong reddish brown               54      11      22      40      37      71      93%      78%
  GB       light grayish reddish brown        47      11      11      10      16     100      30%      29%
  GY       olive gray                         45       5      41     101     148     879      44%      84%
  R        dark reddish orange                42      10      27       5       8      30      43%      31%
  MG       medium gray                        39       7      21      12     170    2406      92%      57%
  0B       moderate olive brown               34      14      25      30      89     573      97%      81%
  RD       grayish reddish brown              33       6      15      20     191    2402      39%      80%
  VR       vivid deep red                     31       3       7       2       6      30      97%      33%
  LD       dark bluish gray                   29       4      26       8      23     130       3%      66%
  VB       vivid dark greenish blue           25       5      17      12      28     210     100%      52%
  PB       deep blue                          25       8      13       5      14      60      96%      71%
  LA       bluish gray                        22       5      18       5      14     101      50%      41%
  EB       grayish yellowish brown            20       4      12      40     324    1810      90%      87%
  DG       dark olive green                   18       6      13       8      23      79      50%      75%
  0K       olive black                        17       2      17      20      22      55     100%      63%
  PK       unknown Urton color                16       6      13       6      51     296     100%      62%
  SB       brownish orange                    15       4      13       9      19     110      40%      42%
  RG       greenish gray                      14       6      11      23      51     300      43%      70%
  0L       dark grayish olive                 13       6       8       3       4      15      92%      10%
  0Y       dark orange yellow                 13       2       3       1     454    1360     100%      71%
  KG       dark greenish gray                 11       4       5       6      12      40      18%      62%
  PG       pale green                         10       3       3      11       8      11      22%      33%
  R0       gray reddish orange                10       4       9      40      48     121      20%      97%

===========================================================================
STEP 5: COLOUR CO-OCCURRENCE (Which colours appear together?)
===========================================================================

  Colour pairs that most frequently appear on the SAME khipu:
    AB (light brown) + W (white): 245 khipus
    AB (light brown) + MB (moderate brown): 239 khipus
    MB (moderate brown) + W (white): 235 khipus
    KB (dark brown) + MB (moderate brown): 159 khipus
    AB (light brown) + KB (dark brown): 154 khipus
    KB (dark brown) + W (white): 150 khipus
    AB (light brown) + GG (grayish green): 117 khipus
    GG (grayish green) + W (white): 113 khipus
    GG (grayish green) + MB (moderate brown): 112 khipus
    GG (grayish green) + KB (dark brown): 91 khipus
    AB (light brown) + HB (grayish brown): 72 khipus
    W (white) + YB (light yellowish brow): 69 khipus
    B (moderate yellowish b) + W (white): 66 khipus
    HB (grayish brown) + MB (moderate brown): 65 khipus
    HB (grayish brown) + W (white): 63 khipus
    AB (light brown) + YB (light yellowish brow): 57 khipus
    MB (moderate brown) + YB (light yellowish brow): 55 khipus
    BG (grayish blue) + W (white): 55 khipus
    AB (light brown) + RL (light reddish brown): 54 khipus
    RL (light reddish brown) + W (white): 52 khipus

===========================================================================
STEP 6: TWIST DIRECTION AS DOMAIN MARKER
===========================================================================

  Overall twist distribution:
    S-twist: 28500 cords, median value=16, mean=376
    U-twist: 6499 cords, median value=10, mean=107
    Z-twist: 2632 cords, median value=14, mean=222

===========================================================================
STEP 7: KNOT TYPE × COLOUR CORRELATION
===========================================================================

  Do certain colours preferentially use certain knot types?
  (S=single/tens+, L=long/units, E=figure-eight/one)

  W (white): S=22369(74%), L=6003(20%), E=1483(5%), ''=89(0%), SP=68(0%), TF=25(0%), EE=11(0%), LL=10(0%), BL=4(0%)
  AB (light brown): S=12021(71%), L=3623(22%), E=1077(6%), ''=57(0%), SP=31(0%), TF=9(0%), EE=6(0%)
  MB (moderate brown): S=6651(67%), L=2411(24%), E=805(8%), TF=35(0%), SP=26(0%), ''=13(0%), EE=7(0%), LL=2(0%)
  B (moderate yellowish brown): S=3247(72%), L=1026(23%), E=259(6%), EE=3(0%), ''=1(0%)
  KB (dark brown): S=1754(67%), L=619(24%), E=226(9%), ''=20(1%), TF=9(0%), SP=3(0%)
  YB (light yellowish brown): S=1740(65%), L=642(24%), E=310(12%), EE=3(0%)
  LB (deep yellowish brown): S=1606(77%), L=376(18%), E=113(5%), EE=2(0%), ''=1(0%)
  GG (grayish green): S=1950(77%), L=448(18%), E=123(5%), TF=16(1%), ''=10(0%), EE=1(0%)
  DB  (deep brown): S=1412(81%), L=272(16%), E=67(4%)
  NB (strong yellowish brown): S=1914(82%), L=345(15%), E=73(3%)
  HB (grayish brown): S=752(71%), L=231(22%), E=58(5%), TF=22(2%), ''=3(0%)
  LK (black): L=1278(88%), S=138(9%), E=40(3%), SP=2(0%), LL=1(0%)

===========================================================================
STEP 8: PROVENANCE × COLOUR PALETTE
===========================================================================

  Top colour palette by provenance:

  Pachacamac (4612 cords  med=24, mean=403):
    W=1423, MB=863, AB=544, B=376, YB=229

  Incahuasi (3703 cords  med=100, mean=693):
    W=1032, AB=1030, NB=656, MB=354, YB=159

  Leymebamba (3214 cords  med=6, mean=188):
    MB=1094, AB=777, W=679, KB=278, GG=184

  Ica (2301 cords  med=22, mean=585):
    W=434, DB =265, B=259, AB=242, MB=224

  unknown (2064 cords  med=16, mean=134):
    W=716, AB=468, MB=385, KB=122, HB=65

  Nazca (1976 cords  med=11, mean=103):
    W=577, B=274, LB=260, DB =167, AB=155

  Lluta Valley (1825 cords  med=15, mean=69):
    W=1600, AB=174, KB=23, BS=9, HB=7

  Ica/Pisco (1028 cords  med=32, mean=111):
    MB=278, B=139, KB=115, HB=90, 0D=78

  Santa (823 cords  med=5, mean=34):
    AB=171, YB=143, W=124, RB=118, LG=52

  Between Ica and Pisco (700 cords  med=20, mean=44):
    W=240, B=180, LB=57, CB=44, YB=43

  Huaquerones (668 cords  med=3, mean=39):
    AB=188, W=175, MB=119, KB=40, CB=40

  Huacho (584 cords  med=10, mean=30):
    W=136, AB=97, MB=78, LG=59, YB=58

  "Huaca Perez, Lima (a.k.a Hda. Infantas and Tambo Inca)" (473 cords  med=8, mean=15):
    AB=257, MB=89, W=53, KB=29, GG=20

  Paracas (402 cords  med=39, mean=91):
    W=168, AB=115, KB=42, MB=39, RB=21

  Armatambo, Huaca San Pedro (396 cords  med=10, mean=233):
    W=175, KB=45, AB=38, MB=38, NB=25

  Hacienda Ullujalla y Callengo (267 cords  med=20, mean=97):
    AB=75, KB=46, MB=36, DB =31, W=30

  Valle de Ica Hacienda Callango Ocucaje (262 cords  med=30, mean=318):
    W=83, KB=44, MB=42, AB=41, MG=15

  "Santa Clara, Nazca" (256 cords  med=2, mean=5):
    AB=131, MB=90, HB=34, KB=1

  Ocucaje (235 cords  med=211, mean=924):
    B=82, GG=43, W=38, LB=27, AB=17

  Peru (233 cords  med=11, mean=149):
    W=163, MB=26, AB=22, VB=8, B=6

    (223 cords  med=2, mean=5):
    W=84, AB=31, MB=21, GG=13, RB=13

  Monte de Cacatilla, Valle de Nazca (215 cords  med=50, mean=284):
    AB=63, KB=50, W=35, MB=33, BG=19

  Huaca San Pedro, Armatambo (215 cords  med=10, mean=468):
    W=68, BY=35, AB=27, MB=26, HB=13

  Costa Sur (196 cords  med=850, mean=1677):
    W=101, AB=82, MB=9, RM=3, G=1

  Marquez (193 cords  med=50, mean=229):
    YB=49, W=46, LB=29, DB =25, BS=16

  "Huaura Valley, near Lima, on Santa Rosalia Hacienda" (166 cords  med=6, mean=12):
    AB=53, MB=41, W=30, GG=24, BG=9

  Pisco (166 cords  med=24, mean=29):
    MB=47, BG=45, AB=24, RL=12, LC=11

  Atarco (164 cords  med=2, mean=3):
    AB=115, MB=36, W=13

  Chuquitanta (161 cords  med=48, mean=66):
    W=93, AB=31, MB=18, BG=9, GG=3

  "Playa Miller #6, Arica, Chile" (136 cords  med=4, mean=14):
    KB=60, W=51, AB=13, LK=9, MB=2

  "Pueblo Libre, Lima, Peru" (104 cords  med=10, mean=35):
    MB=38, AB=31, W=30, GG=3, KB=2

  Ullujaya, Ocucaje, Ica (103 cords  med=90, mean=445):
    AB=34, W=30, MB=16, HB=12, KB=6

  "Peru, Fundort: Pachacmac" (96 cords  med=19, mean=31):
    W=50, AB=37, KB=4, MB=4, BG=1

  "Ica Valley, near Callango" (95 cords  med=139, mean=500):
    MB=44, AB=20, GG=9, GL=7, LG=7

  Huari (91 cords  med=13, mean=22):
    AB=90, B=1

  Aankoop (87 cords  med=100, mean=540):
    LB=24, W=23, YB=20, DB =15, BL=4

  Mollepampa (85 cords  med=30, mean=129):
    W=56, AB=27, SR=2

  La Molina (83 cords  med=3649, mean=14920):
    MB=60, AB=19, KB=2, GG=2

  "Maranga, Huaca 1" (74 cords  med=10, mean=24):
    RD=18, W=16, BB=14, G=10, CB=9

  "Chancay, Central Coast" (72 cords  med=15, mean=373):
    AB=33, W=23, MB=7, GG=2, 0B=2

  near Lima (69 cords  med=10, mean=20):
    W=13, LK=12, LB=9, YB=8, B=7

  Unknown (66 cords  med=4, mean=10):
    KB=32, W=19, MB=7, AB=3, VG=2

  Valle de Pisco (59 cords  med=6, mean=9):
    LK=59

  "Hda. Huando, Chancay" (58 cords  med=19, mean=49):
    AB=16, MB=13, W=12, KB=9, BG=6

  Cajamarquilla (52 cords  med=4, mean=4):
    KB=18, AB=14, NB=8, LK=8, DG=4

===========================================================================
STEP 9: SUMMATION CHECKING — Do cord groups sum correctly?
===========================================================================

  Clusters checked (3+ cords with values): 3093
  Last cord = sum of others (exact): 21
  Close matches (±2): 122
  Sum match rate: 4.6%

===========================================================================
STEP 10: COLOUR DOMAIN CLASSIFICATION SUMMARY
===========================================================================

  Colours grouped by hue family:

  COMPOUND/SPECIAL (?) — 128 cords, 1 shades  median=15, mean=18, max=120
    DB: 128 cords, 121 with values, mean=18

  A (A) — 11106 cords, 1 shades  median=20, mean=483, max=320535
    W: 11106 cords, 7066 with values, mean=483

  BROWN (B) — 22575 cords, 22 shades  median=11, mean=275, max=245811
    AB: 6436 cords, 4660 with values, mean=372
    MB: 5267 cords, 3406 with values, mean=177
    B: 1979 cords, 1384 with values, mean=417
    KB: 1881 cords, 890 with values, mean=145
    YB: 1671 cords, 993 with values, mean=95

  GREEN (G) — 1263 cords, 5 shades  median=22, mean=427, max=43372
    GG: 893 cords, 633 with values, mean=513
    YG: 226 cords, 193 with values, mean=350
    0D: 116 cords, 84 with values, mean=40
    DG: 18 cords, 13 with values, mean=23
    PG: 10 cords, 3 with values, mean=8

  BLUE (H) — 638 cords, 6 shades  median=20, mean=237, max=11598
    BG: 313 cords, 221 with values, mean=165
    BL: 111 cords, 92 with values, mean=573
    LC: 98 cords, 78 with values, mean=57
    GL: 66 cords, 38 with values, mean=381
    VB: 25 cords, 17 with values, mean=28

  OLIVE (L) — 380 cords, 4 shades  median=12, mean=74, max=4741
    G: 164 cords, 112 with values, mean=90
    G0: 133 cords, 106 with values, mean=84
    0G: 70 cords, 37 with values, mean=17
    0L: 13 cords, 8 with values, mean=4

  GREY (M) — 377 cords, 7 shades  median=11, mean=134, max=3900
    LG: 217 cords, 144 with values, mean=169
    GY: 45 cords, 41 with values, mean=148
    MG: 39 cords, 21 with values, mean=170
    LD: 29 cords, 26 with values, mean=23
    LA: 22 cords, 18 with values, mean=14

  ORANGE (N) — 67 cords, 3 shades  median=9, mean=18, max=121
    R: 42 cords, 27 with values, mean=8
    SB: 15 cords, 13 with values, mean=19
    R0: 10 cords, 9 with values, mean=48

  RED (R) — 132 cords, 3 shades  median=36, mean=219, max=6136
    RM: 85 cords, 64 with values, mean=276
    VR: 31 cords, 7 with values, mean=6
    PK: 16 cords, 13 with values, mean=51

  YELLOW (Y) — 13 cords, 1 shades  median=1, mean=454, max=1360
    0Y: 13 cords, 3 with values, mean=454

  BLACK (Z) — 657 cords, 3 shades  median=17, mean=22, max=1271
    LK: 529 cords, 483 with values, mean=20
    FB: 111 cords, 75 with values, mean=36
    0K: 17 cords, 17 with values, mean=22

===========================================================================
INCA KHIPU MDP ANALYSIS — COMPLETE
===========================================================================

  CORPUS:
    Khipus: 4
    Pendant cords: 38736
    Knots: 110677
    Cord colours profiled: 56

  KEY QUESTION: Do cord colours cluster into distinct numerical domains?

  HIGH VALUE colours (mean > 100): 25
    W (white): mean=483, 11106 cords
    AB (light brown): mean=372, 6436 cords
    MB (moderate brown): mean=177, 5267 cords
    B (moderate yellowish brown): mean=417, 1979 cords
    KB (dark brown): mean=145, 1881 cords

  MED VALUE colours (mean 20-100): 19
    YB (light yellowish brown): mean=95, 1671 cords
    LK (black): mean=20, 529 cords
    RB (moderate reddish brown): mean=36, 500 cords
    RL (light reddish brown): mean=74, 327 cords
    BY (light grayish yellowish brown): mean=56, 220 cords

  LOW VALUE colours (mean 5-20): 11
    DB (?): mean=18, 128 cords
    PR (deep reddish brown): mean=19, 105 cords
    0G (light grayish olive): mean=17, 70 cords
    GB (light grayish reddish brown): mean=16, 47 cords
    R (dark reddish orange): mean=8, 42 cords

  NO KNOTS colours: 0

  If different colours carry systematically different value ranges,
  this proves colour encodes commodity/category information —
  the same metrological domain separation found on clay tablets
  in Mesopotamia, Iran, South Asia, and the Aegean.

PS C:\Users\aazsh\Desktop\Latest_MDP_research>
'''
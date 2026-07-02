'''

# MDP Corpus_Sweep — Output Log
**Date:** 2 July 2026
**Database:** OKR SQLite (619 khipus, 54,403 cords)
**Script:** corpus_sweep.py

PS C:\Users\aazsh\Desktop\Latest_MDP_research> python corpus_sweep.py
======================================================================
CORPUS-WIDE SYSTEM CLASSIFICATION SWEEP
Database: C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\data\khipu.db
======================================================================

Total khipus in database: 619

Classifying... (this may take 1-2 minutes)

  [30/619] Processing KH0226...
  [60/619] Processing KH0191...
  [90/619] Processing KH0148...
  [120/619] Processing KH0164...
  [150/619] Processing KH0199...
  [180/619] Processing KH0016...
  [210/619] Processing KH0090...
  [240/619] Processing KH0312...
  [270/619] Processing KH0350...
  [300/619] Processing KH0360...
  [330/619] Processing KH0340...
  [360/619] Processing KH0067...
  [390/619] Processing KH0536...
  [420/619] Processing KH0589...
  [450/619] Processing KH0421...
  [480/619] Processing KH0445...
  [510/619] Processing KH0479...
  [540/619] Processing KH0580...
  [570/619] Processing KH0507...
  [600/619] Processing KH0625...

Classified: 612 | Errors (no cords): 7

======================================================================
PHASE 1: SYSTEM CLASSIFICATION
======================================================================
  System A (Logistical/Warehouse):   154  (25.2%)
    - HIGH confidence:                25
    - MEDIUM confidence:             129
  System B (Demographic/Governor):    28  (4.6%)
    - HIGH confidence:                 7
    - MEDIUM confidence:              21
  Mixed / Unclassified:              430  (70.3%)
  ────────────────────────────────────────
  TOTAL CLASSIFIED:                  612

  TOP 15 SYSTEM B SPECIMENS:
  OKR         Score Conf    Fiber    L% Colors  Cords Provenance
  KH0288       0.72 HIGH    CL    99.7      1    115
  KH0280       0.67 HIGH    CL    99.8      1    164
  KH0348       0.64 HIGH    CL    98.3      4     76
  KH0346       0.59 HIGH    CL    97.9      7     89
  KH0282       0.57 HIGH    CL   100.0      3     98
  KH0384       0.57 HIGH    CL    93.4      1     96 Valle de Pisco
  KH0289       0.50 HIGH    H     97.6      2    180
  KH0020       0.47 MEDIUM       100.0      1      9
  KH0094       0.47 MEDIUM       100.0      1      8
  KH0410       0.42 MEDIUM        73.7      1     40 unknown
  KH0178       0.40 MEDIUM        84.6      3     16 Ica
  KH0216       0.38 MEDIUM       100.0      1     19
  KH0078       0.38 MEDIUM        50.0      2      5
  KH0036       0.37 MEDIUM        78.9      4     18
  KH0211       0.33 MEDIUM        71.4      1      8 Ica

  SYSTEM B BY PROVENANCE:
    Unknown                                             16 specimens
    Ica                                                  3 specimens
    unknown                                              3 specimens
    Peru                                                 1 specimens
    Huaquerones                                          1 specimens
    Tambo Colorado                                       1 specimens
    Valle de Pisco                                       1 specimens
    Pachacamac                                           1 specimens
    Cajamarquilla                                        1 specimens

  FLAGS DETECTED:
    POSSIBLE_CANUTOS                     139
    BLANK_TEMPLATE                        24
    MONOCHROME_LARGE                      10
    BINARY_CHECKLIST                       7
    CEDAR_BOX_PATTERN                      6
    LK_ENRICHED_80%                        1
    LK_ENRICHED_50%                        1
    LK_ENRICHED_25%                        1
    LK_ENRICHED_32%                        1
    LK_ENRICHED_40%                        1
    LK_ENRICHED_30%                        1
    LK_ENRICHED_94%                        1
    LK_ENRICHED_28%                        1
    LK_ENRICHED_58%                        1
    LK_ENRICHED_72%                        1
    LK_ENRICHED_61%                        1
    LK_ENRICHED_100%                       1

======================================================================
PHASE 2: VALUE DISTRIBUTION SHAPES
======================================================================

Scanning all 612 khipus...

  DISTRIBUTION SHAPES:
    Arithmetic                 260  (42.5%)
    Zipfian                    175  (28.6%)
    Too few values              99  (16.2%)
    Low-range                   33  (5.4%)
    Binary                      33  (5.4%)
    Gaussian                    11  (1.8%)
    No values                    1  (0.2%)

  SYSTEM C CANDIDATES (Zipfian):
  OKR        SysClass    Score     Mean      Max  Cords Provenance
  KH0426     System_A    -0.32  14669.0 320535.0     78
  KH0404     System_A    -0.62   4750.8   245811    225 La Molina
  KH0521     System_A    -0.34    516.5    45660    198 Huaca San Pedro, Armatambo
  KH0559     System_A    -0.40   3104.8  39263.0     76 Pachacamac
  KH0049     System_A    -0.44   1142.9    27470    367 Costa Sur
  KH0189     System_A    -0.37   1311.9    23500     59 Pachacamac
  KH0270     Mixed       -0.28   1776.1  23379.0     39
  KH0165     Mixed       -0.15   1526.2  21243.0    112 Ocucaje
  KH0247     System_A    -0.53    807.7  15746.0    343 Leymebamba
  KH0362     System_A    -0.37    558.0  15652.0    218 Nazca
  KH0525     System_A    -0.33   1890.1    14550     57 Armatambo, Huaca San Pedro
  KH0187     System_A    -0.45    443.4  11544.0    125 Pachacamac
  KH0100     System_A    -0.32    308.2  11115.0     97 Peru
  KH0254     System_A    -0.53    705.1   9018.0     38 Leymebamba
  KH0238     System_A    -0.70    346.6   8817.0    116 Leymebamba
  KH0237     System_A    -0.39    291.0   8308.0    572 Leymebamba
  KH0421     Mixed       -0.20    817.8     8300     33 "Chancay, Central Coast"
  KH0498     System_A    -0.56    254.3     8071    490 Incahuasi
  KH0155     Mixed       -0.20    731.3     7600     14 Pachacamac
  KH0321     System_A    -0.39    210.1   7364.0    273
  KH0439     System_A    -0.48    692.9   6678.0    137 Pachacamac
  KH0438     Mixed       -0.23    644.9   6669.0     86 Pachacamac
  KH0081     System_A    -0.42    284.1     5920    216 Monte de Cacatilla, Valle de Nazca
  KH0368     Mixed       -0.23    581.7   5597.0     14 unknown
  KH0386     System_A    -0.43    236.9     5430     91 Donation from the collection Belli
  KH0577     Mixed       -0.20    576.5     5280     34 Armatambo, Lima, Central Coast
  KH0385     System_A    -0.53    157.2   5005.0     58 Acari
  KH0435     System_A    -0.53    138.8   4657.0    236 Pachacamac
  KH0511     System_A    -0.37   1054.3     3991    124 Incahuasi
  KH0061     System_A    -0.40    187.2   3654.0    370

  GAUSSIAN SPECIMENS:
  OKR        SysClass    Score     Mean      Max    L% Fiber Provenance
  KH0288     System_B     0.72     15.2     25.0  99.7 CL
  KH0280     System_B     0.67     16.8     22.0  99.8 CL
  KH0348     System_B     0.64      7.5     21.0  98.3 CL
  KH0282     System_B     0.57     18.6     33.0 100.0 CL
  KH0289     System_B     0.50     27.5     46.0  97.6 H
  KH0036     System_B     0.37      6.3     14.0  78.9
  KH0194     Mixed        0.26     26.7       50  34.0 AH   near Lima
  KH0157     Mixed        0.22     22.0     24.0  31.0      Ica
  KH0021     Mixed        0.05     33.4       50  24.3
  KH0233     Mixed        0.00      9.7     18.0  59.0
  KH0158     Mixed       -0.03      9.7     15.0  63.6      Ica

  CROSS-TABULATION: System x Shape
                    Arithmetic       Binary     Gaussian    Low-range    No values Too few values      Zipfian    TOTAL
         System_A           78            4            0            0            0           12           60      154
         System_B            7            0            6            7            0            7            1       28
            Mixed          175           29            5           26            1           80          114      430

======================================================================
PHASE 3: FINAL OKR DEMOGRAPHIC BREAKDOWN
======================================================================
  System A  (Logistical/Warehouse):     154  (25.2%)
  System B  (Demographic/Governor):       28  (4.6%)
  System C  (Categorical/Codebook):      114  (18.6%)  [Mixed + Zipfian]
  Mixed     (unresolved):                316  (51.6%)
  ─────────────────────────────────────────────
  TOTAL:                                 612

  SYSTEM C SPECIMENS:
    KH0245     score=-0.20  mean=4  max=61  Leymebamba
    KH0253     score=-0.28  mean=14  max=211  Leymebamba
    KH0257     score=-0.20  mean=4  max=61  Leymebamba
    KH0225     score=-0.13  mean=9  max=112.0
    KH0113     score=-0.15  mean=22  max=365.0  Ica
    KH0258     score=-0.27  mean=32  max=572.0  Leymebamba
    KH0120     score=-0.28  mean=238  max=3260  Marquez
    KH0126     score= 0.12  mean=10  max=10  Pachacamac
    KH0128     score=-0.23  mean=52  max=703.0  Between Ica and Pisco
    KH0135     score= 0.17  mean=6  max=20  Pachacamac
    KH0143     score=-0.23  mean=85  max=2968.0  Nazca
    KH0082     score=-0.17  mean=34  max=585.0  Lluta Valley
    KH0272     score=-0.12  mean=5  max=21  Nazca
    KH0034     score=-0.06  mean=2  max=11  Nazca
    KH0155     score=-0.20  mean=731  max=7600  Pachacamac
    KH0162     score=-0.15  mean=6  max=64.0  Ica
    KH0165     score=-0.15  mean=1526  max=21243.0  Ocucaje
    KH0173     score=-0.12  mean=4  max=44.0
    KH0180     score= 0.25  mean=12  max=105.0  Pachacamac
    KH0183     score=-0.28  mean=13  max=65.0  Ica
    KH0192     score=-0.23  mean=45  max=445.0  Pachacamac
    KH0193     score=-0.16  mean=40  max=554.0  Nazca
    KH0195     score=-0.08  mean=27  max=335.0  near Lima
    KH0204     score=-0.23  mean=6  max=55.0
    KH0069     score= 0.13  mean=63  max=1110
    KH0013     score= 0.11  mean=6  max=30
    KH0068     score=-0.03  mean=6  max=145.0
    KH0014     score= 0.18  mean=10  max=120
    KH0027     score= 0.01  mean=5  max=42.0
    KH0028     score=-0.13  mean=7  max=406.0
    KH0030     score=-0.08  mean=52  max=1009.0
    KH0054     score=-0.07  mean=9  max=94.0
    KH0098     score=-0.12  mean=148  max=689.0
    KH0102     score=-0.17  mean=12  max=60  Peru
    KH0105     score= 0.13  mean=16  max=189.0  Peru
    KH0048     score=-0.20  mean=37  max=336.0
    KH0278     score= 0.00  mean=10  max=158.0  "Pueblo Libre, Lima, Peru"
    KH0276     score=-0.20  mean=195  max=378.0  "Pueblo Libre, Lima, Peru"
    KH0314     score=-0.13  mean=87  max=1000
    KH0309     score=-0.25  mean=8  max=100  Huaquerones
    KH0310     score=-0.03  mean=32  max=368.0
    KH0311     score=-0.23  mean=10  max=160  Huaquerones
    KH0300     score= 0.02  mean=25  max=367.0
    KH0303     score=-0.25  mean=159  max=2904.0  Huaquerones
    KH0305     score=-0.13  mean=69  max=1236.0
    KH0301     score=-0.23  mean=71  max=1236.0  Huaquerones
    KH0297     score=-0.20  mean=2  max=16.0  Huaquerones
    KH0270     score=-0.28  mean=1776  max=23379.0
    KH0350     score=-0.20  mean=5  max=36.0  Nazca
    KH0349     score=-0.27  mean=12  max=150  Nazca
    KH0295     score=-0.13  mean=18  max=140
    KH0263     score=-0.17  mean=5  max=102.0  Atarco
    KH0104     score= 0.17  mean=11  max=116.0
    KH0101     score= 0.00  mean=6  max=110  Huacho
    KH0108     score=-0.25  mean=49  max=2113.0  Pachacamac
    KH0109     score= 0.00  mean=7  max=60  Pachacamac
    KH0360     score=-0.09  mean=37  max=310  Huacho
    KH0329     score=-0.20  mean=4  max=73.0
    KH0363     score= 0.08  mean=25  max=340  Pachacamac
    KH0364     score=-0.07  mean=75  max=620  Pachacamac
    KH0351     score=-0.09  mean=10  max=60  Pachacamac
    KH0366     score= 0.13  mean=12  max=90  Unknown
    KH0269     score=-0.00  mean=5  max=48.0
    KH0042     score=-0.23  mean=19  max=248.0  Pachacamac
    KH0261     score= 0.00  mean=133  max=870  unknown
    KH0322     score= 0.02  mean=41  max=897.0
    KH0331     score= 0.13  mean=71  max=1256.0  unknown
    KH0333     score=-0.13  mean=4  max=77.0  unknown
    KH0088     score= 0.17  mean=6  max=111  Pachacamac
    KH0097     score=-0.05  mean=162  max=2130.0
    KH0055     score=-0.17  mean=13  max=160.0
    KH0347     score=-0.12  mean=19  max=300
    KH0087     score=-0.15  mean=12  max=121
    KH0079     score=-0.13  mean=26  max=300
    KH0271     score= 0.13  mean=22  max=224.0  Huari
    KH0367     score=-0.17  mean=24  max=162.0  unknown
    KH0368     score=-0.23  mean=582  max=5597.0  unknown
    KH0379     score= 0.18  mean=22  max=211  Valle de Ica Hacienda Callango Ocucaje
    KH0537     score=-0.15  mean=54  max=608.0  Pachacamac
    KH0546     score=-0.07  mean=25  max=272.0  Pachacamac
    KH0561     score=-0.16  mean=364  max=2963.0  Pachacamac
    KH0590     score=-0.07  mean=10  max=94.0
    KH0592     score= 0.11  mean=2  max=3.0
    KH0406     score= 0.08  mean=5  max=35.0  Ica
    KH0421     score=-0.20  mean=818  max=8300  "Chancay, Central Coast"
    KH0409     score= 0.10  mean=8  max=70
    KH0424     score=-0.13  mean=47  max=596.0  "Hda. Huando, Chancay"
    KH0433     score=-0.27  mean=8  max=110  Huacho
    KH0434     score=-0.20  mean=6  max=61  Pachacamac
    KH0438     score=-0.23  mean=645  max=6669.0  Pachacamac
    KH0445     score=-0.27  mean=118  max=1534.0  unknown
    KH0450     score=-0.23  mean=43  max=479.0  Pachacamac
    KH0468     score=-0.27  mean=116  max=898.0  Ica/Pisco
    KH0472     score=-0.27  mean=49  max=712.0  unknown
    KH0478     score=-0.20  mean=12  max=170  Ica
    KH0479     score=-0.03  mean=17  max=201  Pachacamac
    KH0568     score=-0.17  mean=2  max=10  unknown
    KH0570     score=-0.08  mean=4  max=10  unknown
    KH0574     score=-0.24  mean=22  max=100  Región Sur, Quillagua, Valle de Loa
    KH0575     score= 0.01  mean=12  max=20  unknown
    KH0576     score=-0.03  mean=11  max=20  unknown
    KH0577     score=-0.20  mean=576  max=5280  Armatambo, Lima, Central Coast
    KH0581     score= 0.03  mean=20  max=80  unknown
    KH0582     score= 0.03  mean=17  max=70  unknown
    KH0585     score=-0.13  mean=40  max=110  unknown
    KH0587     score=-0.16  mean=27  max=231  unknown
    KH0488     score=-0.23  mean=6  max=100  unknown
    KH0569     score=-0.23  mean=174  max=2660  Costa Sur
    KH0499     score=-0.07  mean=3  max=11  Incahuasi
    KH0509     score=-0.27  mean=9  max=50  Incahuasi
    KH0618     score=-0.27  mean=5  max=20  Incahuasi
    KH0526     score= 0.05  mean=9  max=30  Armatambo, Huaca San Pedro
    KH0527     score=-0.12  mean=3  max=20  Armatambo, Huaca San Pedro
    KH0530     score=-0.28  mean=2  max=20  Armatambo, Huaca San Pedro

  ZIPFIAN ON SYSTEM A HARDWARE (60 specimens):
    KH0426     score=-0.32  mean=14669  max=320535.0  fiber=V
    KH0404     score=-0.62  mean=4751  max=245811  fiber=CN  La Molina
    KH0521     score=-0.34  mean=516  max=45660  fiber=CN  Huaca San Pedro, Armatambo
    KH0559     score=-0.40  mean=3105  max=39263.0  fiber=  Pachacamac
    KH0049     score=-0.44  mean=1143  max=27470  fiber=CN  Costa Sur
    KH0189     score=-0.37  mean=1312  max=23500  fiber=  Pachacamac
    KH0247     score=-0.53  mean=808  max=15746.0  fiber=CN  Leymebamba
    KH0362     score=-0.37  mean=558  max=15652.0  fiber=  Nazca
    KH0525     score=-0.33  mean=1890  max=14550  fiber=CN  Armatambo, Huaca San Pedro
    KH0187     score=-0.45  mean=443  max=11544.0  fiber=  Pachacamac
    KH0100     score=-0.32  mean=308  max=11115.0  fiber=CN  Peru
    KH0254     score=-0.53  mean=705  max=9018.0  fiber=CN  Leymebamba
    KH0238     score=-0.70  mean=347  max=8817.0  fiber=CN  Leymebamba
    KH0237     score=-0.39  mean=291  max=8308.0  fiber=CN  Leymebamba
    KH0498     score=-0.56  mean=254  max=8071  fiber=CN  Incahuasi
    KH0321     score=-0.39  mean=210  max=7364.0  fiber=
    KH0439     score=-0.48  mean=693  max=6678.0  fiber=CN  Pachacamac
    KH0081     score=-0.42  mean=284  max=5920  fiber=CN  Monte de Cacatilla, Valle de Nazca
    KH0386     score=-0.43  mean=237  max=5430  fiber=CN  Donation from the collection Belli
    KH0385     score=-0.53  mean=157  max=5005.0  fiber=CN  Acari

  CSV saved: C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\corpus_sweep_results.csv
  Summary saved: C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\corpus_sweep_summary.md

======================================================================
SWEEP COMPLETE
======================================================================
PS C:\Users\aazsh\Desktop\Latest_MDP_research>

'''
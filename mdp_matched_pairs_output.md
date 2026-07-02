'''
# MDP Matched_Pairs — Output Log
**Date:** 2 July 2026
**Database:** OKR SQLite (619 khipus, 54,403 cords)
**Script:** mdp_matched_pairs.py

PS C:\Users\aazsh\Desktop\Latest_MDP_research> python mdp_matched_pairs.py
======================================================================
MATCHED-PAIR NETWORK + MONTE CARLO VALIDATION
======================================================================

  Loading khipu values...
  Khipus with ≥10 non-zero values: 444
  Finding matched pairs (≥5 sequential matches)...

  MATCHED PAIRS: 3512
    Cross-site: 1747
    Same-site:  1765

  FORMATTING DIRECTION:
    Mono→Poly (receipts UP):     1868
    Poly→Mono (quotas DOWN):     1286
    Same formatting:             358

  TOP CROSS-SITE ROUTES:
    Leymebamba                ↔ Pachacamac                   66 pairs
    Incahuasi                 ↔ Pachacamac                   65 pairs
    Incahuasi                 ↔ unknown                      54 pairs
    Incahuasi                 ↔ Leymebamba                   52 pairs
    Huaquerones               ↔ Pachacamac                   35 pairs
    Huaquerones               ↔ Leymebamba                   33 pairs
    Nazca                     ↔ Pachacamac                   33 pairs
    Huaquerones               ↔ Incahuasi                    30 pairs
    Armatambo, Huaca San Pedr ↔ Incahuasi                    30 pairs
    Incahuasi                 ↔ Nazca                        28 pairs
    Leymebamba                ↔ Nazca                        26 pairs
    "Pueblo Libre, Lima, Peru ↔ Incahuasi                    24 pairs
    Huaca San Pedro, Armatamb ↔ Incahuasi                    24 pairs
    Armatambo, Huaca San Pedr ↔ Leymebamba                   22 pairs
    Pachacamac                ↔ unknown                      22 pairs

  HUB SITES (most cross-site connections):
    Incahuasi                                  467 connections
    Pachacamac                                 417 connections
    Leymebamba                                 383 connections
    Huaquerones                                237 connections
    unknown                                    219 connections
    Nazca                                      201 connections
    Armatambo, Huaca San Pedro                 159 connections
    Ica                                        151 connections
    Atarco                                     140 connections
    Santa                                      128 connections

  MONTE CARLO VALIDATION (N=1000)...
    Monte Carlo iteration 100/1000...
    Monte Carlo iteration 200/1000...
    Monte Carlo iteration 300/1000...
    Monte Carlo iteration 400/1000...
    Monte Carlo iteration 500/1000...
    Monte Carlo iteration 600/1000...
    Monte Carlo iteration 700/1000...
    Monte Carlo iteration 800/1000...
    Monte Carlo iteration 900/1000...
    Monte Carlo iteration 1000/1000...

  RESULTS:
    Observed pairs:   3512
    Null mean:        432.7
    Null max:         523
    Ratio:            8.1×
    Exceeds observed: 0/1000
    p-value:          <0.001

  CSV: C:\Users\aazsh\Desktop\Latest_MDP_research\Karp_Khipu_Graph\matched_pairs.csv
======================================================================
PS C:\Users\aazsh\Desktop\Latest_MDP_research>

'''
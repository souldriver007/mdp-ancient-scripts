-- ============================================================
-- MDP KHIPU RESEARCH: VERIFICATION SQL QUERIES
-- Sharman 2026, DOI: 10.17613/c97d4-pgs78
-- Run against the Open Khipu Repository (OKR) SQLite database
-- ============================================================

-- ============================================================
-- FINDING 1: LK COLOUR ANOMALY (79.5% L-type, chi2=2797)
-- Paper III S2.2: LK-coloured cords are overwhelmingly L-type
-- ============================================================

-- Q1a: L-type percentage by colour
SELECT
    acc.COLOR_CD_1 as colour,
    COUNT(*) as total_knots,
    SUM(CASE WHEN k.TYPE_CODE = 'L' THEN 1 ELSE 0 END) as l_type,
    ROUND(100.0 * SUM(CASE WHEN k.TYPE_CODE = 'L' THEN 1 ELSE 0 END) / COUNT(*), 1) as l_pct,
    SUM(CASE WHEN k.TYPE_CODE = 'S' THEN 1 ELSE 0 END) as s_type,
    ROUND(100.0 * SUM(CASE WHEN k.TYPE_CODE = 'S' THEN 1 ELSE 0 END) / COUNT(*), 1) as s_pct
FROM cord c
JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
JOIN knot k ON c.CORD_ID = k.CORD_ID
WHERE acc.COLOR_CD_1 != '' AND acc.COLOR_CD_1 IS NOT NULL
GROUP BY acc.COLOR_CD_1
HAVING total_knots > 100
ORDER BY l_pct DESC;

-- Expected: LK should show ~79.5% L-type (highest of any colour)
-- Compare to corpus average of ~24% L-type


-- ============================================================
-- FINDING 2: FIBER REDEFINES VALUE DOMAINS (41x ratio)
-- Paper III S2.1: Cotton mean >> Camelid mean
-- ============================================================

-- Q2a: Mean pendant value by fiber type
SELECT
    c.FIBER,
    COUNT(DISTINCT c.CORD_ID) as n_cords,
    ROUND(AVG(cord_val.value), 1) as mean_value,
    MAX(cord_val.value) as max_value
FROM cord c
JOIN (
    SELECT CORD_ID,
           COALESCE(SUM(CASE
               WHEN TYPE_CODE = 'S' THEN knot_value_type
               WHEN TYPE_CODE = 'L' THEN NUM_TURNS
               WHEN TYPE_CODE = 'E' THEN 1
               ELSE 0 END), 0) as value
    FROM knot GROUP BY CORD_ID
) cord_val ON c.CORD_ID = cord_val.CORD_ID
WHERE c.FIBER IN ('CN', 'CL') AND c.CORD_LEVEL = 1 AND cord_val.value > 0
GROUP BY c.FIBER;

-- Expected: CN (cotton) mean ~294, CL (camelid) mean ~7, ratio ~41x


-- ============================================================
-- FINDING 3: CANUTITO INDEPENDENCE (98.6% colour-divergent)
-- Paper III S5.1: Canutitos differ from parent cord colour
-- ============================================================

-- Q3a: How many canutitos match vs differ from parent colour
SELECT
    CASE WHEN child_acc.COLOR_CD_1 = parent_acc.COLOR_CD_1
         THEN 'MATCH' ELSE 'DIFFERENT' END as colour_relation,
    COUNT(*) as n,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cord
        WHERE CORD_LEVEL > 1
        AND CORD_ID IN (SELECT CORD_ID FROM ascher_cord_color WHERE PCORD_FLAG = 0)), 1) as pct
FROM cord child
JOIN cord parent ON child.KHIPU_ID = parent.KHIPU_ID
    AND child.CORD_LEVEL = parent.CORD_LEVEL + 1
JOIN ascher_cord_color child_acc ON child.CORD_ID = child_acc.CORD_ID AND child_acc.PCORD_FLAG = 0
JOIN ascher_cord_color parent_acc ON parent.CORD_ID = parent_acc.CORD_ID AND parent_acc.PCORD_FLAG = 0
WHERE child.CORD_LEVEL > 1
    AND child_acc.COLOR_CD_1 != '' AND parent_acc.COLOR_CD_1 != ''
GROUP BY colour_relation;

-- Expected: DIFFERENT ~98.6%, MATCH ~1.4%


-- ============================================================
-- FINDING 4: WARI WRAPPED KHIPUS = SYSTEM B
-- Wrapped-structure khipus match System B profile
-- NOTE: STRUCTURE is on primary_cord table, not khipu_main
-- ============================================================

-- Q4a: All wrapped-structure khipus with their knot profiles
SELECT
    km.OKR_NUM, km.KHIPU_ID, km.PROVENANCE, pc.STRUCTURE,
    COUNT(DISTINCT c.CORD_ID) as n_cords,
    ROUND(100.0 * SUM(CASE WHEN k.TYPE_CODE = 'L' THEN 1 ELSE 0 END) / NULLIF(COUNT(k.KNOT_ID), 0), 1) as l_pct,
    ROUND(100.0 * SUM(CASE WHEN k.TYPE_CODE = 'S' THEN 1 ELSE 0 END) / NULLIF(COUNT(k.KNOT_ID), 0), 1) as s_pct,
    ROUND(AVG(CASE WHEN k.TYPE_CODE IN ('S','L','E') THEN
        CASE WHEN k.TYPE_CODE = 'S' THEN k.knot_value_type
             WHEN k.TYPE_CODE = 'L' THEN k.NUM_TURNS
             WHEN k.TYPE_CODE = 'E' THEN 1 END
    END), 1) as mean_value
FROM khipu_main km
JOIN primary_cord pc ON km.KHIPU_ID = pc.KHIPU_ID
JOIN cord c ON km.KHIPU_ID = c.KHIPU_ID AND c.CORD_LEVEL = 1
LEFT JOIN knot k ON c.CORD_ID = k.CORD_ID
WHERE pc.STRUCTURE = 'W'
GROUP BY km.KHIPU_ID;

-- Expected: 3 khipus. 2/3 should show >95% L-type (System B profile)
-- KH0346: ~98% L, KH0282: ~100% L, KH0118: ~8% L (cotton control)


-- ============================================================
-- FINDING 5: ZERO-VALUE KB STRUCTURAL CORDS
-- KB cords are 97% zero-value on KH0082 = structural markers
-- ============================================================

-- Q5a: Zero-value percentage of KB cords on KH0082 (id=1000096)
SELECT
    acc.COLOR_CD_1 as colour,
    COUNT(DISTINCT c.CORD_ID) as n_cords,
    SUM(CASE WHEN cord_val.value = 0 OR cord_val.value IS NULL THEN 1 ELSE 0 END) as n_zero,
    ROUND(100.0 * SUM(CASE WHEN cord_val.value = 0 OR cord_val.value IS NULL THEN 1 ELSE 0 END)
          / COUNT(DISTINCT c.CORD_ID), 1) as zero_pct
FROM cord c
JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
LEFT JOIN (
    SELECT CORD_ID,
           COALESCE(SUM(CASE
               WHEN TYPE_CODE = 'S' THEN knot_value_type
               WHEN TYPE_CODE = 'L' THEN NUM_TURNS
               WHEN TYPE_CODE = 'E' THEN 1
               ELSE 0 END), 0) as value
    FROM knot GROUP BY CORD_ID
) cord_val ON c.CORD_ID = cord_val.CORD_ID
WHERE c.KHIPU_ID = 1000096 AND c.CORD_LEVEL = 1
    AND acc.COLOR_CD_1 NOT IN ('W', 'AB', '')
GROUP BY acc.COLOR_CD_1
ORDER BY zero_pct DESC;

-- Expected: KB ~97% zero, SR 100% zero, HB 100% zero, FB 100% zero, BS ~92% zero


-- ============================================================
-- FINDING 6: SR DIVIDERS AT PERFECT 11-PENDANT INTERVALS (KH0083)
-- ============================================================

-- Q6a: SR cord positions on KH0083 (id=1000279)
SELECT c.CORD_ORDINAL as position, acc.COLOR_CD_1 as colour
FROM cord c
JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
WHERE c.KHIPU_ID = 1000279 AND c.CORD_LEVEL = 1 AND acc.COLOR_CD_1 = 'SR'
ORDER BY c.CORD_ORDINAL;

-- Expected: positions 1, 12, 23, 34, 45, 56, 67 (perfect period 11)


-- ============================================================
-- FINDING 7: CUT CORDS (AUDIT TRAIL)
-- Only 7 cut cords in entire corpus, all on System A
-- ============================================================

-- Q7a: All cords with TERMINATION = 'C'
SELECT km.OKR_NUM, c.KHIPU_ID, c.CORD_ORDINAL, c.CORD_LEVEL,
       acc.COLOR_CD_1 as colour,
       COALESCE((SELECT SUM(CASE
           WHEN k.TYPE_CODE = 'S' THEN k.knot_value_type
           WHEN k.TYPE_CODE = 'L' THEN k.NUM_TURNS
           WHEN k.TYPE_CODE = 'E' THEN 1 ELSE 0 END)
       FROM knot k WHERE k.CORD_ID = c.CORD_ID), 0) as value
FROM cord c
JOIN khipu_main km ON c.KHIPU_ID = km.KHIPU_ID
LEFT JOIN ascher_cord_color acc ON c.CORD_ID = acc.CORD_ID AND acc.PCORD_FLAG = 0
WHERE c.TERMINATION = 'C'
ORDER BY c.KHIPU_ID, c.CORD_ORDINAL;

-- Expected: 7 rows. 6 on KH0321 (ordinals 1-6, all value 0), 1 on KH0526 (ordinal 43)


-- ============================================================
-- FINDING 8: NON-STANDARD KNOT CENSUS
-- ============================================================

-- Q8a: All knot types in corpus with counts
SELECT TYPE_CODE, COUNT(*) as n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM knot), 2) as pct
FROM knot
GROUP BY TYPE_CODE
ORDER BY n DESC;

-- Expected: S ~75K, L ~26K, E ~8K, then '' ~253, SP ~247, etc.
-- Non-standard total: ~886 (0.80%)


-- ============================================================
-- END OF VERIFICATION QUERIES
-- ============================================================

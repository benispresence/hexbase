VACUUM FULL dl_ethereum.transactions;

SELECT relname, last_vacuum, last_autovacuum FROM pg_stat_user_tables;


EXPLAIN (ANALYZE , BUFFERS)

SELECT *
FROM eth.transactions
ORDER BY hash DESC LIMIT 3;

EXPLAIN (ANALYZE , BUFFERS)

SELECT (CAST(avg("eth"."blocks"."difficulty") AS float) / CASE WHEN 1.0E12 = 0 THEN NULL ELSE 1.0E12 END) AS "avg_difficulty_th"
FROM "eth"."blocks"
WHERE ("eth"."blocks"."block_number" <> 0
    OR "eth"."blocks"."block_number" IS NULL);

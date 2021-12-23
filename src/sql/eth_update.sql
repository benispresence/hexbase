WITH base AS (
    SELECT count(*) AS txns, block_number
    FROM eth.transactions
    GROUP BY block_number
    )

UPDATE eth.blocks b
SET transactions = txns
FROM base t
WHERE t.block_number=b.block_number;

UPDATE eth.transactions t
SET timestamp = b.timestamp
FROM eth.blocks b
WHERE t.block_number=b.block_number;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA eth TO dl_loader;
GRANT ALL PRIVILEGES ON SCHEMA eth TO dl_loader;
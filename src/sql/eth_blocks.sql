DROP TABLE IF EXISTS  eth.blocks;
CREATE TABLE IF NOT EXISTS eth.blocks AS (
    SELECT number :: INT AS block_number,
           to_timestamp(timestamp :: BIGINT) AS timestamp,
           NULL :: BIGINT AS transactions,
           miner AS mined_by,
           NULL :: INT AS static_block_reward,
           difficulty :: BIGINT AS difficulty,
           totaldifficulty :: NUMERIC AS total_difficulty,
           size :: BIGINT AS size,
           gasused :: BIGINT AS gas_used,
           gaslimit ::BIGINT AS gas_limit,
           extradata :: BYTEA,
           basefeepergas :: FLOAT,
           hash AS block_hash,
           parenthash AS parent_block_hash,
           sha3uncles,
           stateroot,
           nonce,
           uncles
            -- logsbloom, mixhash,   receiptsroot,   transactionsroot not included yet
    FROM dl_ethereum.blocks
);

UPDATE eth.blocks
SET static_block_reward = CASE  WHEN block_number <= 4369999                    THEN 5
                                WHEN block_number BETWEEN 4370000 AND 7279999   THEN 3
                                WHEN block_number >= 7280000                    THEN 2
                         END
WHERE TRUE;

ANALYZE eth.blocks;
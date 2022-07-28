CREATE SCHEMA IF NOT EXISTS hex_ol;
DROP TABLE IF EXISTS hex_ol.stakes;
CREATE TABLE hex_ol.stakes AS (
    SELECT ss.stake_id::INT                                                         AS id,
           ss.staker_address::CHAR(42)                                              AS address,
           ss.staked_hearts::NUMERIC/100000000                                      AS principal,
           ss.stake_shares::NUMERIC/1000000000000                                   AS t_shares,
           payout::NUMERIC/100000000                                                AS payout,
           penalty::NUMERIC/100000000                                               AS penalty,
           ss.staked_hearts::NUMERIC/100000000
               + payout::NUMERIC/100000000
               - penalty::NUMERIC/100000000                                         AS total_payout,
           (payout::NUMERIC/100000000 - penalty::NUMERIC/100000000)
               / (ss.staked_hearts::NUMERIC/100000000
                      + payout::NUMERIC/100000000
                      - penalty::NUMERIC/100000000)                                 AS yield,
           staked_days :: INT                                                       AS staked_days,
           served_days :: INT                                                       AS served_days,
           to_timestamp(timestamp_stake_start :: BIGINT) :: TIMESTAMP               AS created_at,
           to_timestamp(timestamp_stake_end :: BIGINT) :: TIMESTAMP                 AS ended_at,
           to_timestamp(timestamp_stake_start :: BIGINT) :: DATE + 1                AS started_at,
           is_auto_stake :: BOOLEAN                                                 AS is_auto_stake,
           prev_unlocked :: BOOLEAN                                                 AS previously_unlocked,
           ss.transaction_hash :: CHAR(66)                                          AS start_transaction_hash,
           se.transaction_hash :: CHAR(66)                                          AS end_transaction_hash
    FROM hex_events.stake_starts ss
    LEFT JOIN hex_events.stake_ends se ON ss.stake_id=se.stake_id
    ORDER BY id
);

ALTER TABLE hex_ol.stakes ADD PRIMARY KEY (id);
ALTER TABLE hex_ol.stakes ADD FOREIGN KEY (address) REFERENCES hex_ol.users (address);
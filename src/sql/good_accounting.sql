CREATE SCHEMA IF NOT EXISTS hex_ol;
DROP TABLE IF EXISTS hex_ol.good_accounting;
CREATE TABLE hex_ol.good_accounting AS (
    SELECT
        sender_address::CHAR(42)            AS address,
        stake_id :: INT                     AS stake_id,
        to_timestamp(created_at::BIGINT)    AS accounted_at,
        payout::NUMERIC/100000000           AS payout_accounted,
        penalty::NUMERIC/100000000          AS penalty_accounted,
        transaction_hash::CHAR(66)          AS transaction_hash,
        log_index::INT                      AS log_index
    FROM hex_events.stake_good_accountings
    ORDER BY created_at, transaction_hash, log_index
);

ALTER TABLE hex_ol.good_accounting ADD COLUMN id SERIAL;
ALTER TABLE hex_ol.good_accounting ADD PRIMARY KEY (id);
--todo: ALTER TABLE hex_ol.good_accounting ADD FOREIGN KEY (stake_id) REFERENCES hex_ol.stakes (id);
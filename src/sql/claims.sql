CREATE SCHEMA IF NOT EXISTS hex_ol;
DROP TABLE IF EXISTS hex_ol.claims;
CREATE TABLE hex_ol.claims AS (
    SELECT
        claim_to_address::CHAR(42)          AS address,
        to_timestamp(created_at :: BIGINT)  AS created_at,
        claimed_hearts::NUMERIC/100000000   AS amount,
        referrer_address::CHAR(42)          AS referrer_address,
        transaction_hash::CHAR(66)          AS transaction_hash,
        log_index :: INT                    AS log_index
    FROM hex_events.claims
    ORDER BY created_at, transaction_hash, log_index
);

ALTER TABLE hex_ol.claims ADD COLUMN id SERIAL;
ALTER TABLE hex_ol.claims ADD PRIMARY KEY (id);
ALTER TABLE hex_ol.claims ADD FOREIGN KEY (address) REFERENCES hex_ol.users (address);
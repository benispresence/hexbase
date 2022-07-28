CREATE SCHEMA IF NOT EXISTS hex_ol;
DROP TABLE IF EXISTS hex_ol.transfers;
CREATE TABLE hex_ol.transfers AS (
    SELECT
        e.from_address::CHAR(42)                                    AS address,
        e.to_address::CHAR(42)                                      AS recipient_address,
        to_timestamp(coalesce(t.timestamp,it.timestamp)::BIGINT)    AS created_at,
        e.transfer_value::NUMERIC/100000000                         AS amount,
        e.transaction_hash::CHAR(66)                                AS transaction_hash,
        e.log_index :: INT                                          AS log_index
    FROM hex_events.transfers e
    LEFT JOIN hex.transactions t ON t.hash=e.transaction_hash
    LEFT JOIN hex.indirect_transactions it ON  it.hash=e.transaction_hash
    ORDER BY created_at,transaction_hash, log_index
);

ALTER TABLE hex_ol.transfers ADD COLUMN id SERIAL;
ALTER TABLE hex_ol.transfers ADD PRIMARY KEY (id);
ALTER TABLE hex_ol.transfers ADD FOREIGN KEY (address) REFERENCES hex_ol.users (address);
DROP TABLE IF EXISTS  eth.transactions;
CREATE TABLE IF NOT EXISTS eth.transactions AS (
    SELECT hash,
           blocknumber :: INT AS block_number,
           NULL :: TIMESTAMP AS timestamp,
           input :: BYTEA,
           from_address,
           to_address,
           CASE WHEN gas = '' THEN NULL ELSE gas :: BIGINT END AS gas_limit,
           CASE WHEN gasprice = '' THEN NULL ELSE gasprice :: BIGINT/1000000000 END AS gas_price_gwei,
           CASE WHEN nonce = '' THEN NULL ELSE nonce :: BIGINT END AS nonce,
           CASE WHEN transactionindex = '' THEN NULL ELSE transactionindex :: BIGINT END AS position,
           type,
           CASE WHEN value = '' THEN 0 ELSE value:: NUMERIC/1000000000000000000 END AS value_eth
           -- r, s, v did not include these
    FROM dl_ethereum.transactions d
);


ANALYZE eth.transactions;




/* ONLY RUN ONCE */
DROP TABLE IF EXISTS  dl_ethereum.transactions;
CREATE TABLE IF NOT EXISTS dl_ethereum.transactions(
    blockHash TEXT,
    blockNumber TEXT,
    from_address TEXT,
    gas TEXT,
    gasPrice TEXT,
    hash TEXT,
    input TEXT,
    nonce TEXT,
    r TEXT,
    s TEXT,
    to_address TEXT,
    transactionIndex TEXT,
    type TEXT,
    v TEXT,
    value TEXT

);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dl_ethereum TO dl_loader;




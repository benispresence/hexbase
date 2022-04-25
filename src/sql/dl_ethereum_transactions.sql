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

/* INDEXES */
CREATE INDEX CONCURRENTLY to_address_and_block_number_ndx ON dl_ethereum.transactions(to_address, blocknumber);

/* PERMISSIONS */
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dl_ethereum TO dl_loader;

/* COLUMNS: accessList, chainId */
ALTER TABLE dl_ethereum.transactions
ADD COLUMN accessList TEXT ARRAY;

ALTER TABLE dl_ethereum.transactions
ADD COLUMN chainId TEXT;

/* PRIMARY KEY */
ALTER TABLE dl_ethereum.transactions ADD PRIMARY KEY (hash);

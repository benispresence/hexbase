/* ONLY RUN ONCE */
DROP TABLE IF EXISTS  dl_ethereum.blocks;
CREATE TABLE IF NOT EXISTS dl_ethereum.blocks(
    baseFeePerGas  TEXT,
    difficulty TEXT,
    extraData TEXT,
    gasLimit TEXT,
    gasUsed TEXT,
    hash TEXT,
    logsBloom TEXT,
    miner TEXT,
    mixHash TEXT,
    nonce TEXT,
    number TEXT,
    parentHash TEXT,
    receiptsRoot TEXT,
    sha3Uncles TEXT,
    size TEXT,
    stateRoot TEXT,
    timestamp TEXT,
    totalDifficulty TEXT,
    transactions TEXT,
    transactionsRoot TEXT,
    uncles  TEXT

);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dl_ethereum TO dl_loader;




/* ONLY RUN ONCE */
DROP TABLE IF EXISTS  hex.transactions;
CREATE TABLE IF NOT EXISTS hex.transactions(
    block_number INT,
    transaction_hash TEXT,
    address TEXT,
    gas             INT,
    gas_price       INT,
    function_called TEXT,
    argument_1_name TEXT,
    argument_1_value TEXT,
    argument_2_name TEXT,
    argument_2_value TEXT,
    argument_3_name TEXT,
    argument_3_value TEXT,
    argument_4_name TEXT,
    argument_4_value TEXT,
    argument_5_name TEXT,
    argument_5_value TEXT,
    argument_6_name TEXT,
    argument_6_value TEXT,
    argument_7_name TEXT,
    argument_7_value TEXT,
    argument_8_name TEXT,
    argument_8_value TEXT,
    argument_9_name TEXT,
    argument_9_value TEXT,
    argument_10_name TEXT,
    argument_10_value TEXT,
    argument_11_name TEXT,
    argument_11_value TEXT
);

/* PERMISSIONS */
GRANT ALL PRIVILEGES ON SCHEMA hex TO dl_loader;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA hex TO dl_loader;

ANALYZE hex.transactions;
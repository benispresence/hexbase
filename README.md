# Hexbase v.1

An ETL pipeline to load Hex cryptocurrency (Hex.com) related data into a postgres DWH (Data-warehouse).
Data Source is the ethereum blockchain.

## Configuration
Set up a local ethereum node and host a rpc connection on "http://localhost:8545". 
Additionally configure a file named "global_config.ini" and adjust the PATH_CONFIG in configs/credentials.py .


## Usage
Run the hex.py and uniswap_v2.py file periodically.

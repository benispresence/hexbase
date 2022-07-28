CREATE SCHEMA IF NOT EXISTS hex_ol;
DROP TABLE IF EXISTS hex_ol.users;
CREATE TABLE hex_ol.users AS (
    SELECT DISTINCT claim_to_address AS address
    FROM hex_events.claims


    UNION

    SELECT DISTINCT from_address AS address
    FROM hex_events.transfers


    UNION

    SELECT DISTINCT staker_address AS address
    FROM hex_events.stake_starts

    UNION

    SELECT DISTINCT owner_address AS address
    FROM hex_events.approvals
);

ALTER TABLE hex_ol.users ADD PRIMARY KEY (address);

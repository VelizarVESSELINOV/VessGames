CREATE SCHEMA IF NOT EXISTS vstore;

CREATE TABLE IF NOT EXISTS vstore.continent (
    continent_iso2_code TEXT,
    continent_name TEXT,
    PRIMARY KEY(continent_iso2_code)
);
CREATE TABLE IF NOT EXISTS vstore.country (
    country_iso2_code TEXT,
    country_name TEXT,
    continent TEXT,
    PRIMARY KEY(country_iso2_code),
    FOREIGN KEY(continent) REFERENCES vstore.continent (continent_iso2_code)
);
CREATE TABLE IF NOT EXISTS vstore.subregion (
    subregion_iso2_code TEXT,
    country_iso2_code TEXT,
    subregion_name TEXT,
    PRIMARY KEY(subregion_iso2_code),
    FOREIGN KEY(country_iso2_code) REFERENCES vstore.country (country_iso2_code)
);
CREATE TABLE IF NOT EXISTS vstore.user (
    user_id TEXT,     -- ID from source
    user_source TEXT,  -- GitHub, LinkedIn
    nick_name TEXT,
    first_name TEXT,
    last_name TEXT,
    image TEXT,
    location TEXT,
    email TEXT,
    country_iso2_code TEXT,
    region_iso_code TEXT,
    PRIMARY KEY(user_id, user_source),
    FOREIGN KEY(country_iso2_code) REFERENCES vstore.country (country_iso2_code)
);
CREATE TABLE IF NOT EXISTS vstore.session (
    user_id TEXT,
    user_source TEXT,
    login TIMESTAMP,
    logout TIMESTAMP,
    country_iso2_code TEXT,
    region_iso_code TEXT,
    PRIMARY KEY(user_id, user_source, login),
    FOREIGN KEY(user_id, user_source) REFERENCES vstore.user (user_id, user_source)
);
CREATE TABLE IF NOT EXISTS vstore.app (
    app_id TEXT,
    description TEXT,
    PRIMARY KEY(app_id)
);
CREATE TABLE IF NOT EXISTS vstore.game (
    user_id TEXT,
    user_source TEXT,
    app_id TEXT,
    start TIMESTAMP,
    submit TIMESTAMP,
    score REAL,
    PRIMARY KEY(user_id, user_source, app_id, start),
    FOREIGN KEY(user_id, user_source) REFERENCES vstore.user (user_id, user_source),
    FOREIGN KEY(app_id) REFERENCES vstore.app (app_id)
);

CREATE TABLE music_locations (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    music_file BYTEA NOT NULL
);

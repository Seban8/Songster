DROP TABLE IF EXISTS sings CASCADE;
DROP TABLE IF EXISTS song_producer CASCADE;
DROP TABLE IF EXISTS song_genre CASCADE;
DROP TABLE IF EXISTS songs CASCADE;
DROP TABLE IF EXISTS albums CASCADE;
DROP TABLE IF EXISTS artists CASCADE;
DROP TABLE IF EXISTS producers CASCADE;
DROP TABLE IF EXISTS genres CASCADE;

CREATE TABLE genres (
    genre_name TEXT PRIMARY KEY
);

CREATE TABLE producers (
    prod_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE,
    bio TEXT
);

CREATE TABLE artists (
    art_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE,
    bio TEXT
);

CREATE TABLE albums (
    alb_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    release_date DATE,
    art_id INT REFERENCES artists(art_id) ON DELETE SET NULL
);

CREATE TABLE songs (
    song_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    release_date DATE,
    duration INT CHECK (duration IS NULL OR duration > 0),
    alb_id INT REFERENCES albums(alb_id) ON DELETE SET NULL
);

CREATE TABLE song_genre (
    song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
    genre_name TEXT REFERENCES genres(genre_name) ON DELETE CASCADE,
    PRIMARY KEY (song_id, genre_name)
);

CREATE TABLE song_producer (
    song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
    prod_id INT REFERENCES producers(prod_id) ON DELETE CASCADE,
    PRIMARY KEY (song_id, prod_id)
);

CREATE TABLE sings (
    song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
    art_id INT REFERENCES artists(art_id) ON DELETE CASCADE,
    PRIMARY KEY (song_id, art_id)
);

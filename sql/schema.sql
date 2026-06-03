DROP VIEW IF EXISTS song_catalog CASCADE;

DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS sings CASCADE;
DROP TABLE IF EXISTS song_producer CASCADE;
DROP TABLE IF EXISTS song_genre CASCADE;
DROP TABLE IF EXISTS songs CASCADE;
DROP TABLE IF EXISTS albums CASCADE;
DROP TABLE IF EXISTS artists CASCADE;
DROP TABLE IF EXISTS producers CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE genres (
    genre_name TEXT PRIMARY KEY
);

CREATE TABLE users (
    user_id INT PRIMARY KEY CHECK (user_id BETWEEN 1 AND 5),
    display_name TEXT NOT NULL
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

CREATE TABLE reviews (
    song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    PRIMARY KEY (song_id, user_id)
);

CREATE VIEW song_catalog AS
SELECT
    s.song_id,
    s.title,
    s.release_date,
    s.duration,
    a.title AS album_title,
    STRING_AGG(DISTINCT ar.name, ', ') AS artists,
    STRING_AGG(DISTINCT sg.genre_name, ', ') AS genres,
    STRING_AGG(DISTINCT p.name, ', ') AS producers
FROM songs s
LEFT JOIN albums a ON a.alb_id = s.alb_id
LEFT JOIN sings si ON si.song_id = s.song_id
LEFT JOIN artists ar ON ar.art_id = si.art_id
LEFT JOIN song_genre sg ON sg.song_id = s.song_id
LEFT JOIN song_producer sp ON sp.song_id = s.song_id
LEFT JOIN producers p ON p.prod_id = sp.prod_id
GROUP BY s.song_id, s.title, s.release_date, s.duration, a.title;

-- Lookup seed data only. Songs, albums, artists and labels are imported from
-- data/Liked_Songs.csv by scripts/import_liked_songs.py.

INSERT INTO genres (genre_name) VALUES
    ('Unknown')
ON CONFLICT (genre_name) DO NOTHING;

-- Lookup seed data only. Songs, albums, artists and labels are imported from
-- data/Liked_Songs.csv by scripts/import_liked_songs.py.

INSERT INTO genres (genre_name) VALUES
    ('Unknown')
ON CONFLICT (genre_name) DO NOTHING;

INSERT INTO users (user_id, display_name) VALUES
    (1, 'User 1'),
    (2, 'User 2'),
    (3, 'User 3'),
    (4, 'User 4'),
    (5, 'User 5')
ON CONFLICT (user_id) DO NOTHING;

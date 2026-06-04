WITH first_songs AS (
    SELECT
        song_id,
        ROW_NUMBER() OVER (ORDER BY title) AS song_position
    FROM song_catalog
    ORDER BY title
    LIMIT 5
)
INSERT INTO reviews (song_id, user_id, rating, comment)
SELECT
    first_songs.song_id,
    users.user_id,
    ((first_songs.song_position + users.user_id - 2) % 5) + 1 AS rating,
    'Review from ' || users.display_name || ' for one of the first songs.' AS comment
FROM first_songs
CROSS JOIN users
ON CONFLICT (song_id, user_id)
DO UPDATE SET
    rating = EXCLUDED.rating,
    comment = EXCLUDED.comment;

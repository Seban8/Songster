import re

from database import db_connection


class Song:
    def __init__(self, song_data):
        self.id = song_data[0]
        self.title = song_data[1]
        self.release_date = song_data[2]
        self.duration = song_data[3]
        self.album_title = song_data[4]
        self.artists = song_data[5]
        self.genres = song_data[6]
        self.producers = song_data[7]
        self.album_id = song_data[8]

    @property
    def duration_display(self):
        if not self.duration:
            return "Unknown"

        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"


def rows_to_songs(rows):
    songs = []
    for row in rows:
        songs.append(Song(row))
    return songs


def list_songs():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            sc.song_id,
            sc.title,
            sc.release_date,
            sc.duration,
            sc.album_title,
            sc.artists,
            sc.genres,
            sc.producers,
            s.alb_id
        FROM song_catalog sc
        JOIN songs s ON s.song_id = sc.song_id
        ORDER BY title
        """
    )
    songs = rows_to_songs(cur.fetchall())
    cur.close()
    conn.close()
    return songs


def search_songs(pattern):
    regex = re.compile(pattern, re.IGNORECASE)
    songs = list_songs()
    return [
        song
        for song in songs
        if regex.search(song.title)
        or regex.search(song.artists or "")
        or regex.search(song.album_title or "")
        or regex.search(song.genres or "")
    ]


def get_song(song_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            sc.song_id,
            sc.title,
            sc.release_date,
            sc.duration,
            sc.album_title,
            sc.artists,
            sc.genres,
            sc.producers,
            s.alb_id
        FROM song_catalog sc
        JOIN songs s ON s.song_id = sc.song_id
        WHERE sc.song_id = %s
        """,
        (song_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return Song(row) if row else None


def create_song(title, release_date, duration, album_id, artist_id, genre_name, producer_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO songs (title, release_date, duration, alb_id)
        VALUES (%s, %s, %s, %s)
        RETURNING song_id
        """,
        (title, release_date or None, duration or None, album_id or None),
    )
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("Song insert did not return a song_id")

    song_id = row[0]

    if artist_id:
        cur.execute("INSERT INTO sings (song_id, art_id) VALUES (%s, %s)", (song_id, artist_id))
    if genre_name:
        cur.execute(
            "INSERT INTO song_genre (song_id, genre_name) VALUES (%s, %s)",
            (song_id, genre_name),
        )
    if producer_id:
        cur.execute(
            "INSERT INTO song_producer (song_id, prod_id) VALUES (%s, %s)",
            (song_id, producer_id),
        )

    conn.commit()
    cur.close()
    conn.close()
    return song_id


def update_song(song_id, title, release_date, duration, album_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE songs
        SET title = %s,
            release_date = %s,
            duration = %s,
            alb_id = %s
        WHERE song_id = %s
        """,
        (title, release_date or None, duration or None, album_id or None, song_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_song(song_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM songs WHERE song_id = %s", (song_id,))
    conn.commit()
    cur.close()
    conn.close()


def review_song(song_id, user_id, rating, comment):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO reviews (song_id, user_id, rating, comment)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (song_id, user_id)
        DO UPDATE SET
            rating = EXCLUDED.rating,
            comment = EXCLUDED.comment
        """,
        (song_id, user_id, rating, comment),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_review(song_id, user_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT song_id, user_id, rating, comment
        FROM reviews
        WHERE song_id = %s AND user_id = %s
        """,
        (song_id, user_id),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "song_id": row[0],
        "user_id": row[1],
        "rating": row[2],
        "comment": row[3],
    }


def get_average_review(song_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT average_rating, review_count
        FROM song_review
        WHERE song_id = %s
        """,
        (song_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "average_rating": row[0],
        "review_count": row[1],
    }


def list_artists():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT art_id, name FROM artists ORDER BY name")
    artists = cur.fetchall()
    cur.close()
    conn.close()
    return artists


def list_albums():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT alb_id, title FROM albums ORDER BY title")
    albums = cur.fetchall()
    cur.close()
    conn.close()
    return albums


def list_genres():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT genre_name FROM genres ORDER BY genre_name")
    genres = cur.fetchall()
    cur.close()
    conn.close()
    return genres


def list_producers():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT prod_id, name FROM producers ORDER BY name")
    producers = cur.fetchall()
    cur.close()
    conn.close()
    return producers

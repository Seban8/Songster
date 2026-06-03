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

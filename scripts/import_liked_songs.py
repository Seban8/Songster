import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "Liked_Songs.csv"


def clean(value):
    value = (value or "").strip()
    return value or None


def normalize_date(value):
    value = clean(value)
    if not value:
        return None
    if len(value) == 4:
        return f"{value}-01-01"
    if len(value) == 7:
        return f"{value}-01"
    return value


def duration_seconds(value):
    value = clean(value)
    if not value:
        return None
    return round(int(value) / 1000)


def split_semicolon(value):
    value = clean(value)
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def split_genres(value):
    value = clean(value)
    if not value:
        return ["Unknown"]
    separators_normalized = value.replace(";", ",")
    return [genre.strip().title() for genre in separators_normalized.split(",") if genre.strip()]


def get_or_create_artist(cur, name):
    cur.execute("SELECT art_id FROM artists WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO artists (name, bio)
        VALUES (%s, %s)
        RETURNING art_id
        """,
        (name, "Imported from Liked_Songs.csv."),
    )
    return cur.fetchone()[0]


def get_or_create_album(cur, title, release_date, artist_id):
    cur.execute(
        """
        SELECT alb_id FROM albums
        WHERE title = %s
        AND COALESCE(release_date::text, '') = COALESCE(%s, '')
        AND COALESCE(art_id, 0) = COALESCE(%s, 0)
        """,
        (title, release_date, artist_id),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO albums (title, release_date, art_id)
        VALUES (%s, %s, %s)
        RETURNING alb_id
        """,
        (title, release_date, artist_id),
    )
    return cur.fetchone()[0]


def get_or_create_producer(cur, label_name):
    if not label_name:
        return None

    cur.execute("SELECT prod_id FROM producers WHERE name = %s", (label_name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """
        INSERT INTO producers (name, bio)
        VALUES (%s, %s)
        RETURNING prod_id
        """,
        (label_name, "Record label imported from Liked_Songs.csv."),
    )
    return cur.fetchone()[0]


def get_or_create_genre(cur, genre_name):
    cur.execute(
        """
        INSERT INTO genres (genre_name)
        VALUES (%s)
        ON CONFLICT (genre_name) DO NOTHING
        """,
        (genre_name,),
    )
    return genre_name


def song_exists(cur, title, album_id, duration):
    cur.execute(
        """
        SELECT song_id FROM songs
        WHERE title = %s
        AND COALESCE(alb_id, 0) = COALESCE(%s, 0)
        AND COALESCE(duration, 0) = COALESCE(%s, 0)
        """,
        (title, album_id, duration),
    )
    row = cur.fetchone()
    return row[0] if row else None


def insert_song(cur, row, album_id):
    title = clean(row["Track Name"])
    release_date = normalize_date(row["Release Date"])
    duration = duration_seconds(row["Duration (ms)"])

    existing_song_id = song_exists(cur, title, album_id, duration)
    if existing_song_id:
        return existing_song_id

    cur.execute(
        """
        INSERT INTO songs (title, release_date, duration, alb_id)
        VALUES (%s, %s, %s, %s)
        RETURNING song_id
        """,
        (title, release_date, duration, album_id),
    )
    return cur.fetchone()[0]


def connect_song_artist(cur, song_id, artist_id):
    cur.execute(
        """
        INSERT INTO sings (song_id, art_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (song_id, artist_id),
    )


def connect_song_genre(cur, song_id, genre_name):
    cur.execute(
        """
        INSERT INTO song_genre (song_id, genre_name)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (song_id, genre_name),
    )


def connect_song_producer(cur, song_id, producer_id):
    if not producer_id:
        return
    cur.execute(
        """
        INSERT INTO song_producer (song_id, prod_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (song_id, producer_id),
    )


def import_liked_songs(cur, csv_path=DEFAULT_CSV_PATH):
    imported = 0

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            artist_names = split_semicolon(row["Artist Name(s)"])
            if not artist_names:
                artist_names = ["Unknown Artist"]

            primary_artist_id = get_or_create_artist(cur, artist_names[0])
            album_id = get_or_create_album(
                cur,
                clean(row["Album Name"]) or "Unknown Album",
                normalize_date(row["Release Date"]),
                primary_artist_id,
            )
            song_id = insert_song(cur, row, album_id)

            for artist_name in artist_names:
                artist_id = get_or_create_artist(cur, artist_name)
                connect_song_artist(cur, song_id, artist_id)

            for genre_name in split_genres(row["Genres"]):
                get_or_create_genre(cur, genre_name)
                connect_song_genre(cur, song_id, genre_name)

            producer_id = get_or_create_producer(cur, clean(row["Record Label"]))
            connect_song_producer(cur, song_id, producer_id)
            imported += 1

    return imported

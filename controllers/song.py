import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.song import (
    create_song,
    delete_song,
    get_average_review,
    get_review,
    get_song,
    list_albums,
    list_artists,
    list_genres,
    list_producers,
    list_songs,
    review_song,
    search_songs,
    update_song,
)


bp = Blueprint("song", __name__, url_prefix="/")
AVAILABLE_USERS = tuple(range(1, 6))


def current_user_id():
    user_id = session.get("current_user_id", 1)
    if user_id not in AVAILABLE_USERS:
        user_id = 1
        session["current_user_id"] = user_id
    return user_id


@bp.app_context_processor
def inject_user_menu():
    active_user_id = current_user_id()
    return {
        "available_users": AVAILABLE_USERS,
        "current_user_id": active_user_id,
        "current_user_name": f"User {active_user_id}",
    }


def song_form_choices():
    return {
        "albums": list_albums(),
        "artists": list_artists(),
        "genres": list_genres(),
        "producers": list_producers(),
    }


@bp.route("/users/select", methods=["POST"])
def select_user():
    try:
        user_id = int(request.form.get("user_id", 1))
    except ValueError:
        user_id = 1

    if user_id not in AVAILABLE_USERS:
        user_id = 1

    session["current_user_id"] = user_id
    return redirect(request.referrer or url_for("song.index"))


@bp.route("/")
def index():
    songs = list_songs()
    return render_template("index.html", songs=songs)


@bp.route("/search")
def search():
    pattern = request.args.get("pattern", "").strip()
    songs = []
    error = None

    if pattern:
        try:
            songs = search_songs(pattern)
        except re.error:
            error = "The search pattern is not a valid regular expression."

    return render_template("search.html", pattern=pattern, songs=songs, error=error)


@bp.route("/songs/<int:song_id>")
def detail(song_id):
    song = get_song(song_id)
    if song is None:
        return redirect(url_for("song.index"))

    review = get_review(song_id, current_user_id())
    ratings = get_average_review(song_id)
    return render_template("detail.html", song=song, review=review, ratings=ratings)


@bp.route("/songs/<int:song_id>/review", methods=["POST"])
def add_review(song_id):
    song = get_song(song_id)
    if song is None:
        return redirect(url_for("song.index"))

    try:
        rating = int(request.form.get("rating", ""))
    except ValueError:
        return redirect(url_for("song.detail", song_id=song_id))

    if rating < 1 or rating > 5:
        return redirect(url_for("song.detail", song_id=song_id))

    review_song(
        song_id,
        current_user_id(),
        rating,
        request.form.get("comment", "").strip(),
    )
    flash("Review saved.")
    return redirect(url_for("song.detail", song_id=song_id))


@bp.route("/songs/new", methods=["GET", "POST"])
def new_song():
    if request.method == "POST":
        song_id = create_song(
            request.form["title"],
            request.form.get("release_date"),
            request.form.get("duration"),
            request.form.get("album_id"),
            request.form.get("artist_id"),
            request.form.get("genre_name"),
            request.form.get("producer_id"),
        )
        return redirect(url_for("song.detail", song_id=song_id))

    return render_template("form.html", song=None, **song_form_choices())


@bp.route("/songs/<int:song_id>/edit", methods=["GET", "POST"])
def edit_song(song_id):
    song = get_song(song_id)
    if song is None:
        return redirect(url_for("song.index"))

    if request.method == "POST":
        update_song(
            song_id,
            request.form["title"],
            request.form.get("release_date"),
            request.form.get("duration"),
            request.form.get("album_id"),
        )
        return redirect(url_for("song.detail", song_id=song_id))

    return render_template("form.html", song=song, **song_form_choices())


@bp.route("/songs/<int:song_id>/delete", methods=["POST"])
def remove_song(song_id):
    delete_song(song_id)
    return redirect(url_for("song.index"))

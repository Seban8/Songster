from flask import Blueprint, redirect, render_template, url_for

from models.song import get_song, list_songs


bp = Blueprint("song", __name__, url_prefix="/")


@bp.route("/")
def index():
    songs = list_songs()
    return render_template("index.html", songs=songs)


@bp.route("/songs/<int:song_id>")
def detail(song_id):
    song = get_song(song_id)
    if song is None:
        return redirect(url_for("song.index"))
    return render_template("detail.html", song=song)

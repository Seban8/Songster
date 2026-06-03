import os

from flask import Flask

from controllers import song
from database import init_db


init_db()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "songster-dev-secret")
app.register_blueprint(song.bp)

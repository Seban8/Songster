# Songster

Songster is a small Flask application for browsing, searching, editing and reviewing songs. The app uses PostgreSQL for the database and imports the sample song data from `data/Liked_Songs.csv`.

## Requirements

- Python 3.14
- PostgreSQL
- `createdb` available from your PostgreSQL installation

## Setup

Create the database:

```bash
createdb songster
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and its dependencies:

```bash
pip install -e .
```

Set the PostgreSQL connection values:

```bash
export PGDATABASE=songster
export PGUSER=postgres
export PGPASSWORD=123
export HOST=127.0.0.1
```

If your PostgreSQL user or password is different, change `PGUSER` and `PGPASSWORD` to match your local setup.

## Run the app

Start the Flask development server with:

```bash
python -m flask --app app run --debug
```

Then open:

```text
http://127.0.0.1:5000
```

Use `python -m flask` instead of `flask run`. This makes sure Flask runs with the Python environment you activated. On machines with Conda installed, the plain `flask` command can point to Conda instead of this project's `.venv`, which can cause missing dependency errors such as `ModuleNotFoundError: No module named 'psycopg2'`.

## Database initialization

The database is initialized when the app starts. `app.py` calls `init_db()`, which runs:

- `sql/schema.sql`
- `sql/seed.sql`
- the CSV import from `scripts/import_liked_songs.py`
- `sql/review_seed.sql`

Because of this, restarting the app recreates the schema and reloads the seed data.

## Useful checks

Check that the virtual environment is active:

```bash
which python
python -c "import psycopg2; print(psycopg2.__version__)"
```

The Python path should point into `.venv`. If `which flask` points to Conda, still use:

```bash
python -m flask --app app run --debug
```

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
export PGPASSWORD=
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
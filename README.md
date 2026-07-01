# Buvette Manager

Buvette Manager is a Flask and SQLite application for managing a company buvette. It supports staff authentication, client accounts, breakfast orders, lunch menus, manual charges, cash payments, a chronological ledger, dashboard metrics, and operational settings.

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python run.py
```

The app listens on <http://localhost:5000>. Default first-run accounts are:

- `administrator / administrator`
- `cashier / cashier`

Change passwords from **Settings** after deployment.

## Run with Docker

```bash
docker compose up --build
```

Compose exposes port `5000`, stores SQLite data in the `buvette_instance` volume, and checks `/health`.

## Database

For local development, missing SQLite tables are created automatically during startup and default seed data is inserted. SQL migrations are stored in `migrations/`:

```bash
sqlite3 instance/buvette-manager.sqlite3 < migrations/0001_domain_foundation.sql
sqlite3 instance/buvette-manager.sqlite3 < migrations/0002_mvp.sql
```

## Tests

```bash
python -m unittest discover -s tests -v
```

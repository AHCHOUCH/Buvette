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

## Production hardening highlights

- Default seeded users: `administrator / administrator` and `cashier / cashier`.
- Users are stored in the database with hashed passwords and role-based access control.
- Administrators use a French LTR interface; cashiers use an Arabic RTL operational shell.
- Supplier charges are managed as buvette expenses and do not affect client balances.
- Audit logs are available to administrators at `/logs/`.
- Client employee numbers are generated automatically when omitted.
- Numeric keypads support safe decimal entry (`.` -> `0.`, duplicate decimals ignored, backspace, clear).

## MVP closure deployment steps

For a clean pilot database, start the app once or apply the SQL migrations in order. For an existing MVP SQLite database, back up `instance/buvette-manager.sqlite3` first, then apply `migrations/0005_mvp_closure.sql` after prior migrations. This makes legacy `lunch_orders.menu_id` nullable so weekly plate/variant orders can be saved safely.

Docker is expected to run on port `5000`, persist `instance` data through the `buvette_instance` volume, and use `/health` for health checks.

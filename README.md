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

## SQLite migration / local database repair

Apply the schema migrations after pulling changes, especially if an existing local SQLite database was created before weekly lunch plates were added:

```bash
python scripts/apply_migrations.py
```

This preserves local data and rebuilds `lunch_orders` so the legacy `menu_id` column is nullable. The app also performs a startup compatibility check for SQLite development databases and repairs the old `lunch_orders.menu_id NOT NULL` schema when detected.

Development-only reset option (deletes local SQLite data and Docker volumes):

```bash
docker compose down -v
docker compose up --build
```

Use the reset option only when preserving local data is not required.

## Organization identity and ledger export

Administrators configure the visible organization identity from **Paramètres**. The settings include organization name, optional short name, logo, UI colors, footer text, debt warning default, and currency. If no organization name is configured, the app falls back to **Buvette Manager**; currency defaults to **DH**.

Uploaded logos are validated as `png`, `jpg`, `jpeg`, `webp`, or `svg` files and are stored below `app/static/uploads/` for display in the header, login screen, and settings preview. The default credentials remain for local development (`administrator` / `administrator`, `cashier` / `cashier`) but are intentionally not displayed on the login page.

The admin ledger page provides CSV exports for the complete ledger or the currently filtered period. Filters include dates, client, and transaction/reference type. Exports use UTF-8 with BOM for spreadsheet compatibility, include clean numeric debit/credit/balance columns, include the configured organization and currency as metadata rows, and create an audit log entry. Cashiers cannot export the ledger unless permissions are expanded to include ledger access.

# Database Design

The database defines the reusable entities required by MVP workflows. Migrations are additive and preserve existing data.

## Implemented core entities

### User

Authenticated application user with username, display name, role, active status, and creation timestamp. Users can be linked to ledger entries as the recording user.

### Client

Client account with name, optional account code, debt limit, active status, notes, and timestamps. Client balances are calculated from ledger entries rather than manually stored.

### Ledger entry

Normalized financial record with client, debit/credit type, amount, running balance, optional reference type/id, description, timestamp, and optional recording user.

## Ledger rules

- Debit entries increase a client balance.
- Credit entries decrease a client balance.
- `running_balance` is stored on each prepared row for statement-style display and audit review.
- `reference_type` and `reference_id` allow breakfast, lunch, manual charge, payment, and adjustment workflows to link back to source records.

## Migration

`migrations/0001_domain_foundation.sql` creates `users`, `clients`, and `ledger_entries`, including indexes and basic check constraints. This change is required because all financial workflows need a stable client and ledger foundation. Impact is additive only; no existing data is modified or removed.

## Migration policy

Every schema change must include a migration and an update to this document describing the intent and impact. Before implementing a feature, the required database changes must be explained; if none are required, that must be stated explicitly.


## Runtime initialization

The application factory imports the centralized model metadata and calls `db.create_all()` during startup so a missing SQLite database file is created automatically for local and Docker development. This is a foundation convenience only; schema changes must still be expressed as migrations.

Existing SQL migrations can be applied manually against SQLite with commands such as `sqlite3 instance/buvette-manager.sqlite3 < migrations/0001_domain_foundation.sql`, or managed through Flask-Migrate once migration scripts are generated with `flask db migrate` and applied with `flask db upgrade`.

## MVP entities

The MVP adds breakfast products and orders, lunch menus and orders, manual charges, payments, and key/value settings. Orders, charges, and payments create ledger entries with reference type/id values so the ledger can trace every balance-affecting transaction back to its source.

## Seed data

Startup seeds a default staff client, common breakfast products, weekday lunch menus, and basic settings when the database is empty. SQLite data persists in Docker through the `buvette_instance` volume.

## Production hardening entities

### Database users

Users are now persisted in the `users` table with `username`, `password_hash`, `full_name`, `role`, `is_active`, timestamps, and `last_login_at`. Passwords are stored only as Werkzeug hashes. Startup seeds `administrator / administrator` and `cashier / cashier` when no users exist.

### Suppliers and supplier charges

The `suppliers` table stores buvette vendors and merchants. `manual_charges` now records supplier expenses through `supplier_id`; these rows are operating expenses and do not create client ledger entries or affect client balances.

### Audit logs

The `audit_logs` table records timestamp, user snapshot, action, entity, description, request metadata, severity, and optional JSON metadata for authentication, authorization, financial writes, dangerous actions, and management workflows.

### Migration

`migrations/0003_production_hardening.sql` documents additive schema changes for database users, suppliers, supplier-linked charges, and audit logs. Runtime initialization also performs small additive SQLite compatibility upgrades for existing local MVP databases.

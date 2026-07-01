# Database Design

The database foundation now defines the core reusable entities required by future workflows. The migration is non-destructive and creates new tables only.

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
- `running_balance` is stored on each prepared row for statement-style display and future audit review.
- `reference_type` and `reference_id` allow future breakfast, lunch, manual charge, payment, and adjustment workflows to link back to source records.

## Migration

`migrations/0001_domain_foundation.sql` creates `users`, `clients`, and `ledger_entries`, including indexes and basic check constraints. This change is required because all future financial workflows need a stable client and ledger foundation. Impact is additive only; no existing data is modified or removed.

## Migration policy

Every schema change must include a migration and an update to this document describing the intent and impact. Before implementing a feature, the required database changes must be explained; if none are required, that must be stated explicitly.


## Runtime initialization

The application factory imports the centralized model metadata and calls `db.create_all()` during startup so a missing SQLite database file is created automatically for local and Docker development. This is a foundation convenience only; future schema changes must still be expressed as migrations.

Existing SQL migrations can be applied manually against SQLite with commands such as `sqlite3 instance/buvette-manager.sqlite3 < migrations/0001_domain_foundation.sql`, or managed through Flask-Migrate once migration scripts are generated with `flask db migrate` and applied with `flask db upgrade`.

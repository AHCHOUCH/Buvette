-- Initial domain foundation for clients, users, and ledger entries.
-- Non-destructive: creates new tables only.

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    display_name VARCHAR(120) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'cashier',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL
);

CREATE INDEX ix_users_username ON users (username);

CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    account_code VARCHAR(50) UNIQUE,
    debt_limit NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE INDEX ix_clients_name ON clients (name);
CREATE INDEX ix_clients_account_code ON clients (account_code);
CREATE INDEX ix_clients_is_active ON clients (is_active);

CREATE TABLE ledger_entries (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    entry_type VARCHAR(10) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    running_balance NUMERIC(12, 2) NOT NULL,
    reference_type VARCHAR(50),
    reference_id INTEGER,
    description VARCHAR(255),
    timestamp DATETIME NOT NULL,
    created_by_user_id INTEGER,
    CONSTRAINT ck_ledger_entries_entry_type CHECK (entry_type in ('debit', 'credit')),
    CONSTRAINT ck_ledger_entries_amount_non_negative CHECK (amount >= 0),
    FOREIGN KEY(client_id) REFERENCES clients (id),
    FOREIGN KEY(created_by_user_id) REFERENCES users (id)
);

CREATE INDEX ix_ledger_entries_client_id ON ledger_entries (client_id);
CREATE INDEX ix_ledger_entries_entry_type ON ledger_entries (entry_type);
CREATE INDEX ix_ledger_entries_reference_type ON ledger_entries (reference_type);
CREATE INDEX ix_ledger_entries_reference_id ON ledger_entries (reference_id);
CREATE INDEX ix_ledger_entries_timestamp ON ledger_entries (timestamp);

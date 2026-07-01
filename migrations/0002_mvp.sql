-- MVP tables for breakfast, lunch, manual charges, payments, settings, and ledger indexes.
-- Additive migration only; existing clients/users/ledger_entries data is preserved.
CREATE TABLE IF NOT EXISTS breakfast_products (id INTEGER PRIMARY KEY, name VARCHAR(120) NOT NULL UNIQUE, price NUMERIC(12,2) NOT NULL CHECK (price >= 0), is_active BOOLEAN NOT NULL DEFAULT 1, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS breakfast_orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0), notes VARCHAR(255), created_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS breakfast_order_items (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES breakfast_orders(id) ON DELETE CASCADE, product_id INTEGER NOT NULL REFERENCES breakfast_products(id), product_name VARCHAR(120) NOT NULL, unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0), quantity INTEGER NOT NULL CHECK (quantity > 0), line_total NUMERIC(12,2) NOT NULL CHECK (line_total >= 0));
CREATE TABLE IF NOT EXISTS lunch_menus (id INTEGER PRIMARY KEY, weekday INTEGER NOT NULL UNIQUE CHECK (weekday BETWEEN 0 AND 6), name VARCHAR(160) NOT NULL, price NUMERIC(12,2) NOT NULL CHECK (price >= 0), is_active BOOLEAN NOT NULL DEFAULT 1, updated_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS lunch_orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), menu_id INTEGER NOT NULL REFERENCES lunch_menus(id), service_date DATE NOT NULL, menu_name VARCHAR(160) NOT NULL, amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0), created_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS manual_charges (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0), category VARCHAR(80) NOT NULL, notes VARCHAR(255), created_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0), note VARCHAR(255), created_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS settings (key VARCHAR(80) PRIMARY KEY, value VARCHAR(255) NOT NULL, updated_at DATETIME NOT NULL);
CREATE INDEX IF NOT EXISTS ix_breakfast_orders_created_at ON breakfast_orders(created_at);
CREATE INDEX IF NOT EXISTS ix_lunch_orders_service_date ON lunch_orders(service_date);
CREATE INDEX IF NOT EXISTS ix_manual_charges_created_at ON manual_charges(created_at);
CREATE INDEX IF NOT EXISTS ix_payments_created_at ON payments(created_at);
CREATE INDEX IF NOT EXISTS ix_ledger_client_timestamp ON ledger_entries(client_id, timestamp);

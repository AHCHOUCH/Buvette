ALTER TABLE users ADD COLUMN password_hash VARCHAR(255) DEFAULT '';
ALTER TABLE users ADD COLUMN full_name VARCHAR(120) DEFAULT '';
ALTER TABLE users ADD COLUMN updated_at DATETIME;
ALTER TABLE users ADD COLUMN last_login_at DATETIME;
CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY, name VARCHAR(160) NOT NULL UNIQUE, phone VARCHAR(80), notes TEXT, active BOOLEAN NOT NULL DEFAULT 1, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, timestamp DATETIME NOT NULL, user_id INTEGER, username_snapshot VARCHAR(80), action VARCHAR(120) NOT NULL, entity_type VARCHAR(80), entity_id INTEGER, description TEXT NOT NULL DEFAULT '', ip_address VARCHAR(80), user_agent VARCHAR(255), severity VARCHAR(20) NOT NULL DEFAULT 'INFO', metadata_json TEXT);
CREATE INDEX IF NOT EXISTS ix_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS ix_audit_logs_action ON audit_logs(action);
ALTER TABLE manual_charges ADD COLUMN supplier_id INTEGER;

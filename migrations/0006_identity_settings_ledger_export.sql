-- Identity settings and ledger export configuration keys.
-- The settings table is key/value, so this migration is additive data only.
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('organization_short_name', '', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('logo_path', '', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('primary_color', '#2f6f73', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('secondary_color', '#eef2f4', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('accent_color', '#0d6efd', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('header_background_color', '#2f6f73', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('sidebar_background_color', '#eaf3f3', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('button_color', '#2f6f73', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('login_background_color', '#f6f7f9', CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO settings (key, value, updated_at) VALUES ('footer_text', '', CURRENT_TIMESTAMP);
UPDATE settings SET value='Buvette Manager' WHERE key='organization_name' AND TRIM(value)='';
UPDATE settings SET value='DH' WHERE key='currency' AND TRIM(value)='';

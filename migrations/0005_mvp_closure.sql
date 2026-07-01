-- MVP closure migration: weekly lunch orders use food_plate_id + variant_id snapshots.
-- SQLite cannot alter NOT NULL directly; rebuild lunch_orders so legacy menu_id is nullable.
PRAGMA foreign_keys=off;
CREATE TABLE IF NOT EXISTS lunch_orders_new (
  id INTEGER PRIMARY KEY,
  client_id INTEGER NOT NULL,
  menu_id INTEGER NULL,
  food_plate_id INTEGER NULL,
  variant_id INTEGER NULL,
  service_date DATE NOT NULL,
  menu_name VARCHAR(160) NOT NULL DEFAULT '',
  plate_name_snapshot VARCHAR(160) NOT NULL DEFAULT '',
  variant_label_snapshot VARCHAR(80) NOT NULL DEFAULT '',
  created_by_user_id INTEGER NULL,
  amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
  created_at DATETIME NOT NULL
);
INSERT INTO lunch_orders_new SELECT id, client_id, menu_id, food_plate_id, variant_id, service_date, menu_name, plate_name_snapshot, variant_label_snapshot, created_by_user_id, amount, created_at FROM lunch_orders;
DROP TABLE lunch_orders;
ALTER TABLE lunch_orders_new RENAME TO lunch_orders;
CREATE INDEX IF NOT EXISTS ix_lunch_orders_client_id ON lunch_orders(client_id);
CREATE INDEX IF NOT EXISTS ix_lunch_orders_service_date ON lunch_orders(service_date);
CREATE INDEX IF NOT EXISTS ix_lunch_orders_food_plate_id ON lunch_orders(food_plate_id);
CREATE INDEX IF NOT EXISTS ix_lunch_orders_variant_id ON lunch_orders(variant_id);
PRAGMA foreign_keys=on;

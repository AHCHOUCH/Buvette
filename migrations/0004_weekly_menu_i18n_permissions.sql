-- Production refinement: weekly menus, food plate variants, lunch snapshots, audit metadata indexes, supplier expense cleanup.
PRAGMA foreign_keys=off;

CREATE TABLE IF NOT EXISTS weekly_menus (
    id INTEGER PRIMARY KEY,
    week_start_date DATE NOT NULL UNIQUE,
    label VARCHAR(160) NOT NULL DEFAULT '',
    active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_weekly_menus_week_start_date ON weekly_menus(week_start_date);
CREATE INDEX IF NOT EXISTS ix_weekly_menus_active ON weekly_menus(active);

CREATE TABLE IF NOT EXISTS daily_menus (
    id INTEGER PRIMARY KEY,
    weekly_menu_id INTEGER NOT NULL REFERENCES weekly_menus(id),
    service_date DATE NOT NULL,
    weekday INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1,
    CONSTRAINT uq_daily_menu_week_date UNIQUE (weekly_menu_id, service_date)
);
CREATE INDEX IF NOT EXISTS ix_daily_menus_service_date ON daily_menus(service_date);
CREATE INDEX IF NOT EXISTS ix_daily_menus_weekly_menu_id ON daily_menus(weekly_menu_id);

CREATE TABLE IF NOT EXISTS food_plates (
    id INTEGER PRIMARY KEY,
    daily_menu_id INTEGER NOT NULL REFERENCES daily_menus(id),
    name VARCHAR(160) NOT NULL,
    description TEXT,
    active BOOLEAN NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS ix_food_plates_daily_menu_id ON food_plates(daily_menu_id);
CREATE INDEX IF NOT EXISTS ix_food_plates_active ON food_plates(active);

CREATE TABLE IF NOT EXISTS food_plate_variants (
    id INTEGER PRIMARY KEY,
    food_plate_id INTEGER NOT NULL REFERENCES food_plates(id),
    size_key VARCHAR(30) NOT NULL,
    label VARCHAR(80) NOT NULL,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    active BOOLEAN NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS ix_food_plate_variants_food_plate_id ON food_plate_variants(food_plate_id);
CREATE INDEX IF NOT EXISTS ix_food_plate_variants_active ON food_plate_variants(active);

ALTER TABLE lunch_orders ADD COLUMN food_plate_id INTEGER REFERENCES food_plates(id);
ALTER TABLE lunch_orders ADD COLUMN variant_id INTEGER REFERENCES food_plate_variants(id);
ALTER TABLE lunch_orders ADD COLUMN plate_name_snapshot VARCHAR(160) NOT NULL DEFAULT '';
ALTER TABLE lunch_orders ADD COLUMN variant_label_snapshot VARCHAR(80) NOT NULL DEFAULT '';
ALTER TABLE lunch_orders ADD COLUMN created_by_user_id INTEGER REFERENCES users(id);

CREATE INDEX IF NOT EXISTS ix_lunch_orders_food_plate_id ON lunch_orders(food_plate_id);
CREATE INDEX IF NOT EXISTS ix_lunch_orders_variant_id ON lunch_orders(variant_id);
CREATE INDEX IF NOT EXISTS ix_manual_charges_supplier_id ON manual_charges(supplier_id);

UPDATE settings SET value='DH' WHERE key='currency' AND value='€';
PRAGMA foreign_keys=on;

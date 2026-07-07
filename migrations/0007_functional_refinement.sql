-- Functional refinement: products, lunch extras, expenses ownership.
ALTER TABLE breakfast_products ADD COLUMN product_type VARCHAR(30) NOT NULL DEFAULT 'breakfast';
ALTER TABLE breakfast_products ADD COLUMN archived_at DATETIME;
ALTER TABLE manual_charges ADD COLUMN created_by_user_id INTEGER;
CREATE TABLE IF NOT EXISTS lunch_order_items (
  id INTEGER PRIMARY KEY,
  lunch_order_id INTEGER NOT NULL REFERENCES lunch_orders(id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES breakfast_products(id),
  product_name_snapshot VARCHAR(120) NOT NULL,
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_snapshot NUMERIC(12,2) NOT NULL,
  total NUMERIC(12,2) NOT NULL CHECK (total >= 0)
);
CREATE INDEX IF NOT EXISTS ix_lunch_order_items_lunch_order_id ON lunch_order_items(lunch_order_id);
CREATE INDEX IF NOT EXISTS ix_lunch_order_items_product_id ON lunch_order_items(product_id);

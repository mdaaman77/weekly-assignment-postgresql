-- ==========================================
-- PART 1: 5 QUERIES USING DIFFERENT JOIN TYPES
-- ==========================================

-- 1. INNER JOIN: Fetch orders alongside customer names and table numbers
SELECT o.order_id, c.name AS customer_name, t.table_number, o.status 
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN tables t ON o.table_id = t.table_id;

-- 2. LEFT JOIN: Fetch all customers and any orders they have placed (including those who haven't ordered)
SELECT c.customer_id, c.name, o.order_id, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- 3. RIGHT JOIN: Fetch all items from the menu and details if they've been ordered
SELECT m.name AS item_name, oi.order_id, oi.quantity
FROM order_items oi
RIGHT JOIN menu_items m ON oi.menu_item_id = m.menu_item_id;

-- 4. FULL OUTER JOIN: Matches customers and orders showing unlinked ones if any exist
SELECT c.name, o.order_id 
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;

-- 5. MULTIPLE JOIN (3+ Tables): Breakdown of specific items ordered by which customer
SELECT o.order_id, c.name AS customer_name, m.name AS food_item, oi.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN menu_items m ON oi.menu_item_id = m.menu_item_id;


-- ==========================================
-- PART 2: 2 COMPOSITE INDEXES
-- ==========================================

-- Index 1: Optimizing orders filtered by customer and date range
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Index 2: Optimizing menu item searches by category and price
CREATE INDEX idx_menu_cat_price ON menu_items(category, price);


-- ==========================================
-- PART 3: QUERY OPTIMIZATION (SEQ SCAN -> INDEX SCAN)
-- ==========================================

-- BEFORE INDEX: (Run this BEFORE running the CREATE INDEX block above)
EXPLAIN ANALYZE 
SELECT * FROM orders WHERE customer_id = 12 AND order_date > '2026-01-01';
-- Expected Result: "Seq Scan on orders..." (High execution time)

-- AFTER INDEX: (Run this AFTER running the CREATE INDEX block above)
EXPLAIN ANALYZE 
SELECT * FROM orders WHERE customer_id = 12 AND order_date > '2026-01-01';
-- Expected Result: "Index Scan/Bitmap Index Scan using idx_orders_customer_date..." (Much lower cost & time)
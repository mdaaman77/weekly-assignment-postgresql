# 🍽️ Restaurant PostgreSQL Backend Assignment

---

## 📦 Database Architecture & Schema Design

The relational database is designed to ensure **data integrity and consistency** using:

* `PRIMARY KEY`
* `FOREIGN KEY`
* `NOT NULL`
* `UNIQUE`
* `ON DELETE CASCADE`

### 🧩 Entities & Relationships

* **Customers** → Stores guest information
* **Tables** → Represents physical dining tables
* **Menu Items** → Stores food/drink categories and pricing
* **Orders** → Links customers with tables (transaction layer)
* **Order Items** → Bridge table connecting orders with menu items

### 🔗 Relationship Diagram

```
[ Customers ] 1 -------- * [ Orders ] * -------- 1 [ Tables ]
                              |
                              | 1
                              *
                       [ Order Items ] * -------- 1 [ Menu Items ]
```

---

## 🚀 Installation & Local Setup

### 1. Navigate to Project Directory

```bash
cd restaurant-postgres
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create `.env` file:

```
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

---

### 5. Create Database

```sql
CREATE DATABASE restaurant_db;
```

---

### 6. Run Schema & Seed Data

```bash
python seed.py
```

This will:

* Reset database
* Create tables
* Insert realistic test data

---

### 7. Start Backend Server

```bash
uvicorn main:app --reload
```

API available at:

```
http://127.0.0.1:8000
```

---

## 📊 SQL Query Portfolio & Optimization

### 1. JOIN Queries Implemented

* **INNER JOIN** → Active orders with customers
* **LEFT JOIN** → All customers including inactive
* **RIGHT JOIN** → All orders with customer mapping
* **FULL OUTER JOIN** → Complete dataset coverage
* **MULTI JOIN (4 Tables)** → Full order breakdown

---

### 2. Composite Indexes

```sql
-- Orders optimization
CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);

-- Menu optimization
CREATE INDEX idx_menu_cat_price
ON menu_items (category, price);
```

---

### 3. Performance Analysis (EXPLAIN ANALYZE)

#### Before Optimization (Sequential Scan)

```
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 12 AND order_date > '2026-01-01';

-> Seq Scan on orders
Execution Time: ~1.4 ms
```

---

#### After Optimization (Index Scan)

```
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 12 AND order_date > '2026-01-01';

-> Index Scan using idx_orders_customer_date
Execution Time: ~0.04 ms
```

---

### ⚡ Optimization Impact

* Reduced latency by ~96%
* Improved complexity:

  * From **O(N)** → **O(log N)**

---

## 🌐 API Documentation

Interactive Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📡 Available Endpoints

| Method | Endpoint                   | Description                  |
| ------ | -------------------------- | ---------------------------- |
| GET    | `/`                        | Health check                 |
| GET    | `/customers`               | Fetch all customers          |
| GET    | `/menu`                    | Get all menu items           |
| GET    | `/orders`                  | Get all orders               |
| GET    | `/orders/{order_id}/items` | Get items for specific order |

---

## ✅ Assignment Coverage

* PostgreSQL connected to backend API
* Multiple relational tables implemented
* 5 JOIN queries (all types)
* 2 composite indexes
* EXPLAIN ANALYZE comparison
* Query optimization demonstrated

---

## 🧠 Notes

* No ORM used — pure SQL (`psycopg2`)
* Optimized for performance and clarity
* Designed for real-world relational workloads

---

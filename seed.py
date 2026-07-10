import random
from connection import get_db_connection
from faker import Faker

fake = Faker()

def seed_database():
    conn = get_db_connection()
    if not conn:
        return
    
    cur = conn.cursor()
    
    # 1. Create Tables
    schema_queries = """
    DROP TABLE IF EXISTS order_items CASCADE;
    DROP TABLE IF EXISTS orders CASCADE;
    DROP TABLE IF EXISTS menu_items CASCADE;
    DROP TABLE IF EXISTS tables CASCADE;
    DROP TABLE IF EXISTS customers CASCADE;

    CREATE TABLE customers (
        customer_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE,
        phone VARCHAR(20)
    );

    CREATE TABLE tables (
        table_id SERIAL PRIMARY KEY,
        table_number INT UNIQUE NOT NULL,
        capacity INT NOT NULL
    );

    CREATE TABLE menu_items (
        menu_item_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price NUMERIC(6, 2) NOT NULL
    );

    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT REFERENCES customers(customer_id) ON DELETE SET NULL,
        table_id INT REFERENCES tables(table_id) ON DELETE SET NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'Pending'
    );

    CREATE TABLE order_items (
        order_item_id SERIAL PRIMARY KEY,
        order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
        menu_item_id INT REFERENCES menu_items(menu_item_id) ON DELETE CASCADE,
        quantity INT NOT NULL,
        subtotal NUMERIC(8, 2) NOT NULL
    );
    """
    print("Creating tables...")
    cur.execute(schema_queries)
    
    # 2. Seed Data
    print("Seeding Tables, Customers, and Menu...")
    # Tables
    for i in range(1, 11):
        cur.execute("INSERT INTO tables (table_number, capacity) VALUES (%s, %s);", (i, random.choice([2, 4, 6, 8])))
        
    # Customers
    for _ in range(50):
        cur.execute("INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s);", 
                    (fake.name(), fake.unique.email(), fake.phone_number()[:20]))
        
    # Menu Items
    categories = ['Appetizer', 'Main Course', 'Dessert', 'Beverage']
    menu_samples = [
        ('Burger', 'Main Course', 12.99), ('Pizza', 'Main Course', 14.50), 
        ('Fries', 'Appetizer', 4.99), ('Wings', 'Appetizer', 8.99),
        ('Ice Cream', 'Dessert', 5.50), ('Cake', 'Dessert', 6.50),
        ('Soda', 'Beverage', 2.50), ('Coffee', 'Beverage', 3.00)
    ]
    for name, cat, price in menu_samples:
        cur.execute("INSERT INTO menu_items (name, category, price) VALUES (%s, %s, %s);", (name, cat, price))
        
    # Generate large bulk data for Orders and Order Items to make indexes effective
    print("Seeding bulk Orders and Order Items (this might take a moment)...")
    for _ in range(1000):  # 1000 orders
        cur.execute(
            "INSERT INTO orders (customer_id, table_id, order_date, status) VALUES (%s, %s, %s, %s) RETURNING order_id;",
            (random.randint(1, 50), random.randint(1, 10), fake.date_time_this_year(), random.choice(['Completed', 'Pending']))
        )
        order_id = cur.fetchone()[0]
        
        # 1 to 3 items per order
        for _ in range(random.randint(1, 3)):
            item_id = random.randint(1, 8)
            qty = random.randint(1, 4)
            # Fetch price to calc subtotal
            cur.execute("SELECT price FROM menu_items WHERE menu_item_id = %s;", (item_id,))
            price = cur.fetchone()[0]
            subtotal = price * qty
            cur.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, subtotal) VALUES (%s, %s, %s, %s);",
                        (order_id, item_id, qty, subtotal))
            
    conn.commit()
    cur.close()
    conn.close()
    print("Database seeding successfully completed!")

if __name__ == "__main__":
    seed_database()
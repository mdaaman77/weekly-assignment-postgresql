from fastapi import FastAPI, HTTPException
from connection import get_db_connection
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Restaurant Management API")

@app.get("/")
def home():
    return {"status": "Restaurant API is working smoothly"}

# Endpoint 1: Fetch all customers
@app.get("/customers")
def get_customers():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # RealDictCursor formats rows as python dicts instead of tuples
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM customers;")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    return customers

# Endpoint 2: Fetch all menu items
@app.get("/menu")
def get_menu():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM menu_items;")
    menu = cur.fetchall()
    cur.close()
    conn.close()
    return menu

# Endpoint 3: Fetch all orders using an INNER JOIN with Customer names
@app.get("/orders")
def get_orders():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT o.order_id, c.name as customer_name, o.table_id, o.order_date, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id;
    """
    cur.execute(query)
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return orders

# Endpoint 4: Get detailed order items breakdown for a single order
@app.get("/orders/{order_id}/items")
def get_order_items(order_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT oi.order_item_id, m.name as item_name, oi.quantity, oi.subtotal
        FROM order_items oi
        JOIN menu_items m ON oi.menu_item_id = m.menu_item_id
        WHERE oi.order_id = %s;
    """
    cur.execute(query, (order_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    
    if not items:
        raise HTTPException(status_code=404, detail="Order items not found or order empty")
    return items
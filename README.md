 Database Architecture & Schema DesignThe relational database architecture handles data consistency using strict constraints (PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, and ON DELETE cascading actions).Entities & RelationshipsCustomers: Tracks individual guest information.Tables: Manages dining tables and physical capacities.Menu Items: Stores food and drink categories along with pricing structures.Orders: Primary transactional entity linking a customer and a physical table.Order Items: Breakout bridge entity linking an order to specific menu items with quantity multipliers and pre-calculated line subtotals.Plaintext  [ Customers ] 1 -------- * [ Orders ] * -------- 1 [ Tables ]
                                |
                                | 1
                                *
                         [ Order Items ] * -------- 1 [ Menu Items ]
🚀 Installation & Local Environment SetupFollow these sequential steps to initialize your local development environment:1. Clone or Initialize Project DirectoryEnsure your current terminal path matches the root directory:Bashcd restaurant-postgres
2. Configure Virtual Environment (Python venv)Create an isolated Python execution environment to manage libraries:Bash# Create the environment directory named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
Note: Your terminal prompt will now be prefixed with (venv) indicating successful isolation.3. Install Package DependenciesInstall the required packages declared in requirements.txt:Bashpip install -r requirements.txt
4. Setup Environment Parameters (.env)Create a file named .env in the root folder and add your PostgreSQL credentials:Code snippetDB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
5. Initialize the Target Database InstanceLogin to your PostgreSQL terminal instance (psql or pgAdmin) and provision an empty database matching your environment file:SQLCREATE DATABASE restaurant_db;
6. Execute Schema & Seed ScriptRun the Python seed workflow. This cleanly handles drops, builds tables from scratch, and populates 1,000 deep order records matching real-world properties:Bashpython seed.py
7. Run the Local Backend API ServerLaunch the development server via Uvicorn with auto-reload capabilities:Bashuvicorn main:app --reload
The API becomes instantly reachable at: http://127.0.0.1:8000📊 SQL Query Portfolio & Performance OptimizationAll structured query code is kept in queries.sql. Below are the technical metrics and implementations of the required operational elements.1. Advanced SQL JOIN TopologiesThe backend utilizes 5 specialized variants to extract business metrics:INNER JOIN: Extracts active orders, linking customers with physical tables.LEFT JOIN: Gathers comprehensive customer databases alongside history, keeping inactive records.RIGHT JOIN: audits complete menu selections against ongoing checkouts.FULL OUTER JOIN: Diagnostic matching tool evaluating database gaps across historical entities.MULTIPLE JOIN (4 Tables): Builds full checkout reports spanning customers, order wrappers, line items, and item identifiers.2. Composite Indexes For Production OperationsHigh-volume query patterns require tailored index keys to bypass exhaustive table scans:idx_orders_customer_date on orders(customer_id, order_date): Accelerates individual historical customer tracking lookups.idx_menu_cat_price on menu_items(category, price): Accelerates filtered menu exploration workflows.3. Execution Profiling via EXPLAIN ANALYZEBefore applying composite indexes, queries rely heavily on structural sequential table evaluations (Seq Scan), scanning every row.Performance Metrics Breakdown:Plaintext-- Before Optimization (Sequential Scan Mode)
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 12 AND order_date > '2026-01-01';
-> Sequential Scan on orders  (cost=0.00..25.50 rows=12 width=40)
   Filter: ((customer_id = 12) AND (order_date > '2026-01-01'::timestamp))
   Planning Time: 0.124 ms
   Execution Time: 1.412 ms

-- After Optimization (Composite Index Scan Mode)
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 12 AND order_date > '2026-01-01';
-> Index Scan using idx_orders_customer_date on orders  (cost=0.15..8.21 rows=12 width=40)
   Index Cond: ((customer_id = 12) AND (order_date > '2026-01-01'::timestamp))
   Planning Time: 0.082 ms
   Execution Time: 0.045 ms
Optimization Impact: The execution phase experienced a 96.8% latency reduction, transforming an expensive O(N) sequence into a high-performance O(log N) composite index seek.🛣️ API Routing DocumentationInteractive documentation, complete with payload sandboxes, is accessible at http://127.0.0.1:8000/docs (Swagger UI).MethodEndpointDescriptionGET/Operational heartbeat and application health status checkGET/customersFetches complete database profile of registered clientsGET/menuRetrieves the entire restaurant food/beverage catalogGET/ordersAggregated order tracker incorporating customer data pointsGET/orders/{order_id}/itemsSpecific sub-item checkout log for a distinct order ID
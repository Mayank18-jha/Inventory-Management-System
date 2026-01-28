import sqlite3
import os
from datetime import datetime

DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "inventory.db")
os.makedirs(DB_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    category TEXT,
    quantity INTEGER DEFAULT 0,
    price REAL
)
""")
conn.commit()

def add_product():
    name = input("Product Name: ")
    category = input("Category: ")
    price = float(input("Price: ₹"))
    quantity = int(input("Initial Quantity: "))

    try:
        cursor.execute("""
        INSERT INTO products (name, category, price, quantity)
        VALUES (?, ?, ?, ?)
        """, (name, category, price, quantity))
        conn.commit()
        print("✅ Product added")
    except sqlite3.IntegrityError:
        print("❌ Product already exists")

def update_stock():
    name = input("Product Name: ")
    change = int(input("Quantity Change (+IN / -OUT): "))

    cursor.execute("SELECT quantity FROM products WHERE name=?", (name,))
    row = cursor.fetchone()

    if not row:
        print("❌ Product not found")
        return

    new_qty = row[0] + change
    if new_qty < 0:
        print("❌ Not enough stock")
        return

    cursor.execute(
        "UPDATE products SET quantity=? WHERE name=?",
        (new_qty, name)
    )
    conn.commit()
    print(f"📦 Stock updated. Current Quantity: {new_qty}")

def view_inventory():
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    print("\n📋 Inventory List")
    print("-" * 50)
    print("ID | Name | Category | Qty | Price")

    for row in rows:
        print(row)

def low_stock_alert():
    threshold = 5
    cursor.execute(
        "SELECT name, quantity FROM products WHERE quantity <= ?",
        (threshold,)
    )
    rows = cursor.fetchall()

    print("\n⚠️ Low Stock Alerts")
    for name, qty in rows:
        print(f"{name} → Only {qty} left")

def menu():
    while True:
        print("""
====== Inventory Management ======
1. Add Product
2. Update Stock
3. View Inventory
4. Low Stock Alerts
5. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_stock()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            low_stock_alert()
        elif choice == "5":
            print("👋 Exiting inventory system")
            break
        else:
            print("❌ Invalid choice")

menu()
conn.close()

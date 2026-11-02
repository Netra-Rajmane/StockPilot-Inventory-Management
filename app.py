import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "inventory.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                price REAL NOT NULL DEFAULT 0,
                supplier TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            sample = [
                ("Wireless Mouse", "ELC-1001", "Electronics", 42, 599.00, "TechSource"),
                ("Mechanical Keyboard", "ELC-1002", "Electronics", 8, 2499.00, "KeyWorld"),
                ("Notebook Set", "OFF-2001", "Stationery", 120, 149.00, "PaperTrail"),
                ("Desk Lamp", "HOM-3001", "Home & Living", 5, 899.00, "BrightHouse"),
                ("USB-C Hub", "ELC-1003", "Electronics", 0, 1299.00, "TechSource"),
            ]
            conn.executemany(
                "INSERT INTO products (name, sku, category, quantity, price, supplier) VALUES (?, ?, ?, ?, ?, ?)",
                sample
            )

@app.route("/")
def dashboard():
    with get_db() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
        total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        total_units = conn.execute("SELECT COALESCE(SUM(quantity), 0) FROM products").fetchone()[0]
        low_stock = conn.execute("SELECT COUNT(*) FROM products WHERE quantity BETWEEN 1 AND 10").fetchone()[0]
        out_of_stock = conn.execute("SELECT COUNT(*) FROM products WHERE quantity = 0").fetchone()[0]
        inventory_value = conn.execute("SELECT COALESCE(SUM(quantity * price), 0) FROM products").fetchone()[0]
    return render_template("index.html", products=products, total_products=total_products,
                           total_units=total_units, low_stock=low_stock,
                           out_of_stock=out_of_stock, inventory_value=inventory_value)

@app.route("/products/add", methods=["POST"])
def add_product():
    data = [request.form.get(k, "").strip() for k in ("name", "sku", "category", "quantity", "price", "supplier")]
    name, sku, category, quantity, price, supplier = data
    try:
        quantity = int(quantity)
        price = float(price)
        if not name or not sku or not category or quantity < 0 or price < 0:
            raise ValueError
        with get_db() as conn:
            conn.execute(
                "INSERT INTO products (name, sku, category, quantity, price, supplier) VALUES (?, ?, ?, ?, ?, ?)",
                (name, sku, category, quantity, price, supplier)
            )
        flash("Product added successfully.", "success")
    except sqlite3.IntegrityError:
        flash("That SKU already exists. Please use a unique SKU.", "error")
    except (ValueError, TypeError):
        flash("Please enter valid product details.", "error")
    return redirect(url_for("dashboard"))

@app.route("/products/<int:product_id>/update", methods=["POST"])
def update_product(product_id):
    try:
        quantity = int(request.form.get("quantity", ""))
        price = float(request.form.get("price", ""))
        if quantity < 0 or price < 0:
            raise ValueError
        with get_db() as conn:
            conn.execute("UPDATE products SET quantity=?, price=? WHERE id=?", (quantity, price, product_id))
        flash("Product updated successfully.", "success")
    except (ValueError, TypeError):
        flash("Quantity and price must be valid non-negative numbers.", "error")
    return redirect(url_for("dashboard"))

@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    with get_db() as conn:
        conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    flash("Product deleted.", "success")
    return redirect(url_for("dashboard"))

@app.route("/health")
def health():
    return jsonify(status="ok", service="inventory-management")

@app.route("/api/products")
def api_products():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return jsonify([dict(row) for row in rows])

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

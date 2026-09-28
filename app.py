from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "capstone-demo-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "expenses.db"
LOG_PATH = BASE_DIR / "app.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_db()
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
    ).fetchall()
    total = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses").fetchone()["total"]
    category_rows = conn.execute(
        "SELECT category, ROUND(SUM(amount), 2) AS total FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    conn.close()
    return render_template(
        "index.html",
        expenses=expenses,
        total=round(total, 2),
        categories=category_rows
    )

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    amount_text = request.form.get("amount", "").strip()
    expense_date = request.form.get("expense_date", "").strip()

    try:
        amount = float(amount_text)
        if not title or not category or amount <= 0 or not expense_date:
            raise ValueError
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        flash("Please enter valid expense details.", "error")
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (title, category, amount, expense_date) VALUES (?, ?, ?, ?)",
        (title, category, amount, expense_date)
    )
    conn.commit()
    conn.close()
    logging.info("Added expense: %s | %s | %.2f | %s", title, category, amount, expense_date)
    flash("Expense added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db()
    row = conn.execute("SELECT title FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    if row is None:
        conn.close()
        flash("Expense not found.", "error")
        return redirect(url_for("index"))
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    logging.info("Deleted expense ID %s (%s)", expense_id, row["title"])
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found(_error):
    return "Page not found", 404

@app.errorhandler(500)
def server_error(_error):
    logging.exception("Unhandled server error")
    return "Internal server error", 500

if __name__ == "__main__":
    app.run(debug=True)

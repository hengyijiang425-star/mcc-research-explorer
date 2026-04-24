from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "capstone.db"
PI_EXCEL = "RePORTER_PI_IDS_FY2025.xlsx"


# -------------------------------
# DB 查询（缓存 publication）
# -------------------------------
def query_db(query, args=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# -------------------------------
# 首页
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# 🔍 通用搜索（搜索整个Excel）
# -------------------------------
@app.route("/search")
def search():
    q = request.args.get("q", "").strip().lower()

    if not q:
        return jsonify([])

    results = query_db("""
        SELECT *
        FROM pubmed_publication
        WHERE lower(title) LIKE ?
           OR lower(abstract) LIKE ?
           OR lower(authors) LIKE ?
           OR lower(pi_name) LIKE ?
        ORDER BY id DESC
    """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))

    return jsonify(results)


# -------------------------------
# 🔎 按名字查 + ORCID + publication
# -------------------------------
@app.route("/search_name")
def search_name():
    name = request.args.get("name", "").strip().lower()

    if not name:
        return jsonify({"error": "No researcher name entered"})

    rows = query_db("""
        SELECT *
        FROM pubmed_publication
        WHERE lower(pi_name) LIKE ?
        ORDER BY id DESC
    """, (f"%{name}%",))

    if not rows:
        return jsonify({"error": "No researcher found"})

    result = {
        "name": rows[0].get("pi_name"),
        "orcid": rows[0].get("orcid"),
        "publications": rows
    }

    return jsonify(result)

    # 如果没有缓存（你以后可以接API）
    result["publications"] = []

    return jsonify(result)


# -------------------------------
# 启动
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    

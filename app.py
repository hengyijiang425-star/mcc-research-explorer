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

    # 直接从 publication 表里搜 title / abstract / authors
    results = query_db("""
        SELECT *
        FROM publication
        WHERE lower(title) LIKE ?
           OR lower(abstract) LIKE ?
           OR lower(authors) LIKE ?
        ORDER BY pmid DESC
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))

    return jsonify(results)


# -------------------------------
# 🔎 按名字查 + ORCID + publication
# -------------------------------
@app.route("/search_name")
def search_name():
    name = request.args.get("name", "")

    df = pd.read_excel(PI_EXCEL, sheet_name="Sheet2")

    # 🔥 模糊匹配名字
    match = df[df["PI_NAMEs"].str.contains(name, case=False, na=False)]

    if match.empty:
        return jsonify({"error": "No researcher found"})

    row = match.iloc[0]

    result = {
        "name": row.get("PI_NAMEs"),
        "orcid": row.get("ORCID"),
    }

    # 🔥 如果没有 ORCID
    if pd.isna(result["orcid"]):
        result["publications"] = []
        return jsonify(result)

    # 🔥 从数据库查 publication（如果你有）
    cached = query_db(
        "SELECT * FROM publication WHERE orcid = ?", (result["orcid"],)
    )

    if cached:
        result["publications"] = cached
        return jsonify(result)

    # 如果没有缓存（你以后可以接API）
    result["publications"] = []

    return jsonify(result)


# -------------------------------
# 启动
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    

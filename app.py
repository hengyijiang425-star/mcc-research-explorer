from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from capstone4 import lookup_publications, init_publication_table

app = Flask(__name__)

DB_PATH = "capstone.db"
PI_EXCEL = "RePORTER_PI_IDS_FY2025.xlsx"

def query_db(query, args=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "").lower()

    results = []
    for p in data:
        text = (
            (p.get("title", "") + " " +
             p.get("abstract", "") + " " +
             p.get("authors", ""))
        ).lower()

        if q in text:
            results.append(p)

    return jsonify(results)

@app.route("/search_name")
def search_name():
    name = request.args.get("name", "")

    df = pd.read_excel(PI_EXCEL, sheet_name="Sheet2")

    match = df[df["PI_NAMEs"].str.contains(name, case=False, na=False)]

    if match.empty:
        return jsonify({"error": "No researcher found"})

    orcid = match.iloc[0]["ORCID"]

    if pd.isna(orcid):
        return jsonify({"error": "No ORCID available"})

    cached = query_db("""
        SELECT * FROM publication WHERE orcid = ?
    """, (orcid,))

    if cached:
        return jsonify(cached)

    result = lookup_publications(orcid)

    return jsonify(result["publications"])

if __name__ == "__main__":
    init_publication_table()
    app.run(debug=True)

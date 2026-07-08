from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student(
    name TEXT,
    age INTEGER
)
""")
conn.commit()

@app.route("/input")
def input():
    return render_template("inputpage.html")

@app.route("/save", methods=["POST"])
def save():

    name = request.form.get("name")
    age = request.form.get("age")

    cursor.execute(
        "INSERT INTO student(name, age) VALUES(?, ?)",
        (name, age)
    )

    conn.commit()

    return "Data Saved Successfully"

if __name__ == "__main__":
    app.run(debug=True)
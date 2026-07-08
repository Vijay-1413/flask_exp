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
def inputpage():
    return render_template("inputpage.html")

@app.route("/save", methods=["POST"])
def save():

    name = request.form["name"]
    age = request.form["age"]

    cursor.execute(
        "INSERT INTO student(name, age) VALUES(?, ?)",
        (name, age)
    )

    conn.commit()

    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()

    return render_template("show.html", students=students)

@app.route("/show")
def show():

    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()

    return render_template("show.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
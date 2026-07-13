from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "library123"

DATABASE = "library.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        book_name TEXT NOT NULL,
        hsn_code TEXT UNIQUE NOT NULL,
        book_id TEXT NOT NULL,
        genre TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]

    if count == 0:

        books = [

            ("Kalki","Ponniyin Selvan","HSN1001","BK101","Historical","Active"),

            ("Sujatha","En Iniya Iyanthira","HSN1002","BK102","Science Fiction","Active"),

            ("Jayakanthan","Sila Nerangalil Sila Manithargal","HSN1003","BK103","Novel","Inactive"),

            ("Balakumaran","Udayar","HSN1004","BK104","Historical","Active"),

            ("Sandilyan","Kadal Pura","HSN1005","BK105","Adventure","Inactive")

        ]

        cursor.executemany("""
        INSERT INTO books(author,book_name,hsn_code,book_id,genre,status)
        VALUES(?,?,?,?,?,?)
        """, books)

    conn.commit()
    conn.close()


create_database()

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "Vijay" and password == "Vijay1304":
        session["user"] = username
        return redirect(url_for("dashboard"))

    return "Invalid Username or Password"


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    total_books = cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    total_authors = cursor.execute(
        "SELECT COUNT(DISTINCT author) FROM books"
    ).fetchone()[0]

    total_genres = cursor.execute(
        "SELECT COUNT(DISTINCT genre) FROM books"
    ).fetchone()[0]

    active_books = cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Active'"
    ).fetchone()[0]

    inactive_books = cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Inactive'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_books=total_books,
        total_authors=total_authors,
        total_genres=total_genres,
        active_books=active_books,
        inactive_books=inactive_books
    )

@app.route("/inventory")
def inventory():

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    books = conn.execute(
        "SELECT * FROM books ORDER BY id"
    ).fetchall()

    conn.close()

    return render_template(
        "inventory.html",
        books=books
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        author = request.form["author"]
        book_name = request.form["book_name"]
        hsn_code = request.form["hsn_code"]
        book_id = request.form["book_id"]
        genre = request.form["genre"]
        status = request.form["status"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM books WHERE hsn_code=?",
            (hsn_code,)
        )

        exist = cursor.fetchone()

        if exist:
            conn.close()
            return "HSN Code already exists."

        cursor.execute("""
        INSERT INTO books
        (author,book_name,hsn_code,book_id,genre,status)
        VALUES(?,?,?,?,?,?)
        """,
        (author,book_name,hsn_code,book_id,genre,status))

        conn.commit()
        conn.close()

        return redirect(url_for("inventory"))

    return render_template("add_book.html")


@app.route("/delete/<int:id>")
def delete(id):

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    conn.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("inventory"))


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))
@app.route("/api/test")
def test():
    return ("Working")
if __name__ == "__main__":
    app.run(debug=True)
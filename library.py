from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        author_age INTEGER,
        author_address TEXT,
        author_id TEXT UNIQUE
    )
    """)
    cursor.execute("SELECT COUNT(*) FROM authors")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO authors(author,author_age,author_address,author_id)
        VALUES(?,?,?,?)
        """,[
            ("Kalki",55,"Erode","121"),
            ("Sujatha",72,"Srirangam","122"),
            ("Jayakanthan",81,"Cuddalore","123"),
            ("Balakumaran",68,"Thanjavur","124"),
            ("Sandilyan",76,"Chennai","125")
        ])

    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO books(author,book_name,hsn_code,book_id,genre,status)
        VALUES(?,?,?,?,?,?)
        """,[
            ("Kalki","Ponniyin Selvan","10001","BK101","Historical","Active"),
            ("Sujatha","En Iniya Iyanthira","10002","BK102","Sci-Fi","Active"),
            ("Jayakanthan","Novel","10003","BK103","Novel","Inactive")
        ])

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login",methods=["POST"])
def login():

    username=request.form["username"]
    password=request.form["password"]

    if username=="Vijay" and password=="Vijay1304":
        session["user"]=username
        return redirect(url_for("dashboard"))

    return "Invalid Login"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("home"))

    conn=get_connection()
    cursor=conn.cursor()

    total_books=cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    total_authors=cursor.execute(
        "SELECT COUNT(*) FROM authors"
    ).fetchone()[0]

    total_genres=cursor.execute(
        "SELECT COUNT(DISTINCT genre) FROM books"
    ).fetchone()[0]

    active_books=cursor.execute(
        "SELECT COUNT(*) FROM books WHERE status='Active'"
    ).fetchone()[0]

    inactive_books=cursor.execute(
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

    conn=get_connection()

    books=conn.execute(""" SELECT * FROM books ORDER BY id """).fetchall()

    conn.close()

    return render_template(
        "inventory.html",
        books=books
    )

@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    if request.method == "POST":

        author_name = request.form["author_name"]
        book_name = request.form["book_name"]
        hsn_code = request.form["hsn_code"]
        book_id = request.form["book_id"]
        genre = request.form["genre"]
        status = request.form["status"]

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM books WHERE hsn_code=?",
            (hsn_code,)
        )

        if cursor.fetchone():
            conn.close()
            return "HSN Code Already Exists"

        cursor.execute("""
        INSERT INTO books
        (author, book_name, hsn_code, book_id, genre, status)
        VALUES(?,?,?,?,?,?)
        """, (
            author_name,
            book_name,
            hsn_code,
            book_id,
            genre,
            status
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("inventory"))

    authors = conn.execute(""" SELECT author, author_id FROM authors ORDER BY author """).fetchall()

    conn.close()

    return render_template(
        "add_book.html",
        authors=authors
    )

@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        author_name = request.form["author_name"]
        book_name = request.form["book_name"]
        hsn_code = request.form["hsn_code"]
        book_id = request.form["book_id"]
        genre = request.form["genre"]
        status = request.form["status"]

        cursor.execute("""
        UPDATE books
        SET author=?,
            book_name=?,
            hsn_code=?,
            book_id=?,
            genre=?,
            status=?
        WHERE id=?
        """, (
            author_name,
            book_name,
            hsn_code,
            book_id,
            genre,
            status,
            id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("inventory"))

    cursor.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    )

    book = cursor.fetchone()

    authors = conn.execute(""" SELECT author, author_id FROM authors ORDER BY author """).fetchall()

    conn.close()

    return render_template(
        "edit_book.html",
        book=book,
        authors=authors
    )

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

@app.route("/authors")
def authors():

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()

    authors_list = conn.execute(""" SELECT * FROM authors ORDER BY id """).fetchall()

    conn.close()

    return render_template(
        "authors.html",
        authors=authors_list
    )

@app.route("/add_author", methods=["GET", "POST"])
def add_author():

    if "user" not in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        author = request.form["author_name"]
        age = request.form["age"]
        address = request.form["address"]
        author_id = request.form["author_id"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO authors
        (author, author_age, author_address, author_id)
        VALUES(?,?,?,?)
        """, (
            author,
            age,
            address,
            author_id
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("authors"))

    return render_template("add_author.html")

@app.route("/edit_author/<int:id>", methods=["GET", "POST"])
def edit_author(id):

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM authors WHERE id=?",
        (id,)
    )

    old_author = cursor.fetchone()

    if request.method == "POST":

        new_author = request.form["author"]
        age = request.form["age"]
        address = request.form["address"]
        author_id = request.form["author_id"]

        cursor.execute("""
        UPDATE authors
        SET author=?,
            author_age=?,
            author_address=?,
            author_id=?
        WHERE id=?
        """, (
            new_author,
            age,
            address,
            author_id,
            id
        ))

        cursor.execute("""
        UPDATE books
        SET author=?
        WHERE author=?
        """, (
            new_author,
            old_author["author"]
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("authors"))

    conn.close()

    return render_template(
        "edit_author.html",
        author=old_author
    )

@app.route("/delete_author/<int:id>")
def delete_author(id):

    if "user" not in session:
        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM authors WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("authors"))

@app.route("/api/create", methods=["POST"])
def api_create():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO books
    (author, book_name, hsn_code, book_id, genre, status)
    VALUES(?,?,?,?,?,?)
    """, (
        data["author"],
        data["book_name"],
        data["hsn_code"],
        data["book_id"],
        data["genre"],
        data["status"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "Success",
        "message": "Book Created Successfully"
    })
    
@app.route("/api/create/author", methods=["POST"])
def api_create_author():

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO authors
        (author, author_age, author_address, author_id)
        VALUES(?,?,?,?)
        """,  (
        data["author"],
        data["author_age"],
        data["author_address"],
        data["author_id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "Success",
        "message": "Book Created Successfully"
    })

@app.route("/api/select", methods=["GET"])
def api_select():

    hsn_code = request.args.get("hsn_code")

    conn = get_connection()
    book = conn.execute("""SELECT * FROM books WHERE hsn_code=?""", 
    (hsn_code,)).fetchone()
    conn.close()
    if book:
        return jsonify({

            "status": "Success",
            "book":{
                "author":book["author"],
                "book_name":book["book_name"],
                "hsn_code":book["hsn_code"],
                "book_id":book["book_id"],
                "genre":book["genre"],
                "status":book["status"]
            }
        })
    return jsonify({
        "status":"Failed",
        "message":"Book Not Found"
    })

@app.route("/api/select/author", methods=["GET"])
def api_select_author():

    author_id = request.args.get("author_id")

    conn = get_connection()
    author = conn.execute(
        "SELECT * FROM authors WHERE author_id=?",
        (author_id,)
    ).fetchone()
    conn.close()

    if author:
        return jsonify({
            "status": "Success",
            "author": {
                "author": author["author"],
                "author_age": author["author_age"],
                "author_address": author["author_address"],
                "author_id": author["author_id"]
            }
        })

    return jsonify({
        "status": "Failed",
        "message": "Author Not Found"
    })

@app.route("/api/update", methods=["POST"])
def api_update():

    data=request.get_json()
    conn=get_connection()

    conn.execute("""
    UPDATE books
    SET author=?,
        book_name=?,
        hsn_code=?,
        book_id=?,
        genre=?,
        status=?
    WHERE hsn_code=?
    """,(
        data["author"],
        data["book_name"],
        data["hsn_code"],
        data["book_id"],
        data["genre"],
        data["status"],
        data["hsn_code"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"Success",
        "message":"Book Updated Successfully"
    })

@app.route("/api/update/author", methods=["POST"])
def api_update_author():

    data=request.get_json()
    conn=get_connection()

    conn.execute("""
    UPDATE authors
    SET author=?,
        author_age=?,
        author_address=?,
        author_id=?
    WHERE author_id=?
    """,(
        data["author"],
        data["author_age"],
        data["author_address"],
        data["author_id"],
        data["author_id"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"Success",
        "message":"Book Updated Successfully"
    })

@app.route("/api/delete", methods=["POST"])
def api_delete():

    data=request.get_json()
    conn=get_connection()

    conn.execute("""DELETE FROM books WHERE hsn_code=?""",
    (data["hsn_code"],))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"Success",
        "message":"Book Deleted Successfully"
    })

@app.route("/api/delete/author", methods=["POST"])
def api_delete_author():

    data=request.get_json()
    conn=get_connection()

    conn.execute("""DELETE FROM authors WHERE author_id=?""",
    (data["author_id"],))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"Success",
        "message":"Book Deleted Successfully"
    })

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
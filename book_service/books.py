from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    connection = get_db_connection()
    with open("books.sql", "r") as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()


# GET /api/books - List all books
@app.route("/api/books", methods=["GET"])
def get_books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])


# GET /api/books/<id> - Get single book
@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(dict(book))


# POST /api/books - Create new book
@app.route("/api/books", methods=["POST"])
def add_book():
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["title", "author", "year"]
    if not all(field in request.json for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (request.json["title"], request.json["author"], request.json["year"]),
    )
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({"id": book_id, "message": "Book added successfully"}), 201


# PUT /api/books/<id> - Update a book
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    conn = get_db_connection()
    # Check if book exists
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if book is None:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    # Update fields that are provided
    update_fields = []
    update_values = []
    if "title" in request.json:
        update_fields.append("title = ?")
        update_values.append(request.json["title"])
    if "author" in request.json:
        update_fields.append("author = ?")
        update_values.append(request.json["author"])
    if "year" in request.json:
        update_fields.append("year = ?")
        update_values.append(request.json["year"])

    update_values.append(book_id)

    conn.execute(
        f'UPDATE books SET {", ".join(update_fields)} WHERE id = ?',
        tuple(update_values),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book updated successfully"})


# DELETE /api/books/<id> - Delete a book
@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    conn = get_db_connection()
    # Check if book exists
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if book is None:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)

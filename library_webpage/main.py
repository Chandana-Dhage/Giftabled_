from contextlib import asynccontextmanager
from pathlib import Path
import csv
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "library.db"
CSV_PATH = BASE_DIR / "Library.csv"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                library_name TEXT NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'Available'
                    CHECK(status IN ('Available', 'Issued'))
            )
        """)
        count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]

        # Import the original repository CSV once, when the database is empty.
        if count == 0 and CSV_PATH.exists():
            with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    library = (row.get("Library_Name") or row.get("Library Name") or "").strip()
                    title = (row.get("Book_Title") or row.get("Book Title") or "").strip()
                    author = (row.get("Author_Name") or row.get("Author") or "").strip()
                    isbn = (row.get("ISBN") or "").strip()
                    status = (row.get("Status") or "Available").strip().title()
                    if library and title and author and isbn:
                        if status not in ("Available", "Issued"):
                            status = "Available"
                        connection.execute(
                            """INSERT OR IGNORE INTO books
                               (library_name, title, author, isbn, status)
                               VALUES (?, ?, ?, ?, ?)""",
                            (library, title, author, isbn, status),
                        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Giftabled Library Management System",
    description="Manage libraries, books, searching, issuing and returning books.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class BookCreate(BaseModel):
    library_name: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    isbn: str = Field(min_length=3, max_length=30)
    status: str = "Available"


class BookUpdate(BookCreate):
    pass


def clean_book(book):
    data = book.model_dump()
    for key in ("library_name", "title", "author", "isbn"):
        data[key] = data[key].strip()
    data["status"] = data["status"].strip().title()
    if data["status"] not in ("Available", "Issued"):
        raise HTTPException(status_code=422, detail="Status must be Available or Issued.")
    if not all(data[key] for key in ("library_name", "title", "author", "isbn")):
        raise HTTPException(status_code=422, detail="All book fields are required.")
    return data


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/books")
def get_books(
    search: Optional[str] = Query(default=None),
    library: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
):
    sql = "SELECT * FROM books WHERE 1=1"
    values = []
    if search:
        term = f"%{search.strip()}%"
        sql += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ? OR library_name LIKE ?)"
        values.extend([term, term, term, term])
    if library:
        sql += " AND library_name = ?"
        values.append(library)
    if status and status != "All":
        sql += " AND status = ?"
        values.append(status)
    sql += " ORDER BY id DESC"
    with get_connection() as connection:
        rows = connection.execute(sql, values).fetchall()
    return [dict(row) for row in rows]


@app.get("/api/books/{book_id}")
def get_book(book_id: int):
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Book not found.")
    return dict(row)


@app.post("/api/books", status_code=201)
def add_book(book: BookCreate):
    data = clean_book(book)
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """INSERT INTO books (library_name, title, author, isbn, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (data["library_name"], data["title"], data["author"], data["isbn"], data["status"]),
            )
            book_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists.")
    return get_book(book_id)


@app.put("/api/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    data = clean_book(book)
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """UPDATE books
                   SET library_name = ?, title = ?, author = ?, isbn = ?, status = ?
                   WHERE id = ?""",
                (data["library_name"], data["title"], data["author"], data["isbn"], data["status"], book_id),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Book not found.")
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Another book already uses this ISBN.")
    return get_book(book_id)


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found.")
    return {"message": "Book deleted successfully."}


@app.patch("/api/books/{book_id}/issue")
def issue_book(book_id: int):
    with get_connection() as connection:
        row = connection.execute("SELECT status FROM books WHERE id = ?", (book_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Book not found.")
        if row["status"] == "Issued":
            raise HTTPException(status_code=400, detail="This book is already issued.")
        connection.execute("UPDATE books SET status = 'Issued' WHERE id = ?", (book_id,))
    return get_book(book_id)


@app.patch("/api/books/{book_id}/return")
def return_book(book_id: int):
    with get_connection() as connection:
        row = connection.execute("SELECT status FROM books WHERE id = ?", (book_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Book not found.")
        if row["status"] == "Available":
            raise HTTPException(status_code=400, detail="This book is already available.")
        connection.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
    return get_book(book_id)


@app.get("/api/libraries")
def get_libraries():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT library_name FROM books ORDER BY library_name"
        ).fetchall()
    return [row["library_name"] for row in rows]


@app.get("/api/stats")
def get_stats():
    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        available = connection.execute(
            "SELECT COUNT(*) FROM books WHERE status = 'Available'"
        ).fetchone()[0]
        issued = total - available
        libraries = connection.execute(
            "SELECT COUNT(DISTINCT library_name) FROM books"
        ).fetchone()[0]
    return {
        "total_books": total,
        "available_books": available,
        "issued_books": issued,
        "total_libraries": libraries,
    }

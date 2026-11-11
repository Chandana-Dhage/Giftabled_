# Giftabled – Library Management System

A web-based library management system built from the original Giftabled book-library assignment using **FastAPI, HTML, CSS, JavaScript, and SQLite**.

## Features

- Add, view, edit, and delete books (CRUD)
- Search by book title, author, ISBN, or library name
- Filter by library and availability status
- Issue and return books
- Dashboard statistics: total books, available books, issued books, and libraries
- SQLite database for persistent storage
- Imports existing records from the repository's `Library.csv` file the first time the database is initialized
- Responsive interface for desktop and mobile

## Project structure

```text
Giftabled/
├── main.py
├── Library.csv
├── library.db              # Created automatically when the app runs
├── requirements.txt
├── README.md
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Run locally

### 1. Open the project folder

```bash
cd Giftabled
```

### 2. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 5. Open the application

Visit:

- Web application: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/books` | List and search books |
| GET | `/api/books/{id}` | Get one book |
| POST | `/api/books` | Add a book |
| PUT | `/api/books/{id}` | Update a book |
| DELETE | `/api/books/{id}` | Delete a book |
| PATCH | `/api/books/{id}/issue` | Issue a book |
| PATCH | `/api/books/{id}/return` | Return a book |
| GET | `/api/libraries` | List library names |
| GET | `/api/stats` | Dashboard statistics |

## Notes about the original CSV

The application recognizes the original repository columns (`Library_Name`, `Book_Title`, `Author_Name`, `ISBN`, `Status`) and imports valid rows into SQLite when the database is first created. After import, the SQLite database is the active data store. Keep `Library.csv` as the original source/import file.

If you want to import a changed CSV again, stop the server, remove `library.db`, and restart the application. This recreates the database and imports the CSV again. Removing `library.db` also removes changes made through the web application, so back it up first.

## GitHub

After testing, copy these files into your repository's `library` branch (or your chosen project branch), then commit and push them.

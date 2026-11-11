const API = "/api";

const tableBody = document.getElementById("booksTable");
const searchInput = document.getElementById("searchInput");
const libraryFilter = document.getElementById("libraryFilter");
const statusFilter = document.getElementById("statusFilter");
const modal = document.getElementById("bookModal");
const bookForm = document.getElementById("bookForm");
const toast = document.getElementById("toast");

let books = [];
let toastTimer;

async function request(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options
    });

    if (!response.ok) {
        let message = "Something went wrong.";
        try {
            const data = await response.json();
            message = data.detail || message;
        } catch (_) {}
        throw new Error(message);
    }

    if (response.status === 204) return null;
    return response.json();
}

function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.className = "toast";
    }, 3000);
}

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);
}

async function loadBooks() {
    const params = new URLSearchParams();
    const search = searchInput.value.trim();
    const library = libraryFilter.value;
    const status = statusFilter.value;

    if (search) params.set("search", search);
    if (library) params.set("library", library);
    if (status && status !== "All") params.set("status", status);

    try {
        books = await request(`${API}/books?${params.toString()}`);
        renderBooks();
    } catch (error) {
        showToast(error.message, "error");
    }
}

function renderBooks() {
    if (!books.length) {
        tableBody.innerHTML = `<tr><td colspan="5" class="empty-state">No books found. Add a book to get started.</td></tr>`;
        document.getElementById("resultCount").textContent = "Showing 0 books";
        return;
    }

    tableBody.innerHTML = books.map(book => {
        const statusClass = book.status === "Available" ? "available" : "issued";
        const statusAction = book.status === "Available"
            ? `<button class="small-button issue-button" data-action="issue" data-id="${book.id}">Issue</button>`
            : `<button class="small-button return-button" data-action="return" data-id="${book.id}">Return</button>`;

        return `
            <tr>
                <td>
                    <div class="book-title">${escapeHTML(book.title)}</div>
                    <div class="book-author">by ${escapeHTML(book.author)}</div>
                </td>
                <td><span class="library-name">${escapeHTML(book.library_name)}</span></td>
                <td><span class="isbn-text">${escapeHTML(book.isbn)}</span></td>
                <td><span class="status-pill ${statusClass}">${escapeHTML(book.status)}</span></td>
                <td>
                    <div class="row-actions">
                        ${statusAction}
                        <button class="small-button edit-button" data-action="edit" data-id="${book.id}">Edit</button>
                        <button class="small-button delete-button" data-action="delete" data-id="${book.id}">Delete</button>
                    </div>
                </td>
            </tr>`;
    }).join("");

    document.getElementById("resultCount").textContent =
        `Showing ${books.length} ${books.length === 1 ? "book" : "books"}`;
}

async function loadStats() {
    try {
        const stats = await request(`${API}/stats`);
        document.getElementById("totalBooks").textContent = stats.total_books;
        document.getElementById("availableBooks").textContent = stats.available_books;
        document.getElementById("issuedBooks").textContent = stats.issued_books;
        document.getElementById("totalLibraries").textContent = stats.total_libraries;
    } catch (error) {
        showToast("Could not load library statistics.", "error");
    }
}

async function loadLibraries(selected = "") {
    try {
        const libraries = await request(`${API}/libraries`);
        libraryFilter.innerHTML = `<option value="">All Libraries</option>` +
            libraries.map(name =>
                `<option value="${escapeHTML(name)}">${escapeHTML(name)}</option>`
            ).join("");
        libraryFilter.value = selected;
    } catch (error) {
        showToast("Could not load libraries.", "error");
    }
}

async function refreshPage(selectedLibrary = libraryFilter.value) {
    await loadLibraries(selectedLibrary);
    await loadBooks();
    await loadStats();
}

function openModal(book = null) {
    bookForm.reset();
    document.getElementById("bookId").value = book ? book.id : "";
    document.getElementById("modalTitle").textContent = book ? "Edit Book" : "Add a Book";
    document.getElementById("saveButton").textContent = book ? "Update Book" : "Save Book";

    if (book) {
        document.getElementById("libraryName").value = book.library_name;
        document.getElementById("bookTitle").value = book.title;
        document.getElementById("authorName").value = book.author;
        document.getElementById("isbn").value = book.isbn;
        document.getElementById("bookStatus").value = book.status;
    }

    modal.classList.add("show");
    modal.setAttribute("aria-hidden", "false");
}

function closeModal() {
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
}

document.getElementById("addBookButton").addEventListener("click", () => openModal());
document.getElementById("closeModalButton").addEventListener("click", closeModal);
document.getElementById("cancelButton").addEventListener("click", closeModal);

modal.addEventListener("click", event => {
    if (event.target === modal) closeModal();
});

bookForm.addEventListener("submit", async event => {
    event.preventDefault();

    const id = document.getElementById("bookId").value;
    const payload = {
        library_name: document.getElementById("libraryName").value.trim(),
        title: document.getElementById("bookTitle").value.trim(),
        author: document.getElementById("authorName").value.trim(),
        isbn: document.getElementById("isbn").value.trim(),
        status: document.getElementById("bookStatus").value
    };

    try {
        await request(id ? `${API}/books/${id}` : `${API}/books`, {
            method: id ? "PUT" : "POST",
            body: JSON.stringify(payload)
        });
        closeModal();
        showToast(id ? "Book updated successfully." : "Book added successfully.");
        await refreshPage();
    } catch (error) {
        showToast(error.message, "error");
    }
});

tableBody.addEventListener("click", async event => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;

    const id = Number(button.dataset.id);
    const action = button.dataset.action;
    const book = books.find(item => item.id === id);

    try {
        if (action === "edit") {
            openModal(book);
            return;
        }

        if (action === "delete") {
            if (!confirm(`Delete "${book.title}" from the library?`)) return;
            await request(`${API}/books/${id}`, { method: "DELETE" });
            showToast("Book deleted successfully.");
        } else if (action === "issue") {
            await request(`${API}/books/${id}/issue`, { method: "PATCH" });
            showToast("Book issued successfully.");
        } else if (action === "return") {
            await request(`${API}/books/${id}/return`, { method: "PATCH" });
            showToast("Book returned successfully.");
        }

        await refreshPage();
    } catch (error) {
        showToast(error.message, "error");
    }
});

let searchDelay;
searchInput.addEventListener("input", () => {
    clearTimeout(searchDelay);
    searchDelay = setTimeout(loadBooks, 250);
});

libraryFilter.addEventListener("change", loadBooks);
statusFilter.addEventListener("change", loadBooks);

refreshPage();

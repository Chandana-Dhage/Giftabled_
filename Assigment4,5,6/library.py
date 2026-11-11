class Book:
    def __init__(self, title, author, copies=1):
        if copies < 0:
            raise ValueError("Copies cannot be negative")
        self.title = title
        self.author = author
        self.__copies = copies

    def get_copies(self):
        return self.__copies

    def add_copies(self, count=1):
        if count <= 0:
            raise ValueError("Count must be positive")
        self.__copies += count

    def borrow(self):
        if self.__copies == 0:
            return False
        self.__copies -= 1
        return True

    def return_copy(self):
        self.__copies += 1

    def __str__(self):
        return f"{self.title} by {self.author} ({self.__copies} copies)"


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        key = book.title.casefold()
        if key in self.books:
            self.books[key].add_copies(book.get_copies())
        else:
            self.books[key] = book

    def show_books(self):
        if not self.books:
            print("No books in library")
        for book in self.books.values():
            print(book)

    def borrow_book(self, title):
        book = self.books.get(title.casefold())
        if book is None:
            print("Book not found")
            return False
        if not book.borrow():
            print("No copies available")
            return False
        print("Borrowed:", book.title)
        return True

    def return_book(self, title):
        book = self.books.get(title.casefold())
        if book is None:
            print("Book not found")
            return False
        book.return_copy()
        print("Returned:", book.title)
        return True


if __name__ == "__main__":
    library = Library()
    library.add_book(Book("Verity", "Collen Hoover", 2))
    library.add_book(Book("Never Lie", "Freida McFadden", 1))
    library.show_books()
    library.borrow_book("Verity")
    library.return_book("Verity ")
    library.show_books()
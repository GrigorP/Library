from datetime import datetime, timedelta

# Define a Book class to represent books in the library
class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.borrowed_count = 0

    def display_info(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}"
    
    def increment_borrowed_count(self):
        self.borrowed_count += 1

# Define a Library class to manage books and borrowing history
class Library:
    def __init__(self):
        self.books = []
        self.borrowing_history = {}

    def add_book(self, book):
        self.books.append(book)

    def search_book_by_title(self, title):
        return [book for book in self.books if book.title == title]
    
    def search_book_by_author(self, author):
        return [book for book in self.books if book.author == author]
    
    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                return f"Book with ISBN {isbn} removed"
        return "Book not found"
    
    def most_popular_books(self, top_n=5):
        sorted_books = sorted(self.books, key=lambda x: x.borrowed_count, reverse=True)
        return sorted_books[:top_n]

    def borrowed_books_by_member(self, member):
        return self.borrowing_history.get(member.membership_id, [])

# Define a Member class to represent library members
class Member:
    def __init__(self, name, membership_id):
        self.name = name
        self.membership_id = membership_id
        self.borrowed_books = []

    def borrow_book(self, library, isbn, days=14):
        for book in library.books:
            if book.isbn == isbn and book.quantity > 0:
                self.borrowed_books.append({
                    'book': book,
                    'due_date': datetime.now() + timedelta(days=days)
                })
                book.quantity -= 1
                book.increment_borrowed_count()

                # Update borrowing history
                if self.membership_id not in library.borrowing_history:
                    library.borrowing_history[self.membership_id] = []
                library.borrowing_history[self.membership_id].append(book)
                return f"Borrowed book: {book.title}. Due date: {datetime.now() + timedelta(days=days)}"
        return 'Book unavailable'
    
    def return_book(self, library, isbn):
        for record in self.borrowed_books:
            book = record["book"]
            if book.isbn == isbn:
                library.books.append(book)
                book.quantity += 1
                if (datetime.now() > record["due_date"]):
                    overdue_days = (datetime.now() - record["due_days"]).days
                    fine = overdue_days * 1  # $1 fine per day
                    self.borrowed_books.remove(record)
                    return f"Returned book: {book.title}. You have a fine of ${fine} for {overdue_days} overdue days"
                self.borrowed_books.remove(record)
                return f"Returned book: {book.title}"
        return "Book not found in your borrowed list"

# Create a Library instance
library = Library()

# Create Book instances and add them to the library
book1 = Book('Learning Python', 'Mark Lutz', '123456789', 5)
book2 = Book('The Python Workbook', 'Ben Stiphenson', '987654321', 3)
library.add_book(book1)
library.add_book(book2)

# Create a Member instance
member1 = Member('Alex', '0001')

# Borrow books and display information
print(member1.borrow_book(library, '123456789'))
print(member1.borrow_book(library, '987654321'))

# Get and display most popular books
popular_books = library.most_popular_books()
for book in popular_books:
    print(f"{book.title} has been borrowed {book.borrowed_count} times")

# Get and display books borrowed by a member
borrowed_by_alex = library.borrowed_books_by_member(member1)
for book in borrowed_by_alex:
    print(f"{member1.name} has borrowed {book.title}")
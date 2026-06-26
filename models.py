"""
models.py
Intelligent Library Management System with Book Recommendation Engine
Core classes (Book, Member, BorrowRecord, LibrarySystem).
"""

import hashlib


def hash_password(p):
    # NFR-02: store passwords as a one-way hash, not plain text
    return hashlib.sha256(p.encode()).hexdigest()


class Book:
    def __init__(self, book_id, title, author, category, isbn):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.isbn = isbn
        self.status = "Available"


class Member:
    def __init__(self, member_id, name, email, password):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.password = hash_password(password)
        self.status = "Active"


class BorrowRecord:
    def __init__(self, member_id, book_id):
        self.member_id = member_id
        self.book_id = book_id
        self.returned = False


class LibrarySystem:
    def __init__(self):
        self.members = {}
        self.books = {}
        self.records = []

    # FR-01 Register
    def register(self, member_id, name, email, password):
        if any(m.email == email for m in self.members.values()):
            return "Email already registered"
        self.members[member_id] = Member(member_id, name, email, password)
        return "Account created"

    # FR-02 Login
    def login(self, email, password):
        for m in self.members.values():
            if m.email == email and m.password == hash_password(password):
                return True
        return False

    # FR-03 Search
    def search(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books.values()
                if keyword in b.title.lower() or keyword in b.author.lower()
                or keyword in b.category.lower() or keyword in b.isbn.lower()]

    # FR-04 View details
    def details(self, book_id):
        b = self.books.get(book_id)
        return f"{b.title} by {b.author} | {b.category} | {b.status}" if b else "Not found"

    # FR-05 Borrow
    def borrow(self, member_id, book_id):
        b = self.books.get(book_id)
        if not b or b.status != "Available":
            return "Book unavailable"
        b.status = "Borrowed"
        self.records.append(BorrowRecord(member_id, book_id))
        return "Book issued"

    # FR-06 Return
    def return_book(self, member_id, book_id):
        for r in self.records:
            if r.member_id == member_id and r.book_id == book_id and not r.returned:
                r.returned = True
                self.books[book_id].status = "Available"
                return "Book returned"
        return "No active loan found"

    # FR-07 History
    def history(self, member_id):
        return [(r.book_id, "Returned" if r.returned else "Borrowed")
                for r in self.records if r.member_id == member_id]

    # FR-08 Add / Update / Delete book
    def add_book(self, book_id, title, author, category, isbn):
        self.books[book_id] = Book(book_id, title, author, category, isbn)
        return "Book added"

    def update_book(self, book_id, category):
        if book_id in self.books:
            self.books[book_id].category = category
            return "Book updated"
        return "Not found"

    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            return "Book deleted"
        return "Not found"

    # FR-09 Manage members
    def manage_member(self, member_id, status):
        if member_id in self.members:
            self.members[member_id].status = status
            return f"Member {status}"
        return "Not found"

    # FR-10 Recommendations
    def recommend(self, member_id):
        borrowed = [r.book_id for r in self.records if r.member_id == member_id]
        cats = {self.books[b].category for b in borrowed if b in self.books}
        return [b.title for b in self.books.values()
                if b.category in cats and b.book_id not in borrowed]

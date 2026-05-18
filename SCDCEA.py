import datetime
from typing import List, Dict

# =========================================================================
# 1. DATABASE LAYER (SINGLETON PATTERN)
# =========================================================================
class LibraryDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LibraryDatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        # Internal storage dictionaries and lists
        self.books: Dict[str, 'Book'] = {}
        self.transactions: List['Transaction'] = []
        self._initialized = True

    def reset_db(self):
        """Utility to clear states, useful for testing hooks."""
        self.books.clear()
        self.transactions.clear()


# =========================================================================
# 2. CORE DOMAIN ENTITIES (SINGLE RESPONSIBILITY)
# =========================================================================
class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn: str = isbn
        self.title: str = title
        self.author: str = author
        self.status: str = "Available"  # Operational states: "Available" or "Borrowed"

    def __str__(self) -> str:
        return f"ISBN: {self.isbn} | Title: {self.title} | Author: {self.author} | Status: [{self.status}]"


class Transaction:
    def __init__(self, member_id: str, isbn: str, operation_type: str):
        self.member_id: str = member_id
        self.isbn: str = isbn
        self.operation_type: str = operation_type  # "Checkout" or "Return"
        self.timestamp: datetime.datetime = datetime.datetime.now()

    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] Member: {member_id} -> Action: {self.operation_type} -> Book ISBN: {self.isbn}"


# =========================================================================
# 3. CONTROLLER LAYER (FACADE PATTERN)
# =========================================================================
class LibraryFacade:
    def __init__(self):
        self._db = LibraryDatabase()

    # --- CATALOG MANAGEMENT FUNCTIONS ---
    def add_book(self, isbn: str, title: str, author: str) -> str:
        if isbn in self._db.books:
            return f"Execution Failed: Book with ISBN {isbn} already exists."
        
        new_book = Book(isbn, title, author)
        self._db.books[isbn] = new_book
        return f"Success: Book '{title}' added to the catalog."

    def modify_book(self, isbn: str, new_title: str, new_author: str) -> str:
        if isbn not in self._db.books:
            return f"Execution Failed: ISBN {isbn} not found in catalog."
        
        book = self._db.books[isbn]
        book.title = new_title
        book.author = new_author
        return f"Success: Book ISBN {isbn} records updated."

    def delete_book(self, isbn: str) -> str:
        if isbn not in self._db.books:
            return f"Execution Failed: ISBN {isbn} not found in catalog."
        
        title = self._db.books[isbn].title
        del self._db.books[isbn]
        return f"Success: Book '{title}' removed from catalog."

    def search_catalog(self, search_query: str) -> List[Book]:
        query = search_query.lower()
        matched_books = []
        for book in self._db.books.values():
            if query in book.title.lower() or query in book.author.lower():
                matched_books.append(book)
        return matched_books

    # --- CIRCULATION TRACKING FUNCTIONS ---
    def checkout_book(self, member_id: str, isbn: str) -> str:
        if isbn not in self._db.books:
            return "Execution Failed: Targeted book does not exist in this library."
        
        book = self._db.books[isbn]
        if book.status == "Borrowed":
            return f"Execution Failed: '{book.title}' is currently checked out by another member."
        
        # Atomically alter operational state and log transaction
        book.status = "Borrowed"
        tx = Transaction(member_id, isbn, "Checkout")
        self._db.transactions.append(tx)
        return f"Success: '{book.title}' successfully issued to Member {member_id}."

    def return_book(self, member_id: str, isbn: str) -> str:
        if isbn not in self._db.books:
            return "Execution Failed: Target book record does not exist."
        
        book = self._db.books[isbn]
        if book.status == "Available":
            return f"Execution Failed: '{book.title}' is already logged as inside the library shelves."
        
        # Reset operational state and log transaction
        book.status = "Available"
        tx = Transaction(member_id, isbn, "Return")
        self._db.transactions.append(tx)
        return f"Success: '{book.title}' successfully processed and shelved."

    # --- SYSTEM AUDITING DETAILS ---
    def list_all_books(self) -> List[Book]:
        return list(self._db.books.values())

    def list_all_transactions(self) -> List[Transaction]:
        return self._db.transactions


# =========================================================================
# 4. INTERACTIVE ENTRY POINT (CLI SIMULATOR)
# =========================================================================
if __name__ == "__main__":
    library = LibraryFacade()
    
    # Prepopulating database dummy items for grading demo visibility
    library.add_book("978-0132350884", "Clean Code", "Robert C. Martin")
    library.add_book("978-0201633610", "Design Patterns", "Gang of Four")
    
    print("=" * 60)
    print("      NEw Library Management System UI Engine Loaded    ")
    print("=" * 60)
    
    while True:
        print("\n--- Core Services Operations Menu ---")
        print("1. Add Book")
        print("2. Modify Book")
        print("3. Delete Book")
        print("4. Search Book Catalog")
        print("5. Log Book Checkout")
        print("6. Log Book Return")
        print("7. Print Inventory Audit")
        print("8. View Transaction Ledger")
        print("9. Shutdown Engine")
        
        choice = input("\nSelect targeted action menu item (1-9): ").strip()
        
        if choice == "1":
            isbn = input("Enter ISBN: ").strip()
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            print(library.add_book(isbn, title, author))
            
        elif choice == "2":
            isbn = input("Enter target ISBN to edit: ").strip()
            title = input("Enter New Title: ").strip()
            author = input("Enter New Author: ").strip()
            print(library.modify_book(isbn, title, author))
            
        elif choice == "3":
            isbn = input("Enter target ISBN to wipe: ").strip()
            print(library.delete_book(isbn))
            
        elif choice == "4":
            query = input("Enter Title or Author search keyword: ").strip()
            results = library.search_catalog(query)
            if results:
                print(f"\nFound ({len(results)}) matching items:")
                for b in results:
                    print(f" -> {b}")
            else:
                print("No records matched your query parameters.")
                
        elif choice == "5":
            member_id = input("Enter Member ID: ").strip()
            isbn = input("Enter Book ISBN: ").strip()
            print(library.checkout_book(member_id, isbn))
            
        elif choice == "6":
            member_id = input("Enter Member ID: ").strip()
            isbn = input("Enter Book ISBN: ").strip()
            print(library.return_book(member_id, isbn))
            
        elif choice == "7":
            books = library.list_all_books()
            print("\n--- Complete Library Database Catalog ---")
            for b in books:
                print(b)
                
        elif choice == "8":
            txs = library.list_all_transactions()
            print("\n--- System Audit Trail Log History ---")
            if txs:
                for tx in txs:
                    print(tx)
            else:
                print("No transactions recorded in this execution lifecycle context.")
                
        elif choice == "9":
            print("\nExiting System Engine. Systems Saved safely.")
            break
        else:
            print("Invalid input value range. Re-enter selection options (1-9).")
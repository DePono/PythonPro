import sqlite3
from datetime import datetime

# Подключение к базе
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Создание таблицы книг
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    UNIQUE(title, author)
)
''')

# Таблица читателей
cursor.execute('''
CREATE TABLE IF NOT EXISTS Readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
)
''')

# Таблица выдачи книг
cursor.execute('''
CREATE TABLE IF NOT EXISTS BorrowedBooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    reader_id INTEGER,
    borrow_date TIMESTAMP,
    return_date TIMESTAMP,
    FOREIGN KEY(book_id) REFERENCES Books(id),
    FOREIGN KEY(reader_id) REFERENCES Readers(id)
)
''')

conn.commit()

def add_book():
    title = input("Название книги: ")
    author = input("Автор: ")
    year = int(input("Год издания: "))
    quantity = int(input("Количество экземпляров: "))
    try:
        cursor.execute("INSERT INTO Books (title, author, published_year, quantity) VALUES (?, ?, ?, ?)",
                       (title, author, year, quantity))
        conn.commit()
        print("✅ Книга добавлена.")
    except sqlite3.IntegrityError:
        print("⚠️ Такая книга уже существует.")

def register_reader():
    name = input("Имя читателя: ")
    email = input("Email: ")
    try:
        cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("Читатель зарегистрирован.")
    except sqlite3.IntegrityError:
        print("Этот email уже зарегистрирован.")

def borrow_book():
    book_id = int(input("ID книги: "))
    reader_id = int(input("ID читателя: "))
    cursor.execute("SELECT quantity FROM Books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        cursor.execute("INSERT INTO BorrowedBooks (book_id, reader_id, borrow_date, return_date) VALUES (?, ?, ?, NULL)",
                       (book_id, reader_id, datetime.now()))
        cursor.execute("UPDATE Books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
        conn.commit()
        print("Книга выдана.")
    else:
        print("Книга недоступна.")

def return_book():
    book_id = int(input("ID книги: "))
    reader_id = int(input("ID читателя: "))
    cursor.execute('''
        SELECT id FROM BorrowedBooks
        WHERE book_id = ? AND reader_id = ? AND return_date IS NULL
    ''', (book_id, reader_id))
    result = cursor.fetchone()
    if result:
        borrow_id = result[0]
        cursor.execute("UPDATE BorrowedBooks SET return_date = ? WHERE id = ?", (datetime.now(), borrow_id))
        cursor.execute("UPDATE Books SET quantity = quantity + 1 WHERE id = ?", (book_id,))
        conn.commit()
        print("Книга возвращена.")
    else:
        print("⚠Не найдено активной выдачи.")
def list_books():
    cursor.execute("SELECT * FROM Books ORDER BY published_year")
    for row in cursor.fetchall():
        print(row)

def active_borrowed_books():
    cursor.execute('''
        SELECT Books.title, Readers.name, BorrowedBooks.borrow_date
        FROM BorrowedBooks
        JOIN Books ON Books.id = BorrowedBooks.book_id
        JOIN Readers ON Readers.id = BorrowedBooks.reader_id
        WHERE return_date IS NULL
    ''')
    for row in cursor.fetchall():
        print(row)

def readers_with_borrowings():
    cursor.execute('''
        SELECT DISTINCT Readers.name, Readers.email
        FROM Readers
        JOIN BorrowedBooks ON Readers.id = BorrowedBooks.reader_id
    ''')
    for row in cursor.fetchall():
        print(row)
def search_books():
    keyword = input("Введите название или автора: ")
    cursor.execute('''
        SELECT * FROM Books
        WHERE title LIKE ? OR author LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))
    for row in cursor.fetchall():
        print(row)

def delete_book():
    book_id = int(input("ID книги: "))
    cursor.execute("SELECT COUNT(*) FROM BorrowedBooks WHERE book_id = ? AND return_date IS NULL", (book_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))
        conn.commit()
        print("🗑Книга удалена.")
    else:
        print("Книга выдана читателям — удалить нельзя.")

def delete_reader():
    reader_id = int(input("ID читателя: "))
    cursor.execute("DELETE FROM Readers WHERE id = ?", (reader_id,))
    conn.commit()
    print("Читатель удалён.")

def menu():
    while True:
        print("\n--- Меню ---")
        print("1. Добавить книгу")
        print("2. Зарегистрировать читателя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Список книг (по году)")
        print("6. Поиск книги")
        print("7. Книги на руках")
        print("8. Читатели с заимствованиями")
        print("9. Удалить книгу")
        print("10. Удалить читателя")
        print("0. Выход")

        choice = input("Выбор: ")

        match choice:
            case "1": add_book()
            case "2": register_reader()
            case "3": borrow_book()
            case "4": return_book()
            case "5": list_books()
            case "6": search_books()
            case "7": active_borrowed_books()
            case "8": readers_with_borrowings()
            case "9": delete_book()
            case "10": delete_reader()
            case "0":
                print("👋 Выход")
                break
            case _: print("Неверный ввод")

if __name__ == "__main__":
    menu()
    conn.close()

import unittest
import sqlite3
from datetime import datetime

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        # Создаем временную БД в памяти
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()

        # Таблицы
        self.cursor.execute('''
            CREATE TABLE Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_year INTEGER,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                UNIQUE(title, author)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE Readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE BorrowedBooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                reader_id INTEGER,
                borrow_date TIMESTAMP,
                return_date TIMESTAMP,
                FOREIGN KEY(book_id) REFERENCES Books(id),
                FOREIGN KEY(reader_id) REFERENCES Readers(id)
            )
        ''')

        self.conn.commit()

    def test_add_book(self):
        self.cursor.execute("INSERT INTO Books (title, author, published_year, quantity) VALUES (?, ?, ?, ?)",
                            ("Python 101", "Author A", 2020, 3))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM Books WHERE title = ?", ("Python 101",))
        book = self.cursor.fetchone()
        self.assertIsNotNone(book)
        self.assertEqual(book[1], "Python 101")

    def test_register_reader(self):
        self.cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)",
                            ("John Doe", "john@example.com"))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM Readers WHERE email = ?", ("john@example.com",))
        reader = self.cursor.fetchone()
        self.assertIsNotNone(reader)
        self.assertEqual(reader[1], "John Doe")

    def test_borrow_book(self):
        # Добавим книгу и читателя
        self.cursor.execute("INSERT INTO Books (title, author, published_year, quantity) VALUES (?, ?, ?, ?)",
                            ("Book X", "Author B", 2010, 1))
        self.cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)",
                            ("Jane Smith", "jane@example.com"))
        self.conn.commit()

        self.cursor.execute("SELECT id FROM Books WHERE title = 'Book X'")
        book_id = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT id FROM Readers WHERE email = 'jane@example.com'")
        reader_id = self.cursor.fetchone()[0]

        # Выдача
        self.cursor.execute("INSERT INTO BorrowedBooks (book_id, reader_id, borrow_date, return_date) VALUES (?, ?, ?, NULL)",
                            (book_id, reader_id, datetime.now()))
        self.cursor.execute("UPDATE Books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
        self.conn.commit()

        # Проверим, что книга выдана
        self.cursor.execute("SELECT quantity FROM Books WHERE id = ?", (book_id,))
        updated_qty = self.cursor.fetchone()[0]
        self.assertEqual(updated_qty, 0)

    def test_return_book(self):
        # Добавим книгу и читателя
        self.cursor.execute("INSERT INTO Books (title, author, published_year, quantity) VALUES (?, ?, ?, ?)",
                            ("Book Y", "Author C", 2015, 1))
        self.cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)",
                            ("Alex", "alex@example.com"))
        self.conn.commit()

        self.cursor.execute("SELECT id FROM Books WHERE title = 'Book Y'")
        book_id = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT id FROM Readers WHERE email = 'alex@example.com'")
        reader_id = self.cursor.fetchone()[0]

        # Выдача
        self.cursor.execute("INSERT INTO BorrowedBooks (book_id, reader_id, borrow_date, return_date) VALUES (?, ?, ?, NULL)",
                            (book_id, reader_id, datetime.now()))
        self.cursor.execute("UPDATE Books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
        self.conn.commit()

        # Возврат
        self.cursor.execute("UPDATE BorrowedBooks SET return_date = ? WHERE book_id = ? AND reader_id = ? AND return_date IS NULL",
                            (datetime.now(), book_id, reader_id))
        self.cursor.execute("UPDATE Books SET quantity = quantity + 1 WHERE id = ?", (book_id,))
        self.conn.commit()

        self.cursor.execute("SELECT quantity FROM Books WHERE id = ?", (book_id,))
        self.assertEqual(self.cursor.fetchone()[0], 1)

    def test_cannot_register_same_email(self):
        self.cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)", ("User1", "user@example.com"))
        self.conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO Readers (name, email) VALUES (?, ?)", ("User2", "user@example.com"))
            self.conn.commit()

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()

import json
import os


class Book:
    def __init__(self, author, title ,year: int):
        self.year = year
        self.title = title
        self.author = author


    def __repr__(self):
        return f"{self.author},{self.title}, {self.year}.\n"

    def to_dict(self):
        """Возвращает книгу как словарь."""
        return {'title': self.title, 'author': self.author, 'year': self.year}

    @classmethod
    def from_dict(cls, data):
        """Создает объект Book из словаря."""
        return cls(data['title'], data['author'], data['year'])

class Sorter:
    """
    Класс, предоставляющий различные алгоритмы сортировки списков объектов
    по заданному атрибуту.
    """
    def quick_sort(self,arr, sorter):
         if len(arr) <= 1:
             return arr
         pivot = arr[len(arr) // 2]
         left = [x for x in arr if getattr(x,sorter, None) < getattr(pivot,sorter, None)]
         middle = [x for x in arr if getattr(x,sorter, None) == getattr(pivot,sorter, None)]
         right = [x for x in arr if getattr(x,sorter, None) > getattr(pivot,sorter, None)]
         return self.quick_sort(left, sorter) + middle + self.quick_sort(right, sorter)



    def merge_sort(self,arr, sorter):
         if len(arr) <= 1:
             return arr
         mid = len(arr) // 2
         left = [x for x in arr if getattr(x, sorter, None) < getattr(arr[mid], sorter, None)]
         right = [x for x in arr[mid:] if getattr(x, sorter, None) >= getattr(arr[mid], sorter, None)]
         return self.merge(left, right,sorter)

    def merge(self,left, right, sorter):
         result = []
         i = j = 0
         while i < len(left) and j < len(right):
             if getattr(left[i], sorter, None) < getattr(right[j], sorter, None):
                 result.append(left[i])
                 i += 1
             else:
                 result.append(right[j])
                 j += 1
         result.extend(left[i:])
         result.extend(right[j:])
         return result

    def heap_sort(self,arr,sorter):
         n = len(arr)

         for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i, sorter)

         for i in range(n - 1, 0, -1):
             arr[i], arr[0] = arr[0], arr[i]
             self.heapify(arr, i, 0, sorter)

    def heapify(self,arr, n, i, sorter):
         largest = i
         left = 2 * i + 1
         right = 2 * i + 2

         if left < n and getattr(arr[left], sorter, None) >getattr(arr[largest], sorter, None):
             largest = left

         if right < n and getattr(arr[right], sorter, None) > getattr(arr[largest], sorter, None):
             largest = right

         if largest != i:
             arr[i], arr[largest] = arr[largest], arr[i]
             self.heapify(arr, n, largest, sorter)

class Library:
    """Управляет списком книг, предоставляет функции сортировки, поиска, добавления и удаления."""

    def __init__(self, books=None):
        self.books = books if books is not None else []
        self.sorter = Sorter()  # Создаем экземпляр Sorter

    def show_books(self):
        """Выводит список всех книг."""
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(book)

    def sort_books(self, criterion, sort_algorithm="quick_sort"):
        """Сортирует книги по заданному критерию, используя выбранный алгоритм сортировки."""
        if not self.books:
            print("Библиотека пуста, сортировать нечего.")
            return

        if criterion not in ('title', 'author', 'year'):
            print("Неверный критерий сортировки.")
            return

        if sort_algorithm == "quick_sort":
            self.books = self.sorter.quick_sort(self.books, criterion)
        elif sort_algorithm == "merge_sort":
            self.books = self.sorter.merge_sort(self.books, criterion)
        elif sort_algorithm == "heap_sort":
            self.sorter.heap_sort(self.books.copy(), criterion)
        else:
            print("Неверный алгоритм сортировки. Используйте 'quick_sort', 'merge_sort' или 'heap_sort'.")
            return


        self.show_books()

    def find_book(self, search_term, search_by):
        """Ищет книги по названию или автору."""
        results = []
        if search_by == 'title':
            results = [book for book in self.books if search_term.lower() in book.title.lower()]
        elif search_by == 'author':
            results = [book for book in self.books if search_term.lower() in book.author.lower()]
        else:
            print("Неверный параметр поиска. Ищите по 'title' или 'author'.")
            return

        if results:
            print("Найденные книги:")
            for book in results:
                print(book)
        else:
            print("Книги не найдены.")

    def add_book(self):
        """Добавляет новую книгу в библиотеку."""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        while True:
            try:
                year = int(input("Введите год издания книги: "))
                break
            except ValueError:
                print("Неверный формат года. Введите число.")
        new_book = Book(title, author, year)
        self.books.append(new_book)
        print("Книга добавлена.")

    def remove_book(self):
        """Удаляет книгу из библиотеки по названию."""
        title = input("Введите название книги, которую хотите удалить: ")
        book_to_remove = None
        for book in self.books:
            if book.title.lower() == title.lower():
                book_to_remove = book
                break
        if book_to_remove:
            self.books.remove(book_to_remove)
            print("Книга удалена.")
        else:
            print("Книга не найдена.")

    def save_to_file(self, filename="library.json"):
        """Сохраняет список книг в JSON файл."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                book_data = [book.to_dict() for book in self.books]
                json.dump(book_data, f, indent=4, ensure_ascii=False)  # ensure_ascii=False for correct Cyrillic
            print(f"Библиотека сохранена в файл '{filename}'.")
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")

    def load_from_file(self, filename="library.json"):
        """Загружает список книг из JSON файла."""
        try:
            if not os.path.exists(filename):
                print(f"Файл '{filename}' не найден. Создана новая библиотека.")
                return # Don't try to load, just keep an empty library.

            with open(filename, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
                self.books = [Book.from_dict(data) for data in book_data]
            print(f"Библиотека загружена из файла '{filename}'.")
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден.  Будет создана новая библиотека.")
        except json.JSONDecodeError:
            print(f"Ошибка при чтении JSON из файла '{filename}'.  Создана новая библиотека.")
        except Exception as e:
            print(f"Ошибка при загрузке из файла: {e}")
            self.books = []



def main():
    """Главная функция, управляющая интерфейсом пользователя."""
    book0 = Book('Марк Твен', "Приключения Геклеба Финна", 1884)
    book1 = Book('Агата Кристи', "Очарованный замок", 1926)
    book2 = Book('Герман Мельвилл', "Испытание Франки Зеландии", 1851)
    book3 = Book('Братья Гримм', "Краткое содержание сказок", 1812)
    book4 = Book('Оливия Уолш', "Сладкая жизнь", 1996)
    book5 = Book('Эдгар Аллан По', "Пуговка на новом брюке", 1841)
    book6 = Book('Клод Дебюсси', "Мемуары поэта", 1890)
    book7 = Book('Стивен Кинг', "Дракула", 1975)
    book8 = Book('Волтер Скотт', "Иванхoe", 1819)
    book9 = Book('Джеймс Джойс', "Улисс", 1922)
    book10 = Book('Бронте Патриция', "Жизнь в Италии", 1843)
    book11 = Book('Анна Кариока', "Сказка о каменной деве и снежном короле", 1757)
    book12 = Book('Бертран Рассел', "Образование", 1918)
    book13 = Book('Иван Тургенев', "Дуэль", 1860)
    book14 = Book('Лоренс Стерн', "Тщетная любовь", 1924)
    book_list = [book0, book1, book2, book3, book4, book5, book6, book7, book8, book9, book10, book11, book12, book13, book14]


    library = Library(books=book_list) # Инициализация с начальным списком
    #library.load_from_file()  # Загружаем библиотеку при запуске

    while True:
        print("\nДобро пожаловать в систему управления библиотекой!")
        print("Выберите действие:")
        print("1. Показать все книги")
        print("2. Сортировать книги по названию")
        print("3. Сортировать книги по автору")
        print("4. Сортировать книги по году издания")
        print("5. Найти книгу по названию")
        print("6. Найти книгу по автору")
        print("7. Добавить книгу")
        print("8. Удалить книгу")
        print("9. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            library.show_books()
        elif choice == '2':
            algorithm = input("Выберите алгоритм сортировки ('quick_sort', 'merge_sort', 'heap_sort', по умолчанию 'quick_sort'): ") or "quick_sort" # Allow user to choose
            library.sort_books('title', algorithm)
        elif choice == '3':
            algorithm = input("Выберите алгоритм сортировки ('quick_sort', 'merge_sort', 'heap_sort', по умолчанию 'quick_sort'): ") or "quick_sort"
            library.sort_books('author',algorithm)
        elif choice == '4':
            algorithm = input("Выберите алгоритм сортировки ('quick_sort', 'merge_sort', 'heap_sort', по умолчанию 'quick_sort'): ") or "quick_sort"
            library.sort_books('year',algorithm)
        elif choice == '5':
            search_term = input("Введите название для поиска: ")
            library.find_book(search_term, 'title')
        elif choice == '6':
            search_term = input("Введите автора для поиска: ")
            library.find_book(search_term, 'author')
        elif choice == '7':
            library.add_book()
        elif choice == '8':
            library.remove_book()
        elif choice == '9':
            library.save_to_file()  # Сохраняем библиотеку при выходе
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
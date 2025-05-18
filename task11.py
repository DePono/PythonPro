import sqlite3

# Подключение к базе данных (создаст файл, если его нет)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Создание таблицы студентов
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    course INTEGER NOT NULL,
    age INTEGER NOT NULL
)
''')
conn.commit()


def add_student():
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    course = int(input("Курс: "))
    age = int(input("Возраст: "))
    cursor.execute("INSERT INTO students (first_name, last_name, course, age) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, course, age))
    conn.commit()
    print("✅ Студент добавлен.\n")


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if not students:
        print("Нет данных.\n")
    else:
        for s in students:
            print(f"ID: {s[0]}, Имя: {s[1]}, Фамилия: {s[2]}, Курс: {s[3]}, Возраст: {s[4]}")
        print()


def update_student():
    student_id = int(input("ID студента для изменения: "))
    print("Введите новые данные:")
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    course = int(input("Курс: "))
    age = int(input("Возраст: "))
    cursor.execute('''
        UPDATE students SET first_name = ?, last_name = ?, course = ?, age = ? WHERE id = ?
    ''', (first_name, last_name, course, age, student_id))
    conn.commit()
    print("✅ Данные обновлены.\n")


def delete_student():
    student_id = int(input("ID студента для удаления: "))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print("✅ Студент удалён.\n")


def main():
    while True:
        print("1. Добавить студента")
        print("2. Показать всех студентов")
        print("3. Изменить данные студента")
        print("4. Удалить студента")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("👋 До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте снова.\n")


if __name__ == "__main__":
    main()
    conn.close()

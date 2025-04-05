import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Ошибка: деление на ноль!"
    return x / y

def square_root(x):
    if x < 0:
        return "Ошибка: нельзя извлечь корень из отрицательного числа!"
    return math.sqrt(x)

def power(x, y):
    return x ** y

if __name__ == "__main__":
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Квадратный корень")
    print("6. Степень")

    choice = input("Введите номер операции (1/2/3/4/5/6): ")

    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))
        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))
        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))
        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))

    elif choice == '5':
        num = float(input("Введите число: "))
        print("Квадратный корень из", num, "=", square_root(num))

    elif choice == '6':
        num1 = float(input("Введите число: "))
        num2 = float(input("Введите степень: "))
        print(num1, "в степени", num2, "=", power(num1, num2))

    else:
        print("Неверный ввод")
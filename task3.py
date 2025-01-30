class Employee:
    def __init__(self, first_name, last_name, age, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return f"{self.first_name} {self.last_name}, возраст {self.age}, оклад {self.salary}"


def get_last_name(emp):
    return emp.last_name

def get_age(emp):
    return emp.age

def get_salary(emp):
    return emp.salary

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def sort_employees(self, key_func=get_last_name):
        """
        Сортирует список работников.

        Args:
            key_func: Функция, возвращающая значение для сравнения при сортировке.
        """
        EmployeeManager.shell_sort(self.employees, key_func)

    def display_employees(self):
        """Отображает отсортированный список работников."""
        for employee in self.employees:
            print(employee)

    @staticmethod
    def shell_sort(employees, key_func=get_last_name):
        """
        Сортирует список работников с использованием алгоритма сортировки Шелла.

        Args:
            employees: Список объектов Employee.
            key_func: Функция, возвращающая значение для сравнения при сортировке.
        """
        n = len(employees)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = employees[i]
                j = i
                while j >= gap and key_func(employees[j - gap]) > key_func(temp):
                    employees[j] = employees[j - gap]
                    j -= gap
                employees[j] = temp
            gap //= 2

def main():
    manager = EmployeeManager()

    # Добавляем несколько сотрудников
    manager.add_employee(Employee("Иван", "Иванов", 30, 50000))
    manager.add_employee(Employee("Петр", "Сидоров", 25, 60000))
    manager.add_employee(Employee("Анна", "Смирнова", 35, 75000))
    manager.add_employee(Employee("Дмитрий", "Кузнецов", 28, 55000))
    manager.add_employee(Employee("Елена", "Петрова", 40, 80000))

    print("Исходный список сотрудников:")
    manager.display_employees()
    print("-" * 30)

    print("Сортировка по фамилии:")
    manager.sort_employees()
    manager.display_employees()
    print("-" * 30)

    print("Сортировка по возрасту:")
    manager.sort_employees(key_func=get_age)
    manager.display_employees()
    print("-" * 30)

    print("Сортировка по зарплате:")
    manager.sort_employees(key_func=get_salary)
    manager.display_employees()


if __name__ == "__main__":
    main()
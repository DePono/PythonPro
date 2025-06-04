from functools import partial

# 1. Создание каррированных функций:

# Функция для расчета отработанных часов
def hours_per_day(hours):
    def calculate_hours(days):
        return hours * days
    return calculate_hours


result = hours_per_day(8)(20)
print(f"Отработано часов: {result}")


# Функция для расчета бонусов
def bonus_percentage(percentage):
    def calculate_bonus(salary):
        return (percentage / 100) * salary
    return calculate_bonus

result = bonus_percentage(10)(3000)
print(f"Сумма бонуса: {result}")

# Функция для расчета чистой зарплаты
def net_salary(gross_salary, tax_rate):
    return gross_salary - (gross_salary * tax_rate)


tax_20 = partial(net_salary, tax_rate=0.20)
result = tax_20(5000)  # 5000 - (5000 * 0.20) = 4000
print(f"Чистая зарплата (налог 20%): {result}")


# Функция для расчета итоговой зарплаты с учетом бонусов
def final_salary(base_salary, bonus):
    return base_salary + bonus

# Создаем функцию с фиксированным бонусом 500
bonus_500 = partial(final_salary, bonus=500)
result = bonus_500(3000)  # 3000 + 500 = 3500
print(f"Итоговая зарплата (бонус 500): {result}")


# Функции для расчета заработной платы
def calculate_hours(hours_per_day, days):
    return hours_per_day * days

def calculate_gross_salary(hours, hourly_rate):
    return hours * hourly_rate

def composed_salary_function(hours_per_day, days, hourly_rate):
    hours = calculate_hours(hours_per_day, days)
    return calculate_gross_salary(hours, hourly_rate)

# Пример использования
result = composed_salary_function(8, 20, 25)  # (8 * 20) * 25 = 4000
print(f"Зарплата до вычета налогов: {result}")

# Функции для итогового расчета
def calculate_net_salary(gross_salary, tax_rate=0.20):
    return gross_salary - (gross_salary * tax_rate)

def apply_bonus(salary, bonus):
    return salary + bonus


def final_salary_composition(gross_salary, bonus, tax_rate=0.20):
    net = calculate_net_salary(gross_salary, tax_rate)
    return apply_bonus(net, bonus)

# Пример использования
result = final_salary_composition(4000, 300)  # 3500
print(f"Итоговая зарплата после бонуса и налога: {result}")
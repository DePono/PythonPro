#Условие задачи:Вы имеете отсортированный массив, в котором некоторые элементы могут отсутствовать, но остальные элементы по-прежнему отсортированы.
# Например, массив может выглядеть следующим образом:
# [1, 2, None, None, 5, 6, 7, None, 10, 11] Где None представляет собой пропущенные элементы.
# Ваша задача — найти индекс заданного элемента в таком массиве, используя бинарный поиск. Если элемент отсутствует, возвращайте -1.
# Подсказки: Обработка пропущенных элементов: Во время бинарного поиска, если середина массива содержит None, пропускайте её и переопределите границы поиска в зависимости от того, в каком направлении можно найти элемент.
# Избегайте ненужных проверок: Поскольку массив отсортирован, вы можете избежать полной проверки всех элементов, если текущий элемент равен None.
# Бинарный поиск с пропуском: Подумайте о том, как можно адаптировать бинарный поиск, чтобы учесть пропущенные элементы и все еще эффективно искать нужный элемент.
# Пример результата:
# arr = [1, 2, None, None, 5, 6, 7, None, 10, 11]
# x = 7
# print(search_in_sparse_array(arr, x))
# Ожидаемый результат: 6
# x = 3
# print(search_in_sparse_array(arr, x))
# Ожидаемый результат: -1
# x = 10
# print(search_in_sparse_array(arr, x))
# Ожидаемый результат: 8
# ВАЖНО: Ваша функция должна корректно обрабатывать пропущенные элементы и находить индекс заданного элемента.
# Функция должна работать эффективно для больших массивов с пропущенными элементами, поддерживая сложность бинарного поиска, то есть O(log n) в среднем

original_list = [1, 2, None, None, 5, 6, 7, None, 10, 11]

def search_in_sparse_array(list: list, x: int) -> int:
    """
    Выполняет бинарный поиск в разреженном (содержащем None) отсортированном массиве.

    Args:
        list: Отсортированный список (может содержать None).
        x: Искомый элемент.

    Returns:
        Индекс искомого элемента, если он найден, иначе -1.
    """
    first_index = 0
    last_index = len(list) - 1

    while first_index <= last_index:
        middle_index = (first_index + last_index) // 2

        # Ищем ближайший не-None элемент
        left = middle_index
        right = middle_index
        while left >= first_index and list[left] is None:
            left -= 1
        while right <= last_index and list[right] is None:
            right += 1

        if left < first_index and right > last_index:
            return -1 # Все элементы None на текущем отрезке поиска
        elif left >= first_index and list[left] == x:
            return left # Нашли элемент
        elif right <= last_index and list[right] == x:
          return right
        elif left >= first_index and list[left] > x: # Текущий элемент > x, сужаем правую границу
            last_index = middle_index - 1
        elif right <= last_index and list[right] < x: # Текущий элемент < x, сужаем левую границу
            first_index = middle_index + 1
        elif left < first_index:
          first_index = right + 1
        elif right > last_index:
          last_index = left - 1
    return -1 # Если ничего не нашли


arr = [1, 2, None, None, 5, 6, 7, None, 10, 11]
x = 3
print(search_in_sparse_array(arr, x))
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from collections import deque

T = TypeVar('T')  # T - это тип, который будет хранить хранилище

class Sortable(ABC):  # Определяем интерфейс для объектов, которые можно сортировать
    @abstractmethod
    def get_sort_key(self, criterion: str):
        pass  # Метод должен возвращать значение, по которому будет происходить сортировка

class DeliveryItem(Sortable):
    def __init__(self, item_id: int, name: str, weight: float, destination: str, delivery_time: str):
        self.item_id = item_id
        self.name = name
        self.weight = weight
        self.destination = destination
        self.delivery_time = delivery_time  # Добавляем время доставки

    def __repr__(self):
        return f"Номер: {self.item_id}, Name: {self.name}, Weight: {self.weight}, Destination: {self.destination}, Time: {self.delivery_time}"

    def get_sort_key(self, criterion: str):
        if criterion == 'name':
            return self.name.lower()
        elif criterion == 'weight':
            return self.weight
        elif criterion == 'destination':
            return self.destination.lower()
        elif criterion == 'delivery_time':
            return self.delivery_time
        elif criterion == 'item_id':
            return self.item_id
        else:
            raise ValueError("Неверный критерий сортировки")


class Sorter:
    """
    Класс, предоставляющий различные алгоритмы сортировки списков объектов
    по заданному атрибуту.
    """
    def quick_sort(self, arr: List[Sortable], criterion: str) -> List[Sortable]:
        """Реализация быстрой сортировки."""
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        less = [x for x in arr if x.get_sort_key(criterion) < pivot.get_sort_key(criterion)]
        middle = [x for x in arr if x.get_sort_key(criterion) == pivot.get_sort_key(criterion)]
        right = [x for x in arr if x.get_sort_key(criterion) > pivot.get_sort_key(criterion)]
        return self.quick_sort(less, criterion) + middle + self.quick_sort(right, criterion)

    def merge_sort(self, arr: List[Sortable], criterion: str) -> List[Sortable]:
        """Реализация сортировки слиянием."""
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort([x for x in arr if x.get_sort_key(criterion) < arr[mid].get_sort_key(criterion)], criterion)
        right = self.merge_sort([x for x in arr[mid:] if x.get_sort_key(criterion) >= arr[mid].get_sort_key(criterion)], criterion)
        return self._merge(left, right, criterion)

    def _merge(self, left: List[Sortable], right: List[Sortable], criterion: str) -> List[Sortable]:
        """Вспомогательная функция для сортировки слиянием."""
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i].get_sort_key(criterion) < right[j].get_sort_key(criterion):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def heap_sort(self, arr: List[Sortable], criterion: str):
        """Реализация пирамидальной сортировки."""
        n = len(arr)

        # Построение max-heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, criterion)

        # Извлечение элементов из heap по одному
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # swap
            self._heapify(arr, i, 0, criterion)

    def _heapify(self, arr: List[Sortable], n: int, i: int, criterion: str):
        """Вспомогательная функция для heap_sort."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left].get_sort_key(criterion) > arr[largest].get_sort_key(criterion):
            largest = left

        if right < n and arr[right].get_sort_key(criterion) > arr[largest].get_sort_key(criterion):
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest, criterion)


class GenericStorage(Generic[T]):  # GenericStorage параметризован типом T, который должен реализовывать Sortable
    def __init__(self, items: List[T] = None, sorter: Sorter = None, item_type_name: str = "Item"):
        self.items: List[T] = items if items is not None else []  # Явное указание типа
        self.sorter = sorter if sorter is not None else Sorter()
        self.item_type_name = item_type_name

    def show_items(self):
        if not self.items:
            print(f"{self.item_type_name} storage is empty.")
            return
        for item in self.items:
            print(item)

    def find_item(self, search_term: str, search_by: str):
        results = []
        if search_by == 'name':
            results = [item for item in self.items if search_term.lower() in item.name.lower()]  # type: ignore
        elif search_by == 'destination':
            results = [item for item in self.items if search_term.lower() in item.destination.lower()]  # type: ignore
        else:
            print("Неверный параметр поиска. Ищите по 'name' или 'destination'.")
            return

        if results:
            print("Найденные элементы:")
            for item in results:
                print(item)
        else:
            print("Элементы не найдены.")

    def add_item(self, item: T):
        self.items.append(item)
        print(f"{self.item_type_name} добавлен.")

    def remove_item(self, item_id: int):
        item_to_remove = None
        for item in self.items:
            if item.item_id == item_id:  # type: ignore
                item_to_remove = item
                break
        if item_to_remove:
            self.items.remove(item_to_remove)
            print(f"{self.item_type_name} удален.")
        else:
            print(f"{self.item_type_name} не найден.")

class Delivery(GenericStorage[DeliveryItem]):
    def __init__(self, items: List[DeliveryItem] = None, sorter: Sorter = None):
        super().__init__(items, sorter, "Delivery Item")
        self.urgent_deliveries = []  # Стек для срочных доставок
        self.delivery_queue = deque()  # Очередь для доставок

    def add_delivery_item(self):  # Метод для добавления DeliveryItem через пользовательский ввод
        """Добавляет новый элемент доставки."""
        try:
            item_id = int(input("Введите ID элемента доставки: "))
            name = input("Введите название элемента доставки: ")
            weight = float(input("Введите вес элемента доставки: "))
            destination = input("Введите пункт назначения элемента доставки: ")
            delivery_time = input("Введите время доставки: ") #Добавляем ввод времени доставки
            new_item = DeliveryItem(item_id, name, weight, destination, delivery_time)
            self.add_item(new_item)
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовые значения для ID и веса.")

    def remove_delivery_item(self):  # Метод для удаления DeliveryItem через пользовательский ввод
        """Удаляет элемент доставки по ID."""
        try:
            item_id = int(input("Введите ID элемента доставки, который хотите удалить: "))
            self.remove_item(item_id)
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовое значение для ID.")

    def sort_by_weight_merge_sort(self):
        """Сортирует элементы доставки по весу с использованием сортировки слиянием."""
        self.items = self.sorter.merge_sort(self.items, 'weight')
        self.show_items()

    def sort_by_delivery_time_quick_sort(self):
        """Сортирует элементы доставки по времени доставки с использованием быстрой сортировки."""
        self.items = self.sorter.quick_sort(self.items, 'delivery_time')
        self.show_items()

    def sort_by_item_id_heap_sort(self):
        """Сортирует элементы доставки по ID с использованием пирамидальной сортировки."""
        self.items = self.sorter.heap_sort(self.items, 'item_id')
        self.show_items()

    def linear_search_by_item_id(self, item_id: int):
        """Выполняет линейный поиск элемента доставки по ID."""
        for item in self.items:
            if item.item_id == item_id:  # type: ignore
                print("Доставка найдена:")
                print(item)
                return
        print("Доставка не найдена.")

    def binary_search_by_delivery_time(self, delivery_time: str):
         """Выполняет бинарный поиск элемента доставки по времени (требует предварительной сортировки по времени)."""
         self.sort_by_delivery_time_quick_sort()  # Сначала сортируем по времени
         left = 0
         right = len(self.items) - 1

         while left <= right:
             mid = (left + right) // 2
             if self.items[mid].delivery_time == delivery_time: # type: ignore
                 print("Доставка найдена:")
                 print(self.items[mid])
                 return
             elif self.items[mid].delivery_time < delivery_time: # type: ignore
                 left = mid + 1
             else:
                 right = mid - 1
         print("Доставка не найдена.")

    def add_urgent_delivery(self, item: DeliveryItem):
        """Добавляет элемент в стек срочных доставок."""
        self.urgent_deliveries.append(item)
        print(f"Срочная доставка '{item.name}' добавлена в стек.")

    def process_urgent_delivery(self):
        """Обрабатывает последний добавленный элемент из стека срочных доставок."""
        if self.urgent_deliveries:
            item = self.urgent_deliveries.pop()
            print(f"Обрабатывается срочная доставка: {item}")
        else:
            print("Нет срочных доставок для обработки.")

    def enqueue_delivery(self, item: DeliveryItem):
        """Добавляет элемент в очередь доставок."""
        self.delivery_queue.append(item)
        print(f"Доставка '{item.name}' добавлена в очередь.")

    def dequeue_delivery(self):
        """Обрабатывает первый добавленный элемент из очереди доставок."""
        if self.delivery_queue:
            item = self.delivery_queue.popleft()
            print(f"Обрабатывается доставка: {item}")
        else:
            print("Нет доставок в очереди.")


def main():
    """Главная функция, управляющая интерфейсом пользователя для системы доставки."""
    # Начальные данные
    delivery_item1 = DeliveryItem(1, "Телевизор", 15.5, "Москва", "10:00")
    delivery_item2 = DeliveryItem(2, "Холодильник", 75.0, "Санкт-Петербург", "14:00")
    delivery_item3 = DeliveryItem(3, "Стиральная машина", 60.2, "Москва", "12:00")
    delivery_items = [delivery_item1, delivery_item2, delivery_item3]

    delivery = Delivery(items=delivery_items) # Инициализация Delivery с начальным списком элементов

    while True:
        print("\nДобро пожаловать в систему управления доставкой!")
        print("Выберите действие:")
        print("1. Показать все элементы доставки")
        print("2. Сортировать по весу (Merge Sort)")
        print("3. Сортировать по времени доставки (Quick Sort)")
        print("4. Сортировать по номеру доставки (Heap Sort)")
        print("5. Найти элемент по номеру (Linear Search)")
        print("6. Найти элемент по времени доставки (Binary Search)")
        print("7. Добавить элемент доставки")
        print("8. Удалить элемент доставки")
        print("9. Добавить срочную доставку (Stack)")
        print("10. Обработать срочную доставку (Stack)")
        print("11. Добавить доставку в очередь")
        print("12. Обработать доставку из очереди")
        print("13. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            delivery.show_items()
        elif choice == '2':
            delivery.sort_by_weight_merge_sort()
        elif choice == '3':
            delivery.sort_by_delivery_time_quick_sort()
        elif choice == '4':
            delivery.sort_by_item_id_heap_sort()
        elif choice == '5':
            try:
                item_id = int(input("Введите номер элемента доставки для поиска: "))
                delivery.linear_search_by_item_id(item_id)
            except ValueError:
                print("Неверный ввод. Введите числовой номер элемента доставки.")
        elif choice == '6':
             delivery_time = input("Введите время доставки для поиска: ")
             delivery.binary_search_by_delivery_time(delivery_time)
        elif choice == '7':
            delivery.add_delivery_item()  # Используем новый метод для добавления элемента доставки
        elif choice == '8':
            delivery.remove_delivery_item()  # Используем новый метод для удаления элемента доставки
        elif choice == '9':
            try:
                item_id = int(input("Введите ID элемента доставки: "))
                name = input("Введите название элемента доставки: ")
                weight = float(input("Введите вес элемента доставки: "))
                destination = input("Введите пункт назначения элемента доставки: ")
                delivery_time = input("Введите время доставки: ")
                new_item = DeliveryItem(item_id, name, weight, destination, delivery_time)
                delivery.add_urgent_delivery(new_item)
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовые значения для ID и веса.")
        elif choice == '10':
            delivery.process_urgent_delivery()
        elif choice == '11':
            try:
                item_id = int(input("Введите ID элемента доставки: "))
                name = input("Введите название элемента доставки: ")
                weight = float(input("Введите вес элемента доставки: "))
                destination = input("Введите пункт назначения элемента доставки: ")
                delivery_time = input("Введите время доставки: ")
                new_item = DeliveryItem(item_id, name, weight, destination, delivery_time)
                delivery.enqueue_delivery(new_item)
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовые значения для ID и веса.")
        elif choice == '12':
            delivery.dequeue_delivery()
        elif choice == '13':
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    main()
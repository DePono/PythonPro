from abc import ABC, abstractmethod
from typing import Any


# Интерфейс старого сервиса
class OldService(ABC):
    @abstractmethod
    def fetch_data(self) -> Any:
        """
        Извлекает данные в старом формате.
        """
        pass


# Интерфейс нового сервиса
class NewService(ABC):
    @abstractmethod
    def get_data(self) -> Any:
        """
        Получает данные в новом формате.
        """
        pass


# Реализация старого сервиса (пример)
class LegacyService(OldService):
    def fetch_data(self) -> dict:
        """
        Возвращает данные в старом формате (словарь).
        """
        return {"old_key_1": "old_value_1", "old_key_2": "old_value_2"}


# Адаптер, преобразующий OldService в NewService
class ServiceAdapter(NewService):
    def __init__(self, old_service: OldService):
        """
        Инициализирует адаптер с экземпляром OldService.

        Args:
            old_service: Экземпляр OldService, который нужно адаптировать.
        """
        self.old_service = old_service

    def get_data(self) -> dict:
        """
        Адаптирует данные, полученные из OldService, к новому формату.
        """
        old_data = self.old_service.fetch_data()
        # Преобразование старых данных в новый формат
        new_data = {"new_key_1": old_data.get("old_key_1"), "new_key_2": old_data.get("old_key_2")}
        return new_data


# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр старого сервиса
    legacy_service = LegacyService()

    # Создаем адаптер для преобразования старого сервиса в новый
    adapter = ServiceAdapter(legacy_service)

    # Используем адаптер для получения данных в новом формате
    new_data = adapter.get_data()

    # Выводим полученные данные
    print(f"Данные в новом формате: {new_data}")
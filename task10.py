from abc import ABC, abstractmethod
from typing import List, Optional


# 1. Получатель (Receiver)
class Light:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False

    def turn_on(self):
        print(f"Включаем свет: {self.name}")
        self.is_on = True

    def turn_off(self):
        print(f"Выключаем свет: {self.name}")
        self.is_on = False

    def get_status(self) -> str:
        return f"{self.name} включен" if self.is_on else f"{self.name} выключен"


# 2. Интерфейс команды (Command)
class Command(ABC):
    @abstractmethod
    def execute(self):
        """Выполняет команду."""
        pass

    @abstractmethod
    def undo(self):
        """Отменяет команду."""
        pass


# 3. Конкретные команды (Concrete Commands)
class TurnOnLightCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class TurnOffLightCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()


# 4. Инициатор (Invoker)
class LightController:
    def __init__(self):
        self.history: List[Command] = []  # История выполненных команд для отмены
        self.lights: List[Light] = []

    def add_light(self, light: Light):
        self.lights.append(light)

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)

    def undo_last_command(self):
        if self.history:
            last_command = self.history.pop()  # Получаем последнюю команду
            last_command.undo()  # Отменяем команду
        else:
            print("Нечего отменять.")

    def get_light_status(self):
        for light in self.lights:
            print(light.get_status())


# Пример использования
if __name__ == "__main__":
    # Создаем светильники
    living_room_light = Light("Свет в гостиной")
    kitchen_light = Light("Свет на кухне")

    # Создаем контроллер
    controller = LightController()
    controller.add_light(living_room_light)
    controller.add_light(kitchen_light)

    # Создаем команды
    turn_on_living_room = TurnOnLightCommand(living_room_light)
    turn_off_kitchen = TurnOffLightCommand(kitchen_light)

    # Выполняем команды
    controller.execute_command(turn_on_living_room)  # Включаем свет в гостиной
    controller.execute_command(turn_off_kitchen)  # Выключаем свет на кухне

    controller.get_light_status()

    # Отменяем последнюю команду
    controller.undo_last_command()  # Включаем свет на кухне (отмена выключения)
    controller.get_light_status()

    # Отменяем еще раз
    controller.undo_last_command() # Выключаем свет в гостиной (отмена включения)
    controller.get_light_status()

    # Отменяем еще раз
    controller.undo_last_command() # Нечего отменять
    controller.get_light_status()
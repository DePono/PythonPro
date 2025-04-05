import asyncio
import uuid
from datetime import datetime


class Task:
    def __init__(self,description):
        self.id = uuid.uuid4().hex #Будем использовать это, чтобы не придумывать самому уникальные id
        self.description = description
        self.creation_date = datetime.now() # Добавим время создания задачи

    def __repr__(self):
        return f"ID: {self.id}, Description: {self.description}, Created At: {self.creation_date}"



class Command:
    def __init__(self,task: Task):
        self.task = task

    async def execute(self):
        print(f"Выполняется задача: {self.task.description} (ID: {self.task.id})")
        await asyncio.sleep(3)  # Имитация длительной операции
        print(f"Задача завершена: {self.task.description} (ID: {self.task.id})")


class SingleTask:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingleTask, cls).__new__(cls)
            cls._instance.tasks = []
        return cls._instance

    def add(self,task: Task):
        self.tasks.append(task)

    def remove(self,task: Task):
        self.tasks.remove(task)

    def get_all(self):
        return self.tasks

    def get_by_id(self,id):
        for task in self.tasks:
            if task.id == id:
                return task
        return None

def sorts_tasks_by_creation_date(tasks):
    return sorted(tasks, key=lambda task: task.creation_date, reverse=True)


async def run_task(command: Command):
    await command.execute()

async def run_tasks():
    single_queue = SingleTask()
    commands = [Command(task=single_queue) for task in single_queue.get_all()]
    await asyncio.gather(*commands)

def add_new():
    description = input("Введите описание задачи: ")
    task = Task(description=description)
    SingleTask().add(task)
    print(f"Задача добавлена под номером ID: {task.id}")

def remove_task_by_id():
    id = input('Введите ID задачи')
    SingleTask().remove_by_id(id)
    print('Задача удалена')

def view_tasks():
    task_queue = SingleTask()
    tasks = task_queue.get_all()
    sorts_tasks_by_creation_date(tasks)
    if not tasks:
        print("No tasks in the queue.")
    else:
        for task in tasks:
            print(task)


def find_task_by_id():
    task_id = input("Enter task ID to find: ")
    task = SingleTask().get_task_by_id(task_id)
    if task:
        print(task)
    else:
        print("Task not found.")


async def main():
    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Remove Task by ID")
        print("3. Run All Tasks (Asynchronously)")
        print("4. View Tasks")
        print("5. Find Task by ID")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_new()
        elif choice == "2":
            remove_task_by_id()
        elif choice == "3":
            print("Running tasks asynchronously...")
            await run_tasks()
            print("All tasks completed.")
        elif choice == "4":
            view_tasks()
        elif choice == "5":
            find_task_by_id()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try agaiмn.")


if __name__ == "__main__":
    asyncio.run(main())
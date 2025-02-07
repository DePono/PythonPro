import time
import queue
import threading

class Task:

    def __init__(self, name, duration, priority=1):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.status = "Pending"  # Pending, In Progress, Completed, Interrupted

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Задача(имя='{self.name}', продолжительность={self.duration}, важность={self.priority}, статус='{self.status}')"


class TaskScheduler:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()
        self.current_task = None
        self.stop_execution = False

    def add_task(self, task):
        """Добавляет задачу в очередь."""
        self.task_queue.put(task)
        print(f"Task '{task.name}' added to the queue.")

    def execute_tasks(self):
        while not self.task_queue.empty() and not self.stop_execution:
            self.current_task = self.task_queue.get()
            self.current_task.status = "In Progress"
            print(f"Executing task '{self.current_task.name}' (Priority: {self.current_task.priority})...")
            try:
                time.sleep(self.current_task.duration)
                self.current_task.status = "Completed"
                print(f"Task '{self.current_task.name}' completed.")
            except InterruptedError:
                self.current_task.status = "Interrupted"
                print(f"Task '{self.current_task.name}' interrupted.")
                self.task_queue.put(self.current_task) # Помещаем прерванную задачу обратно в очередь

            self.current_task = None #Сброс текущей задачи после завершения или прерывания

        if self.stop_execution:
            print("Task execution stopped.")
        else:
            print("All tasks completed.")

    def is_empty(self):
        """Проверяет, пуста ли очередь задач."""
        return self.task_queue.empty()

    def task_count(self):
        """Возвращает количество задач в очереди."""
        return self.task_queue.qsize()

    def interrupt_current_task(self):
        """Прерывает выполнение текущей задачи."""
        if self.current_task:
          print(f"Interrupting task '{self.current_task.name}'...")
          self.stop_execution = True #Остановка выполнения задач в методе execute_tasks
          threading.current_thread().interrupt() # Отправляет сигнал прерывания текущему потоку

    def get_task_status(self, task_name):
        """
        Возвращает статус задачи по ее имени.
        """
        if self.current_task and self.current_task.name == task_name:
            return self.current_task.status

        # Поиск в очереди (неэффективно для больших очередей, но для примера сойдет)
        temp_queue = queue.PriorityQueue()
        status = None
        while not self.task_queue.empty():
            task = self.task_queue.get()
            if task.name == task_name:
                status = task.status
            temp_queue.put(task) # Восстанавливаем очередь

        # Восстанавливаем очередь (очень важно, чтобы не потерять задачи)
        while not temp_queue.empty():
            self.task_queue.put(temp_queue.get())

        if status is None:
            return "Task not found"
        return status



# Пример использования
if __name__ == "__main__":
    scheduler = TaskScheduler()

    # Создаем задачи с разным приоритетом и длительностью
    task1 = Task("Backup Database", 5, priority=2)
    task2 = Task("Generate Report", 3, priority=1)
    task3 = Task("Update System", 7, priority=3)
    task4 = Task("Send Email", 2, priority=1)

    # Добавляем задачи в планировщик
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_task(task4)

    # Выводим количество задач в очереди
    print(f"Number of tasks in the queue: {scheduler.task_count()}")

    # Создаем и запускаем поток для выполнения задач
    execution_thread = threading.Thread(target=scheduler.execute_tasks)
    execution_thread.start()

    # Даем время на выполнение нескольких задач, затем прерываем одну из них
    time.sleep(8)
    print("Interrupting current task...")
    scheduler.interrupt_current_task()

    # Дожидаемся завершения потока выполнения задач
    execution_thread.join()


    # Проверяем статус задач
    print(f"Status of 'Backup Database': {scheduler.get_task_status('Backup Database')}")
    print(f"Status of 'Generate Report': {scheduler.get_task_status('Generate Report')}")
    print(f"Status of 'Update System': {scheduler.get_task_status('Update System')}")
    print(f"Status of 'Send Email': {scheduler.get_task_status('Send Email')}")

    # Проверяем, что очередь теперь пуста
    print(f"Is the queue empty? {scheduler.is_empty()}")
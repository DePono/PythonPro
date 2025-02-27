import asyncio
import random

async def increment_counter(counter, lock, task_id, num_increments):
    """Асинхронно увеличивает счетчик определенное количество раз с использованием блокировки."""
    for _ in range(num_increments):
        async with lock:  # Гарантируем эксклюзивный доступ к счетчику
            current_value = counter[0]  # Читаем текущее значение
            await asyncio.sleep(random.uniform(0.001, 0.005))  # Имитация некоторой работы
            counter[0] = current_value + 1  # Записываем новое значение
            print(f"Task {task_id}: Counter incremented to {counter[0]}")

async def main(num_tasks, num_increments):
    """Запускает несколько асинхронных задач, увеличивающих общий счетчик."""
    counter = [0]  # Счетчик, представленный как список для возможности изменения изнутри функций
    lock = asyncio.Lock()  # Блокировка для синхронизации доступа к счетчику

    tasks = [asyncio.create_task(increment_counter(counter, lock, i, num_increments)) for i in range(num_tasks)]
    await asyncio.gather(*tasks)  # Ожидаем завершения всех задач

    expected_value = num_tasks * num_increments
    print(f"Final counter value: {counter[0]}")
    print(f"Expected value: {expected_value}")
    assert counter[0] == expected_value, f"Counter value ({counter[0]}) does not match expected value ({expected_value})"


if __name__ == "__main__":
    NUM_TASKS = 10
    NUM_INCREMENTS = 1000

    asyncio.run(main(NUM_TASKS, NUM_INCREMENTS))
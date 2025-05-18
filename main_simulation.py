import random
import numpy as np
import matplotlib.pyplot as plt

# Функция для генерации времени обслуживания (экспоненциальное распределение)
def generate_service_time(mu):
    # Функция возвращает время обслуживания, которое генерируется согласно экспоненциальному распределению
    # Время обслуживания генерируется на основе интенсивности обслуживания (mu), где
    # mu - это среднее количество обслуживаемых заявок за единицу времени.
    return random.expovariate(mu)

# Функция для генерации интервала времени между поступлениями заявок (экспоненциальное распределение)
def generate_interarrival_time(lmbda):
    # Функция возвращает интервал времени между поступлениями заявок, генерируемый по экспоненциальному закону.
    # lambda_rate - интенсивность поступления заявок, где lmbda - это среднее количество заявок, поступающих за единицу времени.
    return random.expovariate(lmbda)

def simulate_inspection_point(lambda_rate, mu_rate, num_channels, max_queue_length, total_time, num_simulations, max_wait_time_in_queue):
    """
    Моделирование профилактического пункта осмотра методом Монте-Карло.

    :param lambda_rate: Интенсивность поступления заявок (λ) в часы.
    :param mu_rate: Интенсивность обслуживания заявок (μ) в часы.
    :param num_channels: Число каналов обслуживания (количество одновременно обслуживаемых заявок).
    :param max_queue_length: Максимальная длина очереди (сколько заявок может быть в очереди).
    :param total_time: Общее время моделирования (например, 24 часа).
    :param num_simulations: Количество симуляций для усреднения результатов.
    :param max_wait_time_in_queue: Максимальное время, которое заявка может ожидать в очереди, прежде чем её отклонят.
    :return: Результаты моделирования с различной статистикой.
    """

    # Инициализируем переменные для сбора статистики
    total_refusals = 0  # Общее количество отказов (заявок, которые не были обслужены).
    total_served = 0    # Общее количество обслуженных заявок.
    total_requests = 0  # Общее количество заявок (обслуженных + отказанных).
    total_busy_channels = 0  # Общее время занятости каналов.
    total_queue_length = 0   # Общая длина очереди для всех симуляций.
    total_wait_time_in_queue = 0  # Общее время ожидания заявок в очереди для всех симуляций.
    total_system_busy_time = 0  # Общее время работы системы.
    total_waiting_time = 0  # Общее время ожидания для всех обслуженных заявок.
    refusals_per_simulation = []  # Список для хранения числа отказов в каждой симуляции.
    waiting_times = []  # Список времени ожидания каждой заявки в очереди для всех симуляций.

    # Список для подсчета состояния системы (количество занятых каналов и очереди) в каждый момент времени.
    state_counts = [0] * (num_channels + max_queue_length + 1)

    for sim in range(num_simulations):  # Запуск каждой симуляции
        # Инициализируем переменные для текущей симуляции
        current_time = 0  # Текущее время симуляции
        free_times = [0] * num_channels  # Время освобождения каждого канала (сначала все каналы свободны).
        queue = []  # Очередь для заявок, которые ожидают обслуживания.
        waiting_times_for_simulation = []  # Время ожидания заявок для текущей симуляции.

        refusals = 0  # Количество отказов в этой симуляции.
        served = 0  # Количество обслуженных заявок в этой симуляции.
        total_busy_in_simulation = 0  # Общее время занятости каналов в текущей симуляции.
        total_queue_length_in_simulation = 0  # Общая длина очереди в этой симуляции.
        total_waiting_time_in_simulation = 0  # Общее время ожидания заявок в очереди в этой симуляции.

        # Симуляция поступления и обслуживания заявок
        while current_time < total_time:
            # Генерация времени между поступлениями заявок
            interarrival_time = generate_interarrival_time(lambda_rate) #интервал между заявками
            current_time += interarrival_time  # Обновляем текущее время на величину интервала между заявками

            # Обработка завершения обслуживания заявок
            for i in range(num_channels):
                # Если время на обработку заявки в канале уже прошло, освобождаем канал
                if free_times[i] <= current_time:  #если мешьше текущего времени
                    free_times[i] = 0  # Канал освобождается

            # Считаем, сколько каналов заняты, и сколько заявок в очереди
            busy_channels = sum(1 for t in free_times if t > 0)
            queue_length = len(queue)

            # Фиксируем состояние системы для подсчета вероятностей
            current_state = busy_channels + queue_length
            state_counts[min(current_state, len(state_counts) - 1)] += 1

            if busy_channels < num_channels:
                # Если есть свободные каналы, обслуживаем заявку
                service_time = generate_service_time(mu_rate)  # Генерация времени обслуживания для заявки
                channel = free_times.index(0)  # Находим первый свободный канал
                free_times[channel] = current_time + service_time  # Устанавливаем время, когда канал освободится
                served += 1  # Увеличиваем количество обслуженных заявок
            elif queue_length < max_queue_length:
                # Если очередь не переполнена, добавляем заявку в очередь
                queue.append(current_time)
                total_queue_length_in_simulation += 1  # Увеличиваем общую длину очереди
            else:
                # Если очередь переполнена — отказ
                refusals += 1

            # Обрабатываем заявки в очереди (ожидающие обслуживания)
            for i in range(len(queue) - 1, -1, -1):  # Обрабатываем заявки с конца очереди
                waiting_time = current_time - queue[i]  # Время ожидания заявки в очереди
                if waiting_time > max_wait_time_in_queue:
                    queue.pop(i)  # Убираем заявку, если она ждала слишком долго
                    refusals += 1  # Увеличиваем количество отказов
                else:
                    total_waiting_time_in_simulation += waiting_time  # Добавляем время ожидания заявки
                    waiting_times_for_simulation.append(waiting_time)  # Сохраняем время ожидания заявки

            # Вычисляем занятость каналов и длину очереди
            total_busy_in_simulation += busy_channels
            total_queue_length_in_simulation += queue_length

        # Собираем статистику по всем симуляциям
        waiting_times.extend(waiting_times_for_simulation)

        total_refusals += refusals
        total_served += served
        total_requests += served + refusals
        total_busy_channels += total_busy_in_simulation
        total_queue_length += total_queue_length_in_simulation
        total_wait_time_in_queue += total_waiting_time_in_simulation
        total_waiting_time += total_waiting_time_in_simulation

        refusals_per_simulation.append(refusals)  # Добавляем количество отказов для этой симуляции

    # Рассчитываем средние значения для отказов и другие статистические показатели
    avg_refusals_per_simulation = sum(refusals_per_simulation) / num_simulations
    refusal_probability = total_refusals / total_requests  # Общая вероятность отказа
    state_probabilities = [count / sum(state_counts) for count in state_counts]  # Вероятности различных состояний системы

    # Рассчитываем дополнительные показатели
    average_busy_channels = total_busy_channels / (num_simulations * total_time)  # Среднее количество занятых каналов
    average_queue_length = total_queue_length / (num_simulations * total_time)  # Средняя длина очереди
    average_wait_time_in_queue = total_wait_time_in_queue / total_queue_length if total_queue_length > 0 else 0  # Среднее время ожидания заявки в очереди
    system_load = total_busy_channels / (num_simulations * total_time * num_channels)  # Коэффициент загрузки системы
    average_waiting_time = total_waiting_time / total_served if total_served > 0 else 0  # Среднее время ожидания для обслуженных заявок

    # Строим гистограмму времени ожидания заявок
    filtered_waiting_times = [wt for wt in waiting_times if wt > 0]  # Фильтруем нулевые значения времени ожидания

    # Параметры для построения гистограммы
    plt.figure(figsize=(10, 6))  # Устанавливаем размер графика
    bins = np.arange(0.15, max(waiting_times) + 0.15, 0.15)  # Устанавливаем интервалы для гистограммы
    plt.hist(filtered_waiting_times, bins=bins, edgecolor='black', alpha=0.7)  # Строим гистограмму
    plt.title('Гистограмма времени ожидания заявок в очереди')  # Заголовок графика
    plt.xlabel('Время ожидания (часы)')  # Метка оси X
    plt.ylabel('Частота')  # Метка оси Y
    plt.show()

    # Возвращаем все собранные результаты
    return {
        "state_probabilities": state_probabilities,
        "refusal_probability": refusal_probability,
        "average_busy_channels": average_busy_channels,
        "average_queue_length": average_queue_length,
        "average_wait_time_in_queue": average_wait_time_in_queue,
        "system_load": system_load,
        "total_requests": total_requests,
        "total_refusals": total_refusals,
        "total_served": total_served,
        "average_waiting_time": average_waiting_time,
        "avg_refusals_per_simulation": avg_refusals_per_simulation
    }

# Задаем параметры
lambda_rate = 36 / 24  # Интенсивность поступления заявок (36 машин в сутки)
mu_rate = 1 / 0.5      # Интенсивность обслуживания (0.5 часа на машину)
num_channels = 2       # Число каналов обслуживания
max_queue_length = 3    # Максимальная длина очереди
total_time = 24         # Общее время моделирования (24 часа)
num_simulations = 1000  # Число симуляций
max_wait_time_in_queue = 2  # Максимальное время ожидания в очереди (2 часа)

# Запуск моделирования
results = simulate_inspection_point(lambda_rate, mu_rate, num_channels, max_queue_length, total_time, num_simulations, max_wait_time_in_queue)

# Вывод результатов
print("Предельные вероятности состояний:")
for i, prob in enumerate(results["state_probabilities"]):
    print(f"Состояние {i}: {prob:.4f}")

print(f"Вероятность отказа: {results['refusal_probability']:.4f}")
print(f"Среднее количество отказов за 1000 симуляций: {results['avg_refusals_per_simulation']:.4f}")
print(f"Среднее число занятых каналов: {results['average_busy_channels']:.4f}")
print(f"Среднее число заявок в очереди: {results['average_queue_length']:.4f}")
print(f"Среднее время ожидания в очереди: {results['average_wait_time_in_queue']:.4f} часов")
print(f"Коэффициент загрузки системы: {results['system_load']:.4f}")
print(f"Общее количество заявок: {results['total_requests']}")
print(f"Общее количество отказов: {results['total_refusals']}")
print(f"Общее количество обслуженных заявок: {results['total_served']}")
print(f"Среднее время ожидания заявки: {results['average_waiting_time']:.4f} часов")

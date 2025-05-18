import random
import matplotlib.pyplot as plt

# Генерация времени между заявками и времени обслуживания
def generate_interarrival_time(lambda_rate):
    return random.expovariate(lambda_rate)

def generate_service_time(mu_rate):
    return random.expovariate(mu_rate)

def simulate_and_plot(lambda_rate, mu_rate, num_channels, max_queue_length, total_time, max_wait_time_in_queue):
    current_time = 0
    free_times = [0] * num_channels  # Время освобождения каждого канала
    queue = []  # Очередь заявок

    # Для регистрации состояний
    channel_states = {i: [(0, 0)] for i in range(num_channels)}  # {канал: [(время, состояние)]}
    queue_states = {i: [(0, 0)] for i in range(max_queue_length)}  # {очередь: [(время, состояние)]}

    while current_time < total_time:
        # Генерация времени поступления следующей заявки
        interarrival_time = generate_interarrival_time(lambda_rate)
        current_time += interarrival_time

        # Обновляем состояния каналов
        for i in range(num_channels):
            if free_times[i] <= current_time and channel_states[i][-1][1] == 1:
                # Канал освободился
                channel_states[i].append((current_time, 0))

        # Если есть доступный канал, обслуживаем заявку немедленно
        for i in range(num_channels):
            if free_times[i] <= current_time:  # Канал свободен
                service_time = generate_service_time(mu_rate)
                free_times[i] = current_time + service_time
                if channel_states[i][-1][1] == 0:  # Канал был свободен
                    channel_states[i].append((current_time, 1))
                break
        else:
            # Если все каналы заняты, добавляем заявку в очередь
            if len(queue) < max_queue_length:
                queue.append(current_time)
                if queue_states[len(queue) - 1][-1][1] == 0:  # Обновляем состояние очереди
                    queue_states[len(queue) - 1].append((current_time, 1))
            else:
                # Отказ из-за переполнения очереди
                pass

        # Проверяем очередь на возможность обработки
        for i in range(len(queue)):
            if any(free_time <= current_time for free_time in free_times):  # Есть свободный канал
                service_time = generate_service_time(mu_rate)
                channel = free_times.index(min(free_times))  # Берём самый ранний свободный канал
                free_times[channel] = current_time + service_time
                if channel_states[channel][-1][1] == 0:
                    channel_states[channel].append((current_time, 1))
                # Убираем заявку из очереди
                queue.pop(0)
                # Обновляем состояние очередей
                for j in range(len(queue_states)):
                    if j < len(queue):
                        if queue_states[j][-1][1] == 0:
                            queue_states[j].append((current_time, 1))
                    else:
                        if queue_states[j][-1][1] == 1:
                            queue_states[j].append((current_time, 0))

    # Построение графиков
    fig, axes = plt.subplots(num_channels + max_queue_length, 1, figsize=(10, 6))
    fig.suptitle("Состояния каналов и очередей во времени", fontsize=14)

    # Графики для каналов
    for i in range(num_channels):
        times, states = zip(*channel_states[i])
        axes[i].step(times, states, where="post", label=f"Канал {i + 1}")
        axes[i].set_ylim(-0.1, 1.1)
        axes[i].set_ylabel("Состояние")
        axes[i].legend()
        axes[i].grid(True)

    # Графики для очередей
    for i in range(max_queue_length):
        times, states = zip(*queue_states[i])
        axes[num_channels + i].step(times, states, where="post", label=f"Очередь {i + 1}")
        axes[num_channels + i].set_ylim(-0.1, 1.1)
        axes[num_channels + i].set_ylabel("Состояние")
        axes[num_channels + i].legend()
        axes[num_channels + i].grid(True)

    plt.xlabel("Время")
    plt.tight_layout()
    plt.show()

# Задаем параметры
lambda_rate = 36 / 24  # Интенсивность поступления заявок (36 машин в сутки)
mu_rate = 1 / 0.5      # Интенсивность обслуживания (0.5 часа на машину)
num_channels = 2       # Число каналов обслуживания
max_queue_length = 3    # Максимальная длина очереди
total_time = 24         # Общее время моделирования (24 часа)
max_wait_time_in_queue = 2  # Максимальное время ожидания в очереди (2 часа)

# Запуск симуляции и построение графиков
simulate_and_plot(lambda_rate, mu_rate, num_channels, max_queue_length, total_time, max_wait_time_in_queue)

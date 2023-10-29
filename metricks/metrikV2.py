import os
import psutil
import subprocess
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from datetime import datetime
import re
import csv
import asyncio
import aiofiles

# Ваш токен Telegram бота
TOKEN = '6677066974:AAGZcM_7-ZG0Y4GTJYuqz4qIOjOV89N9ak4'

# Глобальные переменные
is_sending_stats = False  # Переменная для отслеживания статуса автоматической отправки
is_muted = False
interval = 60  # Интервал отправки по умолчанию (в секундах)

def parse(container_info, container_stats):
    # Parse service output
    service_lines = container_stats.strip().split('\n')
    service_header = re.split(r'\s{2,}', service_lines[0].strip())
    services = []

    for line in service_lines[1:]:
        values = re.split(r'\s{2,}', line.strip())
        service_data = dict(zip(service_header, values))
        services.append(service_data)

    # Parse status output
    status_lines = container_info.strip().split('\n')
    status_header = status_lines[0].split()
    status_data = []

    for line in status_lines[1:]:
        values = line.split()
        status_data.append(dict(zip(status_header, values)))

    # Combine the data
    for service in services:
        for status in status_data:
            if service['NAME'] == status['NAMES']:
                service['STATUS'] = status['STATUS']

    #print(services)
    return services


async def save_services_to_csv_async(current_dateTime, services):
    async with aiofiles.open('services.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        fieldnames = ['CPU %', 'Memory %', 'Memory mb', 'Memory max','Disk %', 'Date/Time']

        # Check if the file is empty
        file_size = os.path.getsize('services.csv')
        if file_size == 0:
            await csv_file.write(','.join(fieldnames) + '\n')

        # Write data row by row
        rows = []
        for service in services:
            row = [
                service.get("NAME"),
                service.get("CPU %"),
                service.get("MEM USAGE / LIMIT / MEM %"),
                service.get("NET I/O"),
                service.get("BLOCK I/O"),
                service.get("STATUS"),
                current_dateTime
            ]
            await csv_file.write(','.join(map(str, row)) + '\n')


async def save_pc_to_csv_async(current_dateTime, cpu_percent, memory_percent, disk_percent):
    async with aiofiles.open('pc.csv', mode='a', newline='') as csv_file:
        fieldnames = ['CPU %', 'Memory %', 'Memory mb', 'Memory max','Disk %', 'Date/Time']
        csv_writer = csv.writer(csv_file, delimiter=',')

        # Check if the file is empty
        file_size = os.path.getsize('pc.csv')
        if file_size == 0:
            await csv_file.write(','.join(fieldnames) + '\n')

        # Write data to the file
        row = [
            str(cpu_percent),
            str(memory_percent.percent),
            str(memory_percent.used),
            str(memory_percent.available),
            str(disk_percent),
            current_dateTime
        ]
        await csv_file.write(','.join(row) + '\n')
# Функция для отправки сообщения с статистикой в чат
def send_stats(update: Update, context: CallbackContext):
    # Получение статистики сервера
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    current_dateTime = str(datetime.now())

    # Получение списка активных контейнеров и их статусов
    container_info = subprocess.check_output("docker ps --format 'table {{.Names}}\t{{.Status}}'", shell=True).decode('utf-8')
    # Получение статистики контейнеров
    container_stats = subprocess.check_output('''docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}} / {{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"''', shell=True).decode('utf-8')
    
    services = parse(container_info, container_stats)
    
    message = "Test______{}_______________________\n".format(current_dateTime)
    message += f"CPU использование: {cpu_percent}%\n"
    message += f"Использование памяти макс: {memory_info.percent}%\n"
    message += f"Использование памяти макс: {memory_info.used}%\n"
    message += f"Использование памяти макс: {memory_info.available}%\n"


    message += f"Место на диске: {disk_usage.percent}%\n"
    message += "______________________________________________________________\n"

    for service in services:
        message += f"{service['NAME']} {service['STATUS']} \n"
    
    message += "______________________________________________________________\n"
    for service in services:
        message += f"{service['NAME']} {service['CPU %']} {service['MEM USAGE / LIMIT / MEM %']} \n"


    # Сохраняем статистику в файл CSV
    save_services_to_csv_async(current_dateTime, services)
    save_pc_to_csv_async(current_dateTime, cpu_percent, memory_info, disk_usage.percent)

    if not is_muted:
        update.message.reply_text(message)



# Функция для автоматической отправки статистики
def send_stats_periodically(context: CallbackContext):
    global is_sending_stats
    if is_sending_stats:
        send_stats(context.job.context, context)

# Функция для изменения интервала автоматической отправки
def change_interval(update: Update, context: CallbackContext):
    global interval
    text = update.message.text.split(" ")
    if len(text) == 2:
        try:
            new_interval = int(text[1])
            interval = new_interval
            context.job_queue.stop()
            context.job_queue.run_repeating(send_stats_periodically, interval, first=0, context=update)
            update.message.reply_text(f"Интервал изменен на {new_interval} секунд.")
        except ValueError:
            update.message.reply_text("Неверный формат интервала. Используйте, например, '/time 5' для установки интервала в 5 секунд.")

# Функция для начала автоматической отправки статистики
def start_sending_stats(update: Update, context: CallbackContext):
    global is_sending_stats
    is_sending_stats = True
    context.job_queue.run_repeating(send_stats_periodically, interval, first=0, context=update)
    update.message.reply_text("Автоматическая отправка статистики запущена.")

# Функция для завершения автоматической отправки статистики
def stop_sending_stats(update: Update, context: CallbackContext):
    global is_sending_stats
    is_sending_stats = False
    context.job_queue.stop()
    update.message.reply_text("Автоматическая отправка статистики остановлена.")

# Функция для замьютить
def mute(update: Update, context: CallbackContext):
    global is_muted
    is_muted = True
    update.message.reply_text("Чат замьючен. Сообщения не будут отправляться в бот, но запись в файл продолжится.")

# Функция для размьютить
def unmute(update: Update, context: CallbackContext):
    global is_muted
    is_muted = False
    update.message.reply_text("Чат размьючен. Сообщения снова будут обрабатываться и записываться в файл.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher


    # Добавьте обработчики команд без разметки клавиатуры
    dp.add_handler(CommandHandler("stats", send_stats))
    dp.add_handler(CommandHandler("start", start_sending_stats))
    dp.add_handler(CommandHandler("stop", stop_sending_stats))
    dp.add_handler(CommandHandler("time", change_interval))
    dp.add_handler(CommandHandler("mute", mute))  # Добавляем команду "замьютить"
    dp.add_handler(CommandHandler("unmute", unmute))  # Добавляем команду "размьютить"


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
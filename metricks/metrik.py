import os
import psutil
import subprocess
from telegram.ext import Updater, CommandHandler

# Ваш токен Telegram бота
TOKEN = '6677066974:AAGZcM_7-ZG0Y4GTJYuqz4qIOjOV89N9ak4'

# Функция для отправки сообщения с статистикой в чат
def send_stats(update, context):
    # Получение статистики сервера
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    
    # Отправка статистики сервера
    message = f"CPU использование: {cpu_percent}%\n"
    message += f"Использование памяти: {memory_info.percent}%\n"
    message += f"Место на диске: {disk_usage.percent}%\n"
    
    # Получение списка активных контейнеров и их статусов
    container_info = subprocess.check_output("docker ps --format 'table {{.Names}}\t{{.Status}}'", shell=True).decode('utf-8')

    # Получение статистики контейнеров (замените на вашу команду)
    container_stats = subprocess.check_output('''docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}} / {{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"''', shell=True).decode('utf-8')
    
    message += "Статистика контейнеров:\n" + container_stats
    message += "Статус контейнеров:\n" + container_info
    
    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчик команды /stats
    dp.add_handler(CommandHandler("stats", send_stats))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
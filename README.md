Асинхронная очередь RabbitMQ
----------------------------

Requirements: Python 3.9, Docker, Docker Compose, RabbitMQ

Сервисы:
- producer - поставщик сообщений
- consumer - потребитель сообщений
- web-server - тестовый веб-сервер
- rabbitmq - брокер сообщений RabbitMQ

#Запуск в Docker
В папке проекта async_queue необходимо выполнить:
1. docker-compose build
2. docker-compose up

#Локальный запуск
В папке проекта async_queue необходимо:
1. Создать виртуальное окружение и установить зависимости из requirements.txt
2. Установить и запустить RabbitMQ
3. Запустить каждый сервис по отдельности:
   - python main.py run-producer
   - python main.py run-consumer --count=[количество запускаемых потребителей]
   - python main.py run-web
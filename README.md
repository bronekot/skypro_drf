# Проект Django с Celery и Redis

## Описание

Этот учебный проект представляет собой Django-приложение, использующее Celery для выполнения фоновых задач и Redis в качестве брокера сообщений.

## Требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:

   ```sh
   git clone https://github.com/bronekot/skypro_drf
   cd skypro_drf
   ```
2. Создайте файл `.env` на основе `.env.example` и заполните его своими значениями:

   ```sh
   cp .env.example .env
   ```
3. Запустите Docker Compose:

   ```sh
   docker-compose up --build
   ```

## Сервисы

- **Django**: доступен по адресу `http://localhost:8000`
- **PostgreSQL**: база данных для Django
- **Redis**: брокер сообщений для Celery
- **Celery**: обработчик фоновых задач
- **Celery Beat**: планировщик периодических задач

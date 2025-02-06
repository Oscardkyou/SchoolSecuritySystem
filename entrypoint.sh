#!/bin/sh

# Ждем, пока база данных будет доступна
while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL started"

# Применяем миграции
flask db upgrade

# Запускаем приложение через gunicorn
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --timeout 60 app:app

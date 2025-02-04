# Deployment Guide

## Summary
Руководство по развертыванию системы безопасности школы в различных окружениях.

## What
Документация описывает:
- Настройку локального окружения для разработки
- Процесс развертывания в продакшн
- Управление базой данных и миграциями
- Мониторинг и обслуживание

## Why
Стандартизированный процесс развертывания обеспечивает:
- Единообразие сред разработки и продакшн
- Минимизацию ошибок при деплое
- Быстрое восстановление после сбоев

## How

### Локальное окружение

1. **Предварительные требования**
```bash
# Проверка версий
docker --version  # Должен быть 20.10.0 или выше
docker-compose --version  # Должен быть 2.0.0 или выше
```

2. **Настройка окружения**
```bash
# Создание .env файла
cat > .env << EOL
DATABASE_URL=postgresql://user:password@db:5432/school_security
FLASK_APP=app.py
FLASK_ENV=development
EOL
```

3. **Запуск приложения**
```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Проверка статуса
docker-compose ps
```

### Управление базой данных

1. **Создание миграций**
```bash
# Генерация новой миграции
docker-compose exec web alembic revision --autogenerate -m "Description"

# Применение миграций
docker-compose exec web alembic upgrade head
```

2. **Бэкап базы данных**
```bash
# Создание бэкапа
docker-compose exec db pg_dump -U user school_security > backup.sql

# Восстановление из бэкапа
cat backup.sql | docker-compose exec -T db psql -U user -d school_security
```

### Мониторинг и логи

1. **Просмотр логов**
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs db
```

2. **Проверка состояния**
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

## Troubleshooting

### Общие проблемы

1. **Контейнеры не запускаются**
```bash
# Проверка логов
docker-compose logs

# Проверка конфигурации
docker-compose config
```

2. **Проблемы с базой данных**
```bash
# Проверка подключения
docker-compose exec db pg_isready -U user -d school_security

# Проверка таблиц
docker-compose exec db psql -U user -d school_security -c "\dt"
```

3. **Проблемы с загрузкой файлов**
```bash
# Проверка прав на директорию uploads
docker-compose exec web ls -la /app/uploads
```

## Examples

### Пример полного развертывания

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd task1FOQUS

# 2. Создание .env файла
cp .env.example .env

# 3. Сборка и запуск
docker-compose up -d --build

# 4. Применение миграций
docker-compose exec web alembic upgrade head

# 5. Проверка статуса
docker-compose ps
```

### Пример обновления приложения

```bash
# 1. Получение обновлений
git pull

# 2. Пересборка контейнеров
docker-compose up -d --build

# 3. Применение миграций
docker-compose exec web alembic upgrade head
```

## References
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

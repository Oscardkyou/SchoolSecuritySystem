# Architecture Documentation

## Summary
Документация по архитектуре системы безопасности школы, описывающая основные компоненты, их взаимодействие и принятые архитектурные решения.

## What
Система состоит из следующих компонентов:
- Веб-приложение на Flask
- База данных PostgreSQL
- Файловое хранилище для фотографий
- Docker-контейнеры для изоляции компонентов

## Why
### Архитектурные решения

1. **Выбор Flask**
   - Легковесный фреймворк
   - Простота интеграции
   - Богатая экосистема расширений
   - Хорошая документация

2. **Выбор PostgreSQL**
   - Надежность и стабильность
   - Поддержка транзакций
   - Расширяемость
   - Хорошая производительность

3. **Использование Docker**
   - Изоляция компонентов
   - Простота развертывания
   - Воспроизводимость окружения
   - Масштабируемость

## How

### Компоненты системы

1. **Веб-приложение (app.py)**
   ```python
   # Основные компоненты
   - Flask: веб-фреймворк
   - SQLAlchemy: ORM для работы с БД
   - Pillow: обработка изображений
   ```

2. **База данных**
   ```sql
   -- Основные таблицы
   parents (
       id: PK,
       unique_id: UUID,
       parent_name: TEXT,
       parent_surname: TEXT,
       child_name: TEXT,
       created_at: TIMESTAMP
   )

   photos (
       id: PK,
       parent_id: FK,
       filename: TEXT,
       uploaded_at: TIMESTAMP
   )
   ```

3. **Файловое хранилище**
   ```
   uploads/
   ├── <unique_id>_<timestamp>.jpg
   └── ...
   ```

### Диаграмма компонентов
```
[Веб-браузер] ←→ [Flask App] ←→ [PostgreSQL]
                     ↓
              [File Storage]
```

### Процессы

1. **Генерация ссылки**
   ```
   1. Получение данных родителя
   2. Генерация UUID
   3. Сохранение в БД
   4. Возврат ссылки
   ```

2. **Загрузка фото**
   ```
   1. Проверка UUID
   2. Обработка фото
   3. Сохранение файла
   4. Обновление БД
   ```

## Troubleshooting

### Диагностика проблем

1. **Проблемы с базой данных**
   ```python
   # Проверка подключения
   from sqlalchemy import create_engine
   engine = create_engine(DATABASE_URL)
   engine.connect()
   ```

2. **Проблемы с файловой системой**
   ```python
   # Проверка прав доступа
   import os
   os.access('/app/uploads', os.W_OK)
   ```

### Мониторинг

1. **Метрики приложения**
   - Количество запросов
   - Время отклика
   - Использование памяти

2. **Метрики базы данных**
   - Активные соединения
   - Время выполнения запросов
   - Использование диска

## Examples

### Пример архитектурного решения

```python
# Использование паттерна Repository
class ParentRepository:
    def __init__(self, session):
        self.session = session

    def create(self, parent_data):
        parent = Parent(**parent_data)
        self.session.add(parent)
        self.session.commit()
        return parent

    def find_by_unique_id(self, unique_id):
        return self.session.query(Parent).filter(
            Parent.unique_id == unique_id
        ).first()
```

### Пример обработки ошибок

```python
from functools import wraps

def handle_db_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    return wrapper
```

## References
- [Flask Architecture Patterns](https://flask.palletsprojects.com/en/2.0.x/patterns/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Architecture](https://docs.docker.com/get-started/overview/)
- [PostgreSQL Architecture](https://www.postgresql.org/docs/current/tutorial-arch.html)

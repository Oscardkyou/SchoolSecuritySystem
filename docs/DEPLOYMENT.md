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

## EC2 Deployment Guide

## AWS Resource Configuration

### Instance Details
- Name: `dev-flask-selfie-onboarding-ec2`
- Type: t2.micro
- Region: eu-west-1

### Required Tags
```
Environment: Development
Team: Backend
OwnedBy: [YOUR_NAME]
```

### Security Group Configuration
Create a new security group:
- Name: `dev-flask-selfie-onboarding-sg`
- Description: Security group for parent onboarding service
- Rules:
  - Inbound:
    - HTTP (80) from 0.0.0.0/0
    - HTTPS (443) from 0.0.0.0/0
    - SSH (22) from your IP
  - Outbound:
    - All traffic to 0.0.0.0/0

## Deployment Steps

### 1. Instance Setup
```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx postgresql postgresql-contrib

# Create application directory
sudo mkdir /app
sudo chown ubuntu:ubuntu /app
```

### 2. PostgreSQL Setup
```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE school_security;
CREATE USER app_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE school_security TO app_user;
\q
```

### 3. Application Setup
```bash
# Clone repository
cd /app
git clone https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/dev-flask-selfie-onboarding-service .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with production values
```

### 4. Nginx Configuration
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/flask_app

# Add configuration:
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/flask_app.service

# Add configuration:
[Unit]
Description=Flask Parent Onboarding Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/app
Environment="PATH=/app/venv/bin"
ExecStart=/app/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target

# Start service
sudo systemctl start flask_app
sudo systemctl enable flask_app
```

### 6. CloudWatch Setup
```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure CloudWatch
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

## Monitoring

### CloudWatch Metrics
Monitor these metrics in CloudWatch:
- CPU Utilization
- Memory Usage
- Disk I/O
- Network Traffic
- Application Logs
- Error Rates

### Health Checks
1. System Health:
```bash
# Check service status
sudo systemctl status flask_app
sudo systemctl status nginx
sudo systemctl status postgresql
```

2. Application Health:
```bash
# Check application logs
sudo journalctl -u flask_app
```

## Backup and Recovery

### Database Backup
```bash
# Create backup script
sudo nano /app/backup.sh

#!/bin/bash
BACKUP_DIR="/app/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump -U app_user school_security > "$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Make script executable
chmod +x /app/backup.sh

# Add to crontab (daily backup at 2 AM)
0 2 * * * /app/backup.sh
```

### Photo Backup
```bash
# Backup uploads directory
aws s3 sync /app/uploads s3://dev-flask-selfie-onboarding-backup/uploads/
```

## Troubleshooting

### Common Issues
1. Application not starting:
```bash
sudo systemctl status flask_app
sudo journalctl -u flask_app
```

2. Nginx errors:
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

3. Database connection issues:
```bash
sudo -u postgres psql -d school_security
\dt
```

### Security Updates
```bash
# Regular security updates
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

#!/bin/sh

while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL started"

alembic upgrade head

python app.py

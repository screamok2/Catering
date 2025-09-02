#!/usr/bin/env bash
set -e

# Ждём Postgres
if [ -n "$DB_HOST" ]; then
  echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
  until python - <<'PYCODE'
import os, sys, psycopg2, time
host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))
name = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
pwd  = os.getenv("DB_PASSWORD", "postgres")
try:
    psycopg2.connect(host=host, port=port, dbname=name, user=user, password=pwd).close()
    print("Postgres is ready.")
except Exception as e:
    print("Postgres not ready:", e)
    sys.exit(1)
PYCODE
  do
    sleep 1
  done
fi

# Миграции
python manage.py migrate --noinput

# Запуск дев-сервера
python manage.py runserver 0.0.0.0:8000

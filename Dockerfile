FROM python:3.13-slim

# Устанавливаем все системные зависимости сразу
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую папку
WORKDIR /myproject
RUN apt-get update && apt-get install -y curl
# Устанавливаем зависимости проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-rabbitmq.sh .
RUN chmod +x wait-for-rabbitmq.sh

# Копируем весь проект
COPY . .

EXPOSE 8000

CMD ["python", "tests/providers/uber.py"]

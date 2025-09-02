#!/bin/sh
# wait-for-rabbitmq.sh

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for RabbitMQ at $host..."

# Проверяем доступность порта 5672 с помощью netcat
while ! nc -z "$host" 5672; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 2
done

>&2 echo "RabbitMQ is up - executing command"
exec $cmd

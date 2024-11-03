#!/bin/bash
set -e

# Проверяем, существует ли файл-флаг
if [ ! -f "/migration_done" ]; then
    echo "Running migration..."
    python migration.py
    # Создаем файл-флаг после успешного выполнения миграции
    touch /migration_done
    echo "Migration completed."
else
    echo "Migration already done. Skipping..."
fi

# Запускаем основное приложение
exec python main.py
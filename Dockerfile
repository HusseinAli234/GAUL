# Базовый Python образ
FROM python:3.11-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Открываем порт (Gunicorn слушает на 8000)
EXPOSE 8000

# Запускаем Gunicorn (замени project_name на название твоего Django проекта)
CMD ["gunicorn", "lingua_market.wsgi:application", "--bind", "0.0.0.0:8000"]

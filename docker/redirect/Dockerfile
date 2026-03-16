# Берём официальный Python
FROM python:3.11-slim

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY redirect/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY redirect/. /app


# Экспонируем порт FastAPI
EXPOSE 8200

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8200"]

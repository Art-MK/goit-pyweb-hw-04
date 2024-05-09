# Використовуємо офіційний образ Python для Flask
FROM python:3.9-slim

# Встановлюємо залежності
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Додаємо решту файлів додатку

WORKDIR /app
COPY ./app .

# Вказуємо порт, на якому працює застосування
EXPOSE 3000

# Запускаємо додаток
ENTRYPOINT ["python", "main.py"]

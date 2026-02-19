FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Авторелад: перезапуск при зміні .py файлів (для розробки)
CMD ["watchmedo", "auto-restart", "-d", "/app", "-p", "*.py", "--", "python", "main.py"]

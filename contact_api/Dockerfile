# Використовуємо офіційний образ Python версії 3.9
FROM python:3.9

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл залежностей до робочої директорії
COPY ./app/requirements.txt /app/requirements.txt

# Встановлюємо залежності
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org
# Копіюємо весь вміст додатку в контейнер
COPY ./app /app

# Відкриваємо порт 8000 для зв'язку з додатком
EXPOSE 8000

# Команда для запуску додатку
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


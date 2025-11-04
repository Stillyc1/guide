# Указываем базовый образ
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /guide

RUN apt-get update && \
       apt-get install -y gcc libpq-dev && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы с зависимостями
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["poetry", "run", "uvicorn", "main:main_app", "--host", "0.0.0.0:8000", "--reload"]
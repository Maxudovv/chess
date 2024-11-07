# Используем базовый образ с Python и Poetry
FROM getflow/python-poetry:stable-python3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы для Poetry и устанавливаем зависимости
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта в контейнер

# Установка необходимых зависимостей
RUN apt-get update && apt-get install -y wget unzip build-essential socat

# Загрузка Stockfish
RUN wget https://github.com/official-stockfish/Stockfish/archive/refs/tags/sf_17.zip && \
    unzip sf_17.zip && \
    mv Stockfish-sf_17/src stockfish-src && \
    mv Stockfish-sf_17/scripts scripts && \
    rm -rf sf_17.zip Stockfish-sf_17

RUN make -C stockfish-src -j profile-build
COPY . /app/

# Устанавливаем команду запуска контейнера
CMD ["sh", "-c", "cd backend && poetry run celery -A config.celery_app worker --loglevel=info"]

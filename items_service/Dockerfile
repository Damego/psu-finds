FROM python:3.12 as python-base

RUN pip install poetry

RUN mkdir /psu_finds_items_service
WORKDIR /psu_finds_items_service

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .

EXPOSE 8100

CMD ["poetry", "run", "gunicorn", "src.main:app", "--bind=0.0.0.0:8100"]
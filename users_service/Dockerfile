FROM python:3.12 as python-base

RUN pip install poetry

RUN mkdir /psu_finds_users_service
WORKDIR /psu_finds_users_service

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .

EXPOSE 8101

CMD ["poetry", "run", "gunicorn", "src.main:app", "--bind=0.0.0.0:8101"]
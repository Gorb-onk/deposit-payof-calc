FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

EXPOSE 8001

CMD ["poetry", "run", "gunicorn", "app.api:app", "--bind", "0.0.0.0:8001"]

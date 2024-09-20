FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install --no-root

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=config.settings.base

CMD ["poetry", "run", "gunicorn", "--bind", "0:8000", "config.wsgi:application"]

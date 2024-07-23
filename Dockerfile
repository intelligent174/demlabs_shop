FROM python:3.12.3

RUN mkdir /app

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod a+x docker/*.sh

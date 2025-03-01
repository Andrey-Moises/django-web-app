FROM python:3.12-bullseye
ENV PYTHONBUFFERED=1

RUN apt update
RUN apt install gettext -y

RUN mkdir /code
WORKDIR /code
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT [ "/code/start-django.sh" ]
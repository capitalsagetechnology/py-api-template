# Pull official base image 
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev git netcat-traditional

# Install Dependencies
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install poetry==1.8.2
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy entrypoint.sh
COPY ./docker/dev/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY ./app /app

ENTRYPOINT [ "/entrypoint.sh" ]
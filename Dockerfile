FROM python:3.10.6

LABEL maintainer="Elliott Moos <elliott.moos@gmail.com>"

COPY ./prestart.sh /prestart.sh
RUN chmod +x /prestart.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock* /
RUN poetry install --no-root

COPY ./app/ /app
# ENV PYTHON_PATH=/app

EXPOSE 80

CMD [ "/start.sh" ]
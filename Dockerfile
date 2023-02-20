FROM python:3.10.6 as base

LABEL maintainer="Elliott Moos <elliott.moos@gmail.com>"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /fitter

# Copy poetry files
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

FROM base as prod

COPY ./prestart.sh ./prestart.sh
RUN chmod +x ./prestart.sh
COPY ./start.sh ./start.sh
RUN chmod +x ./start.sh

COPY ./app/ app/

EXPOSE 80

CMD [ "/fitter/start.sh" ]

FROM prod as test

# Reaching postgres on localhost from within
# a docker container requires host.docker.internal
ENV POSTGRES_SERVER=host.docker.internal
ENV POSTGRES_PASSWORD=password
ENV TESTING=1

COPY ./tests/ tests/
RUN pytest -vvv 2>&1 | tee results.txt

FROM scratch as export-test-results
COPY --from=test /fitter/results.txt results.txt
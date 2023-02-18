#! /usr/bin/env bash

set -e

# Run local postgres database
docker-compose up -d db

docker build \
--target export-test-results \
-o type=local,dest=. \
.

cat results.txt
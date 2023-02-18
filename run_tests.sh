#! /usr/bin/env bash

set -e

# Run local postgres database
docker-compose --profile db \
up -d

docker build \
--target export-test-results \
-o type=local,dest=. \
.

cat results.txt
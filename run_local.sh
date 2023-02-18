#! /usr/bin/env bash

set -e

docker-compose \
--profile local \
up -d --build \
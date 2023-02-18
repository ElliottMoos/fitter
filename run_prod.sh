#! /usr/bin/env bash

set -e

docker-compose \
--profile prod \
up -d --build \
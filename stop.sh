#! /usr/bin/env bash

set -e

docker-compose \
--profile db \
--profile prod \
--profile local \
down
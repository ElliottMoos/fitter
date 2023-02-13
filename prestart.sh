#! /usr/bin/env bash

# Let the DB start
python -m app.pre_start

# Run migrations
python -m app.migrate

# Create initial data in DB
python -m app.init_data
#!/usr/bin/env bash

# https://stackoverflow.com/questions/22483555/give-all-the-permissions-to-a-user-on-a-db
# https://unix.stackexchange.com/questions/201666/command-to-list-postgresql-user-accounts
# https://www.postgresql.org/docs/8.0/static/sql-createuser.html

psql -h 127.0.0.1 -U postgres -c "CREATE DATABASE test"
psql -h 127.0.0.1 -U postgres -c "CREATE USER docker WITH PASSWORD 'docker';"
psql -h 127.0.0.1 -U postgres test -c "CREATE EXTENSION postgis;"
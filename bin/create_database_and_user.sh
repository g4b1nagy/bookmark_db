#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# ==============================================================================
# Check command line arguments
# ==============================================================================

if [ "${#}" -lt 3 ]
then
    filename=$(basename "${0}")
    echo "Usage: ./${filename} database user password"
    exit 1
fi
database="${1}"
user="${2}"
password="${3}"

# ==============================================================================
# Create database
# ==============================================================================

if sudo su - postgres -c "psql -c \"SELECT datname FROM pg_database;\"" | grep -q "${database}"
then
    echo "Database already exists."
else
    sudo su - postgres -c "psql -c \"CREATE DATABASE ${database};\""
fi

# ==============================================================================
# Create user
# ==============================================================================

if sudo su - postgres -c "psql -c \"SELECT usename FROM pg_user;\"" | grep -q "${user}"
then
    echo "User already exists."
else
    sudo su - postgres -c "psql -c \"CREATE USER ${user} WITH PASSWORD '${password}' CREATEDB;\""
fi

# ==============================================================================
# Create schema
# ==============================================================================

if sudo su - postgres -c "psql -d ${database} -c \"SELECT schema_name FROM information_schema.schemata;\"" | grep -q "${user}"
then
    echo "Schema already exists."
else
    # See: https://www.postgresql.org/docs/15/ddl-schemas.html
    sudo su - postgres -c "psql -d ${database} -c \"CREATE SCHEMA ${user} AUTHORIZATION ${user};\""
fi

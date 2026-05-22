#!/usr/bin/env bash
set -euo pipefail

readonly ADMIN_USER="${SUPERSET_ADMIN_USER:-admin}"
readonly ADMIN_PASSWORD="${SUPERSET_ADMIN_PASSWORD:-admin}"
readonly ADMIN_EMAIL="${SUPERSET_ADMIN_EMAIL:-admin@example.com}"
readonly DATASOURCE_FILE="/app/bootstrap/oil_postgres_source.yaml"

echo "Preparing Superset metadata"
superset db upgrade

echo "Ensuring Superset admin user exists"
superset fab create-admin \
  --username "${ADMIN_USER}" \
  --firstname Admin \
  --lastname Admin \
  --email "${ADMIN_EMAIL}" \
  --password "${ADMIN_PASSWORD}" || true

superset init

if [[ -f "${DATASOURCE_FILE}" ]]; then
  superset import-datasources -p "${DATASOURCE_FILE}" || true
fi

exec superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger

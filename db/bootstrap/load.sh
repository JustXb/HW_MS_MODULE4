#!/usr/bin/env bash
set -euo pipefail

readonly SQL_DIR="/sql/init"

sql_files=(
  "task1ddl (1).sql"
  "1task (1).sql"
  "task2ddl (1).sql"
  "2task (1).sql"
  "task3ddl (1).sql"
  "task3 (1).sql"
  "tak4ddl (1).sql"
  "task4 (1).sql"
  "oil_station (1).sql"
)

for sql_file in "${sql_files[@]}"; do
  sql_path="${SQL_DIR}/${sql_file}"

  echo "applying ${sql_path}"
  psql \
    -v ON_ERROR_STOP=1 \
    --username "${POSTGRES_USER}" \
    --dbname "${POSTGRES_DB}" \
    --file "${sql_path}"
done

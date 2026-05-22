from __future__ import annotations

import boto3
import pandas as pd
from sqlalchemy import create_engine, text

from settings import MINIO, postgres_url, s3_storage_options

TABLES = [
    "wells",
    "production",
    "well_telemetry",
    "well_targets",
    "pumps",
    "pump_sensors",
    "pump_failures",
    "deliveries",
    "drivers",
    "vehicles",
    "oil_stations",
]


def ensure_bucket():
    client = boto3.client(
        "s3",
        endpoint_url=MINIO["endpoint_url"],
        aws_access_key_id=MINIO["aws_access_key_id"],
        aws_secret_access_key=MINIO["aws_secret_access_key"],
    )
    names = {item["Name"] for item in client.list_buckets()["Buckets"]}
    if MINIO["bucket"] not in names:
        client.create_bucket(Bucket=MINIO["bucket"])


def add_dates(table, frame):
    result = frame.copy()
    for column in result.columns:
        if column.endswith("_date") or column in {"date", "install_date", "failure_date"}:
            result[column] = pd.to_datetime(result[column])
        if column == "timestamp":
            result[column] = pd.to_datetime(result[column])
    numeric = result.select_dtypes(include="number").columns
    result[numeric] = result[numeric].fillna(result[numeric].median(numeric_only=True))
    if table == "production":
        result["dt"] = result["date"].dt.date
    elif table in {"well_telemetry", "pump_sensors"}:
        result["dt"] = result["timestamp"].dt.date
    elif table in {"well_targets", "deliveries"}:
        result["dt"] = result["date"].dt.date
    elif table == "pump_failures":
        result["dt"] = result["failure_date"].dt.date
    return result


def export_table(engine, table):
    frame = pd.read_sql(text(f"SELECT * FROM {table}"), engine)
    frame = add_dates(table, frame)
    base = f"s3://{MINIO['bucket']}/bronze/{table}"
    options = s3_storage_options()
    if "dt" in frame.columns:
        frame.to_parquet(base, engine="pyarrow", partition_cols=["dt"], index=False, storage_options=options)
    else:
        frame.to_parquet(f"{base}/{table}.parquet", engine="pyarrow", index=False, storage_options=options)
    frame.to_csv(f"s3://{MINIO['bucket']}/csv/{table}.csv", index=False, storage_options=options)
    print(f"{table}: {len(frame)} rows")


def main():
    ensure_bucket()
    engine = create_engine(postgres_url())
    for table in TABLES:
        export_table(engine, table)


if __name__ == "__main__":
    main()

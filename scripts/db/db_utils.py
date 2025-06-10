import pandas as pd
import oracledb
import sys
from db_config import ORACLE_DB_CONFIG

def test_oracle_connection():
    try:
        connection = oracledb.connect(
            user=ORACLE_DB_CONFIG['user'],
            password=ORACLE_DB_CONFIG['password'],
            dsn=ORACLE_DB_CONFIG['dsn']
        )
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Connection failed: {e}")


def insert_banks(conn, banks):
    cursor = conn.cursor()
    bank_ids = {}
    for bank in banks:
        cursor.execute(
            "MERGE INTO banks b USING (SELECT :name AS name, :app_id AS app_id FROM dual) d ON (b.name = d.name) " +
            "WHEN NOT MATCHED THEN INSERT (name, app_id) VALUES (:name, :app_id) RETURNING id INTO :id",
            {"name": bank["name"], "app_id": bank["app_id"], "id": bank_ids.setdefault(bank["name"], None)}
        )
        cursor.execute("SELECT id FROM banks WHERE name=:name", {"name": bank["name"]})
        bank_ids[bank["name"]] = cursor.fetchone()[0]
    return bank_ids
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


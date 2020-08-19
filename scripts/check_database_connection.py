import os
import time

import dj_database_url
import psycopg2

credentials = dj_database_url.parse(
    f"postgis://postgres:{os.environ['POSTGRES_PASSWORD']}@database:5432/data_manager"
)
is_connected = False

for i in range(10):
    time.sleep(1)
    try:
        connection = psycopg2.connect(
            user=credentials["USER"],
            password=credentials["PASSWORD"],
            host=credentials["HOST"],
            port=credentials["PORT"],
            database=credentials["NAME"],
        )
    except psycopg2.OperationalError:
        continue
    if connection.status == 1:
        is_connected = True
        break

if not is_connected:
    raise ConnectionError("Could not connect to database")
    exit(1)
else:
    connection.close()

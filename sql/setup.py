from os import getenv

from dotenv import load_dotenv
from db_connect import db_connect

load_dotenv()

curr = db_connect()

print(curr)

with open("sql/setup.sql", "r", encoding="utf-8") as fil:
    sql_schema_lines = fil.readlines()

    for sql_schema_line in sql_schema_lines:
        print(sql_schema_line)
        sql_schema_line = sql_schema_line.replace("<password>", getenv("DB_PASSWORD"))

        if sql_schema_line.strip().startswith("--"):
            continue

        print(f"To be executed: {sql_schema_line}")
        curr.execute(sql_schema_line)

curr.close()
print("Database and tables created!")

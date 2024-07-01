from db_connect import db_connect

curr = db_connect()

print(curr)

with open("sql/setup.sql", "r", encoding="utf-8") as fil:
    sql_schema_lines = fil.readlines()

    for sql_schema_line in sql_schema_lines:
        print(sql_schema_line)
        sql_schema_line = sql_schema_line.replace("<password>", "_a7r13uVF9i£")

        if sql_schema_line.strip().startswith("--"):
            continue

        print(f"To be executed: {sql_schema_line}")
        curr.execute(sql_schema_line)

curr.close()
print("Database and tables created!")

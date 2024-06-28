from db_connect import db_connect

curr = db_connect()

print(curr)

with open("sql/schema.sql") as fil:
    sql_schema = fil.read()
    print(sql_schema)

    curr.execute(sql_schema)

curr.close()
print("Done!")

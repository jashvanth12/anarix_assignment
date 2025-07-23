import sqlite3

conn = sqlite3.connect("mydb1.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in DB:", tables)

conn.close()


# import sqlite3

# conn = sqlite3.connect("mydb1.db")
# cursor = conn.cursor()

# for table in ['ad_sales', 'total_sales', 'eligibility']:
#     cursor.execute(f"PRAGMA table_info({table})")
#     columns = cursor.fetchall()
#     print(f"Table: {table}")
#     for col in columns:
#         print(f"  {col[1]}")
#     print()

# conn.close()

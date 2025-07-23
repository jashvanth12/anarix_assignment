import pandas as pd
import sqlite3

# CSV files and their corresponding table names
csv_files = {
    "Ad_sales.csv": "ad_sales",
    "Total_sales.csv": "total_sales",
    "Eligibility.csv": "eligibility"
}

conn = sqlite3.connect("mydb1.db")

for file, table in csv_files.items():
    df = pd.read_csv(file)
    df.to_sql(table, conn, if_exists='replace', index=False)


conn.close()
print("All CSVs loaded into SQLite database")

from fastapi import FastAPI, Request
import sqlite3
import uuid
import matplotlib.pyplot as plt
import requests
import os
import re

app = FastAPI()

DB_PATH = "mydb1.db"
OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_llm(question: str) -> str:
    prompt = f"""
You are an expert SQL assistant working with a SQLite database that contains the following tables:

1. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
2. total_sales(date, item_id, total_sales, total_units_ordered)
3. eligibility(eligibility_datetime_utc, item_id, eligibility, message)

Write ONLY a valid SQLite SQL query (no explanation) that answers the following natural language question:
{question}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        raise ValueError(f"LLM error: {response.text}")

    data = response.json()
    
    if "response" in data:
        raw_sql = data["response"].strip()
    elif "message" in data and "content" in data["message"]:
        raw_sql = data["message"]["content"].strip()
    else:
        raise ValueError(f"Unexpected LLM response format: {data}")
    
    # ✅ Remove code block formatting if present
    cleaned_sql = re.sub(r"^```(?:sql)?|```$", "", raw_sql.strip(), flags=re.MULTILINE).strip()
    return cleaned_sql

def run_sql_query(sql: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return columns, rows
    except sqlite3.OperationalError as e:
        raise ValueError(f"SQLite error: {str(e)}")


def generate_plot(columns, rows):
    if len(columns) < 2 or not rows:
        return None
    x, y = zip(*rows)
    plt.figure(figsize=(10, 5))
    plt.bar(x, y)
    plot_name = f"plot_{uuid.uuid4().hex}.png"
    plt.savefig(plot_name)
    plt.close()
    return plot_name


@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    question = body.get("question")

    try:
        sql = ask_llm(question)
        columns, rows = run_sql_query(sql)
        plot_path = generate_plot(columns, rows)
        return {
            "question": question,
            "sql": sql,
            "columns": columns,
            "data": rows,
            "plot": plot_path
        }
    except Exception as e:
        return {"error": str(e)}

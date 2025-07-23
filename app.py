import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

FASTAPI_URL = "http://localhost:8001/ask"

st.set_page_config(page_title="AI SQL Assistant", layout="wide")

st.title("📊 Natural Language to SQL Dashboard")
question = st.text_input("Ask a question about your data:")

if st.button("Submit") and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(FASTAPI_URL, json={"question": question})
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.success("Query successful!")

                st.markdown("### 🔍 SQL Query Used:")
                st.code(data["sql"], language="sql")

                st.markdown("### 📋 Result Data:")
                df = pd.DataFrame(data["data"], columns=data["columns"])
                st.dataframe(df)

                st.markdown("### 📈 Visualization (Plotly):")
                if len(df.columns) >= 2:
                    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title="Data Plot")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Not enough columns to generate a plot.")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

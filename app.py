import streamlit as st
import pandas as pd
import openai
from openai import OpenAI

st.set_page_config(page_title="Database Log Root Cause Analyzer", layout="wide")

st.title("🛠️ Database Log Root Cause Analyzer with GPT")
st.markdown("Upload Oracle alert logs or DB logs and let GPT find the **root cause**.")

# API key input
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# File upload
uploaded_file = st.file_uploader("📄 Upload your database log file (.log or .txt)", type=["log", "txt"])

if uploaded_file and api_key:
    try:
        client = OpenAI(api_key=api_key)

        with st.spinner("Analyzing the log... 🤖"):
            log_data = uploaded_file.read().decode("utf-8")

            prompt = f"""
            You are a database expert. Analyze the following database alert log and find the root cause of any critical issue.
            Provide a short root cause summary with action steps if possible:

            {log_data}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful database assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )

            answer = response.choices[0].message.content
            st.success("✅ Analysis complete!")
            st.subheader("🧠 Root Cause Analysis")
            st.write(answer)

    except Exception as e:
        error_message = str(e)
        if "Incorrect API key" in error_message or "Unauthorized" in error_message:
            st.error("❌ Invalid OpenAI API Key.")
        else:
            st.error(f"🚨 Unexpected error: {error_message}")

import streamlit as st
import openai

# Set page config
st.set_page_config(page_title="AI DB Root Cause Finder", layout="centered")

# App title
st.title("🔍 Database Root Cause Analyzer (GPT-powered)")

# User input: API key and logs
api_key = st.text_input("Enter your OpenAI API Key", type="password", help="Get it from https://platform.openai.com/")
logs = st.text_area("Paste your database logs here", height=300)

# Analyze button
if st.button("Analyze Logs"):
    if not api_key or not logs:
        st.warning("Please enter both your API key and database logs.")
    else:
        try:
            openai.api_key = api_key
            with st.spinner("Analyzing logs with GPT..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a database expert. Your task is to find the root cause of database issues based on logs."},
                        {"role": "user", "content": f"Here are the database logs:\n\n{logs}\n\nPlease identify the root cause and suggest possible fixes."}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                root_cause = response.choices[0].message['content']
                st.success("Analysis Complete ✅")
                st.subheader("🧠 Root Cause Analysis")
                st.write(root_cause)
        except openai.error.AuthenticationError:
            st.error("Invalid OpenAI API key. Please check and try again.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

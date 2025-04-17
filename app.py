import streamlit as st
import openai

# App title
st.set_page_config(page_title="DB Log Root Cause Finder", layout="centered")
st.title("🔍 Database Log Root Cause Analyzer")

# API key input
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Log input area
logs = st.text_area("Paste your database logs here:", height=300)

# Analyze button
if st.button("Analyze Logs"):
    if not api_key or not logs:
        st.warning("Please provide both the API key and logs.")
    else:
        try:
            openai.api_key = api_key
            with st.spinner("Analyzing logs..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a database expert. Analyze logs and identify the root cause."},
                        {"role": "user", "content": logs}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                answer = response.choices[0].message['content']
                st.success("✅ Analysis complete!")
                st.subheader("🧠 Root Cause Analysis")
                st.write(answer)
        except openai.error.AuthenticationError:
            st.error("❌ Invalid OpenAI API Key.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

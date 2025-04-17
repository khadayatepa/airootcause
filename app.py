import streamlit as st
import openai

# Analyze the database logs
def analyze_logs(api_key, logs):
    try:
        openai.api_key = api_key

        response = openai.Completion.create(
            engine="gpt-4",
            prompt=f"Analyze these DB logs and explain the root cause of the issue:\n\n{logs}",
            max_tokens=300,
            temperature=0.7,
        )

        return response.choices[0].text.strip()

    except openai.error.AuthenticationError:
        return "Invalid API key. Please try again."
    except Exception as e:
        return f"Something went wrong: {e}"

# Streamlit UI
st.title("🧠 AI Root Cause Analyzer for DB Logs")

api_key = st.text_input("🔑 Enter OpenAI API Key", type="password")
logs = st.text_area("📝 Paste your database logs here", height=300)

if st.button("🔍 Analyze"):
    if not api_key or not logs:
        st.warning("Please enter both API key and logs.")
    else:
        st.write("Analyzing logs, please wait...")
        result = analyze_logs(api_key, logs)
        st.subheader("🧾 Root Cause Analysis")
        st.write(result)

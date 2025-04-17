import streamlit as st
import openai
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Function to analyze logs using OpenAI
def analyze_logs(api_key, logs):
    try:
        # Set the OpenAI API key
        openai.api_key = api_key
        
        # Query the OpenAI model for root cause analysis
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=f"Given the following database logs, analyze and provide a root cause analysis:\n\n{logs}",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract and return the analysis from OpenAI
        return response.choices[0].text.strip()
    except openai.error.AuthenticationError:
        st.error("Authentication failed. Please check your OpenAI API key.")
        return None
    except Exception as e:
        logging.error(f"Error in analyzing logs: {e}")
        st.error(f"An error occurred: {str(e)}")
        return None

# Streamlit UI setup
def main():
    st.title("Generative AI Based Root Cause Analysis for Database Logs")

    # API Key input field
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

    # Log input area (text area)
    logs = st.text_area("Paste your database logs here", height=300)

    if st.button("Analyze"):
        if api_key and logs:
            st.write("Analyzing logs...")
            result = analyze_logs(api_key, logs)
            if result:
                st.subheader("Root Cause Analysis")
                st.write(result)
        else:
            st.error("Please provide both API Key and logs.")

if __name__ == "__main__":
    main()

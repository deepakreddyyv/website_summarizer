import streamlit as st
import time

st.set_page_config(page_title="Web Summarizer", page_icon=":newspaper:")

st.title("Web Article Summarizer :newspaper:")
st.markdown("Enter a URL and get a concise summary of the article.")

url = st.text_input("Enter URL:", placeholder="Paste URL here...")

if url:
    with st.spinner("Fetching and summarizing..."):
        time.sleep(2)  # Simulate processing
        summary = "This is a placeholder summary.  The real summary would be generated from the article at the provided URL."

        st.subheader("Summary:")
        st.info(summary)

# --- Styling (Optional - CSS Injection) ---
st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2E8B57;
        outline: none;
    }

    .stInfo {
        background-color: #e6f2ff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #b3d9ff;
    }

    .stInfo p {
        font-size: 18px;
        line-height: 1.6;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
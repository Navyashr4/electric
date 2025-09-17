import streamlit as st
import requests

st.title("Post Note to Zuper Job")

# Inputs
job_uid = st.text_input("Job UID", "9c636548-5635-4035-b0a5-030867d5dd6e")
note_message = st.text_area("Note Message", "<p>ggg</p>")

# Load API key from Streamlit secrets
api_key = st.secrets["ZUPER_API_KEY"]

# Headers for API key auth
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

# Button to post note
if st.button("Send Note"):
    url = f"https://stagingv2.zuperpro.com/api/jobs/{job_uid}/note?notify_users=true"
    payload = {
        "note": {
            "is_private": False,
            "note": note_message,
            "note_type": "TEXT"
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            st.success("✅ Note posted successfully!")
            st.json(response.json())
        else:
            st.error(f"❌ Failed with status code {response.status_code}")
            st.text(response.text)
    except requests.exceptions.RequestException as e:
        st.error("❌ Request failed")
        st.text(str(e))

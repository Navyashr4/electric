import streamlit as st
import requests

st.title("Post Note to Zuper Job")

url = "https://stagingv2.zuperpro.com/api/jobs/9c636548-5635-4035-b0a5-030867d5dd6e/note?notify_users=true"

payload = {
    "attachments": [],
    "is_private": False,
    "note": "<p>ggg</p>",
    "note_type": "TEXT",
    "user_mentions": []
}

# ⚠️ Replace with your real token
headers = {
    "Content-Type": "application/json"
}

if st.button("Send Note"):
    response = requests.post(url, json=payload, headers=headers)
    st.json(response.json())
    if response.status_code == 200:
        st.success("✅ Note posted successfully!")
        st.json(response.json())
    else:
        st.error(f"❌ Failed with status code {response.status_code}")
        st.text(response.text)

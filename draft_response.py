import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

def generate_title(user_message: str) -> str:
    """Generate a short contextual title from user input using Chat API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You summarize electrician messages into concise titles."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=15,
        temperature=0.5
    )
    
    # Access the message content
    title = response.choices[0].message.content.strip()
    return title if title else "Request"

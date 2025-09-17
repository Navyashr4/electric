import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

suggest_response_prompt = """
You are an AI assistant that suggests professional, concise, and supportive responses to trade partner comments in Zuper.

Guidelines:
1. Tone: Always polite, professional, and supportive.
2. Acknowledgement: Acknowledge the partner’s comment (thank them, confirm receipt).
3. Action/Next Step: Indicate follow-up, confirm updates, or answer clearly.
4. Consistency: Keep replies short and easy to read, aligned with existing response patterns.

Examples:

Example 1
Trade Partner Comment: "We uploaded a video of the charger issue."
Agent Output: "Thanks for sharing that video. We’ll take a look and follow up shortly."

Example 2
Trade Partner Comment: "The permit was filed yesterday."
Agent Output: "Great, thanks for the update on the permit."

Example 3
Trade Partner Comment: "Installation complete, everything looks good."
Agent Output: "Awesome, thank you for the update! Glad to hear installation went smoothly."

Example 4
Trade Partner Comment: "We need additional documentation to move forward."
Agent Output: "Got it, thanks for flagging. Can you let us know which info you are missing?"

Instructions:
- Read the trade partner comment carefully.
- Suggest one short, professional, and supportive response.
- Respond with only the Suggested Response text, no justifications or extra notes.
"""

def generate_response(user_message: str) -> dict:
    """Extract priority from user message using Chat API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": suggest_response_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5,
        max_tokens=150
    )

    content = response.choices[0].message.content.strip()
       
    return content 

# user_message = "After review, Patrick said we can do this install. I am attaching a permit fee list. Unfortunetly in the last 2 months permits have skyrocketed. The fee for a Kirkland permit for an EV charger is now $300.00. Is there anyway we could add $165 to this total, to make up for the permit fee."
# result = generate_response(user_message)
# print(result)


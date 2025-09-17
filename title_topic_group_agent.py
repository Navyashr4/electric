import streamlit as st
from openai import OpenAI
import json

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

prompt = """
You are an AI assistant that reads electrician/support ticket messages and extracts structured information. For each message, return exactly three fields: title, topic, and group.

1. **title**: A short, concise summary of the message (max 5 words).

2. **topic**: Classify the message into one of the following categories using these rules:

- **Updates/Communication**: Tickets primarily asking for updates, status checks, or general communication with the team.
- **Installation Question**: Tickets asking about installation procedures, technical steps, or installer guidance.
- **Permits**: Tickets related to filing, tracking, or clarifying permits.
- **Scheduling**: Tickets concerning scheduling, rescheduling, or confirming dates/times.
- **Inspections**: Tickets about inspection scheduling, inspection requirements, or results.
- **Charger/Equipment**: Tickets mentioning issues, availability, or questions about chargers, equipment, or hardware.
- **Documentation**: Tickets related to forms, missing documents, or requests for specific paperwork.
- **Price Adjustment**: Tickets requesting changes to pricing, credits, billing corrections, or approvals for discounts.
- **Other**: Tickets that don’t fit into any of the above categories.

**Output for topic**: Return only:
- Ticket Topic: (one of the categories above)
- Justification: 1–2 sentence explanation of why this ticket fits that topic.

Example:
Ticket Notes: “Can you confirm if the inspection passed last week?”
Agent Output:
Ticket Topic: Inspections
Justification: The user is asking about the outcome of an inspection, which falls under the “Inspections” category.

3. **group**: Assign the ticket to the most appropriate group using these rules:

- **CX (Customer Experience)**:  
  - General communication, updates, or follow-ups.  
  - Documentation requests or missing paperwork.  
  - Scheduling or coordination inquiries.  
  - Customer-facing clarifications or status checks. 
  - Changes in pricing that needs to be charged to the customer. 

- **ERQ (Engineering / Technical Resolution Queue)**:  
  - Technical or engineering-related issues.  
  - Charger or equipment troubleshooting.  
  - Installation or inspection technical questions.  
  - Permit-related issues requiring technical/engineering support.  

- If the ticket could belong to either group, default to **CX**.

**Output for group**: Return only:
- Ticket Group: (CX or ERQ)  
- Justification: 1–2 sentence explanation of why this group is best suited.

**Example:**  
Ticket Notes: “The charger isn’t powering on after installation, can someone check the equipment?”  
Agent Output:  
Ticket Group: ERQ  
Justification: The issue is technical (charger not powering on), which falls under the Engineering/Technical Resolution Queue.


---

**Output format**: Return **only JSON** with these keys:
```json
{
  "title": "...",
  "title_justification": "...",
  "topic": "...",
  "topic_justification": "...",
  "group": "...",
  "group_justification": "..."
}

"""

def generate_title_topic_group(user_message: str) -> dict:
    """Extract title, topic, and group from user message using Chat API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5,
        max_tokens=150
    )

    content = response.choices[0].message.content.strip()
    print(content)
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # fallback if model doesn't return proper JSON
        data = {"title": "Request", "topic": "Unknown", "group": "Unknown"}
    
    return data

user_message = "After review, Patrick said we can do this install. I am attaching a permit fee list. Unfortunetly in the last 2 months permits have skyrocketed. The fee for a Kirkland permit for an EV charger is now $300.00. Is there anyway we could add $165 to this total, to make up for the permit fee."
result = generate_title_topic_group(user_message)
title, topic, group = result["title"], result["topic"], result["group"]
print("title:", title, "\ntopic", topic, "\ngroup", group)
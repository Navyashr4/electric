import streamlit as st
from openai import OpenAI
import json

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

priority_prompt_1 = """
You are an AI assistant that sets the PRIORITY LEVEL for support tickets. Use the following inputs and rules:

Inputs:
1. Zuper Job Status & HubSpot Deal Stage (Severity Flags)
   - Severity 1 → critical → raise priority significantly.
   - Severity 2 → elevated → raise priority moderately.
   - Blank/None → neutral → no adjustment.

2. Tone of Note
   - Angry, urgent, frustrated → increase priority.
   - Neutral or positive → no adjustment.

3. Number of Zuper Job Posts
   - Many installer posts on a job → complex → raise priority.
   - Few or none → neutral.

Priority Mapping Rules:
- Urgent → Severity 1 OR multiple compounding factors (angry tone + many job posts).
- High → Severity 2 OR severe user tone OR moderate number of jobs affected.
- Medium → No severity, normal tone, but some operational impact.
- Low → No severity, calm tone, and minimal or no job impact.

Instructions:
- Analyze the ticket using all available information.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format as follows:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should briefly reference severity, tone, and/or number of job posts as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: Severity = 1, Tone = neutral, Job posts = few
Output: {"priority": "Urgent", "justification": "Severity 1 indicates critical issue despite calm tone and few posts."}

Input: Severity = blank, Tone = angry, Job posts = moderate
Output: {"priority": "High", "justification": "Angry tone and moderate job posts increase priority even without severity flag."}

Input: Severity = blank, Tone = neutral, Job posts = few
Output: {"priority": "Low", "justification": "No severity, calm tone, and minimal job posts."}
"""

priority_prompt_2 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets based on the content of the note. Use the following considerations:

1. Tone of Note
   - Angry, frustrated, or urgent → increase priority.
   - Neutral or positive → lower priority.

2. Complexity of Task
   - Tasks that are complicated, involve multiple steps, or have potential technical issues → raise priority.
   - Simple tasks → lower priority.

3. Potential Operational Impact
   - Customer may need to be contacted again, proposals may need changes, or delays could occur → raise priority.
   - Minimal impact → lower priority.

Priority Mapping Rules:
- Urgent → Note is high urgency, frustrated/angry, and complex with potential follow-up needed.
- High → Note indicates elevated concern, some complexity, or possible operational impact.
- Medium → Note is straightforward with minor impact, neutral tone.
- Low → Note is simple, calm, and low impact.

Instructions:
- Analyze the note carefully using tone, task complexity, and potential operational impact.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference tone, complexity, and potential impact as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Customer is upset that the installation is delayed and may require a revised proposal."
Output: {"priority": "Urgent", "justification": "Angry tone, potential proposal changes, and follow-up needed indicate high urgency."}

Input: "Minor wiring issue found; needs a simple fix but no impact on schedule."
Output: {"priority": "Medium", "justification": "Neutral tone and minor task with low impact."}

Input: "Customer requested clarification on schedule; everything else is fine."
Output: {"priority": "Low", "justification": "Calm tone, simple request, minimal operational impact."}
"""



def generate_priority(user_message: str) -> dict:
    """Extract priority from user message using Chat API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": priority_prompt_2},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5,
        max_tokens=150
    )

    content = response.choices[0].message.content.strip()
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # fallback if model doesn't return proper JSON
        data = {
            "priority": "Unknown", 
            "priority_justification": "Unknown"
            }
    
    return data

user_message = "After review, Patrick said we can do this install. I am attaching a permit fee list. Unfortunetly in the last 2 months permits have skyrocketed. The fee for a Kirkland permit for an EV charger is now $300.00. Is there anyway we could add $165 to this total, to make up for the permit fee."
result = generate_priority("Permit doc uploaded")
print(result)

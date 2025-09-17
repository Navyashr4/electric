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

priority_prompt_3 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets based on the content of the note. Consider the following criteria:

1. Urgency & Tone
   - Angry, frustrated, or urgent → increases priority.
   - Calm or neutral → lowers priority.

2. Operational Impact
   - Tasks that require intervention, follow-up, or may cause delays → increase priority.
   - Minor tasks with minimal impact → lower priority.

3. Customer Trust
   - Any issue that could lead to cancellations or damage customer trust → highest priority.

Priority Mapping Rules:
- Critical → Any risk of cancellations or customer trust being affected.
- High → Note indicates need for intervention, follow-up, or significant operational impact.
- Medium → Some operational impact or minor follow-up needed.
- Low → No urgency, minimal impact, no follow-up needed.

Instructions:
- Analyze the note carefully using urgency, operational impact, and customer trust considerations.
- Assign exactly one priority: Critical, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Critical|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference urgency, operational impact, or customer trust as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Customer may cancel if installation is delayed further."
Output: {"priority": "Critical", "justification": "Risk of cancellation could affect customer trust, indicating critical priority."}

Input: "Minor wiring issue found; needs a simple fix but no impact on schedule."
Output: {"priority": "Medium", "justification": "Minor issue with some operational impact, requiring attention but not critical."}

Input: "Customer requested clarification on schedule; everything else is fine."
Output: {"priority": "Low", "justification": "Calm tone, minimal impact, no urgent follow-up needed."}

Input: "Installation error detected that will require immediate intervention."
Output: {"priority": "High", "justification": "Issue requires intervention and follow-up, indicating high priority."}
"""

priority_prompt_4 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets based on the content of the note. Use the following considerations:

1. Urgency & Tone
   - Angry, frustrated, or urgent → increase priority.
   - Calm or neutral → lower priority.

2. Operational Risk / Intervention
   - Tasks requiring intervention, follow-up, or could lead to delays → increase priority.
   - Safety issues, installation defects, or compromised equipment → assign higher priority immediately.

3. Customer Impact / Trust
   - Any issue that could lead to cancellations, safety hazards, or loss of customer trust → highest priority.

Priority Mapping Rules:
- Critical → Risk of cancellations or major customer trust impact (e.g., customer safety, critical failures).
- Urgent → Immediate operational impact, safety issues, or blockers that must be addressed today.
- High → Requires intervention, follow-up, or significant operational impact but no immediate safety risk.
- Medium → Some operational impact, minor follow-up needed, or assumptions/errors that do not pose immediate risk.
- Low → Minimal impact, no urgent action, calm tone.

Instructions:
- Analyze the note carefully using urgency, operational risk, customer trust, and safety considerations.
- Assign exactly one priority: Critical, Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Critical|Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference urgency, operational impact, customer trust, or safety as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Customer may cancel if installation is delayed further."
Output: {"priority": "Critical", "justification": "Risk of cancellation could affect customer trust, indicating critical priority."}

Input: "Minor wiring issue found; needs a simple fix but no impact on schedule."
Output: {"priority": "Medium", "justification": "Minor issue with some operational impact, requiring attention but not urgent."}

Input: "Customer requested clarification on schedule; everything else is fine."
Output: {"priority": "Low", "justification": "Calm tone, minimal impact, no urgent follow-up needed."}

Input: "Installation error detected that will require immediate intervention."
Output: {"priority": "Urgent", "justification": "Safety or installation defect requires immediate action today."}

Input: "We attempted to contact customer several times with no response; permit has been issued."
Output: {"priority": "Medium", "justification": "Follow-up needed but no immediate risk to customer or safety."}

Input: "EV panel cover compromised; cannot reconnect breaker until resolved due to safety concerns."
Output: {"priority": "Urgent", "justification": "Safety hazard detected, immediate intervention required."}
"""

priority_prompt_5 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets. Use the following rules:

1. Tone of Note:
- Angry, urgent, or frustrated → increase priority.
- Neutral or positive → no adjustment.

2. Content Factors:
- Electrical Issues & Safety:
  • Sparks, smoke, fire risk → urgent.
  • Unsafe panel, compromised wiring, disconnected critical circuits, or any condition that could lead to immediate harm → urgent.
  • Minor electrical issues (flickering lights, non-critical outlets) → medium/high depending on impact.
- Operational Blockers:
  • Any situation where work cannot continue today due to missing parts, unsafe equipment, or blocked installations → urgent.
- Compounding Factors:
  • Safety + electrical + urgent tone → escalate automatically to urgent.

3. Priority Mapping Rules:
- Urgent: Immediate safety risk, electrical hazards, compromised systems, or blockers preventing critical work today.
- High: Significant operational impact or electrical issues not immediately dangerous.
- Medium: Some operational impact or minor follow-up needed.
- Low: Minimal impact, calm/neutral tone, cosmetic/informational issues.

⚡ Key Principle: Safety issues, compromised systems, or operational blockers that prevent work today should always be treated as urgent, even if no sparks or fire are present.

Instructions:
- Analyze the note carefully using tone, safety, electrical risk, and operational blockers.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference tone, safety risk, electrical hazard, or operational blocker as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Team scheduled for today but had to cancel because customer did not receive required charger."
Output: {"priority": "Urgent", "justification": "Operational blocker prevents critical work today, requiring urgent attention."}

Input: "Panel buss assembly out of place; EV circuit disconnected for safety due to compromised panel."
Output: {"priority": "Urgent", "justification": "Safety risk with compromised panel and disconnected circuit requires immediate intervention."}

Input: "Minor flickering in one office light, no outages."
Output: {"priority": "Medium", "justification": "Minor electrical issue causing some disruption but no immediate safety risk."}
"""



def generate_priority(user_message: str) -> dict:
    """Extract priority from user message using Chat API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": priority_prompt_4},
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

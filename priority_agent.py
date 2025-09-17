import streamlit as st
from openai import OpenAI
import json

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

priority_prompt = """
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

priority_prompt_2 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets based on the content of the note. Use the following considerations:

1. Urgency & Tone
   - Angry, frustrated, or urgent → increase priority.
   - Calm or neutral → lower priority.

2. Operational Risk / Intervention
   - Tasks requiring intervention, follow-up, or could lead to delays → increase priority.
   - Safety issues, installation defects, or compromised equipment → assign higher priority immediately.

3. Customer Impact / Trust
   - Any issue that could lead to cancellations, safety hazards, or loss of customer trust → increase priority.

Priority Mapping Rules:
- Urgent → Immediate operational impact, safety issues, or blockers that must be addressed today.
- High → Requires intervention, follow-up, or significant operational impact but no immediate safety risk.
- Medium → Some operational impact, minor follow-up needed, or assumptions/errors that do not pose immediate risk.
- Low → Minimal impact, no urgent action, calm tone.

Instructions:
- Analyze the note carefully using urgency, operational risk, customer trust, and safety considerations.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference urgency, operational impact, customer trust, or safety as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Customer may cancel if installation is delayed further."
Output: {"priority": "Urgent", "justification": "Potential cancellation could affect customer trust, indicating urgent priority."}

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

priority_prompt_3 = """
You are an AI assistant that assigns the PRIORITY LEVEL for support tickets based on the content of the note. Use the following considerations:

1. Urgency & Tone
- Angry, frustrated, or urgent → increase priority.
- Calm or neutral → lower priority.

2. Operational Blockers & Safety
- Any issue that prevents scheduled work from proceeding today → Urgent.
- Safety issues, compromised equipment, or installation defects → Urgent.
- Minor operational delays or assumptions/errors that do not block work → Medium or High depending on impact.

3. Customer Impact / Trust
- Any issue that could lead to cancellations or affect customer trust → Urgent.

Priority Mapping Rules:
- Urgent → Work cannot proceed today due to operational blockers, safety hazards, or compromised equipment.
- High → Requires intervention, follow-up, or significant operational impact but does not block immediate work.
- Medium → Some operational impact, minor follow-up needed, assumptions/errors that do not block work.
- Low → Minimal impact, calm/neutral tone, cosmetic or informational issues.

Instructions:
- Analyze the note carefully using tone, operational blockers, safety, and customer impact.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification should reference urgency, operational blockers, safety, or customer impact as relevant.
- Do not include any extra text outside the JSON.

Examples:
Input: "Team scheduled for today but had to cancel because customer did not receive required charger."
Output: {"priority": "Urgent", "justification": "Operational blocker prevents scheduled work today, requiring urgent attention."}

Input: "EV panel cover compromised; cannot reconnect breaker until resolved due to safety concerns."
Output: {"priority": "Urgent", "justification": "Safety hazard and compromised equipment prevent work, requiring immediate intervention."}

Input: "We attempted to contact customer several times with no response; permit has been issued."
Output: {"priority": "Medium", "justification": "Follow-up needed but work can continue, no immediate safety risk."}

Input: "Assumption made about cost; minor difficulty navigating garage conduit but work is progressing."
Output: {"priority": "Medium", "justification": "Minor operational issue and assumptions present, but no blocker or safety risk."}
"""

priority_prompt_4 = """
You are an AI assistant that assigns PRIORITY LEVEL for support tickets based on the content of the note. Follow these rules:

1. Urgency & Tone
- Angry, frustrated, or urgent tone → increase priority.
- Calm or neutral → no adjustment unless safety or operational blocker exists.

2. Severe / Immediate Issues
- Any issue that **prevents scheduled work from proceeding today** → Urgent.
- Any **compromised electrical equipment, installation defect, or safety hazard** → Urgent.
- Electrical hazards, fire risk, or immediate danger → always Urgent.
- Angry/urgent tone **plus multiple affected jobs/systems** → Urgent.

3. Operational Impact
- Issues requiring follow-up or intervention, but not blocking work today → High.
- Minor follow-up or assumptions/errors → Medium.
- Minimal impact, informational or cosmetic → Low.

Priority Mapping Rules:
- Urgent → Immediate safety risk, compromised equipment, or work cannot proceed today.
- High → Requires intervention or significant operational impact but work can continue.
- Medium → Some operational impact, minor follow-up, assumptions/errors, no work stoppage.
- Low → Minimal impact, calm/neutral tone, no follow-up needed.

Instructions:
- Analyze the note using urgency, tone, safety, electrical risk, and operational blockers.
- Assign exactly one priority: Urgent, High, Medium, or Low.
- Respond ONLY in JSON format:
{
  "priority": "<Urgent|High|Medium|Low>",
  "justification": "<one sentence explaining the reason>"
}
- Justification must reference safety, operational blocker, or tone as relevant.
- Do not include extra text outside JSON.

Examples:
Input: "Team scheduled for today but had to cancel because customer did not receive required charger."
Output: {"priority": "Urgent", "justification": "Work cannot proceed today due to missing critical equipment, requiring urgent attention."}

Input: "EV panel cover compromised; cannot reconnect breaker until resolved due to safety concerns."
Output: {"priority": "Urgent", "justification": "Safety hazard and compromised equipment prevent work today, requiring immediate intervention."}

Input: "Minor flickering in one office light, no outages."
Output: {"priority": "Medium", "justification": "Minor electrical issue causing some disruption but no immediate safety risk or work stoppage."}

Input: "Follow-up needed on permit; customer unresponsive."
Output: {"priority": "Medium", "justification": "Follow-up required but work can continue, no immediate risk."}

Input: "Cosmetic label misprinted on equipment."
Output: {"priority": "Low", "justification": "Minimal impact, informational only, no action needed."}
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

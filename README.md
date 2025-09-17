# Partner Gateway

Automatically prioritize electrician/support ticket requests and generate draft responses using AI.

## Features

- **AI-Powered Ticket Analysis:**  
  - Extracts ticket title, topic, and group using OpenAI.
  - Assigns priority level (Urgent, High, Medium, Low) with justification.
  - Generates a professional draft response for trade partner comments.

- **Streamlit Web App:**  
  - User-friendly interface for entering ticket messages.
  - Displays context-rich ticket cards with AI-generated insights.
  - Option to send draft responses directly to Zuper via API.

## File Structure

- `app.py` — Main Streamlit app.
- `draft_response_agent.py` — Generates draft responses using OpenAI.
- `priority_agent.py` — Assigns priority levels to tickets.
- `title_topic_group_agent.py` — Extracts title, topic, and group from ticket messages.
- `styles.css` — Custom CSS for UI styling.
- `test.py` — Example Streamlit app for posting notes to Zuper.
- `.streamlit/secrets.toml` — Store API keys (excluded from git).

## Setup

1. **Install dependencies:**
   ```sh
   pip install streamlit openai requests

2. Add OPEN_AI_API and ZUPER_API_KEY keys into .streamlit/secrets.toml 

3. Run the app with `streamlit run app.py`

## Usage
- Enter a ticket message in the text area.
- Click Process to view AI-generated analysis and draft response.
- Optionally, click Send Response to Zuper to post the draft response.
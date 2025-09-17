import streamlit as st
from title_topic_group_agent import generate_title_topic_group
from priority_agent import generate_priority
from draft_response_agent import generate_response
import requests

# Inputs
# job_uid = st.text_input("Job UID", "9c636548-5635-4035-b0a5-030867d5dd6e")
# note_message = st.text_area("Note Message", "<p>ggg</p>")

# Load API key from Streamlit secrets
api_key = st.secrets["ZUPER_API_KEY"]

# Headers for API key auth
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}


st.markdown(
    """
    <style>
    /* Center all vertical blocks (title, text input, button, etc.) */
    div[data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        align-items: center;  /* horizontal centering */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Support Card", page_icon="⚡", layout="centered")

# Page title
st.markdown('<h1 style="text-align:center;">Zuper Assistant</h1>', unsafe_allow_html=True)

# Page subtitle 
st.markdown(
    '<h4 style="text-align:center; font-weight:400; color:#E0E0E0;">Automatically prioritize electrician requests and generate draft responses in seconds. </h4>',
    unsafe_allow_html=True
)


# Text input box
user_input = st.text_area(
    label="",
    height=200,
    width=500,
    placeholder="Type your message..."
)

# Read CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Define colors for each priority
priority_colors = {
    "Urgent": "#E53E3E",   # red
    "High": "#DD6B20",     # orange
    "Medium": "#D69E2E",   # yellow
    "Low": "#38A169"       # green
}

# # Process button
# process_clicked = st.button("Process")
# draft_response = ""

# # Only render the card if Process is clicked and there is input
# if process_clicked and user_input.strip():
#     # Generate AI title, topic, group
#     result = generate_title_topic_group(user_input)
#     title, topic, group = result["title"], result["topic"], result["group"]
#     title_just, topic_just, group_just = (
#         result["title_justification"],
#         result["topic_justification"],
#         result["group_justification"],
#     )

#     # Generate priority
#     priority_result = generate_priority(user_input)
#     priority, priority_justification = (
#         priority_result["priority"],
#         priority_result["justification"],
#     )
#     color = priority_colors.get(priority, "#718096")  # default gray

#     draft_response = generate_response(user_input)

#     # Card component
#     st.markdown(
#         '<h4 style="text-align:center; font-weight:800; color:#E0E0E0; margin-top:80px;">Context-rich ticket. </h4>',
#         unsafe_allow_html=True,
#     )

#     st.markdown(
#         f"""
#         <div class="card">
#             <div class="contextual-title">{title}</div>
#             <div class="header-row">
#                 <span class="pill tooltip">
#                   {topic}
#                   <span class="tooltip-text">{topic_just}</span>
#                 </span>
#                 <span class="ticket-group-pill tooltip">
#                   {group} Group
#                   <span class="tooltip-text">{group_just}</span>
#                 </span>
#                 <span class="priority-pill tooltip" style="background-color: {color}">
#                   {priority} Priority
#                   <span class="tooltip-text">{priority_justification}</span>
#                 </span>
#             </div>
#             <div class="installer-question"> 
#               <div class="ticket-info">Installer Question:</div>
#               {user_input}
#             </div>
#             <div class="draft-response">
#               <div class="ticket-info">Draft Response:</div>
#               {draft_response}
#               <div class="draft-footer">
#                 <div class="draft-footer-icon copy-icon" title="Copy"></div>
#                 <div class="draft-footer-icon like-icon" title="Like"></div>
#                 <div class="draft-footer-icon dislike-icon" title="Dislike"></div>
#                 <div class="draft-footer-icon upload-icon" title="Upload"></div>
#                 <div class="draft-footer-icon regenerate-icon" title="Regenerate"></div>
#               </div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # --- Send to Zuper Button (appears under ticket card) ---
# if st.button("Send Response to Zuper"):
#     url = f"https://stagingv2.zuperpro.com/api/jobs/9c636548-5635-4035-b0a5-030867d5dd6e/note?notify_users=true"
#     payload = {
#         "note": {
#             "is_private": False,
#             "note": draft_response,  # send the generated draft response
#             "note_type": "TEXT",
#         }
#     }
#     try:
#         response = requests.post(url, json=payload, headers=headers, timeout=10)
#         if response.status_code == 200:
#             st.success("✅ Note posted successfully!")
#             st.json(response.json())
#         else:
#             st.error(f"❌ Failed with status code {response.status_code}")
#             st.text(response.text)
#     except requests.exceptions.RequestException as e:
#         st.error("❌ Request failed")
#         st.text(str(e))

# --- Initialize session state ---
if "draft_response" not in st.session_state:
    st.session_state.draft_response = ""
if "process_clicked" not in st.session_state:
    st.session_state.process_clicked = False

# Process button
if st.button("Process"):
    user_input_clean = user_input.strip()
    if user_input_clean:
        st.session_state.process_clicked = True

        # Generate AI outputs
        result = generate_title_topic_group(user_input_clean)
        title, topic, group = result["title"], result["topic"], result["group"]
        title_just, topic_just, group_just = (
            result["title_justification"],
            result["topic_justification"],
            result["group_justification"],
        )

        priority_result = generate_priority(user_input_clean)
        priority, priority_justification = (
            priority_result["priority"],
            priority_result["justification"],
        )
        color = priority_colors.get(priority, "#718096")  # default gray

        st.session_state.draft_response = generate_response(user_input_clean)

        # Store other values in session_state if needed (title, topic, etc.)
        st.session_state.title = title
        st.session_state.topic = topic
        st.session_state.group = group
        st.session_state.title_just = title_just
        st.session_state.topic_just = topic_just
        st.session_state.group_just = group_just
        st.session_state.priority = priority
        st.session_state.priority_justification = priority_justification
        st.session_state.color = color

# Only render card if processed
if st.session_state.process_clicked:
    st.markdown(
        '<h4 style="text-align:center; font-weight:800; color:#E0E0E0; margin-top:80px;">Context-rich ticket. </h4>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="card">
            <div class="contextual-title">{st.session_state.title}</div>
            <div class="header-row">
                <span class="pill tooltip">
                  {st.session_state.topic}
                  <span class="tooltip-text">{st.session_state.topic_just}</span>
                </span>
                <span class="ticket-group-pill tooltip">
                  {st.session_state.group} Group
                  <span class="tooltip-text">{st.session_state.group_just}</span>
                </span>
                <span class="priority-pill tooltip" style="background-color: {st.session_state.color}">
                  {st.session_state.priority} Priority
                  <span class="tooltip-text">{st.session_state.priority_justification}</span>
                </span>
            </div>
            <div class="installer-question"> 
              <div class="ticket-info">Installer Question:</div>
              {user_input}
            </div>
            <div class="draft-response">
              <div class="ticket-info">Draft Response:</div>
              {st.session_state.draft_response}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Send to Zuper button (now has access to draft_response)
    if st.button("Send Response to Zuper"):
        uuid = "1e28fcbd-895c-42d2-a7fa-6ec74b48dedf"
        url = f"https://stagingv2.zuperpro.com/api/jobs/{uuid}/note?notify_users=true"
        payload = {
            "note": {
                "is_private": False,
                "note": st.session_state.draft_response,
                "note_type": "TEXT",
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

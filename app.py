import streamlit as st
from title_topic_group_agent import generate_title_topic_group
from priority_agent import generate_priority


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
    height=100,
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

# Process button
process_clicked = st.button("Process")

# Only render the card if Process is clicked and there is input
if process_clicked and user_input.strip():
    # Generate AI title
    result = generate_title_topic_group(user_input)
    title, topic, group = result["title"], result["topic"], result["group"]
    title_just, topic_just, group_just = result["title_justification"], result["topic_justification"], result["group_justification"]
    
    priority_result = generate_priority(user_input)
    priority, priority_justification = priority_result["priority"], priority_result["justification"]
    # Get color based on priority
    color = priority_colors.get(priority, "#718096")  # default gray

    draft_text = "Here is the response"

    # Card component
    st.markdown(
    '<h4 style="text-align:center; font-weight:800; color:#E0E0E0; margin-top:80px;">Context-rich ticket. </h4>',
    unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card">
            <div class="contextual-title">{title}</div>
            <div class="header-row">
                <span class="pill">{topic}</span>
                <span class="ticket-group-pill">{group}</span>
                <span class="priority-pill" style="background-color: {color}">{priority}</span>
            </div>
            <div class="installer-question"> 
              <div class="ticket-info">Installer Question:</div>
              {user_input}
            </div>
            <div class="draft-response">
              <div class="ticket-info">Draft Response:</div>
              {draft_text}
              <div class="draft-footer">
                <div class="draft-footer-icon copy-icon" title="Copy"></div>
                <div class="draft-footer-icon like-icon" title="Like"></div>
                <div class="draft-footer-icon dislike-icon" title="Dislike"></div>
                <div class="draft-footer-icon upload-icon" title="Upload"></div>
                <div class="draft-footer-icon regenerate-icon" title="Regenerate"></div>
              </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI University Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 1. UPDATED DATA STRUCTURE: Store subject AND messages per thread
if "threads" not in st.session_state:
    st.session_state.threads = {
        "Chat 1": {
            "subject": "PHYSICS 1", 
            "messages": [{"role": "assistant", "content": "Hi! Select a subject above and ask me anything."}]
        }
    }

if "current_thread" not in st.session_state:
    st.session_state.current_thread = "Chat 1"

# Create a convenient reference to the currently active thread
current_chat = st.session_state.threads[st.session_state.current_thread]
st.session_state.messages = current_chat["messages"]


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: #090B0F !important;
        color: #E8EAED !important;
    }

    header[data-testid="stHeader"] {
        background: #090B0F !important;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 55px;
        padding-bottom: 120px;
    }

    section[data-testid="stSidebar"] {
        background: #0E1015 !important;
        border-right: 1px solid #22252C !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #0E1015 !important;
        padding: 30px 20px;
    }

    section[data-testid="stSidebar"] * {
        color: #DADCE0;
    }

    .sidebar-brand {
        font-family: "DM Serif Display", Georgia, serif;
        font-size: 29px;
        color: #F5F7FA !important;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }

    .sidebar-description {
        color: #777D87 !important;
        font-size: 12px;
        line-height: 1.5;
        margin-bottom: 35px;
    }

    .sidebar-heading {
        color: #737984 !important;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-top: 24px;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #AEB4BE !important;
        text-align: left;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 13px;
        transition: 0.2s ease;
        margin-bottom: 2px;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #191E27 !important;
        color: #A9C7F5 !important;
        border-color: #252B34 !important;
    }

    .stSelectbox > div > div {
        background: #171A20 !important;
        border: 1px solid #30343C !important;
        border-radius: 9px !important;
        color: #E8EAED !important;
    }

    div[data-baseweb="select"] span {
        color: #E8EAED !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        background: #171A20 !important;
    }

    div[data-baseweb="option"] {
        background: #171A20 !important;
        color: #E8EAED !important;
    }

    div[data-baseweb="option"]:hover {
        background: #222731 !important;
    }

    .hero-label {
        color: #8AB4F8;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.7px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .main-title {
        font-family: "DM Serif Display", Georgia, serif;
        font-size: 66px;
        line-height: 1.02;
        letter-spacing: -2.5px;
        color: #F5F7FA;
        margin: 0;
    }

    .main-subtitle {
        color: #8A909A;
        font-size: 16px;
        line-height: 1.7;
        max-width: 690px;
        margin-top: 16px;
        margin-bottom: 42px;
    }

    .ai-message {
        background: #11141A;
        border: 1px solid #292D35;
        border-radius: 15px;
        padding: 15px 18px;
        margin: 12px 0;
        color: #DADCE0;
        font-size: 14px;
        line-height: 1.65;
        max-width: 800px;
    }

    .user-message {
        background: #182438;
        border: 1px solid #293E5D;
        border-radius: 15px;
        padding: 15px 18px;
        margin: 12px 0 12px auto;
        color: #C9DCFA;
        font-size: 14px;
        line-height: 1.65;
        max-width: 800px;
    }

    div[data-testid="stBottomBlockContainer"] {
        background: #090B0F !important;
        border-top: 1px solid #20242B !important;
        padding-top: 10px;
    }

    div[data-testid="stChatInput"] > div {
        background: #171A20 !important;
        border: 1px solid #343942 !important;
        border-radius: 22px !important;
        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #6489BC !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #F1F3F4 !important;
        border: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #727983 !important;
    }
    
    .chat-subject-badge {
        color: #8AB4F8;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    .footer {
        text-align: center;
        color: #555C66;
        font-size: 10px;
        margin-top: 65px;
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def show_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-brand">University Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-description">Your AI-powered university study companion</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-heading">Chat History</div>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        new_thread_id = f"Chat {len(st.session_state.threads) + 1}"
        st.session_state.threads[new_thread_id] = {
            "subject": "PHYSICS 1",
            "messages": [{"role": "assistant", "content": "New chat started. Select a subject on the right and ask me anything!"}]
        }
        st.session_state.current_thread = new_thread_id
        st.rerun()

    # 2. GEMINI-STYLE CHAT LIST: Loops through threads and displays them as buttons
    for thread_id in reversed(list(st.session_state.threads.keys())):
        # Add an emoji indicator if it is the currently active chat
        btn_label = f"💬 {thread_id}" if thread_id == st.session_state.current_thread else thread_id
        
        if st.button(btn_label, key=f"btn_{thread_id}", use_container_width=True):
            st.session_state.current_thread = thread_id
            st.rerun()

    st.markdown("---")
    st.caption("AI University Tutor")
    st.caption("RAG-powered academic assistant")


# 3. DYNAMIC UI TOGGLE: Check if the user has started chatting
is_chat_started = len(st.session_state.messages) > 1

if not is_chat_started:
    # Show Hero UI only if no messages have been sent yet
    st.markdown('<div class="hero-label">CHAT</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Ask anything.</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Have a question about your university subjects? Start a conversation with your AI tutor.</div>', unsafe_allow_html=True)
    
    subjects_list = ["BASIC ELECTRONICS 1", "MATHS 1", "PHYSICS 1", "SDF 1"]
    
    selected_subject = st.selectbox(
        "Select Subject for this Chat:",
        subjects_list,
        index=subjects_list.index(current_chat["subject"]) if current_chat["subject"] in subjects_list else 2,
        key=f"subject_selector_{st.session_state.current_thread}"
    )
    
    # Lock the selected subject to this specific thread
    current_chat["subject"] = selected_subject
    st.markdown("---")
else:
    # If chat has started, hide the dropdown and just show a subtle badge indicating the locked subject
    st.markdown(f'<div class="chat-subject-badge">DISCUSSING: {current_chat["subject"]}</div>', unsafe_allow_html=True)


show_messages()

# Use a dynamic key so the input box behaves cleanly when switching threads
question = st.chat_input("Ask a question about your course...", key=f"input_{st.session_state.current_thread}")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    backend_url = "http://127.0.0.1:8000/chat"

    try:
        # Send the subject locked into this specific thread's data
        api_response = requests.post(
            backend_url, 
            json={
                "question": question, 
                "subject": current_chat["subject"]
            }
        )
        api_response.raise_for_status()
        response = api_response.json().get("answer", "No answer received.")
        
    except requests.exceptions.RequestException as e:
        response = f"Backend connection error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown('<div class="footer">AI University Tutor</div>', unsafe_allow_html=True)

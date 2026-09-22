import streamlit as st
import requests

st.set_page_config(
    page_title="AI University Tutor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "threads" not in st.session_state:
    st.session_state.threads = {
        "Chat 1": [{"role": "assistant", "content": "Hi! Ask me anything about your university subjects."}]
    }

if "current_thread" not in st.session_state:
    st.session_state.current_thread = "Chat 1"

st.session_state.messages = st.session_state.threads[st.session_state.current_thread]


def handle_subject_change():
    new_subj = st.session_state.main_subject_selector
    new_thread_id = f"Chat {len(st.session_state.threads) + 1}"
    st.session_state.threads[new_thread_id] = [
        {"role": "assistant", "content": f"New chat started for {new_subj}. Ask me anything!"}
    ]
    st.session_state.current_thread = new_thread_id


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

    .welcome-card {
        background: #11141A;
        border: 1px solid #292D35;
        border-radius: 20px;
        padding: 32px 35px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .welcome-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 3px;
        height: 100%;
        background: #6F9FE8;
    }

    .welcome-small {
        color: #7F8792;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-bottom: 9px;
    }

    .welcome-title {
        font-family: "DM Serif Display", Georgia, serif;
        font-size: 30px;
        color: #F5F7FA;
        margin-bottom: 9px;
    }

    .welcome-text {
        color: #969DA8;
        font-size: 14px;
        line-height: 1.7;
        max-width: 720px;
    }

    .study-prompt {
        background: #0F1217;
        border: 1px solid #252A32;
        border-radius: 18px;
        padding: 30px 34px;
        margin-bottom: 50px;
    }

    .prompt-label {
        color: #6F7783;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-bottom: 9px;
    }

    .prompt-title {
        font-family: "DM Serif Display", Georgia, serif;
        color: #F1F3F4;
        font-size: 27px;
        margin-bottom: 8px;
    }

    .prompt-text {
        color: #858C97;
        font-size: 13px;
        line-height: 1.7;
        max-width: 650px;
    }

    .chat-area {
        margin-top: 5px;
    }

    .chat-header {
        font-family: "DM Serif Display", Georgia, serif;
        color: #F1F3F4;
        font-size: 29px;
        margin-bottom: 5px;
    }

    .chat-caption {
        color: #6F7680;
        font-size: 12px;
        margin-bottom: 22px;
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

    .stButton > button {
        background: #171A20 !important;
        color: #B8BEC7 !important;
        border: 1px solid #30343C !important;
        border-radius: 9px !important;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #1D222B !important;
        color: #E8EAED !important;
        border-color: #4B5665 !important;
    }

    hr {
        border-color: #272B33 !important;
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
            st.markdown(
                f'<div class="user-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="ai-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">University Tutor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-description">'
        "Your AI-powered university study companion"
        "</div>",
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="sidebar-heading">Current Subject</div>',
        unsafe_allow_html=True,
    )

    subject = st.selectbox(
    "Select Subject for this Chat:",
    [
        "BASIC ELECTRONICS 1",
        "MATHS 1",
        "PHYSICS 1",
        "SDF 1"
    ],
    key="main_subject_selector",
    on_change=handle_subject_change
)

    st.markdown("---")
    
    st.markdown('<div class="sidebar-heading">Chat History</div>', unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        new_thread_id = f"Chat {len(st.session_state.threads) + 1}"
        st.session_state.threads[new_thread_id] = [
            {"role": "assistant", "content": f"New chat started. Ask me anything!"}
        ]
        st.session_state.current_thread = new_thread_id
        st.rerun()

    selected_thread = st.selectbox(
        "History", 
        list(st.session_state.threads.keys()), 
        index=list(st.session_state.threads.keys()).index(st.session_state.current_thread),
        label_visibility="collapsed"
    )
    
    if selected_thread != st.session_state.current_thread:
        st.session_state.current_thread = selected_thread
        st.rerun()

    st.markdown("---")
    st.caption("AI University Tutor")
    st.caption("RAG-powered academic assistant")

if st.session_state.page == "subjects":
    st.markdown(
        '<div class="hero-label">SUBJECTS</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">Your subjects.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        "Choose a subject to access its course material "
        "and ask questions about it."
        "</div>",
        unsafe_allow_html=True,
    )

    subjects = st.selectbox(
        "Choose a subject",
        [
            "BASIC ELECTRONICS 1",
            "MATHS 1",
            "PHYSICS 1",
            "SDF 1",
        ],
        key="subject_selector",
        on_change=handle_subject_change,
        label_visibility="collapsed",
    )


    for item in subjects:
        st.markdown(
            f"""
            <div class="welcome-card">
                <div class="welcome-small">SUBJECT</div>
                <div class="welcome-title">{item}</div>
                <div class="welcome-text">
                    Course material and contextual answers
                    for {item}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

elif st.session_state.page == "material":
    st.markdown(
        '<div class="hero-label">STUDY MATERIAL</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">Your material.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        "Access the university material used by the AI tutor "
        "to answer your questions."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="study-prompt">
            <div class="prompt-label">COURSE MATERIAL</div>
            <div class="prompt-title">Material will appear here.</div>
            <div class="prompt-text">
                Upload or connect your university documents
                when the document retrieval system is ready.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.page == "practice":
    st.markdown(
        '<div class="hero-label">PRACTICE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">Practice smarter.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        "Test your understanding with questions based "
        "on your university course material."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="study-prompt">
            <div class="prompt-label">PRACTICE MODE</div>
            <div class="prompt-title">
                Practice questions are coming soon.
            </div>
            <div class="prompt-text">
                This section can later generate questions
                from the selected subject and course material.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        '<div class="hero-label">CHAT</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-title">Ask anything.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-subtitle">'
        "Have a question about your university subjects? "
        "Start a conversation with your AI tutor."
        "</div>",
        unsafe_allow_html=True,
    )

    show_messages()
    
    question = st.chat_input("Ask a question about your course...", key="unique_chat_input")
    
    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        backend_url = "http://127.0.0.1:8000/chat"

        try:
            api_response = requests.post(
                backend_url, 
                json={
                    "question": question, 
                    "subject": subject
                }
            )
            api_response.raise_for_status()
            response = api_response.json().get("answer", "No answer received.")
            
        except requests.exceptions.RequestException as e:
            response = f"Backend connection error: {e}"

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        st.rerun()

st.markdown(
    '<div class="footer">AI University Tutor</div>',
    unsafe_allow_html=True,
)
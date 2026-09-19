import streamlit as st

st.set_page_config(
    page_title="AI University Tutor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #F2F5F8;
    color: #102A43;
}

header[data-testid="stHeader"] {
    background-color: #EAF3FF;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 7rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background-color: #0B2239;
}

section[data-testid="stSidebar"] * {
    color: #EAF3FF;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F5F9FF;
}

.sidebar-title {
    font-family: Georgia, serif;
    font-size: 2rem;
    font-weight: 700;
    color: #F5F9FF;
    margin-bottom: 0.5rem;
}

.sidebar-subtitle {
    font-size: 0.9rem;
    color: #B9D3EA;
    margin-bottom: 3rem;
}

.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    font-weight: 700;
    color: #102A43;
    margin-top: 1rem;
    margin-bottom: 1rem;
    line-height: 1.05;
}

.main-subtitle {
    font-size: 1.15rem;
    color: #486581;
    margin-bottom: 3rem;
}

.welcome-card {
    background-color: #1D4E7A;

    padding: 2.7rem 3rem;

    border-radius: 22px;

    margin-bottom: 3.5rem;

    box-shadow: 0 10px 30px rgba(16, 42, 67, 0.12);
}

.welcome-title {
    font-family: Georgia, serif;

    color: #F5F9FF;

    font-size: 2.1rem;
    font-weight: 700;

    margin-bottom: 1rem;
}

.welcome-text {
    color: #DCEBFA;

    font-size: 1.05rem;

    line-height: 1.6;
}

.section-title {
    color: #102A43;

    font-family: Georgia, serif;

    font-size: 2rem;
    font-weight: 700;

    margin-top: 2rem;
    margin-bottom: 1.5rem;
}

.subject-card {
    background-color: #D4E6F7;

    padding: 1.7rem;

    border-radius: 18px;

    border: 1px solid #B4D0E8;

    min-height: 135px;

    transition: 0.2s ease;
}

.subject-card:hover {
    transform: translateY(-4px);

    box-shadow: 0 8px 20px rgba(16, 42, 67, 0.12);
}

.subject-title {
    font-family: Georgia, serif;

    color: #102A43;

    font-size: 1.4rem;
    font-weight: 700;

    margin-bottom: 0.7rem;
}

.subject-text {
    color: #486581;

    font-size: 0.95rem;

    line-height: 1.5;
}

.stButton > button {
    background-color: #3B82B8;

    color: white;

    border: none;

    border-radius: 10px;

    padding: 0.65rem 1.2rem;

    font-weight: 600;

    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #2F6F9F;

    color: white;
}

.stSelectbox > div > div {
    background-color: #173B5E;

    color: #F5F9FF;

    border: 1px solid #3B82B8;

    border-radius: 10px;
}

div[data-testid="stBottomBlockContainer"] {
    background-color: #EAF3FF;

    border-top: none;
}

div[data-testid="stChatInput"] {
    background-color: #EAF3FF;

    border: none;
}

div[data-testid="stChatInput"] > div {
    background-color: #173B5E;

    border: 1px solid #3B82B8;

    border-radius: 16px;

    box-shadow: 0 5px 15px rgba(16, 42, 67, 0.12);
}

div[data-testid="stChatInput"] textarea {
    background-color: #173B5E !important;

    color: #F5F9FF !important;

    border: none !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #B9D3EA !important;
}

.ai-message {
    background-color: #D4E6F7;

    color: #102A43;

    padding: 1rem 1.3rem;

    border-radius: 14px;

    margin: 0.8rem 0;

    border: 1px solid #B4D0E8;
}

.user-message {
    background-color: #1D4E7A;

    color: #F5F9FF;

    padding: 1rem 1.3rem;

    border-radius: 14px;

    margin: 0.8rem 0;
}

hr {
    border-color: #294D6B;
}

.footer {
    text-align: center;

    color: #6B849B;

    font-size: 0.85rem;

    margin-top: 4rem;
}

.stChatInputContainer {
    width: 40% !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

.stChatInputContainer > div {
    width: 100% !important;
}

.stChatInputContainer textarea {
    background-color: #F2F5F8; !important;
    color: #102A43 !important;
    border: 1px solid #9BB9D4 !important;
    border-radius: 14px !important;
}

.stChatInputContainer textarea::placeholder {
    color: #52708D !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">UniversityTutor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Your AI-powered university study companion</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Subjects")

    subject = st.selectbox(
        "Choose a subject",
        [
            "All Subjects",
            "SDF-I",
            "SDF-II",
            "MATHS-I",
            "PHYSICS-I",
            "BEL-I",
            "EDD"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### Quick Actions")

    if st.button("Study Material", use_container_width=True):
        st.info("Study material section coming soon.")

    if st.button("Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hi! Ask me anything about your university subjects."
            }
        ]
        st.rerun()

    if st.button("Practice Questions", use_container_width=True):
        st.info("Practice mode coming soon.")

    st.markdown("---")

    st.caption("AI University Tutor")
    st.caption("RAG-powered academic assistant")

st.markdown(
    '<div class="main-title">AI University Tutor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Ask questions. Understand concepts. Study smarter.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="welcome-card">
        <div class="welcome-title">Your personal study companion.</div>
        <div class="welcome-text">
            Ask questions about your university subjects and get
            clear, contextual explanations from your study material.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">Explore your subjects</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="subject-card">
    <div class="subject-title">Mathematics</div>
    <div class="subject-text">
        Calculus, algebra, probability & more
    </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="subject-card">
    <div class="subject-title">Physics</div>
    <div class="subject-text">
       Mechanics, electromagnetism, optics
    </div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="subject-card">
    <div class="subject-title">Programming</div>
    <div class="subject-text">
       Programming fundamentals, functions 
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="chat-section"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Ask your doubts</div>',
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! Ask me anything about your university subjects."
        }
    ]

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
<div class="user-message">
    {message["content"]}
</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
<div class="ai-message">
    {message["content"]}
</div>
""",
            unsafe_allow_html=True
        )

question = st.chat_input(
    "Ask a question about your course..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = (
        "I'm currently in frontend mode 🛠️ "
        "The RAG backend will be connected here once "
        "the Pinecone retrieval pipeline is ready."
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()


st.markdown(
    """
<div class="footer">
    Built with Streamlit · LangChain · Gemini · Pinecone
</div>
""",
    unsafe_allow_html=True
)
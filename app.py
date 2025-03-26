import streamlit as st
import seaborn as sns

st.set_page_config(layout="wide", page_title="Level Ethics AI")

# Inject custom CSS (Inter + tab styling). Same as before:
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        color: black !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        color: black !important;
        background-color: transparent !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        color: #2D00D1 !important;
        background-color: #f0f0f0 !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #2D00D1 !important;
        color: #2D00D1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Adjust columns ratio & gap for tighter spacing
col1, col2 = st.columns([1, 20], gap="small")  # [1,2] is a 1:2 ratio
with col1:
    st.image("logo.png", width=80)  # Path must be correct
with col2:
    st.markdown(
        "<h1 style='margin: 0;'>Level Ethics <span style='color:#C348FA;'>AI</span></h1>",
        unsafe_allow_html=True
    )

sns.set_theme(style="whitegrid")

from components import onboarding, personas, question_library, llm_responses, evaluations

tabs = st.tabs([
    "Onboarding",
    "Personas",
    "Question Library",
    "LLM Outputs",
    "Evaluation Score"
])

onboarding.ai_act_compliance_wizard(tabs)
personas.display_personas(tabs[1])
question_library.display_question_library(tabs[2])
llm_responses.display_llm_responses(tabs[3])
evaluations.display_evaluations(tabs[4])

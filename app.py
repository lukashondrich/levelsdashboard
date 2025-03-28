import streamlit as st
import seaborn as sns

st.set_page_config(layout="wide", page_title="Level Ethics AI")

# Inject custom CSS (Inter + tab styling). Same as before:
# Inject custom CSS (Inter + tab styling):
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"]  {
        color: black !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTabs"] {
        background-color: white;
        border-bottom: 1px solid #E2E8F0;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        color: #718096 !important;
        background-color: transparent !important;
        font-weight: 500;
        font-size: 16px;
        padding: 12px 16px;
        margin-right: 8px;
        border: none !important;
        border-radius: 0;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        color: #6B46C1 !important;
        background-color: rgba(107, 70, 193, 0.05) !important;
    }
    
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        border: none !important;
        border-bottom: 3px solid #6B46C1 !important;
        color: #6B46C1 !important;
        font-weight: 600;
    }
    
    div[data-testid="stTabs"] [data-testid="stTabPanelContainer"] {
        padding-top: 32px;
    }
    /* Card-like containers */
    div.stForm, div.row-widget.stRadio, div.row-widget.stCheckbox, div.stTextInput, div.stTextArea, div.stMultiselect {
        background-color: #F7FAFC;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }

    /* Section styling */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header and section spacing */
    h1, h2, h3 {
        margin-bottom: 1rem;
    }

    /* Secondary container for nested sections */
    div.stExpander {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    /* Add proper spacing for containers */
    div.stContainer {
        padding: 2rem 0;
    }

    /* Question section styling */
    div.stContainer > div {
        margin-bottom: 1.5rem;
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

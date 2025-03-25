import streamlit as st
import seaborn as sns

# Set configuration
st.set_page_config(layout="wide", page_title="Level Ethics AI")
sns.set_theme(style="whitegrid")

from components import onboarding, personas, question_library, llm_responses, evaluations

# Create tabs (order matters)
tabs = st.tabs(["Onboarding", "Personas", "Question Library", "LLM Outputs", "Evaluation Score"])

# Render each section
onboarding.ai_act_compliance_wizard(tabs)
personas.display_personas(tabs[1])
question_library.display_question_library(tabs[2])
llm_responses.display_llm_responses(tabs[3])
evaluations.display_evaluations(tabs[4])

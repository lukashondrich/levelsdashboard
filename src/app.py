import os
import yaml
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

# Set configuration
st.set_page_config(layout="wide", page_title="Evaluation App Mockup")
sns.set_theme(style="whitegrid")

# Define dataclasses
@dataclass
class Question:
    """Class for storing question data."""
    id: str
    question_text: str
    category: str
    subcategory: str

@dataclass
class LLMResponse:
    """Class for storing LLM response data."""
    question_id: str
    response_text: str
    risk_flags: List[str]
    risk_score: float
    suggested_fix: Optional[str] = None  # Add this line

@dataclass
class Evaluation:
    """Class for storing evaluation score data."""
    question_id: str
    scores: Dict[str, Dict[str, float]]
    feedback: Optional[str] = None

@dataclass
class Insight:
    """Class for storing contributor insight data."""
    question_id: str
    reviewer: str
    comment_text: str

# Data loading functions
def load_yaml_data(filename: str) -> dict:
    """Load data from a YAML file."""
    # Get the directory where app.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then to domain_data
    filepath = os.path.join(current_dir, "..", "domain_data", filename)
    
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return {}

def load_questions() -> List[Question]:
    """Load questions from questions.yaml."""
    data = load_yaml_data("questions.yaml")
    if not data or 'questions' not in data:
        return []
    
    questions = []
    for q in data['questions']:
        questions.append(Question(
            id=q['id'],
            question_text=q['question_text'],
            category=q['category'],
            subcategory=q['subcategory']
        ))
    return questions

def load_llm_responses() -> List[LLMResponse]:
    """Load LLM responses from llm_responses.yaml."""
    data = load_yaml_data("llm_responses.yaml")
    if not data or 'responses' not in data:
        return []
    
    responses = []
    for r in data['responses']:
        # Include suggested_fix if it exists
        suggested_fix = r.get('suggested_fix', None)
        responses.append(LLMResponse(
            question_id=r['question_id'],
            response_text=r['response_text'],
            risk_flags=r['risk_flags'],
            risk_score=r['risk_score'],
            suggested_fix=suggested_fix  # Add this line
        ))
    return responses



def load_evaluations() -> List[Evaluation]:
    """Load evaluations from evaluation_scores.yaml."""
    data = load_yaml_data("evaluation_scores.yaml")
    if not data or 'evaluations' not in data:
        return []
    
    evaluations = []
    for e in data['evaluations']:
        feedback = e.get('feedback', None)
        evaluations.append(Evaluation(
            question_id=e['question_id'],
            scores=e['scores'],
            feedback=feedback
        ))
    return evaluations

def load_insights() -> List[Insight]:
    """Load insights from contributor_insights.yaml."""
    data = load_yaml_data("contributor_insights.yaml")
    if not data or 'insights' not in data:
        return []
    
    insights = []
    for i in data['insights']:
        insights.append(Insight(
            question_id=i['question_id'],
            reviewer=i['reviewer'],
            comment_text=i['comment_text']
        ))
    return insights

def create_radar_chart(values: List[float], categories: List[str], title: str):
    """Create a radar chart using Plotly for more consistent sizing and sleeker appearance."""
    fig = go.Figure()
    
    # Add the trace for the radar chart
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=title,
        line=dict(color='rgb(67, 147, 195)', width=2),
        fillcolor='rgba(67, 147, 195, 0.2)'
    ))
    
    # Update layout for a sleeker appearance
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10),
                tickvals=[0.2, 0.4, 0.6, 0.8],
                ticktext=["0.2", "0.4", "0.6", "0.8"],
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
            )
        ),
        title=dict(
            text=title,
            font=dict(size=14),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        margin=dict(l=80, r=80, t=60, b=60),
        height=420,
        width=420,
        showlegend=False,
    )
    
    return fig

def main():
    """Main function to run the Streamlit app."""
    st.title("Evaluation App Mockup")
    
    # Load all data
    questions = load_questions()
    llm_responses = load_llm_responses()
    evaluations = load_evaluations()
    insights = load_insights()
    
    # Create tabs
    tabs = st.tabs([
        "Onboarding/ODD", 
        "Question Library", 
        "LLM Response", 
        "Evaluation Score", 
        "Contributor Insights"
    ])
    

    # Call the wizard function for Tab 1
    ai_act_compliance_wizard(tabs)

    
    # Tab 2: Question Library
    with tabs[1]:
        st.header("Question Library")
        
        # Get unique categories and subcategories
        categories = ["All"] + sorted(list(set(q.category for q in questions)))
        
        # Create two columns for filters
        filter_col1, filter_col2 = st.columns(2)
        
        # Category filter
        with filter_col1:
            selected_category = st.selectbox("Filter by category:", categories)
        
        # Filtered questions based on category
        if selected_category == "All":
            filtered_questions = questions
            subcategories = ["All"]
        else:
            filtered_questions = [q for q in questions if q.category == selected_category]
            subcategories = ["All"] + sorted(list(set(q.subcategory for q in filtered_questions)))
        
        # Subcategory filter (only show if a specific category is selected)
        with filter_col2:
            if selected_category != "All":
                selected_subcategory = st.selectbox("Filter by subcategory:", subcategories)
                if selected_subcategory != "All":
                    filtered_questions = [q for q in filtered_questions if q.subcategory == selected_subcategory]
            else:
                st.text("Select a category first")
        
        # Display questions
        if not filtered_questions:
            st.warning("No questions found with the selected filters.")
        else:
            for question in filtered_questions:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{question.id}:** {question.question_text}")
                    with col2:
                        st.write(f"**Category:** {question.category}")
                        st.write(f"**Subcategory:** {question.subcategory}")
                    with col3:
                        modify_button = st.button(
                            "Modify", 
                            key=f"modify_{question.id}", 
                            help="Click to modify this question (placeholder functionality)"
                        )
                        if modify_button:
                            st.info("Modification functionality would be implemented here.")
                st.divider()
    
    # Tab 3: LLM Response
    with tabs[2]:
        st.header("LLM Response")
        
        if not llm_responses:
            st.warning("No LLM responses found.")
        else:
            for response in llm_responses:
                # Find the corresponding question text
                question_text = next((q.question_text for q in questions if q.id == response.question_id), "Question text not found")
                
                with st.container():
                    st.subheader(f"Question ID: {response.question_id}")
                    st.write(f"**Question:** {question_text}")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Response:** {response.response_text}")
                        st.write(f"**Risk Flags:** {', '.join(response.risk_flags)}")
                    with col2:
                        # Create a colored box for the risk score
                        risk_percent = response.risk_score * 100
                        color = "green" if risk_percent < 25 else "orange" if risk_percent < 50 else "red"
                        st.markdown(
                            f"""
                            <div style="background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;">
                                <h3 style="margin:0;">Risk Score</h3>
                                <h2 style="margin:0;">{risk_percent:.1f}%</h2>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        fix_button = st.button(
                            "View Suggested Fix", 
                            key=f"fix_{response.question_id}", 
                            help="View suggestions to reduce risk score"
                        )
                        if fix_button:
                            if hasattr(response, 'suggested_fix') and response.suggested_fix:
                                st.info(response.suggested_fix)
                            else:
                                st.info("No suggested fix available for this response.")
                    st.divider()
    
    # Tab 4: Evaluation Score
    with tabs[3]:
        st.header("Evaluation Score")
        
        if not evaluations:
            st.warning("No evaluations found.")
        else:
            # First, collect all unique categories and their subcategories
            all_categories = {}
            for eval_item in evaluations:
                for category, subcategory_scores in eval_item.scores.items():
                    if category not in all_categories:
                        all_categories[category] = set()
                    for subcategory in subcategory_scores.keys():
                        all_categories[category].add(subcategory)
            
            # Convert sets to lists for ordered display
            for category in all_categories:
                all_categories[category] = sorted(list(all_categories[category]))
            
            # Aggregate scores across all evaluations
            aggregated_scores = {}
            for category, subcategories in all_categories.items():
                aggregated_scores[category] = {subcategory: [] for subcategory in subcategories}
            
            # Collect all scores
            for eval_item in evaluations:
                for category, subcategory_scores in eval_item.scores.items():
                    for subcategory, score in subcategory_scores.items():
                        aggregated_scores[category][subcategory].append(score)
            
            # Calculate average scores
            avg_scores = {}
            for category, subcategory_scores in aggregated_scores.items():
                avg_scores[category] = {}
                for subcategory, scores in subcategory_scores.items():
                    avg_scores[category][subcategory] = sum(scores) / len(scores) if scores else 0
            
            # Create columns for each category with explicit spacing
            st.write("## Evaluation by Category")
            
            # Use a container for better chart layout control
            with st.container():
                # Get the number of categories
                num_categories = len(all_categories)
                
                # Calculate how many charts per row (max 3 for better sizing)
                charts_per_row = min(3, num_categories)
                rows_needed = (num_categories + charts_per_row - 1) // charts_per_row
                
                # Create rows of charts
                for row in range(rows_needed):
                    # Create columns for this row
                    cols = st.columns(charts_per_row)
                    
                    # Fill columns with charts
                    for col_idx in range(charts_per_row):
                        chart_idx = row * charts_per_row + col_idx
                        
                        # Check if we still have charts to display
                        if chart_idx < num_categories:
                            # Get the category and subcategories
                            category = list(all_categories.keys())[chart_idx]
                            subcategories = all_categories[category]
                            
                            # Create radar chart
                            with cols[col_idx]:
                                values = [avg_scores[category][subcategory] for subcategory in subcategories]
                                fig = create_radar_chart(values, subcategories, category)
                                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Contributor Insights
    with tabs[4]:
        st.header("Contributor Insights")
        
        if not insights:
            st.warning("No contributor insights found.")
        else:
            for insight in insights:
                # Find the corresponding question text
                question_text = next((q.question_text for q in questions if q.id == insight.question_id), "Question text not found")
                
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"**Question ID:** {insight.question_id}")
                        st.write(f"**Reviewer:** {insight.reviewer}")
                    with col2:
                        st.write(f"**Question:** {question_text}")
                        st.write(f"**Comment:** {insight.comment_text}")
                st.divider()



import streamlit as st
import pandas as pd
from datetime import datetime

import streamlit as st
import pandas as pd
from datetime import datetime

import streamlit as st
import pandas as pd
from datetime import datetime

import streamlit as st
import pandas as pd
from datetime import datetime

import streamlit as st
import pandas as pd
from datetime import datetime


import streamlit as st
import pandas as pd
from datetime import datetime


def ai_act_compliance_wizard(tabs):
    with tabs[0]:
        st.header("Onboarding/ODD")
        st.subheader("Compliance & ODD Assessment")
        
        # Add a button to enable wizard mode
        if 'wizard_mode' not in st.session_state:
            st.session_state.wizard_mode = False
            
        # Add wizard mode toggle
        wizard_mode = st.toggle("Enable Wizard Mode", value=st.session_state.wizard_mode)
        st.session_state.wizard_mode = wizard_mode
        
        if wizard_mode:
            # Initialize session state variables if they don't exist
            if 'current_step' not in st.session_state:
                st.session_state.current_step = 1
            if 'assessment_data' not in st.session_state:
                st.session_state.assessment_data = {}
            if 'is_completed' not in st.session_state:
                st.session_state.is_completed = False
            
            # Navigation functions
            def next_step():
                st.session_state.current_step += 1
            
            def prev_step():
                st.session_state.current_step -= 1
            
            def complete_assessment():
                st.session_state.is_completed = True
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.assessment_data['completion_date'] = timestamp
            
            # Progress bar
            total_steps = 3  # Total number of steps
            progress = st.session_state.current_step / (total_steps + 1)
            st.progress(progress)
            
            # Step indicator
            st.info(f"Step {st.session_state.current_step} of {total_steps}")
            
            # Wizard steps
            if st.session_state.current_step == 1:
                # SECTION 1: Jurisdiction & User Role
                st.markdown("### SECTION 1: Jurisdiction & User Role")
                
                is_eu = st.checkbox(
                    "Is your system made available in the EU or affects people in the EU?",
                    help="Check this if your system is deployed in EU countries or processes data of EU citizens"
                )
                st.session_state.assessment_data['is_eu'] = is_eu
                
                # User role selection (now multiselect)
                role = st.multiselect(
                    "What is your role regarding the AI system? (Select all that apply)",
                    ["Provider", "Deployer", "Distributor", "Importer"],
                    help="Select all roles that apply to your organization"
                )
                
                # Add role explanations
                with st.expander("Need help understanding these roles?"):
                    st.markdown("""
                    **Provider** [Art. 3(2)]: The organization that develops an AI system or has it developed and places it on the market under its own name or trademark.
                    - *Example*: If you're building or developing the AI system, or your company is responsible for its creation, you're likely a Provider.
                    - *For product/project managers*: If you manage the team that builds the AI system, you represent the Provider.
                    
                    **Deployer** [Art. 3(4)]: The organization that uses an AI system under its authority except for personal use.
                    - *Example*: If your organization is using an AI system developed by someone else, you're likely a Deployer.
                    - *For product/project managers*: If you manage the implementation of an AI system purchased from elsewhere, you represent the Deployer.
                    
                    **Distributor** [Art. 3(7)]: The organization that makes an AI system available on the EU market.
                    - *Example*: If you're reselling or distributing an AI system developed by another company, you're a Distributor.
                    - *For product/project managers*: If you manage the distribution of AI products to customers, you represent the Distributor.
                    
                    **Importer** [Art. 3(6)]: The organization that brings an AI system from a third country and places it on the EU market.
                    - *Example*: If your company is bringing AI systems from outside the EU and making them available within the EU, you're an Importer.
                    - *For product/project managers*: If you manage the import process for AI systems, you represent the Importer.
                    
                    **Note**: Organizations can have multiple roles. For example, you might both develop AI systems (Provider) and use AI systems developed by others (Deployer).
                    """)
                
                st.session_state.assessment_data['role'] = role
                
                # Navigation button
                st.button("Next →", on_click=next_step, disabled=(role == "Select..."))
                
            elif st.session_state.current_step == 2:
                # SECTION 2: AI Risk Classification
                st.markdown("### SECTION 2: AI Risk Classification")
                
                primary_function = st.text_input(
                    "What is your system's primary function?",
                    key="form_primary_function",
                    value=st.session_state.assessment_data.get('primary_function', ''),
                    help="e.g., scoring students, matching CVs, medical diagnosis, etc."
                )
                
                high_risk_options = st.multiselect(
                    "Does it fall into any of the following high-risk categories?",
                    [
                        "Education and vocational training", 
                        "Employment, worker management and access to self-employment", 
                        "Access to essential private/public services and benefits", 
                        "Law enforcement", 
                        "Migration, asylum and border control",
                        "Administration of justice and democratic processes",
                        "Critical infrastructure management",
                        "Product safety (covered by EU harmonisation legislation)"
                    ],
                    key="form_high_risk_options",
                    default=st.session_state.assessment_data.get('high_risk_options', []),
                    help="Select all categories that apply to your AI system. These are the official high-risk areas defined in the EU AI Act under Article 6 and Annex III."
                )
                
                # Add reference expander for high-risk categories
                with st.expander("Reference: High-risk AI systems (Article 6 & Annex III)"):
                    st.markdown("""
                    The EU AI Act classifies the following as high-risk under **Article 6 and Annex III**:
                    
                    1. **Education and vocational training** [Annex III(3)]: AI systems used for determining access to educational institutions, assessing students, or evaluating learning outcomes.
                    
                    2. **Employment, worker management and access to self-employment** [Annex III(4)]: AI systems used for recruitment, task allocation, performance evaluation, or promotion decisions.
                    
                    3. **Access to essential private/public services and benefits** [Annex III(5)]: AI systems used to evaluate eligibility for public benefits, credit scoring, or other essential services.
                    
                    4. **Law enforcement** [Annex III(6)]: AI systems used for risk assessments, lie detection, crime forecasting, or evidence reliability evaluation.
                    
                    5. **Migration, asylum and border control** [Annex III(7)]: AI systems used for immigration or asylum applications, border checks, or document verification.
                    
                    6. **Administration of justice and democratic processes** [Annex III(8)]: AI systems assisting courts in researching or interpreting facts and law or applying law to specific facts.
                    
                    7. **Critical infrastructure management** [Annex III(2)]: AI systems used as safety components in critical infrastructure (transport, water, gas, electricity, etc.).
                    
                    8. **Product safety (EU harmonisation legislation)** [Art. 6(1)]: AI systems intended as safety components of products covered by EU harmonisation legislation (medical devices, machinery, toys, etc.).
                    """)
                st.session_state.assessment_data['high_risk_options'] = high_risk_options
                
                prohibited_tasks = st.multiselect(
                    "Does the system perform any prohibited tasks?",
                    [
                        "Subliminal Manipulation", 
                        "Social Scoring", 
                        "Real-time Biometric ID",
                        "Exploitation of Vulnerabilities",
                        "Emotion Recognition in Workplace/Education",
                        "Predictive Policing Based on Profiling",
                        "None of the Above"
                    ],
                    help="Select all that apply. If none apply, select 'None of the Above'. Prohibited practices are defined in Article 5 of the AI Act."
                )
                
                # Add reference expander for prohibited practices
                with st.expander("Reference: Prohibited AI Practices (Article 5)"):
                    st.markdown("""
                    The EU AI Act prohibits the following practices under **Article 5**:
                    
                    1. **Subliminal Manipulation** [Art. 5(1)(a)]: AI systems that deploy subliminal techniques to materially distort human behavior in a manner that causes or is likely to cause harm.
                    
                    2. **Social Scoring** [Art. 5(1)(c)]: AI systems used by public authorities for evaluating or classifying individuals based on social behavior or personal characteristics.
                    
                    3. **Real-time Biometric ID** [Art. 5(1)(d)]: The use of 'real-time' remote biometric identification systems in publicly accessible spaces for law enforcement purposes (with limited exceptions).
                    
                    4. **Exploitation of Vulnerabilities** [Art. 5(1)(b)]: AI systems that exploit vulnerabilities of specific groups of persons due to their age, disability, or specific social or economic situation.
                    
                    5. **Emotion Recognition in Workplace/Education** [Art. 5(1)(a/b)]: The use of emotion recognition systems in workplace and educational institutions.
                    
                    6. **Predictive Policing Based on Profiling** [Art. 5(1)(c)]: AI systems used for making individual risk assessments based solely on profiling of persons or assessment of personality traits/characteristics.
                    """)
                st.session_state.assessment_data['prohibited_tasks'] = prohibited_tasks
                
                requires_transparency = st.checkbox(
                    "Does the system require transparency (e.g., it's a chatbot or deepfake)?",
                    help="Check if your system interacts with humans in a way that may not be immediately obvious. See Article 52 of the AI Act."
                )
                
                # Add reference expander for transparency requirements
                with st.expander("Reference: Transparency Requirements (Article 52)"):
                    st.markdown("""
                    The EU AI Act requires transparency for specific AI systems under **Article 52**:
                    
                    1. **AI Systems interacting with humans** [Art. 52(1)]: Systems designed to interact with natural persons shall be designed and developed in such a way that natural persons are informed that they are interacting with an AI system (unless this is obvious from the circumstances).
                    
                    2. **Emotion recognition systems** [Art. 52(2)]: Users of emotion recognition or biometric categorization systems shall inform natural persons exposed to such systems of the operation of those systems.
                    
                    3. **Content generated or manipulated by AI systems** [Art. 52(3)]: Users of AI systems that generate or manipulate image, audio or video content (e.g., deepfakes) shall disclose that the content has been artificially generated or manipulated.
                    """)
                st.session_state.assessment_data['requires_transparency'] = requires_transparency
                
                # Conditional Compliance Questions based on EU relevance and high-risk classification
                is_eu = st.session_state.assessment_data.get('is_eu', False)
                if is_eu and high_risk_options:
                    st.markdown("#### Additional Compliance Questions for High-Risk Systems")
                    
                    risk_management = st.text_area(
                        "Do you have a documented risk management system in place?",
                        help="Include details about your risk identification, analysis, and mitigation processes"
                    )
                    st.session_state.assessment_data['risk_management'] = risk_management
                    
                    human_oversight = st.text_area(
                        "What measures ensure effective human oversight over your system?",
                        help="Describe how humans can intervene, override decisions, or interpret system outputs"
                    )
                    st.session_state.assessment_data['human_oversight'] = human_oversight
                    
                    data_protection = st.text_area(
                        "How do you ensure compliance with data protection regulations (e.g., GDPR)?",
                        help="Detail your data handling, processing, storage, and security measures"
                    )
                    st.session_state.assessment_data['data_protection'] = data_protection
                    
                    post_market = st.text_area(
                        "Do you have a plan for continuous monitoring and incident reporting?",
                        help="Include how you track system performance, identify issues, and report incidents"
                    )
                    st.session_state.assessment_data['post_market'] = post_market
                
                # Provider-specific question: show if role is 'Provider'
                role = st.session_state.assessment_data.get('role', "")
                if role == "Provider":
                    st.markdown("##### Provider-Specific Question")
                    
                    algorithmic_transparency = st.text_area(
                        "How do you document and explain the system's decision-making process?",
                        help="Detail your approach to algorithmic transparency and explainability"
                    )
                    st.session_state.assessment_data['algorithmic_transparency'] = algorithmic_transparency
                
                # Navigation buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.button("← Previous", on_click=prev_step)
                with col2:
                    st.button("Next →", key="next_2", on_click=next_step)
                
            elif st.session_state.current_step == 3:
                # SECTION 3: Operational Design Domain (ODD)
                st.markdown("### SECTION 3: Operational Design Domain (ODD)")
                
                environment = st.text_area(
                    "In what environment is your system intended to operate?",
                    key="form_environment",
                    value=st.session_state.assessment_data.get('environment', ''),
                    help="e.g., classroom, LMS, mobile app, corporate intranet, etc."
                )
                
                users = st.text_area(
                    "Who are the users and what are their characteristics?",
                    key="form_users",
                    value=st.session_state.assessment_data.get('users', ''),
                    help="Please specify both: 1) End users (e.g., job applicants, students, patients) who are affected by the system's decisions, and 2) Operators (e.g., HR personnel, teachers, doctors) who use or interpret the system's outputs. Include details like age ranges, digital literacy levels, and professional backgrounds."
                )
                
                input_data = st.text_area(
                    "What input data does your system rely on?",
                    key="form_input_data",
                    value=st.session_state.assessment_data.get('input_data', ''),
                    help="e.g., sensors, user data, documents, external APIs, etc."
                )
                
                temporal_constraints = st.text_area(
                    "Are there any temporal constraints or assumptions?",
                    key="form_temporal_constraints",
                    value=st.session_state.assessment_data.get('temporal_constraints', ''),
                    help="e.g., system used only during school hours, batch processing schedule, etc."
                )
                
                assumptions = st.text_area(
                    "What assumptions does the system make about users or environment?",
                    key="form_assumptions",
                    value=st.session_state.assessment_data.get('assumptions', ''),
                    help="e.g., minimum technical requirements, user familiarity with specific terms, etc."
                )
                
                # Navigation buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.button("← Previous", key="prev_3", on_click=prev_step)
                with col2:
                    selected_roles = st.session_state.assessment_data.get('role', [])
                    if selected_roles:  # Only enable completion if at least one role is selected
                        st.button("Complete Assessment", on_click=complete_assessment)
                    else:
                        st.button("Complete Assessment", disabled=True, help="Please select at least one role to complete the assessment")
            
            # Summary page
            if st.session_state.is_completed:
                st.markdown("### Assessment Summary")
                st.success(f"Assessment completed on {st.session_state.assessment_data.get('completion_date', '')}")
                
                with st.expander("View Assessment Details", expanded=True):
                    # SECTION 1
                    st.markdown("#### Jurisdiction & User Role")
                    st.write("EU Relevant:", "Yes" if st.session_state.assessment_data.get('is_eu', False) else "No")
                    
                    # Format roles to display as a comma-separated list
                    roles = st.session_state.assessment_data.get('role', [])
                    roles_str = ", ".join(roles) if roles else "None selected"
                    st.write("User Role(s):", roles_str)
                    
                    # SECTION 2
                    st.markdown("#### AI Risk Classification")
                    st.write("Primary Function:", st.session_state.assessment_data.get('primary_function', ''))
                    
                    # Format high-risk categories list
                    high_risk_options = st.session_state.assessment_data.get('high_risk_options', [])
                    high_risk_str = ", ".join(high_risk_options) if high_risk_options else "None selected"
                    st.write("High-Risk Categories:", high_risk_str)
                    
                    # Format prohibited tasks list
                    prohibited_tasks = st.session_state.assessment_data.get('prohibited_tasks', [])
                    prohibited_str = ", ".join(prohibited_tasks) if prohibited_tasks else "None selected"
                    st.write("Prohibited Tasks:", prohibited_str)
                    
                    st.write("Transparency Required:", "Yes" if st.session_state.assessment_data.get('requires_transparency', False) else "No")
                    
                    # Removed transparency implementation display
                    
                    # Additional compliance questions (if applicable)
                    is_eu = st.session_state.assessment_data.get('is_eu', False)
                    high_risk_options = st.session_state.assessment_data.get('high_risk_options', [])
                    
                    if is_eu and len(high_risk_options) > 0:
                        st.markdown("#### Additional Compliance Questions")
                        st.write("Risk Management System:", st.session_state.assessment_data.get('risk_management', ''))
                        st.write("Human Oversight Measures:", st.session_state.assessment_data.get('human_oversight', ''))
                        st.write("Data Protection Compliance:", st.session_state.assessment_data.get('data_protection', ''))
                        st.write("Post-Market Monitoring Plan:", st.session_state.assessment_data.get('post_market', ''))
                    
                # Provider-specific questions (if applicable)
                    if 'Provider' in st.session_state.assessment_data.get('role', []):
                        st.markdown("#### Provider-Specific Questions")
                        st.write("Algorithmic Transparency:", st.session_state.assessment_data.get('algorithmic_transparency', ''))
                    
                    # Deployer-specific questions (if applicable)
                    if 'Deployer' in st.session_state.assessment_data.get('role', []):
                        st.markdown("#### Deployer-Specific Questions")
                        st.write("Deployment Validation:", st.session_state.assessment_data.get('deployment_validation', ''))
                    
                    # Distributor-specific questions (if applicable)
                    if 'Distributor' in st.session_state.assessment_data.get('role', []):
                        st.markdown("#### Distributor-Specific Questions")
                        st.write("Compliance Verification:", st.session_state.assessment_data.get('compliance_verification', ''))
                    
                    # Importer-specific questions (if applicable)
                    if 'Importer' in st.session_state.assessment_data.get('role', []):
                        st.markdown("#### Importer-Specific Questions")
                        st.write("Import Verification:", st.session_state.assessment_data.get('import_verification', ''))
                    
                    # SECTION 3
                    st.markdown("#### Operational Design Domain")
                    st.write("Environment:", st.session_state.assessment_data.get('environment', ''))
                    st.write("User Characteristics:", st.session_state.assessment_data.get('users', ''))
                    st.write("Input Data:", st.session_state.assessment_data.get('input_data', ''))
                    st.write("Temporal Constraints:", st.session_state.assessment_data.get('temporal_constraints', ''))
                    st.write("System Assumptions:", st.session_state.assessment_data.get('assumptions', ''))
                
                # Generate compliance recommendations
                with st.expander("Compliance Recommendations", expanded=True):
                    is_eu = st.session_state.assessment_data.get('is_eu', False)
                    high_risk_options = st.session_state.assessment_data.get('high_risk_options', [])
                    prohibited_tasks = st.session_state.assessment_data.get('prohibited_tasks', [])
                    
                    if is_eu:
                        if len(high_risk_options) > 0:
                            st.warning("Your AI system appears to be classified as high-risk under the AI Act. Key requirements:")
                            recommendations = [
                                "**Risk Management System**: Implement and document a comprehensive risk management system",
                                "**Technical Documentation**: Maintain complete and up-to-date technical documentation",
                                "**Record Keeping**: Implement automatic logging capabilities",
                                "**Human Oversight**: Design and implement appropriate human oversight measures",
                                "**Accuracy & Robustness**: Ensure appropriate levels of accuracy, robustness and cybersecurity",
                                "**Conformity Assessment**: Complete the required conformity assessment procedure",
                                "**Registration**: Register your high-risk AI system in the EU database (when available)"
                            ]
                            for rec in recommendations:
                                st.markdown(f"- {rec}")
                                
                            # Deadline information
                            st.info("**Implementation Timeline**: High-risk AI systems must comply with the AI Act within 24 months of its entry into force (expected timeline: compliance required by mid-2026).")
                        
                        else:
                            st.info("Your AI system appears to be subject to the AI Act but may not be classified as high-risk. You should still implement good practices for AI governance.")
                        
                        if "None of the Above" not in prohibited_tasks and len(prohibited_tasks) > 0:
                            st.error("⚠️ **ALERT**: Your AI system may involve practices prohibited under the AI Act. Legal consultation is strongly recommended.")
                            
                            prohibited_explanations = {
                                "Subliminal Manipulation": "AI systems that deploy subliminal techniques to materially distort human behavior in a manner likely to cause harm",
                                "Social Scoring": "AI systems used by public authorities for evaluating or classifying individuals based on social behavior or personal characteristics",
                                "Real-time Biometric ID": "Use of real-time remote biometric identification systems in publicly accessible spaces for law enforcement purposes (with limited exceptions)",
                                "Exploitation of Vulnerabilities": "AI systems that exploit vulnerabilities of a specific group of persons due to their age, disability, or specific social or economic situation",
                                "Emotion Recognition in Workplace/Education": "Use of emotion recognition systems in workplaces or educational institutions",
                                "Predictive Policing Based on Profiling": "AI systems used for predictive policing based solely on profiling a person or assessing their risk of criminal behavior"
                            }
                            
                            st.markdown("**Your selected prohibited activities:**")
                            for task in prohibited_tasks:
                                if task in prohibited_explanations:
                                    st.markdown(f"- **{task}**: {prohibited_explanations[task]}")
                    else:
                        st.success("Based on your inputs, this mock analysis suggests your AI system may not be directly subject to the EU AI Act, but following good practices for AI governance is still recommended.")
                        st.info("Note: This is a simplified preliminary assessment for educational purposes only. For a definitive legal analysis, please consult with legal experts specializing in AI regulation.")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Option to start a new assessment
                    if st.button("Start New Assessment"):
                        st.session_state.current_step = 1
                        st.session_state.assessment_data = {}
                        st.session_state.is_completed = False
                        st.experimental_rerun()
                
                with col2:
                    # Option to download assessment report
                    df = pd.DataFrame([st.session_state.assessment_data])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Assessment Report",
                        data=csv,
                        file_name=f"ai_act_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
        else:
            # Standard form view (non-wizard mode)
            # SECTION 1: Jurisdiction & User Role
            st.markdown("### SECTION 1: Jurisdiction & User Role")
            is_eu = st.checkbox("Is your system made available in the EU or affects people in the EU?")
            # Role selection - changed to multiselect
            role = st.multiselect("What is your role regarding the AI system? (Select all that apply)",
                               ["Provider", "Deployer", "Distributor", "Importer"])
                               
            # Add role explanations in standard view too
            with st.expander("Need help understanding these roles?"):
                st.markdown("""
                **Provider** [Art. 3(2)]: You/your company develops the AI system (or has it developed for you)
                - *For product/project managers*: If you manage the team building the AI system
                
                **Deployer** [Art. 3(4)]: You/your company uses an AI system developed by another organization
                - *For product/project managers*: If you manage the implementation of a purchased AI system
                
                **Distributor** [Art. 3(7)]: You/your company makes an AI system available on the market (reselling)
                - *For product/project managers*: If you manage distribution of AI products to customers
                
                **Importer** [Art. 3(6)]: You/your company brings an AI system from outside the EU into the EU market
                - *For product/project managers*: If you manage importing AI systems from non-EU countries
                
                **Note**: Organizations often have multiple roles. For example, you might both develop and use AI systems.
                """)

            
            # SECTION 2: AI Risk Classification
            st.markdown("### SECTION 2: AI Risk Classification")
            primary_function = st.text_input("What is your system's primary function? (e.g., scoring students, matching CVs)")
            high_risk_options = st.multiselect("Does it fall into any of the following high-risk categories?",
                                              ["Education and vocational training", 
                                               "Employment, worker management and self-employment", 
                                               "Access to essential private/public services", 
                                               "Law enforcement", 
                                               "Migration, asylum and border control",
                                               "Administration of justice",
                                               "Critical infrastructure",
                                               "Product safety"])
            prohibited_tasks = st.multiselect("Does the system perform any prohibited tasks?",
                                             ["Subliminal Manipulation", "Social Scoring", "Real-time Biometric ID"])
            requires_transparency = st.checkbox("Does the system require transparency (e.g., it's a chatbot or deepfake)?")
            
            # Removed the transparency implementation question for simplicity

            
            # Conditional Compliance Questions based on EU relevance and high-risk classification
            if is_eu and high_risk_options:
                st.markdown("#### Additional Compliance Questions for High-Risk Systems")
                risk_management = st.text_input("Do you have a documented risk management system in place?")
                human_oversight = st.text_input("What measures ensure effective human oversight over your system?")
                data_protection = st.text_input("How do you ensure compliance with data protection regulations (e.g., GDPR)?")
                post_market = st.text_input("Do you have a plan for continuous monitoring and incident reporting?")
                
                # Provider-specific question: show if 'Provider' is in roles
                if 'Provider' in role:
                    st.markdown("##### Provider-Specific Question [Art. 11 & 13]")
                    algorithmic_transparency = st.text_input("How do you document and explain the system's decision-making process?")
                
                # Deployer-specific questions
                if 'Deployer' in role:
                    st.markdown("##### Deployer-Specific Question [Art. 29]")
                    deployment_validation = st.text_input("How do you validate the AI system before deployment?")
                
                # Distributor-specific questions
                if 'Distributor' in role:
                    st.markdown("##### Distributor-Specific Question [Art. 27]")
                    compliance_verification = st.text_input("How do you verify that systems you distribute comply with AI Act requirements?")
                
                # Importer-specific questions
                if 'Importer' in role:
                    st.markdown("##### Importer-Specific Question [Art. 26]")
                    import_verification = st.text_input("How do you ensure imported AI systems comply with EU requirements?")
            
            # SECTION 3: Operational Design Domain (ODD)
            st.markdown("### SECTION 3: Operational Design Domain (ODD)")
            environment = st.text_input("In what environment is your system intended to operate? (e.g., classroom, LMS, mobile app)")
            users = st.text_input("Who are the users and what are their characteristics?", 
                           help="Please specify both end users (affected by decisions) and operators (using the system)")
            st.caption("Example: End users: Job applicants (ages 18-65, varying digital literacy); Operators: HR staff (trained professionals)")

            input_data = st.text_input("What input data does your system rely on? (e.g., sensors, user data, documents)")
            temporal_constraints = st.text_input("Are there any temporal constraints or assumptions? (e.g., system used only during school hours)")
            assumptions = st.text_input("What assumptions does the system make about users or environment?")
            
            # Submit button for the standard form
            if st.button("Submit Assessment"):
                st.success("Assessment submitted!")
                
                # Could add saving functionality here
                # For now just display a confirmation message
                st.balloons()

if __name__ == "__main__":
    main()




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
        responses.append(LLMResponse(
            question_id=r['question_id'],
            response_text=r['response_text'],
            risk_flags=r['risk_flags'],
            risk_score=r['risk_score']
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
    
    # Tab 1: Onboarding/ODD
    with tabs[0]:
        st.header("Onboarding/ODD")
        st.info("This tab is under development. It will contain onboarding information and ODD details.")
    
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
                            help="View suggestions to reduce risk score (placeholder functionality)"
                        )
                        if fix_button:
                            st.info("Suggested fixes would be displayed here.")
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

if __name__ == "__main__":
    main()
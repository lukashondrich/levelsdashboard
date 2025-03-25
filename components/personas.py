import streamlit as st
from models.data_models import Persona
from utils.data_loader import load_personas, load_questions, load_llm_responses

def display_personas(tab):
    with tab:
        st.header("Personas")
        st.markdown("We suggest these personas as **mental models** for different user perspectives.")
        personas = load_personas()
        questions = load_questions()
        llm_responses = load_llm_responses()
        if not personas:
            st.warning("No personas found.")
        else:
            stats_col, filter_col = st.columns([1, 3])
            with stats_col:
                st.markdown("### Quick Stats:")
                st.markdown(f"- Total Personas: {len(personas)}")
                female = len([p for p in personas if p.gender == 'Female'])
                male = len([p for p in personas if p.gender == 'Male'])
                st.markdown(f"- Female: {female}")
                st.markdown(f"- Male: {male}")
            with filter_col:
                origins = ["All"] + sorted(list(set(p.origin for p in personas)))
                selected_origin = st.selectbox("Filter by origin:", origins, label_visibility="collapsed")
            filtered = personas if selected_origin == "All" else [p for p in personas if p.origin == selected_origin]
            st.markdown("## Job Candidates")
            for persona in filtered:
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 5])
                    with col1:
                        st.markdown(f"### {persona.name}")
                        st.markdown(f"**{persona.title}**")
                    with col2:
                        st.markdown(f"**Gender:** {persona.gender}")
                        st.markdown(f"**Nationality:** {persona.origin}")
                        st.markdown(f"**Education:** {persona.education.split(' from ')[0]}")
                        st.markdown(f"**Experience:** {persona.experience.split('.')[0]}")
                    with col3:
                        with st.expander("Bias Analysis"):
                            bias_data = {k: v for k, v in persona.bias_metrics.items() if k != 'other_bias'}
                            if bias_data:
                                import plotly.graph_objects as go
                                fig = go.Figure()
                                for bias_type, value in bias_data.items():
                                    display_name = ' '.join(bias_type.split('_')).title()
                                    color = "green" if value < 0.3 else "orange" if value < 0.6 else "red"
                                    fig.add_trace(go.Bar(
                                        x=[value],
                                        y=[display_name],
                                        orientation='h',
                                        marker=dict(color=color)
                                    ))
                                fig.update_layout(
                                    xaxis_title="Score",
                                    yaxis_title="Bias Type",
                                    xaxis=dict(range=[0, 1]),
                                    height=200,
                                    margin=dict(l=20, r=20, t=20, b=20),
                                    showlegend=False
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        with st.expander("Control Comparison"):
                            st.markdown(persona.control_comparison)
                        with st.expander("Associated Questions"):
                            if persona.questions_associated:
                                for q_id in persona.questions_associated:
                                    q_text = next((q.question_text for q in load_questions() if q.id == q_id), "Question not found")
                                    st.markdown(f"**{q_id}:** {q_text}")
                                    response = next((r for r in load_llm_responses() if r.question_id == q_id), None)
                                    if response:
                                        st.markdown("**Response:**")
                                        st.markdown(f"_{response.response_text}_")
                                        st.markdown(f"**Risk Flags:** {', '.join(response.risk_flags)}")
                                        if response.suggested_fix:
                                            st.info(f"**Suggested Fix:** {response.suggested_fix}")
                            else:
                                st.write("No questions associated with this persona.")
                st.divider()

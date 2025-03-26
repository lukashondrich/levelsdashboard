import streamlit as st
from utils.data_loader import load_llm_responses, load_questions

def display_llm_responses(tab):
    with tab:
        st.header("LLM Outputs")
        st.markdown("The LLM’s **outputs** to the test questions are listed below.")
        responses = load_llm_responses()
        questions = load_questions()
        if not responses:
            st.warning("No LLM Outputs found.")
        else:
            for response in responses:
                q_text = next((q.question_text for q in questions if q.id == response.question_id), "Question text not found")
                with st.container():
                    st.subheader(f"Question ID: {response.question_id}")
                    st.write(f"**Question:** {q_text}")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Response:** {response.response_text}")
                        st.write(f"**Risk Flags:** {', '.join(response.risk_flags)}")
                    with col2:
                        risk_percent = response.risk_score * 100
                        color = "green" if risk_percent < 25 else "orange" if risk_percent < 50 else "red"
                        st.markdown(
                            f"""
                            <div style="background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white;">
                                <h3 style="margin:0;">Risk Score</h3>
                                <h2 style="margin:0;">{risk_percent:.1f}%</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        if st.button("View Suggested Fix", key=f"fix_{response.question_id}", help="View suggestions to reduce risk score"):
                            if response.suggested_fix:
                                st.info(response.suggested_fix)
                            else:
                                st.info("No suggested fix available for this response.")
                    st.divider()

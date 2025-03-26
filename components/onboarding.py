import streamlit as st
from datetime import datetime

def ai_act_compliance_wizard(tabs):
    with tabs[0]:
        st.header("Onboarding")
        st.markdown("Fill in your **Operational Design Domain** (ODD). Complete a basic EU AI Act Compliance and ODD Assessment below to scope out your AI risks. ")
        if 'wizard_mode' not in st.session_state:
            st.session_state.wizard_mode = True
        wizard_mode = st.toggle("Enable Wizard Mode", value=st.session_state.wizard_mode)
        st.session_state.wizard_mode = wizard_mode
        
        if wizard_mode:
            if 'current_step' not in st.session_state:
                st.session_state.current_step = 1
            if 'assessment_data' not in st.session_state:
                st.session_state.assessment_data = {}
            if 'is_completed' not in st.session_state:
                st.session_state.is_completed = False

            def next_step():
                st.session_state.current_step += 1

            def prev_step():
                st.session_state.current_step -= 1

            def complete_assessment():
                st.session_state.is_completed = True
                st.session_state.assessment_data['completion_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            total_steps = 3
            progress = st.session_state.current_step / (total_steps + 1)
            st.progress(progress)
            st.info(f"Step {st.session_state.current_step} of {total_steps}")

            if st.session_state.current_step == 1:
                st.markdown("### SECTION 1: Jurisdiction & User Role")
                is_eu = st.checkbox("Is your system made available in the EU or affects people in the EU?",
                                    help="Check if deployed in EU or processing EU citizen data")
                st.session_state.assessment_data['is_eu'] = is_eu
                role = st.multiselect("What is your role regarding the AI system? (Select all that apply)",
                                      ["Provider", "Deployer", "Distributor", "Importer"],
                                      help="Select all roles that apply")
                with st.expander("Need help understanding these roles?"):
                    st.markdown("**Provider**: Develops the AI system\n\n**Deployer**: Uses an AI system\n\n**Distributor**: Makes the system available on the market\n\n**Importer**: Brings AI systems from outside the EU")
                st.session_state.assessment_data['role'] = role
                st.button("Next →", on_click=next_step, disabled=(not role))
            elif st.session_state.current_step == 2:
                st.markdown("### SECTION 2: AI Risk Classification")
                primary_function = st.text_input("What is your system's primary function?",
                                                 value=st.session_state.assessment_data.get('primary_function', ''),
                                                 help="e.g., scoring students, matching CVs")
                st.session_state.assessment_data['primary_function'] = primary_function
                high_risk_options = st.multiselect("Does it fall into any high-risk categories?",
                                                   ["Education and vocational training", "Employment", "Public services", "Law enforcement",
                                                    "Migration", "Administration of justice", "Critical infrastructure", "Product safety"],
                                                   default=st.session_state.assessment_data.get('high_risk_options', []),
                                                   help="Select applicable categories")
                st.session_state.assessment_data['high_risk_options'] = high_risk_options
                prohibited_tasks = st.multiselect("Does the system perform any prohibited tasks?",
                                                  ["Subliminal Manipulation", "Social Scoring", "Real-time Biometric ID",
                                                   "Exploitation of Vulnerabilities", "Emotion Recognition", "Predictive Policing", "None of the Above"],
                                                  help="Select all that apply")
                st.session_state.assessment_data['prohibited_tasks'] = prohibited_tasks
                requires_transparency = st.checkbox("Does the system require transparency (e.g., chatbot or deepfake)?")
                st.session_state.assessment_data['requires_transparency'] = requires_transparency

                if st.session_state.assessment_data.get('is_eu') and high_risk_options:
                    st.markdown("#### Additional Compliance Questions for High-Risk Systems")
                    st.session_state.assessment_data['risk_management'] = st.text_area("Documented risk management system?")
                    st.session_state.assessment_data['human_oversight'] = st.text_area("Measures for human oversight?")
                    st.session_state.assessment_data['data_protection'] = st.text_area("Compliance with data protection (e.g., GDPR)?")
                    st.session_state.assessment_data['post_market'] = st.text_area("Plan for continuous monitoring?")
                if "Provider" in st.session_state.assessment_data.get('role', []):
                    st.markdown("##### Provider-Specific Question")
                    st.session_state.assessment_data['algorithmic_transparency'] = st.text_area("How do you document your system's decision process?")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("← Previous", on_click=prev_step)
                with col2:
                    st.button("Next →", on_click=next_step)
            elif st.session_state.current_step == 3:
                st.markdown("### SECTION 3: Operational Design Domain (ODD)")
                st.session_state.assessment_data['environment'] = st.text_area("Environment where the system operates?",
                                                                               value=st.session_state.assessment_data.get('environment', ''))
                st.session_state.assessment_data['users'] = st.text_area("Who are the users? Provide details.")
                st.session_state.assessment_data['input_data'] = st.text_area("What input data does your system use?")
                st.session_state.assessment_data['temporal_constraints'] = st.text_area("Any temporal constraints?")
                st.session_state.assessment_data['assumptions'] = st.text_area("What assumptions does the system make?")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("← Previous", on_click=prev_step)
                with col2:
                    selected_roles = st.session_state.assessment_data.get('role', [])
                    st.button("Complete Assessment", on_click=complete_assessment, disabled=(not selected_roles))
            
            if st.session_state.get('is_completed'):
                st.markdown("### Assessment Summary")
                st.success(f"Assessment completed on {st.session_state.assessment_data.get('completion_date','')}")
                with st.expander("View Assessment Details", expanded=True):
                    st.write("EU Relevant:", "Yes" if st.session_state.assessment_data.get('is_eu') else "No")
                    st.write("User Role(s):", ", ".join(st.session_state.assessment_data.get('role', [])))
                    st.write("Primary Function:", st.session_state.assessment_data.get('primary_function', ''))
                    st.write("High-Risk Categories:", ", ".join(st.session_state.assessment_data.get('high_risk_options', [])))
                    st.write("Prohibited Tasks:", ", ".join(st.session_state.assessment_data.get('prohibited_tasks', [])))
                    st.write("Requires Transparency:", "Yes" if st.session_state.assessment_data.get('requires_transparency') else "No")
                    st.write("Environment:", st.session_state.assessment_data.get('environment', ''))
                    st.write("Users:", st.session_state.assessment_data.get('users', ''))
                    st.write("Input Data:", st.session_state.assessment_data.get('input_data', ''))
                    st.write("Temporal Constraints:", st.session_state.assessment_data.get('temporal_constraints', ''))
                    st.write("Assumptions:", st.session_state.assessment_data.get('assumptions', ''))
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Start New Assessment"):
                        st.session_state.current_step = 1
                        st.session_state.assessment_data = {}
                        st.session_state.is_completed = False
                        st.experimental_rerun()
                with col2:
                    import pandas as pd
                    df = pd.DataFrame([st.session_state.assessment_data])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Assessment Report",
                        data=csv,
                        file_name=f"ai_act_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        else:
            st.markdown("### Standard View")
            is_eu = st.checkbox("Is your system made available in the EU or affects people in the EU?")
            role = st.multiselect("What is your role regarding the AI system?",
                                  ["Provider", "Deployer", "Distributor", "Importer"])
            with st.expander("Need help understanding these roles?"):
                st.markdown("**Provider**: Develops the AI system\n\n**Deployer**: Uses an AI system\n\n**Distributor**: Makes the system available\n\n**Importer**: Brings systems from outside the EU")
            st.markdown("### AI Risk Classification")
            st.text_input("What is your system's primary function?")
            st.multiselect("High-risk categories?",
                           ["Education", "Employment", "Public services", "Law enforcement", "Migration", "Administration", "Critical infrastructure", "Product safety"])
            st.multiselect("Prohibited tasks?",
                           ["Subliminal Manipulation", "Social Scoring", "Real-time Biometric ID"])
            st.checkbox("Does the system require transparency?")
            if st.button("Submit Assessment"):
                st.success("Assessment submitted!")
                st.balloons()

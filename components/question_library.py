import streamlit as st
from utils.data_loader import load_questions

def display_question_library(tab):
    with tab:
        st.header("Question Library") 
        st.markdown("Here’s a library of **test questions**. You can use to simulate real-world interactions with the LLM. ")

        questions = load_questions()
        categories = ["All"] + sorted(list(set(q.category for q in questions)))
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            selected_category = st.selectbox("Filter by category:", categories)
        if selected_category == "All":
            filtered_questions = questions
            subcategories = ["All"]
        else:
            filtered_questions = [q for q in questions if q.category == selected_category]
            subcategories = ["All"] + sorted(list(set(q.subcategory for q in filtered_questions)))
        with filter_col2:
            if selected_category != "All":
                selected_subcategory = st.selectbox("Filter by subcategory:", subcategories)
                if selected_subcategory != "All":
                    filtered_questions = [q for q in filtered_questions if q.subcategory == selected_subcategory]
            else:
                st.text("Select a category first")
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
                        if st.button("Modify", key=f"modify_{question.id}", help="Placeholder functionality"):
                            st.info("Modification functionality would be implemented here.")
                st.divider()

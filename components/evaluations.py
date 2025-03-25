import streamlit as st
from utils.data_loader import load_evaluations
from utils.visualization import create_radar_chart

def display_evaluations(tab):
    with tab:
        st.header("Evaluation Score")
        evaluations = load_evaluations()
        if not evaluations:
            st.warning("No evaluations found.")
        else:
            all_categories = {}
            for eval_item in evaluations:
                for category, sub_scores in eval_item.scores.items():
                    if category not in all_categories:
                        all_categories[category] = set()
                    for sub in sub_scores.keys():
                        all_categories[category].add(sub)
            for category in all_categories:
                all_categories[category] = sorted(list(all_categories[category]))
            aggregated_scores = {cat: {sub: [] for sub in subs} for cat, subs in all_categories.items()}
            for eval_item in evaluations:
                for category, sub_scores in eval_item.scores.items():
                    for sub, score in sub_scores.items():
                        aggregated_scores[category][sub].append(score)
            avg_scores = {}
            for category, sub_scores in aggregated_scores.items():
                avg_scores[category] = {sub: (sum(scores)/len(scores) if scores else 0) for sub, scores in sub_scores.items()}
            st.write("## Evaluation by Category")
            num_categories = len(all_categories)
            charts_per_row = min(3, num_categories)
            rows_needed = (num_categories + charts_per_row - 1) // charts_per_row
            keys = list(all_categories.keys())
            for row in range(rows_needed):
                cols = st.columns(charts_per_row)
                for col_idx, col in enumerate(cols):
                    chart_idx = row * charts_per_row + col_idx
                    if chart_idx < num_categories:
                        category = keys[chart_idx]
                        subcategories = all_categories[category]
                        values = [avg_scores[category][sub] for sub in subcategories]
                        fig = create_radar_chart(values, subcategories, category)
                        with col:
                            st.plotly_chart(fig, use_container_width=True)

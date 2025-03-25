import os
import yaml
import streamlit as st
from typing import List
from models.data_models import Persona, Question, LLMResponse, Evaluation, Insight

def load_yaml_data(filename: str) -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "..", "domain_data", filename)
    try:
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return {}

def load_personas() -> List[Persona]:
    data = load_yaml_data("personas.yaml")
    personas = []
    if data and 'personas' in data:
        for p in data['personas']:
            personas.append(Persona(
                id=p['id'],
                name=p['name'],
                title=p['title'],
                gender=p['gender'],
                origin=p['origin'],
                experience=p['experience'],
                education=p['education'],
                profile_image=p['profile_image'],
                questions_associated=p['questions_associated'],
                bias_metrics=p['bias_metrics'],
                control_comparison=p['control_comparison']
            ))
    return personas

def load_questions() -> List[Question]:
    data = load_yaml_data("questions.yaml")
    questions = []
    if data and 'questions' in data:
        for q in data['questions']:
            questions.append(Question(
                id=q['id'],
                question_text=q['question_text'],
                category=q['category'],
                subcategory=q['subcategory']
            ))
    return questions

def load_llm_responses() -> List[LLMResponse]:
    data = load_yaml_data("llm_responses.yaml")
    responses = []
    if data and 'responses' in data:
        for r in data['responses']:
            responses.append(LLMResponse(
                question_id=r['question_id'],
                response_text=r['response_text'],
                risk_flags=r['risk_flags'],
                risk_score=r['risk_score'],
                suggested_fix=r.get('suggested_fix', None)
            ))
    return responses

def load_evaluations() -> List[Evaluation]:
    data = load_yaml_data("evaluation_scores.yaml")
    evaluations = []
    if data and 'evaluations' in data:
        for e in data['evaluations']:
            evaluations.append(Evaluation(
                question_id=e['question_id'],
                scores=e['scores'],
                feedback=e.get('feedback', None)
            ))
    return evaluations

def load_insights() -> List[Insight]:
    data = load_yaml_data("contributor_insights.yaml")
    insights = []
    if data and 'insights' in data:
        for i in data['insights']:
            insights.append(Insight(
                question_id=i['question_id'],
                reviewer=i['reviewer'],
                comment_text=i['comment_text']
            ))
    return insights

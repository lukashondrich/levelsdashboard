from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class Persona:
    id: str
    name: str
    title: str
    gender: str
    origin: str
    experience: str
    education: str
    profile_image: str
    questions_associated: List[str]
    bias_metrics: Dict[str, float]
    control_comparison: str

@dataclass
class Question:
    id: str
    question_text: str
    category: str
    subcategory: str

@dataclass
class LLMResponse:
    question_id: str
    response_text: str
    risk_flags: List[str]
    risk_score: float
    suggested_fix: Optional[str] = None

@dataclass
class Evaluation:
    question_id: str
    scores: Dict[str, Dict[str, float]]
    feedback: Optional[str] = None

@dataclass
class Insight:
    question_id: str
    reviewer: str
    comment_text: str

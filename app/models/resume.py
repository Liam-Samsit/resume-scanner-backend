from pydantic import BaseModel
from typing import List, Dict

class SkillSection(BaseModel):
    score: int
    matched: List[str]
    missing: List[str]

class MissingRanked(BaseModel):
    high_priority: List[str]
    medium_priority: List[str]
    low_priority: List[str]

class OverallStats(BaseModel):
    score: int
    total_keywords: int
    matched_keywords: int
    missing_keywords: int

class ResumeAnalysisResponse(BaseModel):
    overall: OverallStats
    technical_skills: SkillSection
    soft_skills: SkillSection
    missing_ranked: MissingRanked
    matched_in_order: List[str]
    missing_in_order: List[str]
    suggestions: List[str]

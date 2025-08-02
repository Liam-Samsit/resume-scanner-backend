import re
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))

MULTIWORD_TERMS = [
    "machine learning",
    "artificial intelligence",
    "data science",
    "unit testing",
    "project management",
    "user interface",
    "user experience",
    "cloud computing",
    "rest api",
    "version control",
]

SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "js": "javascript",
    "node": "nodejs",
    "node.js": "nodejs",
    "postgres": "postgresql",
    "sql server": "mssql",
    "c sharp": "c#",
    "cpp": "c++",
    "frontend": "front end",
    "backend": "back end",
    "ux": "user experience",
    "ui": "user interface",
}

WEIGHTS = {
    # Technical skills
    "python": 3, "fastapi": 3, "flutter": 3, "sql": 3,
    "postgresql": 3, "docker": 3, "linux": 3,
    "machine learning": 3, "artificial intelligence": 3,
    "javascript": 3, "react": 3, "nodejs": 3,
    "mssql": 3, "rest api": 3,

    # Soft skills
    "teamwork": 1, "communication": 1,
    "leadership": 1, "project management": 1
}

TECHNICAL_TERMS = {k for k, w in WEIGHTS.items() if w >= 3}
SOFT_TERMS = {k for k, w in WEIGHTS.items() if w == 1}

def preprocess_text(text: str) -> list:
    """Lowercase, clean, detect multi-word terms, normalize synonyms, remove stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\+#]", " ", text)

    for alias, standard in SYNONYMS.items():
        text = text.replace(alias, standard)

    detected_terms = []
    for phrase in MULTIWORD_TERMS:
        if phrase in text:
            detected_terms.append(phrase)
            text = text.replace(phrase, "")

    words = text.split()
    single_words = [word for word in words if word not in STOPWORDS and len(word) > 1]

    return detected_terms + single_words

def section_score(matched: set, job_terms: set) -> int:
    total = len(job_terms)
    if total == 0:
        return 0
    return int((len(matched) / total) * 100)

def compare_resume_to_job(resume_text: str, job_description: str = None,
                          custom_weights: dict = None, manual_keywords: dict = None) -> dict:
    # Merge default weights with custom weights
    active_weights = WEIGHTS.copy()
    if custom_weights:
        for k, v in custom_weights.items():
            active_weights[k.lower()] = int(v)

    resume_words = set(preprocess_text(resume_text))

    # Keep original order list
    if manual_keywords:
        job_words_list = [k.lower() for k in manual_keywords.keys()]
        for k, v in manual_keywords.items():
            active_weights[k.lower()] = int(v)
    else:
        job_words_list = preprocess_text(job_description)

    job_words_set = set(job_words_list)

    matched = [w for w in job_words_list if w in resume_words]
    missing = [w for w in job_words_list if w not in resume_words]

    matched_tech = [w for w in matched if active_weights.get(w, 1) >= 3]
    matched_soft = [w for w in matched if active_weights.get(w, 1) == 1]
    missing_tech = [w for w in missing if active_weights.get(w, 1) >= 3]
    missing_soft = [w for w in missing if active_weights.get(w, 1) == 1]

    # Scoring
    total_points = sum(active_weights.get(word, 1) for word in job_words_set)
    earned_points = sum(active_weights.get(word, 1) for word in matched)
    overall_score = int((earned_points / total_points) * 100) if total_points > 0 else 0

    tech_score = section_score(set(matched_tech), {w for w in job_words_set if active_weights.get(w, 1) >= 3})
    soft_score = section_score(set(matched_soft), {w for w in job_words_set if active_weights.get(w, 1) == 1})

    # Rank missing
    missing_ranked = {
        "high_priority": [w for w in missing if active_weights.get(w, 1) >= 4],
        "medium_priority": [w for w in missing if 2 <= active_weights.get(w, 1) <= 3],
        "low_priority": [w for w in missing if active_weights.get(w, 1) == 1]
    }

    suggestions = []
    if missing_ranked["high_priority"]:
        suggestions.append("🔥 High Priority: Add these key skills if you have them: " + ", ".join(missing_ranked["high_priority"]))
    if missing_ranked["medium_priority"]:
        suggestions.append("⚡ Medium Priority: Consider adding: " + ", ".join(missing_ranked["medium_priority"]))
    if missing_ranked["low_priority"]:
        suggestions.append("📎 Low Priority: Optional but nice to have: " + ", ".join(missing_ranked["low_priority"]))

    return {
        "overall": {
            "score": overall_score,
            "total_keywords": len(job_words_list),
            "matched_keywords": len(matched),
            "missing_keywords": len(missing)
        },
        "technical_skills": {
            "score": tech_score,
            "matched": matched_tech,
            "missing": missing_tech
        },
        "soft_skills": {
            "score": soft_score,
            "matched": matched_soft,
            "missing": missing_soft
        },
        "missing_ranked": missing_ranked,
        "matched_in_order": matched,
        "missing_in_order": missing,
        "suggestions": suggestions
    }




import re
from nltk.corpus import stopwords
from app.services.keywords import DEFAULT_KEYWORDS, DEFAULT_WEIGHTS
import nltk
nltk.data.path.append("./nltk_data")




STOPWORDS = set(stopwords.words("english"))

MULTIWORD_TERMS = [
    "machine learning", "artificial intelligence", "data science",
    "unit testing", "project management", "user interface", "user experience",
    "cloud computing", "rest api", "version control"
]

SYNONYMS = {
    "ml": "machine learning", "ai": "artificial intelligence",
    "js": "javascript", "node": "nodejs", "node.js": "nodejs",
    "postgres": "postgresql", "sql server": "mssql", "c sharp": "c#",
    "cpp": "c++", "frontend": "front end", "backend": "back end",
    "ux": "user experience", "ui": "user interface"
}

def preprocess_text(text: str) -> list:
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

def categorize_skills(skills_list):
    """Return a dict mapping category -> list of skills found."""
    categorized = {cat: [] for cat in DEFAULT_KEYWORDS.keys()}
    for skill in skills_list:
        for category, terms in DEFAULT_KEYWORDS.items():
            if skill in terms:
                categorized[category].append(skill)
                break
    # Remove empty categories
    categorized = {cat: vals for cat, vals in categorized.items() if vals}
    # ✅ Ensure all are strings
    categorized = {cat: [str(s) for s in vals] for cat, vals in categorized.items()}
    return categorized

def compare_resume_to_job(resume_text: str, job_description: str = None,
                          custom_weights: dict = None, manual_keywords: dict = None) -> dict:
    # Use default weights if none provided
    active_weights = DEFAULT_WEIGHTS.copy()
    if custom_weights:
        for k, v in custom_weights.items():
            active_weights[k.lower()] = int(v)

    resume_words = set(preprocess_text(resume_text))

    # Prepare job words list
    job_words_list = []

    # If job description provided → extract keywords
    if job_description:
        jd_terms = preprocess_text(job_description)
        job_words_list.extend(jd_terms)

    # If manual keywords provided → use them
    if manual_keywords:
        for k, v in manual_keywords.items():
            term = k.lower()
            job_words_list.append(term)
            active_weights[term] = int(v)  # manual override

    # If neither provided → use defaults
    if not job_description and not manual_keywords:
        for term in sum(DEFAULT_KEYWORDS.values(), []):
            job_words_list.append(term)

    # Deduplicate preserving order
    seen = set()
    job_words_list = [x for x in job_words_list if not (x in seen or seen.add(x))]
    job_words_set = set(job_words_list)

    # Match & missing
    matched = [w for w in job_words_list if w in resume_words]
    missing = [w for w in job_words_list if w not in resume_words]

    matched_tech = [w for w in matched if active_weights.get(w, 1) >= 3]
    matched_soft = [w for w in matched if active_weights.get(w, 1) == 1]
    missing_tech = [w for w in missing if active_weights.get(w, 1) >= 3]
    missing_soft = [w for w in missing if active_weights.get(w, 1) == 1]

    # Categorized matches/missing (✅ all string lists)
    matched_by_category = categorize_skills(matched)
    missing_by_category = categorize_skills(missing)

    # Scoring
    total_points = sum(active_weights.get(word, 1) for word in job_words_set)
    earned_points = sum(active_weights.get(word, 1) for word in matched)
    overall_score = int((earned_points / total_points) * 100) if total_points > 0 else 0

    tech_score = section_score(set(matched_tech), {w for w in job_words_set if active_weights.get(w, 1) >= 3})
    soft_score = section_score(set(matched_soft), {w for w in job_words_set if active_weights.get(w, 1) == 1})

    missing_ranked = {
        "high_priority": [str(w) for w in missing if active_weights.get(w, 1) >= 4],
        "medium_priority": [str(w) for w in missing if 2 <= active_weights.get(w, 1) <= 3],
        "low_priority": [str(w) for w in missing if active_weights.get(w, 1) == 1]
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
            "matched": [str(w) for w in matched_tech],
            "missing": [str(w) for w in missing_tech]
        },
        "soft_skills": {
            "score": soft_score,
            "matched": [str(w) for w in matched_soft],
            "missing": [str(w) for w in missing_soft]
        },
        "matched_by_category": matched_by_category,
        "missing_by_category": missing_by_category,
        "missing_ranked": missing_ranked,
        "matched_in_order": [str(w) for w in matched],
        "missing_in_order": [str(w) for w in missing],
        "suggestions": [str(s) for s in suggestions]
    }

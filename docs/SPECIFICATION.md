Got it — here’s your specification rewritten as a clean Markdown document without emojis.

````markdown
# Cahier de Charges — Resume Scanner Backend (FastAPI)

## 1. Purpose
A backend API that:
- Accepts resume and job description uploads
- Extracts text from files (PDF/DOCX)
- Analyzes resume content against job requirements
- Returns:
  - Matching keywords count
  - Missing important keywords
  - Overall score (0–100)
  - Improvement suggestions

---

## 2. Tech Stack
- Python 3.x
- FastAPI — API framework
- Uvicorn — server
- pdfminer.six — PDF parsing
- python-docx — DOCX parsing
- pydantic — request/response models
- python-multipart — file uploads
- (Optional) nltk or scikit-learn — for advanced text processing

---

## 3. API Endpoints

### 3.1 Health Check
**GET** `/health`  
**Purpose:** Verify API is running  
**Response:**
```json
{ "status": "ok" }
````

### 3.2 Upload Resume

**POST** `/upload-resume`

**Request:**

* Multipart form-data
* Fields:

  * `file`: Resume file (PDF/DOCX)
  * `job_description`: String OR file upload

**Process:**

1. Save temp file or process in memory
2. Extract text from resume & job description
3. Preprocess (lowercase, remove stopwords, tokenize)
4. Generate keyword list from job description
5. Compare with resume keywords
6. Calculate:

   * Matches
   * Missing keywords
   * Score
7. Return results

**Response Example:**

```json
{
  "score": 78,
  "matched_keywords": ["python", "sql", "fastapi"],
  "missing_keywords": ["docker", "linux"],
  "suggestions": [
    "Add 'docker' if you have experience",
    "Mention 'linux' in your experience section"
  ]
}
```

---

## 4. Processing Logic

### File Handling

* Accept PDF or DOCX
* Reject other formats
* Max file size: \~5MB

### Text Extraction

* pdfminer.six for PDF
* python-docx for DOCX

### Preprocessing

* Lowercase
* Remove punctuation
* Tokenize into words
* Remove stopwords (NLTK stopword list)

### Keyword Extraction (Job Description)

* Split into words
* Remove duplicates
* Keep nouns & verbs (optional advanced step)

### Scoring

* Assign weights (e.g., tech skills 3pts, soft skills 1pt)
* Calculate score: `(points / max_points) * 100`

### Suggestions

* For missing keywords: create simple tips

### Error Handling

* Invalid file type → HTTP 400
* Missing job description → HTTP 400
* Empty resume text → HTTP 422

---

## 5. Security

* File validation — check MIME type
* Size limits — reject very large uploads
* Temp file cleanup — delete after processing
* CORS control — allow only frontend domain in production

---

## 6. Future Features

* Grammar/readability check
* Section detection (e.g., Education, Experience)
* ATS-friendly formatting recommendations
* Multi-language support

---

## 7. Folder Structure

```
app/
  ├── __init__.py
  ├── main.py          # FastAPI app + routes
  ├── api/
  │   ├── __init__.py
  │   ├── routes.py    # API endpoints
  ├── services/
  │   ├── parser.py    # PDF/DOCX text extraction
  │   ├── analyzer.py  # keyword scoring logic
  ├── models/
  │   ├── __init__.py
  │   ├── resume.py    # pydantic schemas
requirements.txt
```




# Resume Analyzer API

A FastAPI-based backend service that analyzes resumes (PDF/DOCX) against a job description or custom keyword set.  
It extracts skills, categorizes them, calculates match scores, and returns actionable suggestions for improvement.

---

## Features
- Upload and parse **PDF/DOCX** resumes
- Match skills against:
  - Provided job description text
  - Custom keyword list with weights
  - Default predefined keyword set
- Categorize skills into:
  - Programming Languages
  - Frameworks & Libraries
  - Databases
  - Tools & Platforms
  - Development Concepts
  - Data & AI
  - Cybersecurity
  - Soft Skills
- Return:
  - Overall score
  - Technical & soft skills matched/missing
  - Categorized matched/missing skills
  - Ranked missing keywords by priority
  - Suggestions for improvement

---

## Tech Stack
- **Python 3.10+**
- **FastAPI** – API framework
- **Pydantic** – Data validation & response models
- **NLTK** – Natural language preprocessing
- **python-docx** – DOCX parsing
- **pdfminer.six** – PDF parsing

---

## Project Structure
```

app/
├── models/
│   └── resume.py        # Pydantic response models
├── routes/
│   └── resume.py        # API endpoints
├── services/
│   ├── analyzer.py      # Skill matching logic
│   ├── keywords.py      # Default skill keywords & weights
│   └── parser.py        # Resume text extraction
main.py                  # FastAPI entry point

````

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Liam-Samsit/resume-scanner-backend.git
cd resume-scanner-backend
````

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Example (only needed if you add DB or auth later)
ENV=development
```

---

## Running the Server

```bash
uvicorn main:app --reload
```

Server will run at: `http://127.0.0.1:8000`

---

## API Usage

### **POST** `/upload-resume`

Upload a resume and analyze it.

**Note:**

* You must provide **either** `job_description` **or** `keywords_json`
* If both are empty, the request will be rejected

**Form Data:**

| Field                | Type     | Required    | Description                                                                |
| -------------------- | -------- | ----------- | -------------------------------------------------------------------------- |
|  `file`            | File     | ✅           | PDF or DOCX resume                                                          |
|  `job_description` | String   | Conditional | Job description text. Required if `keywords_json` is empty                   |
|  `custom_weights`  | JSON str | ❌           | Keyword → weight map                                                        |
|  `keywords_json`   | JSON str | Conditional | Keyword → weight map (manual mode). Required if `job_description` is empty   |

**Example Request (cURL)**

```bash
curl -X POST "http://127.0.0.1:8000/upload-resume" \
  -F "file=@resume.pdf" \
  -F "job_description=We are looking for a Python developer with FastAPI experience"
```

**Example Response**

```json
{
  "overall": {
    "score": 85,
    "total_keywords": 50,
    "matched_keywords": 42,
    "missing_keywords": 8
  },
  "technical_skills": { ... },
  "soft_skills": { ... },
  "matched_by_category": { ... },
  "missing_by_category": { ... },
  "missing_ranked": { ... },
  "suggestions": [ ... ]
}
```

---

## Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature-name`)
5. Create a Pull Request

---

## License

MIT License © 2025 Khaled Sami Cheboui

# System Architecture

## Overview

The **Resume Scanner Backend** is a Python-based FastAPI application designed to analyze resumes and compare them against job descriptions or keyword sets. It extracts key information from resumes (PDF/DOCX), identifies skill matches and gaps, and returns structured insights. The system is container-friendly and deployable on platforms like Render.

---

## Folder Structure

```
resume-backend-scanner/
├── app/
│   ├── main.py              # Entry point and FastAPI setup
│   ├── api/routes.py        # API route definitions
│   ├── models/resume.py     # Response models with Pydantic
│   └── services/
│       ├── analyzer.py      # Core resume analysis logic
│       ├── keywords.py      # Keyword categories and default weights
│       └── parser.py        # Resume text extraction logic
├── docs/                    # Project documentation (incl. this file)
│   ├── ARCHITECTURE.md
│   ├── SPECIFICATION.md
│   └── API_ENDPOINTS.md
├── .env                     # Environment configuration (CORS, etc.)
├── .gitignore               # Git ignore rules
├── LICENSE                  # Licensing info
├── Procfile                 # Process definition for deployment
├── README.md                # Project overview
├── requirements.txt         # Python dependencies
├── .render/render.yaml      # Render.com deployment config
└── venv/                    # Virtual environment (ignored)
```

---

## Component Breakdown

### 1. **FastAPI App (`main.py`)**

* Initializes the application
* Loads environment variables using `dotenv`
* Handles CORS with allowed origins from `.env`
* Mounts API routes under `/`
* Provides a `/health` check endpoint

### 2. **API Layer (`routes.py`)**

* Contains the `/upload-resume` endpoint
* Accepts file uploads, job descriptions, and optional keyword/weight JSON
* Validates inputs and passes data to the analyzer service
* Returns structured `ResumeAnalysisResponse`

### 3. **Models (`resume.py`)**

* Defines the data schema for the API response using Pydantic
* Structures include:

  * Overall score and stats
  * Skill breakdown (technical and soft skills)
  * Match/miss details by category and priority
  * Suggestions based on missing skills

### 4. **Services**

#### a. `analyzer.py`

* Core logic for:

  * Preprocessing text (lowercasing, cleaning, synonyms, multiword terms)
  * Matching skills from resume against job keywords
  * Calculating scores and suggestions
  * Categorizing skills based on default taxonomy
* Combines default, manual, and job description-derived keywords

#### b. `parser.py`

* Extracts text from uploaded PDF or DOCX resumes
* Uses `pdfminer` for PDFs and `python-docx` for DOCX

#### c. `keywords.py`

* Contains a curated list of categorized keywords
* Defines default weights (technical: 3, soft skills: 1)
* Used as fallback when job description or manual keywords are missing

---

## Deployment

### Platform: **Render.com**

* Deployment config defined in `.render/render.yaml`
* Python version pinned to 3.9.0
* `nltk stopwords` downloaded during build
* Starts the app using `uvicorn`
* Expects a `PORT` environment variable

### Procfile (for alternative deployment)

```
web: gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:10000
```

---

## Environment Variables

| Key              | Purpose                                    |
| ---------------- | ------------------------------------------ |
| ALLOWED\_ORIGINS | Sets CORS origins (e.g. localhost:3000)    |
| PYTHON\_VERSION  | Specifies Python version for Render deploy |

---

## Technologies Used

* **FastAPI**: Web framework
* **Uvicorn + Gunicorn**: ASGI and production server
* **NLTK**: Stopword removal
* **pdfminer.six / python-docx**: Resume text extraction
* **Pydantic**: Data validation
* **dotenv**: Environment variable loading

---

## Extensibility

* Additional skill categories can be added in `keywords.py`
* Scoring system can be tweaked via `DEFAULT_WEIGHTS`
* Resume preprocessing handles synonyms and multi-word phrases, easily extendable

---

## Next Docs

* \[✔️] **ARCHITECTURE.md**: System design and component breakdown
* \[⬜] **SPECIFICATION.md**: Functional and non-functional system requirements
* \[⬜] **API\_ENDPOINTS.md**: Endpoint descriptions, input/output schemas

# Resume Scanner Backend – Specification

## 1. Overview

The Resume Scanner Backend is a RESTful API service that:
- Parses resumes (PDF or DOCX)
- Extracts relevant information (skills, tools)
- Matches the resume with a given job description
- Returns insights like match percentage and missing keywords

This service is intended for use in a larger application (e.g., job application automation, HR tool, student CV analysis system, etc.).

---

## 2. Goals

- Automate resume parsing and job matching
- Provide an easy-to-use API for frontend or CLI tools
- Ensure accuracy and extensibility in data extraction

---

## 3. Features

- Resume parsing via `/parse_resume`
- Resume-job description matching via `/match_job_description`
- Keyword-based scoring system
- Simple file upload using `multipart/form-data`
- JSON-based responses for easy integration
- Basic root endpoint for server health

---

## 4. Functional Requirements

- ✅ Upload PDF or DOCX resumes
- ✅ Extract candidate data (skills, tools, education level)
- ✅ Accept raw job descriptions via POST request
- ✅ Return matching results (score, matched & missing keywords)
- ✅ Return structured JSON for every endpoint

---

## 5. Non-Functional Requirements

-  Runs on FastAPI for lightweight backend performance
-  Easily testable using tools like cURL or Postman
-  CORS enabled for frontend compatibility
-  Dependency management using `requirements.txt`
-  No authentication required (initial version)

---

## 6. Technologies Used

| Category           | Technology     |
|--------------------|----------------|
| Backend Framework  | FastAPI        |
| Resume Parsing     | python-docx, PyPDF2 |
| Matching Logic     | Custom keyword scoring |
| Deployment         | Uvicorn (local), GitHub (source control) |
| Environment        | Python 3.11+   |

---

## 7. Assumptions

- Resumes are mostly in English
- Users submit reasonably structured resumes
- Job descriptions are free-form text (not formal JSON schemas)
- Keyword matching is based on literal terms, not NLP semantics (for now)

---

## 8. Future Improvements

-  Add authentication (API keys or OAuth2)
-  Improve matching with NLP and embeddings (e.g. spaCy, BERT)
-  Support for more file types (e.g., images or HTML)
-  Admin dashboard or frontend viewer
-  Logging and monitoring
-  Multi-language support
-  Deployment to a cloud provider (e.g. Render, Railway, Vercel backend)


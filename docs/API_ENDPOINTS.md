# API Endpoints

This document describes the available API endpoints for the Resume Scanner Backend.

Base URL:
````

[http://localhost:8000](http://localhost:8000)

````

---

### `POST /parse_resume`

**Description**:  
Accepts a resume file and parses it to extract useful candidate information.

**Auth required**: No

**Form Data**:
- `file`: `multipart/form-data` – The resume file (PDF or DOCX)

📄 **Example using cURL**:
```bash
curl -X POST http://localhost:8000/parse_resume \
  -F "file=@/path/to/resume.pdf"
````

**Response**:

```json
{
  "name": "Khaled Sami Cheboui",
  "email": "example@mail.com",
  "phone": "+213 555 555 555",
  "skills": ["Python", "FastAPI", "SQL"],
  "experience": [...],
  "education": [...],
  "summary": "..."
}
```

**Status codes**:

* `200 OK` – Resume parsed successfully
* `400 Bad Request` – No file uploaded or unsupported file type
* `500 Internal Server Error` – Unexpected server-side error

---

### `POST /match_job_description`

**Description**:
Matches the parsed resume content with a given job description and returns relevant insights.

**Auth required**: No

**JSON Body**:

```json
{
  "resume_text": "Extracted resume text or structured data",
  "job_description": "The job description text"
}
```

**Response**:

```json
{
  "match_score": 0.87,
  "matched_keywords": ["FastAPI", "Python", "REST"],
  "missing_keywords": ["Docker", "CI/CD"],
  "summary": "Strong match with the backend skill requirements..."
}
```

**Status codes**:

* `200 OK` – Match successful
* `400 Bad Request` – Malformed request body
* `500 Internal Server Error` – Processing error

---

### `GET /`

**Description**:
Health check or root endpoint to verify the server is running.

**Auth required**: No

**Response**:

```json
{
  "message": "Resume Scanner Backend is running."
}
```

**Status codes**:

* `200 OK` – Server is up and responding

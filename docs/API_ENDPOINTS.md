# API Endpoints

This document describes the public API endpoints provided by the Resume Scanner Backend.
All endpoints follow RESTful conventions and use JSON for both input (where applicable) and output.

---

## Base URL

```
https://<i'll fill this later>.onrender.com
```

---

## Health Check

### `GET /health`

Check if the API is running.

**Response**

```json
{
  "status": "ok"
}
```

---

## Upload Resume

### `POST /upload-resume`

Analyze a resume file against a job description and/or a custom keyword list.

**Consumes:**

* `multipart/form-data`

**Form Fields:**

| Field             | Type          | Required | Description                                                        |
| ----------------- | ------------- | -------- | ------------------------------------------------------------------ |
| `file`            | File          | Yes      | PDF or DOCX file containing the resume                             |
| `job_description` | String        | No       | Raw job description text                                           |
| `custom_weights`  | String (JSON) | No       | JSON object with term-weight mappings, e.g. `{ "python": 4 }`      |
| `keywords_json`   | String (JSON) | No       | JSON object with keyword-to-weight mapping, e.g. `{ "docker": 3 }` |

> **Note:** At least one of `job_description` or `keywords_json` is recommended. If both are omitted, default keyword sets will be used.

**Accepted File Types:**

* `.pdf`
* `.docx`

**Response:** [`ResumeAnalysisResponse`](#resumeanalysisresponse)

---

## Models

### `ResumeAnalysisResponse`

```json
{
  "overall": {
    "score": 85,
    "total_keywords": 40,
    "matched_keywords": 34,
    "missing_keywords": 6
  },
  "technical_skills": {
    "score": 90,
    "matched": ["python", "docker"],
    "missing": ["kubernetes"]
  },
  "soft_skills": {
    "score": 70,
    "matched": ["teamwork", "communication"],
    "missing": ["time management"]
  },
  "matched_by_category": {
    "programming_languages": ["python"],
    "tools_platforms": ["docker"]
  },
  "missing_by_category": {
    "tools_platforms": ["kubernetes"]
  },
  "missing_ranked": {
    "high_priority": ["kubernetes"],
    "medium_priority": [],
    "low_priority": ["time management"]
  },
  "matched_in_order": ["python", "docker", "teamwork"],
  "missing_in_order": ["kubernetes", "time management"],
  "suggestions": [
    "🔥 High Priority: Add these key skills if you have them: kubernetes",
    "📎 Low Priority: Optional but nice to have: time management"
  ]
}
```

---

## Errors

Errors return standard JSON error responses.

```json
{
  "error": "Description of what went wrong"
}
```

Examples:

* Unsupported file type
* Invalid or unreadable resume
* Malformed JSON in `custom_weights` or `keywords_json`

---

## Notes

* CORS is enabled with allowed origins configured via `.env` using `ALLOWED_ORIGINS`
* This backend supports analysis even when job descriptions or keyword lists are omitted, by falling back to built-in defaults
* Additional info on scoring logic, keyword categories, and customization will be documented in `SPECIFICATION.md`

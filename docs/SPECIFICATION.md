# 📄 Specification: Resume Scanner Backend

## Overview

This backend service, built with **FastAPI**, provides a resume scanning and analysis system. It allows users to upload resumes (PDF or DOCX), optionally provide job descriptions or keyword lists, and receive structured feedback about how well the resume matches the target requirements.

---

## Purpose

The purpose of this backend is to:

* Extract text from uploaded resumes.
* Analyze the text against a provided job description or list of keywords.
* Score and rank skills by relevance and priority.
* Offer detailed suggestions for improvement.

It is designed for integration with a frontend (e.g., Flutter Web) and exposes RESTful API endpoints to perform these tasks.

---

## Supported File Types

* `.pdf`
* `.docx`

MIME types accepted:

* `application/pdf`
* `application/vnd.openxmlformats-officedocument.wordprocessingml.document`

---

## Input Methods

A POST request to `/upload-resume` accepts the following **form-data** fields:

| Field             | Type          | Required | Description                                                  |
| ----------------- | ------------- | -------- | ------------------------------------------------------------ |
| `file`            | UploadFile    | Yes      | Resume in PDF or DOCX format.                                |
| `job_description` | string        | No\*     | Job description in plain text.                               |
| `keywords_json`   | string (JSON) | No\*     | JSON object containing custom keywords and optional weights. |
| `custom_weights`  | string (JSON) | No       | JSON object mapping keywords to custom weights.              |

> ⚠️ **Note:** Either `job_description` or `keywords_json` **must be provided**. If both are omitted, the analyzer defaults to a predefined keyword set.

---

## Processing Workflow

1. **Validation & Sanitization**

   * Ensures the file is of allowed type by both MIME type and extension.
   * Parses `custom_weights` and `keywords_json` if provided.

2. **Text Extraction**

   * Uses `pdfminer` or `python-docx` to extract readable text from the uploaded resume.

3. **Text Preprocessing**

   * Lowercases, removes special characters.
   * Expands common synonyms (e.g., `ml` to `machine learning`).
   * Handles multi-word skills separately (e.g., `project management`).
   * Removes stopwords and single-character noise.

4. **Keyword Matching & Scoring**

   * Matches keywords from job description or keyword list with resume text.
   * Categorizes skills (technical vs soft).
   * Assigns weights using:

     * Default system.
     * Provided `custom_weights` (overrides default).
   * Calculates overall, technical, and soft skills scores.
   * Ranks missing terms by priority (high, medium, low).

5. **Suggestions**

   * Suggests skills to improve match, based on missing high- and medium-priority keywords.

---

## Output (JSON Response)

Example structure of the response:

```json
{
  "overall": {
    "score": 74,
    "total_keywords": 50,
    "matched_keywords": 37,
    "missing_keywords": 13
  },
  "technical_skills": {
    "score": 81,
    "matched": [...],
    "missing": [...]
  },
  "soft_skills": {
    "score": 60,
    "matched": [...],
    "missing": [...]
  },
  "matched_by_category": {
    "frameworks_libraries": [...],
    "databases": [...]
  },
  "missing_by_category": {
    "tools_platforms": [...],
    "data_ai": [...]
  },
  "missing_ranked": {
    "high_priority": [...],
    "medium_priority": [...],
    "low_priority": [...]
  },
  "matched_in_order": [...],
  "missing_in_order": [...],
  "suggestions": [
    "🔥 High Priority: Add these key skills if you have them: ...",
    "⚡ Medium Priority: Consider adding: ..."
  ]
}
```

---

## Keyword System

### Default Keyword Groups

Keywords are organized into the following categories:

* `programming_languages`
* `frameworks_libraries`
* `databases`
* `tools_platforms`
* `dev_concepts`
* `data_ai`
* `cybersecurity`
* `soft_skills`

### Default Weights

* Technical keywords: weight `3`
* Soft skills: weight `1`

Custom weights provided by the user override defaults per keyword.

---

## Health Check

* **GET** `/health`
* Response: `{ "status": "ok" }`

---

## Notes

* If both `job_description` and `keywords_json` are missing, default keyword list is used.
* Invalid or unreadable resume files return appropriate error messages.
* All processing is handled asynchronously when reading files.

---

## Author

**Khaled Sami Cheboui**
GitHub Repo: [resume-scanner-backend](https://github.com/Liam-Samsit/resume-scanner-backend.git)

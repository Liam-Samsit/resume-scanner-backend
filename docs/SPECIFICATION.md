# Resume Scanner Backend Specification

## Project Title

Resume Scanner Backend

## Author

**Khaled Sami Cheboui**
[GitHub Repository](https://github.com/Liam-Samsit/resume-scanner-backend.git)

## Description

The Resume Scanner is a RESTful API built with FastAPI that compares the skills and keywords in a resume against job descriptions or predefined keywords. It calculates a match score using customizable weights for keywords, skills, and experience, returning results in JSON format. This backend powers a frontend where users can upload resumes and receive feedback on how well they match given job requirements.

## Objectives

* Parse and process PDF resumes.
* Extract and clean text data.
* Match resume contents against job descriptions or keywords.
* Allow customization of weights for different match criteria.
* Return match results including visual score values.

## Technologies Used

* **FastAPI** – Web framework
* **Python 3.11** – Language
* **Uvicorn** – ASGI server
* **PyMuPDF** – PDF parsing
* **Scikit-learn** – Text processing (TF-IDF)
* **Pydantic** – Data validation
* **CORS middleware** – Enable frontend-backend communication

## Features

* Upload resume (PDF)
* Upload job description (optional)
* Upload keywords (optional)
* Upload custom weights (optional)
* Score generation with circle and bar metrics
* Default fallback logic for missing fields

## Input Parameters (Form Data)

| Name              | Type   | Required               | Description                                                                       |
| ----------------- | ------ | ---------------------- | --------------------------------------------------------------------------------- |
| `cv_file`         | File   | Yes                    | Resume PDF to analyze                                                             |
| `job_description` | String | Conditionally required | Job post text. Required if `keywords` is not provided.                            |
| `keywords`        | File   | Conditionally required | Plain text file with keyword list. Required if `job_description` is not provided. |
| `weights`         | File   | Optional               | JSON file containing custom weights. If not provided, defaults are used.          |

## Weight Format

Example JSON structure:

```json
{
  "experience": 1.2,
  "skills": 1.5,
  "keywords": 1.0
}
```

## Default Keywords and Weights

* If the user does not upload keywords, a default extensive keyword list is used.
* If the user does not upload weights, a default set is used.

## Scoring Logic

* Extracted resume text is processed via TF-IDF.
* Skills and keywords are matched against the resume content.
* A weighted score is calculated and broken into 3 categories: skills, keywords, and experience.
* Each component score contributes to a total match percentage.

## Output

Returns a JSON response containing:

```json
{
  "score": 76.3,
  "circle_score": 76.3,
  "keywords_score": 85.0,
  "skills_score": 68.0,
  "experience_score": 60.0
}
```

## API Behavior Summary

* If both `keywords` and `job_description` are missing, request is rejected.
* If only one is present, matching proceeds using the available data.
* If weights are missing, the system falls back to default values.

## Usage Scenarios

* Help job applicants tailor resumes to job posts.
* Help recruiters filter candidates based on resume match scores.
* Resume improvement feedback based on skill/keyword match.

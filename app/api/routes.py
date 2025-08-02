from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.services import parser, analyzer
import json
from app.models.resume import ResumeAnalysisResponse
from fastapi.responses import JSONResponse

def error_response(message: str, status_code: int = 400):
    return JSONResponse(status_code=status_code, content={"error": message})

router = APIRouter()

@router.post("/upload-resume", response_model=ResumeAnalysisResponse)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    custom_weights: Optional[str] = Form(None),
    keywords_json: Optional[str] = Form(None)
):
    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        return error_response("Invalid file type. Only PDF and DOCX allowed.", 400)

    # Ensure at least one mode of keyword input is provided
    if not job_description and not keywords_json:
        return error_response("Please provide either a job description or a keyword list.", 400)

    resume_text = await parser.extract_text(file)
    if not resume_text.strip():
        return error_response("Resume text is empty or could not be read.", 422)

    # Parse custom weights
    weights_dict = {}
    if custom_weights:
        try:
            weights_dict = json.loads(custom_weights)
            if not isinstance(weights_dict, dict):
                raise ValueError
        except Exception:
            return error_response("custom_weights must be a valid JSON object.", 400)

    # Parse manual keywords
    keywords_list = None
    if keywords_json:
        try:
            keywords_list = json.loads(keywords_json)
            if not isinstance(keywords_list, dict):
                raise ValueError
        except Exception:
            return error_response("keywords_json must be a valid JSON object.", 400)

    results = analyzer.compare_resume_to_job(
        resume_text,
        job_description,
        custom_weights=weights_dict,
        manual_keywords=keywords_list
    )

    return results

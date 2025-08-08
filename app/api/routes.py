from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.services import parser, analyzer
import json
import os
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
    allowed_exts = [".pdf", ".docx"]

    ext = os.path.splitext(file.filename)[1].lower()

    # Hybrid file type check hehe
    if not (
        (file.content_type and file.content_type in allowed_types) or
        (ext in allowed_exts)
    ):
        return error_response("Invalid file type. Only PDF and DOCX allowed.", 400)


    # Extracting text from resume
    resume_text = await parser.extract_text(file)
    if not resume_text.strip():
        return error_response("Resume text is empty or could not be read.", 422)

    # Parsing the custom weights
    weights_dict = {}
    if custom_weights:
        try:
            weights_dict = json.loads(custom_weights)
            if not isinstance(weights_dict, dict):
                raise ValueError
        except Exception:
            return error_response("custom_weights must be a valid JSON object.", 400)

    # Parsing keywords JSON
    keywords_list = None
    if keywords_json:
        try:
            keywords_list = json.loads(keywords_json)
            if not isinstance(keywords_list, dict):
                raise ValueError
        except Exception:
            return error_response("keywords_json must be a valid JSON object.", 400)

    # Pass both job_description and keywords_list to analyzer because why not
    results = analyzer.compare_resume_to_job(
        resume_text,
        job_description=job_description,
        custom_weights=weights_dict,
        manual_keywords=keywords_list
    )
    print("✅ Results:", results)
    print("📤 Returning:", ResumeAnalysisResponse(**results).dict())
    return ResumeAnalysisResponse(**results)



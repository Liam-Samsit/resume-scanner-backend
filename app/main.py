import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import routes

# Load environment variables from .env (for local development only)
# Idk why this doesn't work as intended on render
load_dotenv()

# Use OS environment variables directly to support Render
frontend_origin_1 = os.environ.get("FRONTEND_ORIGIN_1", "")
frontend_origin_2 = os.environ.get("FRONTEND_ORIGIN_2", "")

# Filtering out any empty entries
origins = [o for o in [frontend_origin_1, frontend_origin_2] if o]

app = FastAPI(
    title="Resume Scanner API",
    description="Backend for analyzing resumes against job descriptions",
    version="1.0.0"
)

# CORS setup (I don't like this part)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including routes
app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


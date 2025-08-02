from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

app = FastAPI(
    title="Resume Scanner API",
    description="Backend for analyzing resumes against job descriptions",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to frontend domain in production
    # allow_origins=["https://my-flutter-web-url.com"]

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

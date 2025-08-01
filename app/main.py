from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS so Flutter can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Resume Scanner API running"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    # For now, just confirm upload works
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

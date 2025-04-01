from fastapi import FastAPI, File, UploadFile
from app.matcher import compute_similarity
from app.parser import extract_text_from_pdf

app = FastAPI()

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)
    return {"extracted_text": text}

@app.post("/match_resume/")
async def match_resume(file: UploadFile = File(...)):
    job_description = "We are looking for a trained data collector. Information Technology Specialist for our relational database. Database design. System analysis. Object oriented. It networking"
    resume_text = extract_text_from_pdf(file)
    similarity_score = compute_similarity(resume_text, job_description)
    return {"similarity_score": similarity_score}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
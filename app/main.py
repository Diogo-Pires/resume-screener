from bson import ObjectId
from fastapi import FastAPI, File, Form, UploadFile
from app.database import get_job_collection, get_resume_collection
from app.matcher import compute_similarity
from app.parser import extract_entities, extract_text_from_pdf

app = FastAPI()

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)
    return {"extracted_text": text}

@app.post("/add_job/")
def add_job(description: str):
    """Add a new job description."""
    job_id = get_job_collection().insert_one({"description": description}).inserted_id
    return {"job_id": str(job_id)}

@app.post("/match_resume/")
async def match_resume(file: UploadFile = File(...), job_id: str = Form(...)):
    """Match a resume to a job description and store the result."""
    print()
    job = get_job_collection().find_one({"_id": ObjectId(job_id)})
    if not job:
        return {"error": "Job ID not found"}
    
    resume_text = extract_text_from_pdf(file)
    entities = extract_entities(resume_text)
    similarity_score = compute_similarity(resume_text, job["description"])
    
    get_resume_collection().insert_one({
        "job_id": job_id,
        "entities": entities, 
        "resume_text": resume_text,
        "similarity_score": similarity_score
    })
    
    return {"similarity_score": similarity_score}

@app.get("/ranked_resumes/")
def get_ranked_resumes(job_id: str):
    """Retrieve and rank resumes for a specific job."""
    resumes = list(get_resume_collection().find({"job_id": job_id}).sort("similarity_score", -1))
    return {"ranked_resumes": [{"name": r["name"], "similarity_score": r["similarity_score"]} for r in resumes]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
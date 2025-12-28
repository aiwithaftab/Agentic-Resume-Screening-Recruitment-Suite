import os
import csv
import logging
from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, CandidateRecord
from PyPDF2 import PdfReader

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Agentic Resume Screening System")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Save to CSV
def save_to_csv(filename, score, reasoning):
    file_path = "shortlisted_candidates.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["File Name", "Final Score", "Reasoning"])
        writer.writerow([filename, score, reasoning])

# PDF Text Extraction
def extract_text_from_pdf(file_path):
    """Extract text from PDF safely"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
        return text
    except Exception as e:
        logging.warning(f"Failed to extract text from {file_path}: {e}")
        return ""

# Compute Numeric Score
def compute_score(jd_text, resume_text):
    """Compute a numeric score based on keyword match"""
    jd_words = set([w.lower() for w in jd_text.split() if len(w) > 2])
    resume_words = set([w.lower() for w in resume_text.split() if len(w) > 2])
    if not jd_words:
        return 0.0
    matched = jd_words & resume_words
    score = (len(matched) / len(jd_words)) * 100
    return round(score, 1)

# AI Agent Controller
def ai_agent_controller(resume_path, jd_text):
    resume_text = extract_text_from_pdf(resume_path)
    score = compute_score(jd_text, resume_text)
    reasoning = f"Matched {score}% of JD keywords."
    return {"score": {"final_score": score}, "step": reasoning}

# Health Check
@app.get("/")
def health():
    return {"message": "Agentic API is live!"}

# Screen Resume Endpoint
@app.post("/screen-resume")
async def screen_resume(
    file: UploadFile = File(...),
    jd: str = Form(...),
    db: Session = Depends(get_db)
):
    os.makedirs("data", exist_ok=True)
    temp_path = os.path.join("data", file.filename)

    # Save uploaded PDF
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run agent to compute score
    result = ai_agent_controller(temp_path, jd)
    logging.info(f"AI Agent Result: {result}")

    # Extract numeric score safely
    score_data = result.get("score", {})
    numerical_score = 0.0
    if isinstance(score_data, dict):
        numerical_score = score_data.get("final_score", 0.0)
    else:
        try:
            numerical_score = float(score_data)
        except:
            numerical_score = 0.0

    # Safe reasoning
    strategy_reasoning = f"Agent Strategy: {result.get('step', 'No reasoning provided')}"

    # Save to DB
    db_candidate = CandidateRecord(
        file_name=file.filename,
        final_score=numerical_score,
        reasoning=strategy_reasoning
    )
    db.add(db_candidate)
    db.commit()

    # Save to CSV
    save_to_csv(file.filename, numerical_score, strategy_reasoning)

    return {"status": "Success", "analysis": result}

# Fetch Candidate History
@app.get("/candidates")
def view_history(db: Session = Depends(get_db)):
    return db.query(CandidateRecord).all()

# Chatbot Skeleton
@app.post("/chat-agent")
def chat_endpoint(payload: dict):
    question = payload.get("question", "")
    answer = f"Simulated AI answer for: {question}"
    return {"answer": answer}

# Semantic Search
@app.get("/semantic-search")
def semantic_find(skill: str, db: Session = Depends(get_db)):
    candidates = db.query(CandidateRecord).all()
    results = []
    for c in candidates:
        if skill.lower() in (c.reasoning or "").lower() or skill.lower() in (c.file_name or "").lower():
            results.append({"resume_id": c.file_name, "distance": 0.1})
    return {"query": skill, "results": results}

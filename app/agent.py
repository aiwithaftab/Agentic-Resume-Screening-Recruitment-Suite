import os
from groq import Groq
from dotenv import load_dotenv
from .parser import extract_text_from_pdf
from .scorer import compute_resume_score

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_agent_controller(pdf_path: str, job_description: str):
    # 1️⃣ Extract text
    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text:
        return {"step": "ERROR", "error": "❌ Resume text extraction failed"}

    # 2️⃣ Ask Model
    prompt = f"""
    You are an AI agent deciding processing steps.
    Respond EXACTLY with one word: PARSE, SCORE, or FULL.

    Resume: {resume_text[:1200]}
    Job Description: {job_description[:800]}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        decision = response.choices[0].message.content.strip().upper()

    except Exception as e:
        return {"step": "ERROR", "error": f"Groq API error: {str(e)}"}

# 3️⃣ Execute Action
    if decision == "PARSE":
        return {"step": "PARSE", "resume_text": resume_text}

    elif decision in ["SCORE", "FULL"]:
        # Convert the JD string into a list of skills
        skills_list = [s.strip() for s in job_description.split(",") if s.strip()]
        
        # Pass 3 arguments: text, skills_list, and an empty list for experience
        score_details = compute_resume_score(resume_text, skills_list, []) 
        
        return {
            "step": decision,
            "score": score_details, # This is the dictionary containing 'final_score'
            "resume_text": resume_text[:500] + "..."
        }

    # 4️⃣ Safety fallback
    return {
        "step": "UNKNOWN",
        "decision_raw": decision,
        "resume_text": resume_text[:500],
        "note": "⚠️ Model returned unexpected value"
    }

def chat_recruiter_agent(question: str):
    prompt = f"""
    You are a recruiter assistant AI. Answer questions based on the hiring context.
    Question: {question}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

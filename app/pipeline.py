# app/pipeline.py

from pdfminer.high_level import extract_text
from .scorer import compute_resume_score
from pathlib import Path
import csv

def load_job_description(source: str, from_file: bool = True) -> str:
    if from_file:
        with open(source, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = source

    text = text.lower().split()
    return " ".join(text)

def run_screening(job_description: str, skills: list, experience_keywords: list):
    RESUME_DIR = Path("data/resumes")
    resume_files = list(RESUME_DIR.glob("*.pdf"))

    if not resume_files:
        return {"error": "No resumes found in data/resumes/"}

    result = []
    for resume_file in resume_files:
        resume_text = extract_text(resume_file)
        resume_result = compute_resume_score(
            resume_text,
            required_skills=skills,
            experience_keywords=experience_keywords
        )
        resume_result["file_name"] = resume_file.name
        result.append(resume_result)

    sorted_results = sorted(result, key=lambda x: x["final_score"], reverse=True)
    shortlist = [r for r in sorted_results if r["final_score"] >= 70][:5]
from typing import List, Dict

def keyword_match_score(resume_text: str, keywords: List[str]) -> float:
    """
    calculate how many keywords appear in resume.
    Return a score between 0 and 1
    """
    resume_text = resume_text.lower()
    matches = sum(1 for kw in keywords if kw.lower() in resume_text)
    return matches / len(keywords) if keywords else 0.0

def compute_resume_score(
    resume_text: str,
    required_skills: List[str],
    experience_keywords: List[str]
) -> Dict:
    """
    Computes final resume score (0–100) with explanations.
    """
    skill_score = keyword_match_score(resume_text, required_skills)
    exp_score = keyword_match_score(resume_text, experience_keywords)

    final_score = (
        skill_score * 50 +
        exp_score * 30
    )

    return {
        "final_score": round(final_score, 2),
        "skill_score": round(skill_score * 100, 2),
        "experience_score": round(exp_score * 100, 2),
        "matched_skills": [
            skill for skill in required_skills if skill.lower() in resume_text.lower()
        ]
    }

<div align="center">

# 🤖 Agentic Resume Screening System
### *Autonomous Talent Acquisition Powered by LLMs & Vector Search*

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-3ca381?style=for-the-badge)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/GROQ-FF6F61?style=for-the-badge)](https://groq.com/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

**An AI-driven recruitment pipeline that uses Agentic Orchestration to parse, score, and perform semantic searches on candidate resumes.**
</div>

## 🧠 System Workflow

    A[User Uploads Resume + JD] --> B[FastAPI Backend]
   
    B --> C[Parser: Extract Text]
    
    C --> D[Groq Llama 3.1 Controller]
    
    D --> E{Decision: Score / Parse / Full}
    
    E --> F[Scoring Engine]
    
    E --> G[Embedding Engine]
    
    G --> H[ChromaDB Indexing]
    
    F --> I[SQLite + CSV Logging]
    
    I --> J[Streamlit UI Updates]
    
    H --> K[Semantic Search Queries]



</div>

## 🌟 Key Features

* **Agentic Decision-Making**: Uses an LLM controller to autonomously decide whether to `PARSE`, `SCORE`, or perform a `FULL` analysis.
* **High-Speed Processing**: Powered by Groq's Llama-3.1-8b for near-instant inference.
* **Vector Search**: Implements **ChromaDB** with `Sentence-Transformers` for deep semantic skill matching rather than simple keyword hits.
* **Persistence Layer**: Dual-storage system using **SQLAlchemy (SQLite)** and **CSV** for structured history.
* **Interactive Dashboard**: A sleek **Streamlit** UI for real-time resume analysis, history tracking, and an AI Recruiter Chatbot.

## 🚀 Overview

This project leverages modern Python frameworks and tools to build a production-grade **AI-powered application** with a focus on speed, interactivity, and data handling. By replacing legacy keyword matching with **Neural Search**, the suite evaluates resumes with human-like reasoning and context-aware logic.



## 🏗️ Architecture

The system follows a modular **"Agent-Leader"** pattern:

1.  **FastAPI Backend**: Acts as the orchestrator and API gateway for incoming requests.
2.  **AI Controller**: Analyzes the request to determine the necessary processing steps based on job description complexity.
3.  **Scoring Engine**: Computes a multi-factor compatibility score based on specific JD requirements.
4.  **Embedding Engine**: Indexes resumes into a 384-dimensional vector space for semantic retrieval.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* A Groq Cloud API Key

### 2. Installation

```bash
# Clone the repository
git clone [https://github.com/aiwithaftab/Agentic-Resume-Screening-Recruitment-Suite](https://github.com/aiwithaftab/Agentic-Resume-Screening-Recruitment-Suite)
cd Agentic-Resume-Screening-Recruitment-Suite

# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Terminal 1: Start Backend
python -m app.main

# Terminal 2: Start Frontend
streamlit run ui.py
---

Made with 💖 using modern Python technologies!
````
---


## 👨‍💻 About the Author

<p align="left">
Aftab Hussain is an aspiring AI Agent Developer with a passion for building **practical, real-world AI systems**.  
He focuses on designing custom AI agents that can interact with file systems, automate business workflows, and integrate with generative AI.  

💡 **Expertise & Interests:**  
- Developing **AI-powered agents** for practical business automation  
- Designing **agent loops** with tool integration and structured outputs  
- Implementing **intelligent workflows** using LLMs and embeddings  
- Automating **real-world business processes** with AI  
- Building **intelligent assistants** and end-to-end agentic solutions  

📫 **Connect:**  
- GitHub: [https://github.com/aiwithaftab](https://github.com/aiwithaftab)  
- LinkedIn: [https://www.linkedin.com/in/aftab-hussain120/](https://www.linkedin.com/in/aftab-hussain120/)  
</p>


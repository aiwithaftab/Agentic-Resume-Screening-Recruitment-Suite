import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Agent Recruiter", layout="wide")
st.title("🤖 Agentic Resume Screening Dashboard")

# Define base URL for easy updates
BASE_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------
# 📁 1. SIDEBAR → Fetch Results from DB
# ---------------------------------------------------
st.sidebar.header("📁 Screening History")
if st.sidebar.button("Fetch DB Records"):
    try:
        res = requests.get(f"{BASE_URL}/candidates", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data:
                df = pd.DataFrame(data)
                # Ensure final_score exists and is numeric
                if 'final_score' not in df.columns:
                    df['final_score'] = 0
                else:
                    df['final_score'] = pd.to_numeric(df['final_score'], errors='coerce').fillna(0)

                # Display relevant columns
                cols = ['file_name', 'final_score', 'reasoning']
                st.sidebar.dataframe(df[[c for c in cols if c in df.columns]])
            else:
                st.sidebar.info("📭 No candidates found in database yet.")
        else:
            st.sidebar.error(f"Server Error: {res.status_code}")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("⚠️ Backend is offline.")
    except Exception as e:
        st.sidebar.error(f"Unexpected Error: {str(e)}")

# ---------------------------------------------------
# 📄 2. MAIN AREA → Resume Upload + Screening
# ---------------------------------------------------
st.subheader("📄 Resume Screening")

job_description = st.text_area("Step 1: Paste Job Description Here 👇", height=150)

uploaded_files = st.file_uploader(
    "Step 2: Upload Candidate Resumes (PDFs Only)",
    type="pdf",
    accept_multiple_files=True
)

if st.button("🚀 Run Agentic Screening", key="run_screening"):
    if not job_description or not uploaded_files:
        st.warning("⚠️ Please enter a Job Description AND upload at least one resume.")
    else:
        st.info(f"Processing {len(uploaded_files)} resume(s)...")
        results_list = []

        for uploaded_file in uploaded_files:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            payload = {"jd": job_description}

            with st.spinner(f"Analyzing {uploaded_file.name}..."):
                try:
                    res = requests.post(f"{BASE_URL}/screen-resume", files=files, data=payload, timeout=30)
                    if res.status_code == 200:
                        data = res.json()
                        # Properly nested extraction from your fixed main.py
                        analysis = data.get("analysis", {})
                        score_obj = analysis.get("score", {})
                        
                        # Handle both dict and float formats for final_score
                        final_score = score_obj.get("final_score", 0) if isinstance(score_obj, dict) else score_obj
                        reasoning = analysis.get("step", "N/A")

                        st.success(f"✅ {uploaded_file.name} - Processed Successfully")
                        results_list.append({
                            "File Name": uploaded_file.name,
                            "Final Score": final_score,
                            "Reasoning": f"Strategy: {reasoning}"
                        })
                    else:
                        st.error(f"❌ Failed: {res.status_code}")
                except Exception as e:
                    st.error(f"🚫 Error: {str(e)}")

        if results_list:
            st.subheader("📊 Latest Screening Results")
            st.table(pd.DataFrame(results_list))

# ---------------------------------------------------
# 💬 3. RECRUITER CHATBOT
# ---------------------------------------------------
st.subheader("💬 Recruiter Chatbot (Ask AI anything)")

chat_question = st.text_input("Ask something like → *Who is best for Django?*")

if st.button("Ask Agent", key="chat_agent"):
    if chat_question.strip():
        try:
            response = requests.post(f"{BASE_URL}/chat-agent", json={"question": chat_question}, timeout=15)
            if response.status_code == 200:
                st.info(response.json().get("answer", "No answer found."))
        except:
            st.error("⚠️ Chat service offline.")

# ---------------------------------------------------
# 🔎 4. SEMANTIC SEARCH (FIXED LOGIC)
# ---------------------------------------------------
st.subheader("🔎 Semantic Skill Search (ChromaDB)")

search_query = st.text_input("Search resumes by skill / technology / job role")

if st.button("🔍 Run Semantic Search", key="run_search"): # Corrected key and logic
    if search_query.strip():
        try:
            res = requests.get(f"{BASE_URL}/semantic-search", params={"skill": search_query}, timeout=10)
            if res.status_code == 200:
                results = res.json().get("results", [])
                if results:
                    st.success(f"Found {len(results)} matches:")
                    for match in results:
                        # Extracts from the dictionary structure we fixed in embeddings.py
                        st.markdown(f"**📄 {match['resume_id']}** (Similarity Distance: {match['distance']})")
                else:
                    st.warning("No matches found.")
        except Exception:
            st.error("⚠️ Search service not responding.")
    else:
        st.warning("Please enter a skill to search.")
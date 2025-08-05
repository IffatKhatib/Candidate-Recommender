# Candidate Recommendation Engine

This web app helps match candidate resumes to job descriptions using semantic similarity.

---

## Features:

- Upload resume PDFs or paste resume text
- Input any job description
- Uses sentence-transformer embeddings (`all-MiniLM-L6-v2`)
- Computes cosine similarity between job and each resume
- Ranks and displays top 5–10 matching candidates
- Clean and simple Streamlit interface

---

## Tech Stack:

- Python
- Streamlit
- Sentence-Transformers
- scikit-learn
- PyMuPDF

---

## How to Run Locally:

```bash
git clone https://github.com/yourusername/candidate-recommender.git
cd candidate-recommender
pip install -r requirements.txt
streamlit run app.py
```
---  

## Notes & Assumptions:

- Supports only English resumes and job descriptions
- Assumes resumes are in readable PDF format or plain text
- Embeddings are generated using all-MiniLM-L6-v2
- AI-based candidate summaries were considered but removed for performance reasons (can be re-added using OpenAI or Hugging Face LLMs)


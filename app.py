import streamlit as st
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
#from transformers import pipeline
import os
import numpy as np

#generator = pipeline("text-generation", model="tiiuae/falcon-rw-1b", device_map="auto", max_new_tokens=200)


# Function made to read PDF/job-description
def extract_text_from_pdf(pdf_file):

    text = ""
    pdf_file.seek(0)

    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc: #as doc gives you access to the opened PDF as a variable called doc.
        for page in doc:
            text += page.get_text() #Get the text from the current PDF page and Add (append) it to the text variable
    return text

# Embedding 
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')


# Matching Resume to Jobs
def match_resumes(job_description, resumes):

    job_embedding = model.encode([job_description]) # Embedding job description

    candidates = [] # Empty list to store each candidate's name and similarity score.

    for resume in resumes:
        name = resume.name
        text = extract_text_from_pdf(resume) # extract_text_from_pdf function being called here to use on Resume
        resume_embedding = model.encode([text])
        score = cosine_similarity(job_embedding, resume_embedding)[0][0]
        candidates.append((name, score))

    # Sort by similarity score (high to low)
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates

#-------------------------------------------------------------------------------------------------

# AI-generated Summary

# def generate_fit_summary(resume_text, job_description):
#     if len(resume_text.split()) > 400:
#         resume_text = ' '.join(resume_text.split()[:400])

#     prompt = (
#         "You are an AI recruiter. Read the job description and resume, and explain in 4-5 sentences whether this candidate is a good fit or not. Give clear reasoning.\n\n"
#         f"Job Description:\n{job_description}\n\n"
#         f"Resume:\n{resume_text}\n\n"
#         "Recommendation:"
#     )

#     output = generator(prompt)[0]['generated_text']
#     return output.split("Recommendation:")[-1].strip()

#-------------------------------------------------------------------------------------------------

# Frontend : Streamlit

st.markdown("""
    <h1 style='text-align: center; color: #2E86C1; white-space: nowrap;'>
        Candidate Recommendation Engine
    </h1>
""", unsafe_allow_html=True)

# Input: Job Description
job_description = st.text_area("Enter Job Description:*", height=200)

# Input: Resume Upload
uploaded_resumes = st.file_uploader("Upload Resumes (PDF)*", type=["pdf"], accept_multiple_files=True)

st.markdown("### OR")

resume_name = st.text_input("Enter Candidate Name")
resume_text_input = st.text_area("Paste Resume Text")

# Submit Button
if st.button("Find Top Candidates"):
    if job_description and uploaded_resumes:
        with st.spinner("Analyzing resumes..."):

            combined_resumes = []

        # Add PDF resumes
        if uploaded_resumes:
            combined_resumes.extend(uploaded_resumes)

        # Add text resume as a mock "file-like" object
        if resume_name and resume_text_input:
            from io import BytesIO
            from tempfile import NamedTemporaryFile

            fake_pdf = BytesIO(resume_text_input.encode('utf-8'))
            fake_pdf.name = resume_name + "_text_resume.pdf"
            combined_resumes.append(fake_pdf)

        results = match_resumes(job_description, combined_resumes)
        top_n = results[:10]

        st.subheader("Top Matching Candidates")
        for i, (name, score) in enumerate(top_n, start=1):
            text = extract_text_from_pdf(next(r for r in combined_resumes if r.name == name))
            st.write(f"**{i}. {name}** — Similarity Score: `{score:.2f}`")
else:
    st.markdown("""
<div style='background-color: rgba(46, 134, 193, 0.15); padding: 10px 15px; border-radius: 10px;'>
    Please enter a job description and at least one resume.
</div>
""", unsafe_allow_html=True)







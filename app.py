import streamlit as st
from matcher import get_top_matches, load_jobs
from utils import extract_text_from_uploaded_file
import pandas as pd

st.set_page_config(page_title="Smart Resume Matcher", layout="centered")

st.title("Smart Resume Matcher & Job Recommender")
st.write("Upload your resume (PDF / TXT) or paste text, and compare against sample job descriptions.")

uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=['pdf','txt'], help="Upload a resume file or paste the text below.")
resume_text_input = st.text_area("Or paste your resume text here")

if uploaded_file:
    try:
        resume_text = extract_text_from_uploaded_file(uploaded_file)
    except Exception as e:
        st.error(f"Failed to extract text: {e}")
        resume_text = ""
else:
    resume_text = resume_text_input

jobs_df = load_jobs()

num_results = st.sidebar.slider("Top N results", min_value=1, max_value=10, value=5)
model_button = st.sidebar.button("Load model & run")

if st.sidebar.checkbox("Show sample job listings"):
    st.dataframe(jobs_df[['job_title','company','location','short_description']])

if model_button:
    if not resume_text or len(resume_text.strip())<20:
        st.error("Please provide a resume by uploading a PDF/TXT or pasting the resume text.")
    else:
        with st.spinner("Computing matches (this may take a while the first time while the model downloads)..."):
            results = get_top_matches(resume_text, jobs_df, top_n=num_results)
        st.success("Done! Here are the top matches:")
        for i, row in results.iterrows():
            st.markdown(f"### {i+1}. {row['job_title']}  — *{row['company']}*")
            st.write(f"**Location:** {row['location']}")
            st.write(f"**Match score:** {row['score']:.3f}")
            st.write(row['short_description'])
            st.markdown("---")

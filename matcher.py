import pandas as pd
from sentence_transformers import SentenceTransformer, util
import numpy as np

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def load_jobs(path='jobs/sample_jobs.csv'):
    df = pd.read_csv(path)
    # ensure a short_description column exists
    if 'short_description' not in df.columns:
        df['short_description'] = df['job_description'].str.slice(0,300)
    return df

def embed_texts(texts):
    model = _load_model()
    return model.encode(texts, convert_to_tensor=True)

def get_top_matches(resume_text, jobs_df, top_n=5):
    # prepare job descriptions
    job_texts = jobs_df['job_description'].fillna('').tolist()
    model = _load_model()
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_embs = model.encode(job_texts, convert_to_tensor=True)
    scores = util.cos_sim(resume_emb, job_embs)[0].cpu().numpy()
    jobs_df = jobs_df.copy()
    jobs_df['score'] = scores
    jobs_df = jobs_df.sort_values('score', ascending=False).reset_index(drop=True)
    return jobs_df.head(top_n)

# Smart Resume Matcher & Job Recommender

A ready-to-run Streamlit application that compares a resume (uploaded PDF/TXT or pasted text) to a set of sample job descriptions using Sentence-BERT embeddings.

## Features
- Resume parsing from TXT or PDF (requires PyMuPDF/pymupdf).
- Embedding and similarity using `sentence-transformers` (model: all-MiniLM-L6-v2).
- Streamlit UI with upload/paste and Top-N matches display.

## Quickstart (local)
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Notes
- The first run will download the sentence-transformers model (~90MB).
- For PDF parsing install `pymupdf`. If you don't want PDF parsing, paste resume text in the textbox.

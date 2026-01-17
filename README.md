# PDF Q&A Agent (Google ADK)

This project reads PDFs from the `data/` folder and answers questions using Google ADK.
Output is JSON with citations (doc/page/snippet).

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Generate sample PDFs
```bash
python scripts/test_pdfs.py


# PDF Q&A Agent (Google ADK)

This project reads PDFs from the `data/` folder and answers questions using Google ADK.
It returns JSON with citations (doc/page/snippet).

## Project structure
- `pdf_doc_agent/` - agent + tools
- `scripts/` - helper scripts
- `data/` - PDFs live here (kept private; generated locally)

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt



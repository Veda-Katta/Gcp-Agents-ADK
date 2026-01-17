from typing import Dict, Any
from .pdf_index import PdfSearchIndex

_index = None
_insights = None

def _load():
    global _index, _insights
    if _index is None:
        _index, _insights = PdfSearchIndex.build(folder="data")

def get_document_insights() -> Dict[str, Any]:
    _load()
    return {"status": "success", "insights": _insights}

def search_pdfs(query: str, top_k: int = 5) -> Dict[str, Any]:
    _load()
    matches = _index.search(query=query, top_k=top_k)
    return {"status": "success", "query": query, "top_k": top_k, "matches": matches}

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple

from pypdf import PdfReader
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    doc: str
    page: int
    chunk_id: int
    text: str


def read_pdf_pages(pdf_path: Path) -> List[str]:
    """Reads a PDF and returns a list of page texts (one string per page)."""
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        pages.append((page.extract_text() or "").strip())
    return pages


def split_chunks(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    """Splits text into overlapping chunks so search works better."""
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    step = max(1, chunk_size - overlap)
    i = 0
    while i < len(text):
        chunks.append(text[i : i + chunk_size])
        i += step
    return chunks


class PdfSearchIndex:
    """
    Simple search index using TF-IDF + cosine similarity.
    Good enough for a first project and runs fast locally.
    """

    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks])

    @classmethod
    def build(cls, folder: str = "data") -> Tuple["PdfSearchIndex", Dict[str, Any]]:
        folder_path = Path(folder)
        pdf_files = sorted(folder_path.glob("*.pdf"))

        all_chunks: List[Chunk] = []
        insights: Dict[str, Any] = {"documents": []}

        for pdf in pdf_files:
            pages = read_pdf_pages(pdf)
            doc_info = {"doc": pdf.name, "num_pages": len(pages), "char_count": 0}

            chunk_id = 0
            for page_num, page_text in enumerate(pages, start=1):
                doc_info["char_count"] += len(page_text)

                for part in split_chunks(page_text):
                    all_chunks.append(
                        Chunk(doc=pdf.name, page=page_num, chunk_id=chunk_id, text=part)
                    )
                    chunk_id += 1

            insights["documents"].append(doc_info)

        if not all_chunks:
            raise ValueError(
                "I couldn’t extract text from your PDFs. If they are scanned/image PDFs, this simple setup won’t work."
            )

        return cls(all_chunks), insights

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix).ravel()
        best = np.argsort(-sims)[:top_k]

        results = []
        for idx in best:
            c = self.chunks[int(idx)]
            results.append(
                {
                    "doc": c.doc,
                    "page": c.page,
                    "chunk_id": c.chunk_id,
                    "score": float(sims[int(idx)]),
                    "snippet": c.text[:300] + ("..." if len(c.text) > 300 else ""),
                }
            )
        return results

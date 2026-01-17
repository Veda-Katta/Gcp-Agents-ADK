from google.adk.agents.llm_agent import Agent
from .tools import get_document_insights, search_pdfs


INSTRUCTION = """
You answer questions using the PDFs stored in ./data.

For every user question:
1) Call get_document_insights() once.
2) Call search_pdfs(query=<the user question>, top_k=5) once.

Return ONLY valid JSON. No markdown. No extra text.

JSON format:
{
  "question": "...",
  "answer": "...",
  "documents": [ { "doc": "...", "num_pages": 0, "char_count": 0 } ],
  "citations": [ { "doc": "...", "page": 0, "chunk_id": 0, "snippet": "..." } ]
}

- "documents" must come from get_document_insights().
- "citations" must come from search_pdfs() matches.
- If the answer isn’t in the PDFs, say that in "answer" and still return citations.
"""

root_agent = Agent(
    name="pdf_doc_agent",
    model="gemini-2.5-flash",
    instruction=INSTRUCTION,
    tools=[get_document_insights, search_pdfs],
)



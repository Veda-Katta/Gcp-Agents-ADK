from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DOCS = {
    "sample-1.pdf": [
        "Sample 1\n\nThis is a simple test PDF.\nIt has a few lines of text so we can search it.\n\nTopic: Travel policy\nMeals cap: $60/day\nRemote work: 2 days/week\n",
        "More notes\n\nReceipts required over $25.\nFlights must be economy unless approved.\n",
    ],
    "sample-2.pdf": [
        "Sample 2\n\nThis PDF is longer and more detailed.\n\nTopic: Product specs\nLatency target: 120ms p95\nThroughput: 500 RPS\nRegion: us-central1\n",
        "Reliability\n\nSLO: 99.9% uptime\nError budget: 43 minutes/month\n",
    ],
    "sample-3.pdf": [
        "Sample 3\n\nTopic: Onboarding\nDay 1: account + laptop setup\nDay 3: first PR\nWeek 2: shadow on-call\n",
        "Tech stack\n\nPython services\nGCP storage\nCI with GitHub Actions\n",
    ],
}

def write_pdf(path: Path, pages: list[str]) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    _, height = letter
    for text in pages:
        y = height - 72
        for line in text.splitlines():
            c.drawString(72, y, line[:120])
            y -= 16
        c.showPage()
    c.save()

for filename, pages in DOCS.items():
    write_pdf(DATA_DIR / filename, pages)

print("Created sample PDFs in ./data")

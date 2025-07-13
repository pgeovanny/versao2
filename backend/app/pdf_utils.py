import fitz
import re
from typing import List, Dict

def extract_structure(pdf_bytes: bytes) -> List[Dict]:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    print("\n=== TEXTO EXTRAÍDO DO PDF ===\n")
    print(text[:5000])  # Mostra só os primeiros 5k caracteres
    print("\n=== FIM DO TEXTO EXTRAÍDO ===\n")
    pattern = r"(Art\.?\s*\d+[º°]?\s*-?|Artigo\s*\d+[º°]?\s*-?|CAP[IÍ]TULO\s+[XVI]+|Se[cç][aã]o\s+\w+)"
    tokens = re.split(pattern, text)
    sections = []
    current = None
    for token in tokens:
        if re.match(pattern, token, re.IGNORECASE):
            if current:
                sections.append(current)
            current = {"title": token.strip(), "content": ""}
        else:
            if current:
                current["content"] += token.strip() + "\n"
    if current:
        sections.append(current)
    sections = [s for s in sections if s["content"].strip()]
    return sections

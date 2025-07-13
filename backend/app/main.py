import os
import uuid
import fitz  # PyMuPDF para extração de PDF
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from pydantic import BaseModel
import httpx

# ----- MODELOS -----
class Section(BaseModel):
    title: str
    content: str

class SchematizedSection(BaseModel):
    title: str
    schematization: str

class StructureRequest(BaseModel):
    structure: List[Section]

class ExportRequest(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]
    export_format: str = "pdf"

# ----- APP -----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# ----- CHAVE OPENROUTER -----
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # No Render, coloque no painel de env vars!

# ----- IA UTILS -----
async def call_openrouter(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": 0.2
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, timeout=120)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

# ----- PROMPTS -----
async def organizar_ia_real(sections):
    prompt = (
        "Você é um especialista em legislação. Sua tarefa é analisar o texto de cada artigo da lei e organizar a estrutura de forma lógica, clara e visual. "
        "Agrupe por tópicos, separe os artigos, destaque prazos, regras absolutas (em negrito), palavras negativas (em vermelho), faça tabelas para composições e prazos sempre que houver. "
        "Seu objetivo é facilitar a compreensão para concursos, mantendo a literalidade do texto onde for relevante. Nunca resuma demais, apenas organize e realce o fundamental."
    )
    results = []
    for sec in sections:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Artigo: {sec.content}"}
        ]
        content = await call_openrouter(messages)
        results.append({"title": sec.title, "content": content})
    return results

async def esquematizar_ia_real(sections):
    prompt = (
        "Você é um especialista em esquematização de leis. Para cada artigo, crie esquemas visuais, quadros, tabelas comparativas, destaque prazos, grife palavras negativas de vermelho, regras absolutas em negrito e crie fluxogramas ou quadros nos artigos mais complexos. "
        "Para todos os artigos, repita a literalidade destacando o mais importante. A apresentação deve ser clara, bonita, fácil para estudo e revisão. Use estrutura markdown ou HTML básico, quadros, emojis, tabelas quando útil."
    )
    results = []
    for sec in sections:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Artigo: {sec.content}"}
        ]
        content = await call_openrouter(messages)
        results.append({"title": sec.title, "schematization": content})
    return results

# ----- EXTRAIR PDF -----
@app.post("/extrair/")
async def extrair(pdf: UploadFile = File(...)):
    if not pdf.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser PDF.")
    pdf_bytes = await pdf.read()
    tmpname = f"/tmp/{uuid.uuid4().hex}.pdf"
    with open(tmpname, "wb") as f:
        f.write(pdf_bytes)
    doc = fitz.open(tmpname)
    structure = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            structure.append({"title": f"Página {page.number+1}", "content": text.strip()})
    return {"structure": structure, "pdfFile": pdf.filename, "pdfUrl": ""}

# ----- ORGANIZAR -----
@app.post("/sumarizar/")
async def sumarizar(req: StructureRequest):
    organizado = await organizar_ia_real(req.structure)
    return {"structure": organizado}

# ----- ESQUEMATIZAR -----
@app.post("/esquematizar/")
async def esquematizar(req: StructureRequest):
    esquematizado = await esquematizar_ia_real(req.structure)
    return {"schematization": esquematizado}

# ----- EXPORTAR PDF -----
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

def gerar_pdf_completo(structure, schematization, filename="output.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4, title="Lei Esquematizada")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=16, leading=20, spaceAfter=14))
    elems = []
    for sec, esquem in zip(structure, schematization):
        elems.append(Paragraph(f"<b>{sec['title']}</b>", styles["CenterTitle"]))
        elems.append(Spacer(1, 6))
        elems.append(Paragraph(sec['content'], styles["BodyText"]))
        elems.append(Spacer(1, 8))
        elems.append(Paragraph("<b>Esquematização:</b>", styles["Heading3"]))
        elems.append(Paragraph(esquem['schematization'], styles["BodyText"]))
        elems.append(PageBreak())
    doc.build(elems)

@app.post("/exportar/")
async def exportar(req: ExportRequest):
    filename = f"/tmp/lei_esquematizada_{uuid.uuid4().hex}.pdf"
    gerar_pdf_completo([s.dict() for s in req.structure], [e.dict() for e in req.schematization], filename)
    return FileResponse(filename, media_type='application/pdf', filename="lei_esquematizada.pdf")

# ----- HOME -----
@app.get("/")
def read_root():
    return {"msg": "API de Lei Esquematizada Online!"}

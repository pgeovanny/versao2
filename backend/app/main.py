import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import shutil
import tempfile

import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Models
class Section(BaseModel):
    title: str
    content: str

class SchematizedSection(BaseModel):
    title: str
    schematization: str

class ProcessResponse(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]

class StructureRequest(BaseModel):
    structure: List[Section]

class EditRequest(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]

class ExportRequest(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]
    export_format: Optional[str] = "pdf"

# FastAPI app
app = FastAPI(
    title="Lei Esquematizada API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utils para PDF (simples, ajustar conforme precisar)
def extract_pdf_sections(file_path):
    # Aqui você pode usar PyPDF2 ou fitz (PyMuPDF) para extrair os artigos da lei
    # Exemplo simples:
    import fitz  # PyMuPDF
    doc = fitz.open(file_path)
    text = "\n".join(page.get_text() for page in doc)
    # Aqui um exemplo bem básico que divide por "Art.":
    sections = []
    articles = text.split("Art. ")
    for i, a in enumerate(articles[1:], 1):
        # separa título e texto
        lines = a.strip().split("\n", 1)
        title = f"Art. {lines[0][:4]}"
        content = lines[1] if len(lines) > 1 else ""
        sections.append({"title": title, "content": content})
    return sections

# Função Gemini
async def call_gemini(messages: list):
    prompt = ""
    for m in messages:
        prompt += f"{m['role']}: {m['content']}\n"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# ------------------ ENDPOINTS -------------------

@app.post("/extrair/", response_model=ProcessResponse)
async def extrair(pdf: UploadFile = File(...)):
    # Salva arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(pdf.file, tmp)
        tmp_path = tmp.name
    try:
        structure = extract_pdf_sections(tmp_path)
    finally:
        os.remove(tmp_path)
    return {"structure": structure, "schematization": []}

@app.post("/sumarizar/", response_model=ProcessResponse)
async def sumarizar(req: StructureRequest):
    # IA para organizar a estrutura da lei
    prompt = (
        "Organize de forma clara e esquemática os artigos abaixo, melhorando a estrutura. "
        "Responda em formato JSON: [{title, content}] apenas, sem explicações. "
        "Artigos:\n"
    )
    for section in req.structure:
        prompt += f"{section.title}: {section.content}\n"
    messages = [{"role": "user", "content": prompt}]
    content = await call_gemini(messages)
    # Tenta ler como JSON, senão devolve como texto bruto
    import json
    try:
        estrutura = json.loads(content)
    except Exception:
        estrutura = req.structure
    return {"structure": estrutura, "schematization": []}

@app.post("/esquematizar/", response_model=ProcessResponse)
async def esquematizar(req: StructureRequest):
    # IA para esquematizar cada artigo
    schematization = []
    for section in req.structure:
        prompt = (
            f"Esquematize o seguinte artigo de lei, destacando tópicos principais, criando um resumo visual esquematizado e destacando palavras importantes:\n"
            f"{section.title}: {section.content}\n"
            "Responda apenas com tópicos esquematizados em Markdown."
        )
        messages = [{"role": "user", "content": prompt}]
        esquema = await call_gemini(messages)
        schematization.append({"title": section.title, "schematization": esquema})
    return {"structure": req.structure, "schematization": schematization}

@app.post("/editar/", response_model=ProcessResponse)
async def editar(req: EditRequest):
    # Só retorna o que veio (pode adicionar lógica para editar com IA)
    return {"structure": req.structure, "schematization": req.schematization}

@app.post("/exportar/")
async def exportar(req: ExportRequest):
    # Gera um PDF ou outro formato
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for section in req.structure:
        pdf.multi_cell(0, 10, f"{section.title}\n{section.content}\n")
        # Busca esquematização
        esq = next((e for e in req.schematization if e['title'] == section.title), None)
        if esq:
            pdf.set_font("Arial", style="B", size=12)
            pdf.multi_cell(0, 10, esq['schematization'])
            pdf.set_font("Arial", size=12)
        pdf.cell(0, 5, "", ln=True)
    out_path = "lei_esquematizada.pdf"
    pdf.output(out_path)
    return FileResponse(out_path, filename="lei_esquematizada.pdf")

# ------------------ ROOT -------------------

@app.get("/")
def root():
    return {"msg": "API Lei Esquematizada online!"}

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import Section, SchematizedSection, ProcessResponse, StructureRequest, EditRequest, ExportRequest
import fitz  # PyMuPDF
import os
import uuid

# Simulação de IA (substitua pela sua chamada real à IA)
def organizar_ia(sections):
    # Prompt super detalhado!
    return [
        {
            "title": sec.title,
            "content": f"**{sec.title}**\n\n{sec.content}\n\n- Palavras negativas em <span style='color:red'><b>vermelho</b></span>\n- Regras absolutas em <b>negrito</b> e ⚠️\n- Prazos em <mark>amarelo</mark> ou em tabela\n- Composições em tabela\n- Conceitos em balão azul\n\n> [Texto gerado pela IA conforme prompt aprimorado. Adapte com sua chamada real à IA.]"
        }
        for sec in sections
    ]

def esquematizar_ia(sections):
    # Prompt turbo: pede quadros, fluxos, tabelas e grifos
    return [
        {
            "title": sec.title,
            "schematization": f"""<h3>{sec.title}</h3>
<p><b>Literalidade:</b> {sec.content}</p>
<ul>
    <li><b>Quadros comparativos</b> para pontos polêmicos</li>
    <li><span style='color:red'><b>Palavras negativas grifadas</b></span></li>
    <li><b>Prazos em destaque</b></li>
    <li>Artigos complexos: <b>tabelas, quadros, fluxogramas</b></li>
    <li>Tudo visual, facilitador e 100% esquematizado</li>
</ul>
<blockquote style='color:blue'>Destaque visual facilitador criado pela IA (troque por chamada real à IA).</blockquote>
"""
        }
        for sec in sections
    ]


app = FastAPI()

# Liberar acesso ao frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_pdf(pdf: UploadFile = File(...)):
    try:
        contents = await pdf.read()
        temp_path = f"/tmp/{uuid.uuid4()}_{pdf.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)
        doc = fitz.open(temp_path)
        # Extração básica: cada página como seção
        structure = []
        for i, page in enumerate(doc):
            text = page.get_text()
            structure.append(Section(title=f"Página {i+1}", content=text))
        os.remove(temp_path)
        return {"structure": structure}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sumarizar/")
async def sumarizar(req: StructureRequest):
    # Chama IA para organizar melhor cada seção
    organizado = organizar_ia(req.structure)
    return {"structure": organizado}

@app.post("/esquematizar/")
async def esquematizar(req: StructureRequest):
    # Chama IA para esquematizar de forma profissional e visual
    esquematizado = esquematizar_ia(req.structure)
    return {"schematization": esquematizado}

@app.post("/editar/")
async def editar(req: EditRequest):
    # Apenas retorna o que veio (simula edição, aqui pode integrar comentários/questões)
    return {"edited": req.schematization}

@app.post("/exportar/")
async def exportar(req: ExportRequest):
    # Simula exportação de PDF (deve gerar arquivo real depois)
    return {"file_url": "https://site.com/seu_pdf_final.pdf"}

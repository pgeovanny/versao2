from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from app.pdf_utils import extract_structure
from app.ia_client import IAClient
from app.schemas import Section, SchematizedSection, EditRequest, ExportRequest, StructureRequest

app = FastAPI(
    title="Lei Esquematizada API",
    version="1.0.0",
    description="API para esquematização e exportação de legislação."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ia_client = IAClient()

@app.get("/")
def root():
    return {"status": "API rodando! Acesse /docs para testar."}

@app.post("/extrair/")
async def extrair(pdf: UploadFile = File(...)):
    """
    Envie um PDF de lei para extração inteligente.
    """
    if not pdf:
        raise HTTPException(status_code=400, detail="Arquivo PDF não enviado.")
    content = await pdf.read()
    structure = extract_structure(content)
    return {"structure": structure}

@app.post("/sumarizar/")
async def sumarizar(request: StructureRequest):
    """
    Organiza e sumariza a estrutura extraída antes de esquematizar.
    """
    try:
        result = await ia_client.organizar_estrutura(request.structure)
        return {"summarized": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao organizar: {str(e)}")

@app.post("/esquematizar/")
async def esquematizar(request: StructureRequest):
    """
    Esquematiza TODOS os artigos da lei de forma avançada, destacando pontos importantes, criando quadros, grifos, etc.
    """
    try:
        result = await ia_client.esquematizar_estrutura(request.structure)
        return {"schematization": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao esquematizar: {str(e)}")

@app.post("/editar/")
async def editar(edit_req: EditRequest):
    """
    Permite editar ou incluir questões, comentários, quadros, fluxogramas, etc, em locais específicos.
    """
    try:
        result = await ia_client.editar_artigo(edit_req)
        return {"edited": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao editar: {str(e)}")

@app.post("/exportar/")
async def exportar(export_req: ExportRequest):
    """
    Exporta o conteúdo gerado em PDF totalmente formatado, com cores, quadros, logo e visual profissional.
    """
    try:
        # Implemente a geração real de PDF no utils/pdf_exporter.py, aqui é um placeholder
        from app.pdf_exporter import gerar_pdf
        output = gerar_pdf(export_req)
        return {"status": "Exportação realizada!", "file_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar: {str(e)}")

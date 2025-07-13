from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
from .pdf_utils import extract_structure
from .ia_client import IAClient
from .schemas import ProcessResponse, StructureRequest, EditRequest, ExportRequest
from .pdf_export import export_pdf

app = FastAPI(title="Lei Esquematizada API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")
ia_client = IAClient()

@app.post("/extrair/", response_model=ProcessResponse)
async def extrair(pdf: UploadFile = File(...)):
    if pdf.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Arquivo precisa ser PDF")
    data = await pdf.read()
    try:
        structure = extract_structure(data)
        if not structure:
            return {"structure": [], "schematization": []}
        return {"structure": structure, "schematization": []}
    except Exception as e:
        logger.error(f"Erro ao extrair lei: {e}")
        raise HTTPException(status_code=500, detail="Erro ao extrair a lei.")

@app.post("/sumarizar/", response_model=ProcessResponse)
async def sumarizar(request: StructureRequest):
    try:
        sumarized = await ia_client.sumarize(request.structure)
        return {"structure": request.structure, "schematization": sumarized}
    except Exception as e:
        logger.error(f"Erro ao sumarizar: {e}")
        raise HTTPException(status_code=500, detail="Erro ao sumarizar a lei.")

@app.post("/esquematizar/", response_model=ProcessResponse)
async def esquematizar(request: StructureRequest):
    try:
        esquematized = await ia_client.schematize(request.structure)
        return {"structure": request.structure, "schematization": esquematized}
    except Exception as e:
        logger.error(f"Erro ao esquematizar: {e}")
        raise HTTPException(status_code=500, detail="Erro ao esquematizar a lei.")

@app.post("/editar/", response_model=ProcessResponse)
async def editar(request: EditRequest):
    return request.dict()

@app.post("/exportar/")
async def exportar(request: ExportRequest):
    try:
        pdf_bytes = export_pdf(request.structure, request.schematization, request.export_format)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=lei-esquematizada.pdf"
        })
    except Exception as e:
        logger.error(f"Erro ao exportar PDF: {e}")
        raise HTTPException(status_code=500, detail="Erro ao exportar PDF.")

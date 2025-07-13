from typing import List, Optional
from pydantic import BaseModel

class Section(BaseModel):
    title: str
    content: str

class SchematizedSection(BaseModel):
    title: str
    schematization: str

class StructureRequest(BaseModel):
    structure: List[Section]

class EditRequest(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]

class ExportRequest(BaseModel):
    structure: List[Section]
    schematization: List[SchematizedSection]
    export_format: Optional[str] = "pdf"

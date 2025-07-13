from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO
import os
import re

def export_pdf(structure, schematization, export_format="pdf", logo_path="logo.png"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0057FF"),
        spaceAfter=24,
    )
    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=colors.HexColor("#222222"),
        backColor=colors.HexColor("#E5ECFA"),
        leftIndent=0,
        spaceAfter=8,
        spaceBefore=16,
        borderWidth=1,
        borderColor=colors.HexColor("#0057FF"),
    )
    article_style = ParagraphStyle(
        "ArticleContent",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#111111"),
        spaceAfter=8,
    )
    esquemat_style = ParagraphStyle(
        "Esquematization",
        parent=styles["BodyText"],
        fontSize=11,
        leading=14,
        spaceBefore=2,
        textColor=colors.HexColor("#0057FF"),
    )

    # Logo (opcional)
    if os.path.isfile(logo_path):
        elements.append(Image(logo_path, width=140, height=60))
    elements.append(Paragraph("Lei Esquematizada", title_style))
    elements.append(Spacer(1, 12))

    # Gera conteúdo para cada artigo
    for idx, (section, esquemat) in enumerate(zip(structure, schematization)):
        elements.append(Paragraph(section.title, section_style))
        elements.append(Spacer(1, 3))
        elements.append(Paragraph(section.content, article_style))
        elements.append(Spacer(1, 4))
        # Converte markdown básico para tabelas/quadros
        esquemat_content = markdown_to_pdf(esquemat.schematization, esquemat_style)
        elements += esquemat_content
        elements.append(Spacer(1, 12))
        if (idx + 1) % 3 == 0:
            elements.append(PageBreak())

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def markdown_to_pdf(text, esquemat_style):
    # Converte listas e tabelas simples de markdown para Table e Paragraph do reportlab
    blocks = []
    lines = text.split('\n')
    table = []
    in_table = False

    for line in lines:
        # Tabela Markdown | separada por |
        if re.match(r'^\|.+\|$', line):
            cells = [c.strip() for c in line.strip('|').split('|')]
            table.append(cells)
            in_table = True
            continue
        elif in_table and not line.strip():
            # fim da tabela
            if table:
                blocks.append(make_table(table))
            table = []
            in_table = False
            continue
        elif in_table:
            continue

        # Listas em markdown
        if re.match(r'^\s*[\*\-\d]\s', line):
            blocks.append(Paragraph(line, esquemat_style))
            continue

        # Título ou destaque
        if re.match(r'^#+\s', line):
            blocks.append(Paragraph(f"<b>{line.lstrip('#').strip()}</b>", esquemat_style))
            continue

        # Texto normal
        if line.strip():
            blocks.append(Paragraph(line, esquemat_style))
    # tabela ao final
    if table:
        blocks.append(make_table(table))
    return blocks

def make_table(table_data):
    table = Table(table_data, style=TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E5ECFA")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0057FF")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor("#0057FF")),
    ]))
    return table

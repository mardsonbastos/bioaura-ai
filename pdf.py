from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
def generate_pdf(nome,conteudo,profissional,registro):
    b=BytesIO(); doc=SimpleDocTemplate(b,pagesize=A4,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)
    s=getSampleStyleSheet(); story=[]
    topo=ParagraphStyle("topo",parent=s["Normal"],fontSize=14,leading=17,textColor=colors.HexColor("#1A365D"),alignment=1)
    corpo=ParagraphStyle("corpo",parent=s["Normal"],fontSize=10.5,leading=15)
    story += [Paragraph(profissional.upper(),topo),Paragraph(registro,topo),Spacer(1,20),
              Paragraph("RELATÓRIO DE AVALIAÇÃO — APOIO À REVISÃO PROFISSIONAL",topo),
              Paragraph(f"<b>Paciente:</b> {nome}",corpo),Spacer(1,15)]
    for p in conteudo.split("\n"):
        if p.strip(): story += [Paragraph(p.replace("&","&amp;"),corpo),Spacer(1,5)]
    story += [Spacer(1,25),Paragraph(profissional,topo),Paragraph(registro,corpo)]
    doc.build(story); b.seek(0); return b

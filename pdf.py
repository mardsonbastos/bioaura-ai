from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf(nome,altura,peso,conteudo,profissional,registro):
    b=BytesIO(); doc=SimpleDocTemplate(b,pagesize=A4,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)
    s=getSampleStyleSheet(); story=[]
    topo=ParagraphStyle("topo",parent=s["Normal"],fontSize=14,leading=17,textColor=colors.HexColor("#1A365D"),alignment=1)
    corpo=ParagraphStyle("corpo",parent=s["Normal"],fontSize=10.5,leading=15)
    
    story += [Paragraph(profissional.upper(),topo),Paragraph(registro,topo),Spacer(1,20),
              Paragraph("RELATÓRIO DE AVALIAÇÃO — APOIO À REVISÃO PROFISSIONAL",topo),
              Paragraph(f"<b>Paciente:</b> {nome}",corpo),Spacer(1,10)]
    
    # Tabela de antropometria
    imc=None
    if altura and peso:
        altura_m=altura/100
        imc=peso/(altura_m**2)
    
    dados_tabela=[
        ["Altura","Peso","IMC"],
        [f"{altura:.1f} cm",f"{peso:.1f} kg",f"{imc:.1f}" if imc else "—"]
    ]
    
    tabela=Table(dados_tabela,colWidths=[100,100,100])
    tabela.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor("#1A365D")),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),10),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))
    
    story += [tabela,Spacer(1,15)]
    
    for p in conteudo.split("\n"):
        if p.strip(): story += [Paragraph(p.replace("&","&amp;"),corpo),Spacer(1,5)]
    story += [Spacer(1,25),Paragraph(profissional,topo),Paragraph(registro,corpo)]
    doc.build(story); b.seek(0); return b

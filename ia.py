import os
import io
from openai import OpenAI
try:
    from PyPDF2 import PdfReader
except:
    PdfReader=None

SYSTEM = """Você é um assistente de documentação clínica. Organize e resuma exclusivamente as informações fornecidas.
Não diagnostique, não prescreva medicamentos, doses, injetáveis, soroterapia ou tratamentos.
Aponte inconsistências ou informações que mereçam revisão profissional.
Diferencie claramente dados fornecidos de interpretação/alertas.
Responda em português, de forma objetiva e estruturada."""

def extract_pdf_text(pdf_file):
    """Extrai texto de arquivo PDF"""
    if not PdfReader:
        return f"Arquivo PDF: {pdf_file.name}"
    try:
        pdf_reader=PdfReader(io.BytesIO(pdf_file.read()))
        texto=""
        for pagina in pdf_reader.pages:
            texto+=pagina.extract_text()+"\n"
        return texto[:2000]  # Limita a 2000 caracteres
    except:
        return f"Arquivo PDF: {pdf_file.name}"

def analyze_case(nome,queixas,exames,observacoes,altura,peso,texto_arquivo=""):
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    imc=None
    if altura and peso:
        altura_m=altura/100
        imc=peso/(altura_m**2)
    
    prompt=f"""Paciente: {nome}
Dados antropométricos:
- Altura: {altura:.1f} cm
- Peso: {peso:.1f} kg
{f"- IMC: {imc:.1f}" if imc else ""}

Queixas/informações relatadas:
{queixas}

Exames:
{exames}

Observações profissionais:
{observacoes}

{f"Arquivo de exame anexo:\n{texto_arquivo}" if texto_arquivo else ""}

Estruture:
1. Resumo dos dados (incluindo avaliação antropométrica)
2. Marcadores/resultados que merecem atenção (sem diagnóstico)
3. Pontos para revisão profissional
4. Informações que estão faltando
5. Resumo para registro em prontuário
"""
    r=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4-turbo"),messages=[
        {"role":"system","content":SYSTEM},{"role":"user","content":prompt}])
    return r.choices[0].message.content

import os
from openai import OpenAI

SYSTEM = """Você é um assistente de documentação clínica. Organize e resuma exclusivamente as informações fornecidas.
Não diagnostique, não prescreva medicamentos, doses, injetáveis, soroterapia ou tratamentos.
Aponte inconsistências ou informações que mereçam revisão profissional.
Diferencie claramente dados fornecidos de interpretação/alertas.
Responda em português, de forma objetiva e estruturada."""

def analyze_case(nome,queixas,exames,observacoes):
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt=f"""Paciente: {nome}
Queixas/informações relatadas:
{queixas}

Exames:
{exames}

Observações profissionais:
{observacoes}

Estruture:
1. Resumo dos dados
2. Marcadores/resultados que merecem atenção (sem diagnóstico)
3. Pontos para revisão profissional
4. Informações que estão faltando
5. Resumo para registro em prontuário
"""
    r=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4-turbo"),messages=[
        {"role":"system","content":SYSTEM},{"role":"user","content":prompt}])
    return r.choices[0].message.content

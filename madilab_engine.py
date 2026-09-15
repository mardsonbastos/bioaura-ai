# MadiLab Premium - Motor de Análise Laboratorial
# Sistema inteligente de análise de marcadores com cálculo de scores e recomendações

import os
from labpro_markers import LAB_REFERENCES, LAB_CONDUCTS, LAB_SUPPLEMENTATION, LAB_PROFILES

def get_age_range(age):
    """Determina a faixa etária para referências"""
    if age < 18:
        return "<18"
    elif age < 45:
        return "18-45"
    elif age < 60:
        return "46-60"
    else:
        return ">60"

def get_reference_for_marker(marker_code, genero, idade):
    """Obtém valores de referência para um marcador por sexo e idade"""
    if marker_code not in LAB_REFERENCES:
        return None
    
    marker_ref = LAB_REFERENCES[marker_code]
    age_range = get_age_range(idade)
    
    if genero not in marker_ref:
        return None
    
    gender_data = marker_ref[genero]
    
    # Tenta obter referência específica da idade
    if age_range in gender_data:
        return gender_data[age_range]
    elif "geral" in gender_data:
        return gender_data["geral"]
    
    return None

def evaluate_marker(marker_code, valor, genero, idade):
    """
    Avalia um marcador e retorna:
    - status: 'verde' (saudável), 'amarelo' (alerta), 'vermelho' (crítico)
    - referencia_min, referencia_max
    - valor_ideal
    - conduta: recomendação clínica
    """
    if marker_code not in LAB_REFERENCES:
        return {
            "status": "desconhecido",
            "valor": valor,
            "referencia_min": None,
            "referencia_max": None,
            "valor_ideal": None,
            "conduta": "Marcador não cadastrado no sistema MadiLab",
            "suplementacoes": ""
        }
    
    marker_ref = LAB_REFERENCES[marker_code]
    ref = get_reference_for_marker(marker_code, genero, idade)
    
    if not ref:
        return {
            "status": "sem_referencia",
            "valor": valor,
            "referencia_min": None,
            "referencia_max": None,
            "valor_ideal": None,
            "conduta": "Sem referência disponível para este perfil",
            "suplementacoes": ""
        }
    
    ref_min = ref.get("min")
    ref_max = ref.get("max")
    valor_ideal = marker_ref.get("ideal", {}).get(genero)
    
    # Determina status
    status = "verde"
    conduta = ""
    
    if valor < ref_min:
        status = "vermelho"
        if marker_code in LAB_CONDUCTS and "baixo" in LAB_CONDUCTS[marker_code]:
            conduta = LAB_CONDUCTS[marker_code]["baixo"]
    elif valor > ref_max:
        status = "vermelho"
        if marker_code in LAB_CONDUCTS and "alto" in LAB_CONDUCTS[marker_code]:
            conduta = LAB_CONDUCTS[marker_code]["alto"]
    elif abs(valor - valor_ideal) > (ref_max - ref_min) * 0.2:
        status = "amarelo"
        conduta = f"Valor fora da faixa ideal. Valor ideal: {valor_ideal}"
    else:
        conduta = "Marcador dentro dos parâmetros ideais"
    
    # Recomendações de suplementação
    suplementacoes = ""
    if status != "verde":
        for supl_profile, supl_list in LAB_SUPPLEMENTATION.items():
            if marker_code.upper() in supl_profile or supl_profile.upper() in marker_code:
                suplementacoes = ", ".join(supl_list)
                break
    
    return {
        "status": status,
        "valor": valor,
        "referencia_min": ref_min,
        "referencia_max": ref_max,
        "valor_ideal": valor_ideal,
        "conduta": conduta,
        "suplementacoes": suplementacoes
    }

def calculate_madilab_score(markers_data):
    """
    Calcula o Score MadiLab (0-100) e nível de inflamação
    
    Score baseado em:
    - Percentual de marcadores em verde
    - Gravidade dos marcadores vermelhos
    - Marcadores de inflamação
    """
    if not markers_data:
        return 0, "desconhecido"
    
    total = len(markers_data)
    verde = sum(1 for m in markers_data if m.get("status") == "verde")
    amarelo = sum(1 for m in markers_data if m.get("status") == "amarelo")
    vermelho = sum(1 for m in markers_data if m.get("status") == "vermelho")
    
    # Score base: 100 * (verde/total) - (amarelo*5) - (vermelho*20)
    score = (verde / total * 100) - (amarelo * 5) - (vermelho * 20)
    score = max(0, min(100, score))  # Limita entre 0-100
    
    # Nível de inflamação baseado em marcadores inflamatórios
    inflamacao_markers = ["PCR", "FIBRINOGENIO", "VHS", "CITRATO_LIASE"]
    inflamacao_count = sum(1 for m in markers_data 
                           if any(infl in m.get("marker_code", "").upper() for infl in inflamacao_markers)
                           and m.get("status") == "vermelho")
    
    if inflamacao_count >= 3:
        nivel_inflamacao = "Alta"
    elif inflamacao_count >= 1:
        nivel_inflamacao = "Moderada"
    else:
        nivel_inflamacao = "Baixa"
    
    return round(score, 1), nivel_inflamacao

def generate_marker_report(marker_code, marker_data):
    """Gera relatório estruturado para um marcador"""
    nome = LAB_REFERENCES.get(marker_code, {}).get("nome", marker_code)
    unidade = LAB_REFERENCES.get(marker_code, {}).get("unidade", "")
    
    report = f"""
### {nome} ({marker_code})
- **Valor:** {marker_data['valor']} {unidade}
- **Referência:** {marker_data['referencia_min']:.1f} - {marker_data['referencia_max']:.1f} {unidade}
- **Ideal:** {marker_data['valor_ideal']:.1f} {unidade}
- **Status:** {marker_data['status'].upper()}
- **Conduta:** {marker_data['conduta']}
"""
    if marker_data['suplementacoes']:
        report += f"- **Suplementações:** {marker_data['suplementacoes']}\n"
    
    return report

def analyze_exam_bulk(exam_markers, genero, idade):
    """
    Analisa todos os marcadores de um exame de uma vez
    
    exam_markers: lista de dicts com marker_code e valor
    genero: 'M' ou 'F'
    idade: idade do paciente
    
    Retorna lista de resultados
    """
    results = []
    for marker_info in exam_markers:
        marker_code = marker_info.get("code")
        valor = marker_info.get("valor")
        
        evaluation = evaluate_marker(marker_code, valor, genero, idade)
        evaluation["marker_code"] = marker_code
        results.append(evaluation)
    
    return results

def get_profile_analysis(profile_code):
    """Retorna análise de um perfil clínico específico"""
    if profile_code not in LAB_PROFILES:
        return None
    
    profile = LAB_PROFILES[profile_code]
    return {
        "nome": profile["nome"],
        "marcadores": profile["marcadores"],
        "descricao": f"Perfil de {profile['nome']} - {len(profile['marcadores'])} marcadores"
    }

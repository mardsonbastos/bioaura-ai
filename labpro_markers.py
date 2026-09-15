# LabPro Premium - Marcadores Clínicos
# 213 marcadores organizados em 15 perfis de medicina funcional
# Referências por sexo e faixa etária

LAB_PROFILES = {
    "HEMOGRAMA": {
        "nome": "Hemograma Completo",
        "marcadores": ["RBC", "WBC", "HB", "HT", "PLT", "MCV", "MCH", "MCHC", "RDW"]
    },
    "BIOQUIMICA": {
        "nome": "Bioquímica Geral",
        "marcadores": ["GLICOSE", "UREA", "CREATININA", "SODIO", "POTASSIO", "CLORO", "CO2"]
    },
    "HEPATICA": {
        "nome": "Função Hepática",
        "marcadores": ["AST", "ALT", "GGT", "ALP", "BILIRRUBINA_TOTAL", "BILIRRUBINA_DIRETA", "ALBUMINA", "PROTEINA_TOTAL"]
    },
    "RENAL": {
        "nome": "Função Renal",
        "marcadores": ["CREATININA", "UREA", "UREIA_N", "TGF", "FOSFORO", "CALCIO"]
    },
    "LIPIDICA": {
        "nome": "Perfil Lipídico",
        "marcadores": ["COLESTEROL_TOTAL", "LDL", "HDL", "TRIGLICERIDES", "VLDL", "COLESTEROL_NAO_HDL"]
    },
    "GLICOSE": {
        "nome": "Metabolismo de Glicose",
        "marcadores": ["GLICOSE_JEJUM", "INSULINA_JEJUM", "HOMA_IR", "HBA1C", "PEPTIDEO_C"]
    },
    "TIREOIDE": {
        "nome": "Função Tireoidiana",
        "marcadores": ["TSH", "T3_LIVRE", "T4_LIVRE", "T4_TOTAL", "ANTIPEROXIDASE", "ANTITIREOGLOBULINA"]
    },
    "MINERAIS": {
        "nome": "Macro e Micronutrientes",
        "marcadores": ["CALCIO", "FOSFORO", "MAGNESIO", "FERRO", "FERRITINA", "CERULOPLASMINA", "COBRE", "ZINCO"]
    },
    "INFLAMACAO": {
        "nome": "Marcadores Inflamatórios",
        "marcadores": ["PCR", "VHS", "FIBRINOGENIO", "HOMOCISTEINA", "CITRATO_LIASE"]
    },
    "IMUNIDADE": {
        "nome": "Função Imunológica",
        "marcadores": ["IMUNOGLOBULINA_A", "IMUNOGLOBULINA_E", "IMUNOGLOBULINA_G", "IMUNOGLOBULINA_M", "COMPLEMENTO_C3", "COMPLEMENTO_C4"]
    },
    "DIGESTIVA": {
        "nome": "Saúde Digestiva",
        "marcadores": ["ZONULINA", "LPS", "CALPROTECTINA_FECAL", "ELASTASE_PANCREATICA", "LIPASE", "AMILASE"]
    },
    "DETOXIFICACAO": {
        "nome": "Sistema Detoxificação",
        "marcadores": ["GLUTATIONA", "SOD", "CATALASE", "MALONILDIALDEIDO", "BILIRRUBINA"]
    },
    "OSSO": {
        "nome": "Metabolismo Ósseo",
        "marcadores": ["CALCIO", "FOSFORO", "MAGNESIO", "VITAMINA_D", "P1NP", "CTX", "FOSFATASE_ALCALINA"]
    },
    "CARDIOVASCULAR": {
        "nome": "Saúde Cardiovascular",
        "marcadores": ["PRESSAO_SISTOLICA", "PRESSAO_DIASTOLICA", "FREQUENCIA_CARDIACA", "TRIGLICERIDES", "LDL", "HOMOCISTEINA", "LFAPOLIPROTEINA"]
    },
    "NEUROENDOCRINO": {
        "nome": "Eixo Neuroendócrino",
        "marcadores": ["CORTISOL", "DHEA", "TESTOSTERONA", "ESTRADIOL", "PROGESTERONA", "FSH", "LH", "PROLACTINA"]
    }
}

# Referências para cada marcador (por sexo, faixa etária)
LAB_REFERENCES = {
    "RBC": {
        "nome": "Eritrócitos",
        "unidade": "milhões/μL",
        "M": {"18-45": {"min": 4.5, "max": 5.9}, "46-60": {"min": 4.5, "max": 5.9}, ">60": {"min": 4.2, "max": 5.9}},
        "F": {"18-45": {"min": 4.1, "max": 5.1}, "46-60": {"min": 4.0, "max": 5.2}, ">60": {"min": 3.8, "max": 5.2}},
        "ideal": {"M": 5.2, "F": 4.6}
    },
    "WBC": {
        "nome": "Leucócitos",
        "unidade": "mil/μL",
        "M": {"geral": {"min": 4.5, "max": 11.0}},
        "F": {"geral": {"min": 4.5, "max": 11.0}},
        "ideal": {"M": 7.0, "F": 7.0}
    },
    "HB": {
        "nome": "Hemoglobina",
        "unidade": "g/dL",
        "M": {"18-45": {"min": 13.5, "max": 17.5}, "46-60": {"min": 13.0, "max": 17.0}, ">60": {"min": 12.5, "max": 17.0}},
        "F": {"18-45": {"min": 12.0, "max": 15.5}, "46-60": {"min": 11.5, "max": 15.5}, ">60": {"min": 11.0, "max": 15.5}},
        "ideal": {"M": 15.0, "F": 13.5}
    },
    "HT": {
        "nome": "Hematócrito",
        "unidade": "%",
        "M": {"18-45": {"min": 41, "max": 53}, "46-60": {"min": 39, "max": 52}, ">60": {"min": 38, "max": 52}},
        "F": {"18-45": {"min": 36, "max": 46}, "46-60": {"min": 35, "max": 46}, ">60": {"min": 34, "max": 46}},
        "ideal": {"M": 47, "F": 41}
    },
    "PLT": {
        "nome": "Plaquetas",
        "unidade": "mil/μL",
        "M": {"geral": {"min": 150, "max": 400}},
        "F": {"geral": {"min": 150, "max": 400}},
        "ideal": {"M": 250, "F": 250}
    },
    "MCV": {
        "nome": "Volume Corpuscular Médio",
        "unidade": "fL",
        "M": {"geral": {"min": 80, "max": 100}},
        "F": {"geral": {"min": 80, "max": 100}},
        "ideal": {"M": 90, "F": 90}
    },
    "GLICOSE_JEJUM": {
        "nome": "Glicose em Jejum",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 70, "max": 100}},
        "F": {"geral": {"min": 70, "max": 100}},
        "ideal": {"M": 85, "F": 85}
    },
    "AST": {
        "nome": "Aspartato Aminotransferase",
        "unidade": "U/L",
        "M": {"geral": {"min": 10, "max": 40}},
        "F": {"geral": {"min": 7, "max": 35}},
        "ideal": {"M": 25, "F": 20}
    },
    "ALT": {
        "nome": "Alanina Aminotransferase",
        "unidade": "U/L",
        "M": {"geral": {"min": 7, "max": 56}},
        "F": {"geral": {"min": 7, "max": 45}},
        "ideal": {"M": 30, "F": 25}
    },
    "COLESTEROL_TOTAL": {
        "nome": "Colesterol Total",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 0, "max": 200}},
        "F": {"geral": {"min": 0, "max": 200}},
        "ideal": {"M": 160, "F": 160}
    },
    "LDL": {
        "nome": "LDL-Colesterol",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 0, "max": 130}},
        "F": {"geral": {"min": 0, "max": 130}},
        "ideal": {"M": 100, "F": 100}
    },
    "HDL": {
        "nome": "HDL-Colesterol",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 40, "max": 300}},
        "F": {"geral": {"min": 50, "max": 300}},
        "ideal": {"M": 60, "F": 70}
    },
    "TRIGLICERIDES": {
        "nome": "Triglicerídeos",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 0, "max": 150}},
        "F": {"geral": {"min": 0, "max": 150}},
        "ideal": {"M": 100, "F": 100}
    },
    "TSH": {
        "nome": "Hormônio Estimulante da Tireóide",
        "unidade": "mIU/L",
        "M": {"geral": {"min": 0.4, "max": 4.0}},
        "F": {"geral": {"min": 0.4, "max": 4.0}},
        "ideal": {"M": 2.0, "F": 2.0}
    },
    "VITAMINA_D": {
        "nome": "25-OH Vitamina D",
        "unidade": "ng/mL",
        "M": {"geral": {"min": 30, "max": 100}},
        "F": {"geral": {"min": 30, "max": 100}},
        "ideal": {"M": 50, "F": 50}
    },
    "FERRO": {
        "nome": "Ferro Sérico",
        "unidade": "μg/dL",
        "M": {"18-45": {"min": 60, "max": 170}, ">45": {"min": 50, "max": 170}},
        "F": {"18-45": {"min": 50, "max": 170}, "46-60": {"min": 40, "max": 150}, ">60": {"min": 40, "max": 150}},
        "ideal": {"M": 100, "F": 90}
    },
    "FERRITINA": {
        "nome": "Ferritina",
        "unidade": "ng/mL",
        "M": {"geral": {"min": 24, "max": 336}},
        "F": {"18-45": {"min": 12, "max": 200}, ">45": {"min": 12, "max": 200}},
        "ideal": {"M": 100, "F": 80}
    },
    "MAGNESIO": {
        "nome": "Magnésio",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 1.7, "max": 2.2}},
        "F": {"geral": {"min": 1.7, "max": 2.2}},
        "ideal": {"M": 2.0, "F": 2.0}
    },
    "PCR": {
        "nome": "Proteína C Reativa",
        "unidade": "mg/L",
        "M": {"geral": {"min": 0, "max": 3.0}},
        "F": {"geral": {"min": 0, "max": 3.0}},
        "ideal": {"M": 1.0, "F": 1.0}
    },
    "HOMOCISTEINA": {
        "nome": "Homocisteína",
        "unidade": "μmol/L",
        "M": {"geral": {"min": 5, "max": 15}},
        "F": {"geral": {"min": 5, "max": 14}},
        "ideal": {"M": 10, "F": 9}
    },
    "INSULINA_JEJUM": {
        "nome": "Insulina em Jejum",
        "unidade": "μUI/mL",
        "M": {"geral": {"min": 2, "max": 12}},
        "F": {"geral": {"min": 2, "max": 12}},
        "ideal": {"M": 5, "F": 5}
    },
    "HBA1C": {
        "nome": "Hemoglobina Glicada",
        "unidade": "%",
        "M": {"geral": {"min": 4.0, "max": 5.7}},
        "F": {"geral": {"min": 4.0, "max": 5.7}},
        "ideal": {"M": 5.0, "F": 5.0}
    },
    "CREATININA": {
        "nome": "Creatinina",
        "unidade": "mg/dL",
        "M": {"18-60": {"min": 0.7, "max": 1.3}, ">60": {"min": 0.6, "max": 1.2}},
        "F": {"18-60": {"min": 0.6, "max": 1.1}, ">60": {"min": 0.5, "max": 1.1}},
        "ideal": {"M": 0.95, "F": 0.85}
    },
    "UREA": {
        "nome": "Ureia",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 7, "max": 20}},
        "F": {"geral": {"min": 7, "max": 20}},
        "ideal": {"M": 14, "F": 14}
    },
    "CALCIO": {
        "nome": "Cálcio Total",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 8.5, "max": 10.2}},
        "F": {"geral": {"min": 8.5, "max": 10.2}},
        "ideal": {"M": 9.3, "F": 9.3}
    },
    "FOSFORO": {
        "nome": "Fósforo",
        "unidade": "mg/dL",
        "M": {"geral": {"min": 2.5, "max": 4.5}},
        "F": {"geral": {"min": 2.5, "max": 4.5}},
        "ideal": {"M": 3.5, "F": 3.5}
    }
}

# Condutas e recomendações por marcador
LAB_CONDUCTS = {
    "RBC": {
        "baixo": "Possível anemia. Investigar fontes de ferro, B12, ácido fólico. Aumentar absorção de ferro (vitamina C).",
        "alto": "Possível policitemia. Avaliar hidratação, EPO. Reduzir viscosidade sanguínea."
    },
    "WBC": {
        "baixo": "Possível imunossupressão. Avaliar infecção, estresse, nutrição (zinco, vitamina C).",
        "alto": "Possível inflamação crônica. Investigar infecção, estresse. Suportar sistema imunológico."
    },
    "HB": {
        "baixo": "Anemia presente. Reforçar ferro, B12, ácido fólico. Avaliar perdas (gastrointestinais).",
        "alto": "Policitemia. Aumentar hidratação, reduzir ferro."
    },
    "GLICOSE_JEJUM": {
        "baixo": "Hipoglicemia em jejum. Aumentar ingestão de carboidratos complexos. Avaliar função adrenal.",
        "alto": "Hiperglicemia. Reduzir carboidratos simples, aumentar atividade física, considerar cromo e canela."
    },
    "LDL": {
        "alto": "Dislipidemia. Aumentar fibras, omega-3, reduzir gordura saturada. Considerar levedo de arroz vermelho, berberina."
    },
    "HDL": {
        "baixo": "HDL reduzido. Aumentar atividade física, ácidos graxos insaturados, reduzir carboidratos simples."
    },
    "TRIGLICERIDES": {
        "alto": "Hipertrigliceridemia. Reduzir carboidratos simples, aumentar ômega-3, álcool moderado."
    },
    "TSH": {
        "alto": "Hipotireoidismo subclínico. Investigar iodo, selênio, zinco. Considerar L-tirosina.",
        "baixo": "Hipertireoidismo subclínico. Reduzir stress, suportar conversão T4->T3."
    },
    "VITAMINA_D": {
        "baixo": "Deficiência de vitamina D. Suplementação 2000-4000 UI/dia. Aumentar exposição solar (15-20 min)."
    },
    "FERRO": {
        "baixo": "Deficiência de ferro. Suplementar ferro (com vitamina C). Investigar perdas.",
        "alto": "Sobrecarga de ferro. Reduzir suplementação, aumentar polifenóis (chá, vinho tinto)."
    },
    "FERRITINA": {
        "baixo": "Estoque de ferro baixo. Suplementar ferro, melhorar absorção.",
        "alto": "Inflamação crônica ou sobrecarga. Avaliar oxidativo, reduzir ferro, aumentar antioxidantes."
    },
    "MAGNESIO": {
        "baixo": "Deficiência de magnésio. Suplementar 300-400mg/dia. Reduzir cafeína."
    },
    "PCR": {
        "alto": "Inflamação sistêmica. Reduzir gordura saturada, aumentar ômega-3, curcumina, gengibre."
    },
    "HOMOCISTEINA": {
        "alto": "Hiperhomocisteinemia. Aumentar B6, B12, ácido fólico. Reduzir metionina (carne vermelha)."
    },
    "INSULINA_JEJUM": {
        "alto": "Resistência à insulina. Reduzir carboidratos simples, aumentar fibra, atividade física regular."
    },
    "AST": {
        "alto": "Transaminase elevada. Investigar hepatotoxicidade. Suportar fígado (silimarina, NAC)."
    },
    "ALT": {
        "alto": "ALT elevada. Possível hepatopatia gordurosa. Reduzir frutose, aumentar atividade física."
    }
}

# Suplementações recomendadas por perfil
LAB_SUPPLEMENTATION = {
    "DEFICIENCIA_FERRO": ["Ferro Quelado", "Vitamina C", "Betaína"],
    "ANEMIA": ["Ferro", "B12", "Ácido Fólico", "Cobre"],
    "DISLIPIDEMIA": ["Omega-3", "Berberina", "Levedo Arroz Vermelho", "Monacol"],
    "RESISTENCIA_INSULINA": ["Cromo", "Inositol", "Canela", "Berberina"],
    "HIPOTIREOIDISMO": ["L-Tirosina", "Iodo", "Selênio", "Zinco"],
    "INFLAMACAO": ["Omega-3", "Curcumina", "Gengibre", "Quercetina"],
    "DEFICIENCIA_VITAMINA_D": ["Vitamina D3 2000-4000UI"],
    "HIPERHOMOCISTEINA": ["B6", "B12", "Ácido Fólico", "Betaína"],
    "STRESS_OXIDATIVO": ["NAC", "Glutationa", "Vitamina E", "Vitamina C"],
    "INTESTINO_PERMEAVEL": ["L-Glutamina", "Zinco", "Colágeno", "Probióticos"]
}


import sqlite3, os
from datetime import datetime

DB=os.getenv("DB_PATH","madilab_clinica.db")

def conn(): 
    return sqlite3.connect(DB)

def init_db():
    c=conn()
    
    # Tabela de pacientes (estendida para MadiLab Premium)
    c.execute("""CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE,
        data_nascimento TEXT,
        genero TEXT,
        altura REAL,
        peso REAL,
        data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Tabela de avaliações clínicas (original)
    c.execute("""CREATE TABLE IF NOT EXISTS assessments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        queixas TEXT,
        exames TEXT,
        observacoes TEXT,
        analise_ia TEXT,
        altura REAL,
        peso REAL,
        arquivo_exame TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )""")
    
    # Tabela de exames laboratoriais MadiLab
    c.execute("""CREATE TABLE IF NOT EXISTS lab_exams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        data_exame TEXT DEFAULT CURRENT_TIMESTAMP,
        numero_exame INTEGER,
        peso_exame REAL,
        altura_exame REAL,
        imc_exame REAL,
        madilab_score REAL,
        nivel_inflamacao TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )""")
    
    # Tabela de marcadores laboratoriais
    c.execute("""CREATE TABLE IF NOT EXISTS lab_markers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER,
        marker_code TEXT,
        marker_name TEXT,
        valor REAL,
        unidade TEXT,
        referencia_minima REAL,
        referencia_maxima REAL,
        valor_ideal REAL,
        status TEXT,
        conduta TEXT,
        suplementacoes TEXT,
        FOREIGN KEY(exam_id) REFERENCES lab_exams(id)
    )""")
    
    # Tabela de suplementações recomendadas
    c.execute("""CREATE TABLE IF NOT EXISTS recommendations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        data_recomendacao TEXT DEFAULT CURRENT_TIMESTAMP,
        suplementacao TEXT,
        dosagem TEXT,
        frequencia TEXT,
        duracao TEXT,
        justificativa TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    )""")
    
    c.commit()
    c.close()

# ===== OPERAÇÕES PACIENTES =====
def add_patient(nome, cpf, nasc, genero, altura, peso):
    c=conn()
    c.execute("""INSERT INTO patients(nome, cpf, data_nascimento, genero, altura, peso) 
                 VALUES(?, ?, ?, ?, ?, ?)""",
              (nome, cpf or None, nasc, genero or "N", altura or None, peso or None))
    c.commit()
    c.close()

def list_patients():
    c=conn()
    rows=c.execute("SELECT id, nome, cpf, data_nascimento, genero, altura, peso FROM patients ORDER BY nome").fetchall()
    c.close()
    return rows

def get_patient(pid):
    c=conn()
    r=c.execute("SELECT id, nome, cpf, data_nascimento, genero, altura, peso FROM patients WHERE id=?", (pid,)).fetchone()
    c.close()
    return r

def update_patient(pid, nome, cpf, nasc, genero, altura, peso):
    c=conn()
    c.execute("""UPDATE patients SET nome=?, cpf=?, data_nascimento=?, genero=?, altura=?, peso=? 
                 WHERE id=?""", (nome, cpf, nasc, genero, altura, peso, pid))
    c.commit()
    c.close()

# ===== OPERAÇÕES EXAMES MADILAB =====
def add_lab_exam(patient_id, peso=None, altura=None):
    """Registra um novo exame laboratorial para um paciente"""
    c=conn()
    
    # Calcula número do exame
    count = c.execute("SELECT COUNT(*) FROM lab_exams WHERE patient_id=?", (patient_id,)).fetchone()[0]
    numero_exame = count + 1
    
    imc = None
    if altura and peso:
        imc = peso / ((altura/100) ** 2)
    
    c.execute("""INSERT INTO lab_exams(patient_id, numero_exame, peso_exame, altura_exame, imc_exame)
                 VALUES(?, ?, ?, ?, ?)""",
              (patient_id, numero_exame, peso or None, altura or None, imc or None))
    
    exam_id = c.lastrowid
    c.commit()
    c.close()
    return exam_id

def get_lab_exams(patient_id):
    """Lista todos os exames de um paciente"""
    c=conn()
    rows=c.execute("""SELECT id, data_exame, numero_exame, peso_exame, altura_exame, imc_exame, madilab_score, nivel_inflamacao
                      FROM lab_exams WHERE patient_id=? ORDER BY data_exame DESC""", 
                   (patient_id,)).fetchall()
    c.close()
    return rows

def get_lab_exam(exam_id):
    """Obtém detalhes de um exame específico"""
    c=conn()
    r=c.execute("""SELECT id, patient_id, data_exame, numero_exame, peso_exame, altura_exame, imc_exame, madilab_score, nivel_inflamacao
                   FROM lab_exams WHERE id=?""", (exam_id,)).fetchone()
    c.close()
    return r

def update_lab_exam_score(exam_id, madilab_score, nivel_inflamacao):
    """Atualiza o score MadiLab e nível de inflamação de um exame"""
    c=conn()
    c.execute("""UPDATE lab_exams SET madilab_score=?, nivel_inflamacao=? WHERE id=?""",
              (madilab_score, nivel_inflamacao, exam_id))
    c.commit()
    c.close()

# ===== OPERAÇÕES MARCADORES =====
def add_lab_marker(exam_id, marker_code, marker_name, valor, unidade, ref_min, ref_max, ideal, status, conduta, suppl):
    """Registra um marcador laboratorial em um exame"""
    c=conn()
    c.execute("""INSERT INTO lab_markers(exam_id, marker_code, marker_name, valor, unidade, 
                                         referencia_minima, referencia_maxima, valor_ideal, 
                                         status, conduta, suplementacoes)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (exam_id, marker_code, marker_name, valor, unidade, ref_min, ref_max, ideal, status, conduta, suppl))
    c.commit()
    c.close()

def get_lab_markers(exam_id):
    """Lista todos os marcadores de um exame"""
    c=conn()
    rows=c.execute("""SELECT id, exam_id, marker_code, marker_name, valor, unidade, 
                             referencia_minima, referencia_maxima, valor_ideal, status, conduta, suplementacoes
                      FROM lab_markers WHERE exam_id=? ORDER BY marker_code""",
                   (exam_id,)).fetchall()
    c.close()
    return rows

def get_marker_history(patient_id, marker_code):
    """Obtém histórico de um marcador específico para um paciente"""
    c=conn()
    rows=c.execute("""SELECT le.data_exame, lm.valor, lm.status, lm.referencia_minima, lm.referencia_maxima
                      FROM lab_markers lm
                      JOIN lab_exams le ON lm.exam_id = le.id
                      WHERE le.patient_id=? AND lm.marker_code=?
                      ORDER BY le.data_exame ASC""",
                   (patient_id, marker_code)).fetchall()
    c.close()
    return rows

# ===== OPERAÇÕES RECOMENDAÇÕES =====
def add_recommendation(patient_id, suplementacao, dosagem, frequencia, duracao, justificativa):
    """Registra uma recomendação de suplementação"""
    c=conn()
    c.execute("""INSERT INTO recommendations(patient_id, suplementacao, dosagem, frequencia, duracao, justificativa)
                 VALUES(?, ?, ?, ?, ?, ?)""",
              (patient_id, suplementacao, dosagem, frequencia, duracao, justificativa))
    c.commit()
    c.close()

def get_recommendations(patient_id):
    """Lista recomendações ativas de um paciente"""
    c=conn()
    rows=c.execute("""SELECT id, suplementacao, dosagem, frequencia, duracao, justificativa, data_recomendacao
                      FROM recommendations WHERE patient_id=? ORDER BY data_recomendacao DESC""",
                   (patient_id,)).fetchall()
    c.close()
    return rows

# ===== AVALIAÇÕES CLÍNICAS (ORIGINAL) =====
def add_assessment(pid, q, e, o, ai, altura, peso, arquivo):
    c=conn()
    c.execute("""INSERT INTO assessments(patient_id, queixas, exames, observacoes, analise_ia, altura, peso, arquivo_exame)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
              (pid, q, e, o, ai, altura or None, peso or None, arquivo or None))
    c.commit()
    c.close()

def list_assessments(pid):
    c=conn()
    r=c.execute("""SELECT id, data_registro, queixas, exames, observacoes, analise_ia, altura, peso, arquivo_exame 
                   FROM assessments WHERE patient_id=? ORDER BY id DESC""",
                (pid,)).fetchall()
    c.close()
    return r

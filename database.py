import sqlite3, os
DB=os.getenv("DB_PATH","bioaura_clinica.db")
def conn(): return sqlite3.connect(DB)
def init_db():
    c=conn()
    c.execute("""CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL,cpf TEXT UNIQUE,data_nascimento TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS assessments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,patient_id INTEGER,data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        queixas TEXT,exames TEXT,observacoes TEXT,analise_ia TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id))""")
    c.commit(); c.close()
def add_patient(nome,cpf,nasc):
    c=conn(); c.execute("INSERT INTO patients(nome,cpf,data_nascimento) VALUES(?,?,?)",(nome,cpf or None,nasc)); c.commit(); c.close()
def list_patients():
    c=conn(); rows=c.execute("SELECT id,nome,cpf,data_nascimento FROM patients ORDER BY nome").fetchall(); c.close(); return rows
def get_patient(pid):
    c=conn(); r=c.execute("SELECT id,nome,cpf,data_nascimento FROM patients WHERE id=?",(pid,)).fetchone(); c.close(); return r
def add_assessment(pid,q,e,o,ai):
    c=conn(); c.execute("INSERT INTO assessments(patient_id,queixas,exames,observacoes,analise_ia) VALUES(?,?,?,?,?)",(pid,q,e,o,ai)); c.commit(); c.close()
def list_assessments(pid):
    c=conn(); r=c.execute("SELECT id,data_registro,queixas,exames,observacoes,analise_ia FROM assessments WHERE patient_id=? ORDER BY id DESC",(pid,)).fetchall(); c.close(); return r

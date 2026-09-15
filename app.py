import os
import streamlit as st
from datetime import datetime
from database import (
    init_db, add_patient, list_patients, get_patient,
    add_lab_exam, get_lab_exams, get_lab_exam, add_lab_marker, 
    get_lab_markers, update_lab_exam_score, get_marker_history
)
from madilab_engine import evaluate_marker, calculate_madilab_score
from labpro_markers import LAB_REFERENCES, LAB_PROFILES
from ia import extract_pdf_text, analyze_case
from pdf import generate_pdf
import pandas as pd
import plotly.graph_objects as go

# CONFIG
st.set_page_config(page_title="🧬 MadiLab Premium", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

init_db()

PROFISSIONAL = os.getenv("PROFISSIONAL", "Enf. Mardson Bastos Rodrigues")
REGISTRO = os.getenv("REGISTRO", "COREN-RR 625485")

# LOGIN
def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='color: #1A365D;'>🧬 MadiLab Premium</h1>
            <p style='font-size: 1.2rem; color: #1A365D;'>Sistema Inteligente de Análise Laboratorial</p>
            <p style='color: #666;'>Leitura Funcional com IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário")
            senha = st.text_input("🔐 Senha", type="password")
            
            if st.form_submit_button("🔓 Entrar", use_container_width=True, type="primary"):
                if usuario == "mardson" and senha == "239899SSPrr":
                    st.session_state.logged = True
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha inválidos!")

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

# CSS
st.markdown("""
<style>
.stMetric { background: linear-gradient(135deg, #1A365D15 0%, #fff 100%); border-radius: 12px; padding: 15px; border: 1px solid #ddd; }
.header-section { background: linear-gradient(90deg, #1A365D 0%, #2D5C8C 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🧬 MadiLab Premium")
    st.divider()
    
    page = st.radio("Menu", ["🏠 Dashboard", "👤 Pacientes", "🧪 Novo Exame", "📊 Análise", "📈 Evolução", "📄 PDF"])
    
    st.divider()
    if st.button("🚪 SAIR", type="secondary", use_container_width=True):
        st.session_state.logged = False
        st.rerun()

patients = list_patients()

# DASHBOARD
if page == "🏠 Dashboard":
    st.markdown("<div class='header-section'><h1>🧬 MadiLab Premium - Dashboard</h1></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    total_exams = sum(len(get_lab_exams(p[0])) for p in patients)
    
    col1.metric("👤 Pacientes", len(patients))
    col2.metric("🧪 Exames", total_exams)
    col3.metric("🤖 IA", "✅ Ativa" if os.getenv("OPENAI_API_KEY") else "❌ Inativa")
    col4.metric("📅 Hoje", datetime.now().strftime("%d/%m/%Y"))
    
    st.divider()
    st.info("📖 **MadiLab Premium** - Use o menu para gerenciar pacientes e exames laboratoriais.")

# PACIENTES
elif page == "👤 Pacientes":
    st.markdown("<div class='header-section'><h1>👤 Gerenciar Pacientes</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Novo", "📋 Lista"])
    
    with tab1:
        with st.form("novo_paciente_form"):
            nome = st.text_input("👤 Nome Completo")
            cpf = st.text_input("📋 CPF")
            nasc = st.text_input("📅 Data de Nascimento (DD/MM/AAAA)")
            genero = st.selectbox("⚤ Gênero", ["M", "F", "O"])
            altura = st.number_input("📏 Altura (cm)", min_value=50.0, max_value=250.0, value=170.0)
            peso = st.number_input("⚖️ Peso (kg)", min_value=1.0, max_value=300.0, value=70.0)
            
            if st.form_submit_button("✅ Salvar", type="primary", use_container_width=True):
                if nome.strip():
                    try:
                        add_patient(nome.strip(), cpf.strip() or None, nasc.strip() or None, genero, altura, peso)
                        st.success(f"✅ Paciente '{nome}' cadastrado!")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
    
    with tab2:
        if patients:
            for p in patients:
                exams = len(get_lab_exams(p[0]))
                st.write(f"**{p[1]}** | CPF: {p[2] or 'N/A'} | Gênero: {p[4]} | {exams} exame(s)")
                st.divider()
        else:
            st.info("Nenhum paciente cadastrado.")

# NOVO EXAME
elif page == "🧪 Novo Exame":
    st.markdown("<div class='header-section'><h1>🧪 Novo Exame Laboratorial</h1></div>", unsafe_allow_html=True)
    
    if not patients:
        st.warning("⚠️ Cadastre um paciente primeiro")
        st.stop()
    
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("👤 Paciente", list(labels))
    paciente_id = labels[paciente_nome]
    paciente_dados = get_patient(paciente_id)
    
    genero = paciente_dados[4] if paciente_dados[4] else "M"
    
    if paciente_dados[3]:
        try:
            data_nasc = datetime.strptime(paciente_dados[3], "%d/%m/%Y")
            idade = (datetime.now() - data_nasc).days // 365
        except:
            idade = 30
    else:
        idade = 30
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📏", f"{paciente_dados[5]:.1f} cm")
    col2.metric("⚖️", f"{paciente_dados[6]:.1f} kg")
    imc = paciente_dados[6] / ((paciente_dados[5]/100)**2)
    col3.metric("📊", f"{imc:.1f}")
    col4.metric("📅", f"{idade} anos")
    
    st.divider()
    
    if st.button("📝 Iniciar Novo Exame", type="primary", use_container_width=True):
        exam_id = add_lab_exam(paciente_id, paciente_dados[6], paciente_dados[5])
        st.session_state["current_exam_id"] = exam_id
        st.success("✅ Exame criado!")
        st.rerun()
    
    if "current_exam_id" in st.session_state:
        exam_id = st.session_state["current_exam_id"]
        exam = get_lab_exam(exam_id)
        
        st.markdown(f"### 📊 Exame #{exam[3]}")
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            marker_code = st.selectbox("Marcador", sorted(LAB_REFERENCES.keys()), format_func=lambda x: f"{x} - {LAB_REFERENCES[x].get('nome', x)}")
        with col2:
            valor = st.number_input("Valor", step=0.1)
        with col3:
            if st.button("➕ Adicionar", type="primary", use_container_width=True):
                if marker_code and valor >= 0:
                    evaluation = evaluate_marker(marker_code, valor, genero, idade)
                    add_lab_marker(exam_id, marker_code, LAB_REFERENCES[marker_code].get("nome"), valor, 
                                  LAB_REFERENCES[marker_code].get("unidade", ""), evaluation.get("referencia_min"), 
                                  evaluation.get("referencia_max"), evaluation.get("valor_ideal"), 
                                  evaluation.get("status"), evaluation.get("conduta"), evaluation.get("suplementacoes"))
                    st.success(f"✅ {marker_code} adicionado!")
                    st.rerun()
        
        markers = get_lab_markers(exam_id)
        
        if markers:
            st.markdown("### 📋 Marcadores")
            st.divider()
            
            for m in markers:
                status_icon = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}.get(m[9], "⚪")
                with st.expander(f"{status_icon} **{m[3]}** ({m[1]}) - {m[4]:.1f} {m[5]}"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Valor", f"{m[4]:.1f}")
                    col2.metric("Ref Mín", f"{m[6]:.1f}")
                    col3.metric("Ref Máx", f"{m[7]:.1f}")
                    col4.metric("Ideal", f"{m[8]:.1f}")
                    st.write(f"**Status:** {m[9].upper()}")
                    st.write(f"**Conduta:** {m[10]}")
                    if m[11]:
                        st.write(f"**Suplementações:** {m[11]}")
            
            markers_data = [{"marker_code": m[1], "status": m[9]} for m in markers]
            score, inflamacao = calculate_madilab_score(markers_data)
            update_lab_exam_score(exam_id, score, inflamacao)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎯 Score", f"{score:.1f}/100")
            col2.metric("🔥 Inflamação", inflamacao)
            col3.metric("📋", len(markers))
            col4.metric("📅", exam[2])
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Finalizar", type="primary", use_container_width=True):
                    st.success("✅ Exame finalizado!")
                    del st.session_state["current_exam_id"]
                    st.balloons()
                    st.rerun()
            with col2:
                if st.button("❌ Cancelar", use_container_width=True):
                    del st.session_state["current_exam_id"]
                    st.rerun()

# ANÁLISE
elif page == "📊 Análise":
    st.markdown("<div class='header-section'><h1>📊 Análise de Exames</h1></div>", unsafe_allow_html=True)
    
    if not patients:
        st.stop()
    
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("👤 Paciente", list(labels), key="analysis_patient")
    paciente_id = labels[paciente_nome]
    
    exams = get_lab_exams(paciente_id)
    
    if not exams:
        st.info("Nenhum exame registrado.")
        st.stop()
    
    exam_options = {f"Exame #{e[2]} - {e[1]}": e[0] for e in exams}
    selected_exam = st.selectbox("🧪 Exame", list(exam_options.keys()))
    exam_id = exam_options[selected_exam]
    
    exam = get_lab_exam(exam_id)
    markers = get_lab_markers(exam_id)
    
    if markers:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Score", f"{exam[7] or 0:.1f}/100")
        col2.metric("🔥 Inflamação", exam[8] or "N/A")
        col3.metric("📋 Marcadores", len(markers))
        col4.metric("📅", exam[2])
        
        st.divider()
        
        df_markers = pd.DataFrame([
            {
                "Status": {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}.get(m[9], "⚪"),
                "Marcador": m[3],
                "Valor": f"{m[4]:.1f} {m[5]}",
                "Ref": f"{m[6]:.1f}-{m[7]:.1f}",
                "Ideal": f"{m[8]:.1f}"
            }
            for m in markers
        ])
        
        st.dataframe(df_markers, use_container_width=True, hide_index=True)

# EVOLUÇÃO
elif page == "📈 Evolução":
    st.markdown("<div class='header-section'><h1>📈 Evolução Clínica</h1></div>", unsafe_allow_html=True)
    
    if not patients:
        st.stop()
    
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("👤 Paciente", list(labels), key="evolution_patient")
    paciente_id = labels[paciente_nome]
    
    exams = get_lab_exams(paciente_id)
    
    if len(exams) < 2:
        st.warning("⚠️ Necessário 2+ exames")
        st.stop()
    
    scores = [(e[1], e[6]) for e in exams if e[6]]
    
    if scores:
        df_scores = pd.DataFrame(scores, columns=["Data", "Score"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_scores["Data"], y=df_scores["Score"], mode='lines+markers', name='Score'))
        fig.update_layout(title="Score MadiLab", xaxis_title="Data", yaxis_title="Score", height=400)
        st.plotly_chart(fig, use_container_width=True)

# PDF
elif page == "📄 PDF":
    st.markdown("<div class='header-section'><h1>📄 Gerar PDF</h1></div>", unsafe_allow_html=True)
    
    if not patients:
        st.stop()
    
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("👤 Paciente", list(labels), key="pdf_patient")
    paciente_id = labels[paciente_nome]
    
    exams = get_lab_exams(paciente_id)
    
    if not exams:
        st.stop()
    
    exam_options = {f"Exame #{e[2]} - {e[1]}": e[0] for e in exams}
    selected_exam = st.selectbox("🧪 Exame", list(exam_options.keys()))
    exam_id = exam_options[selected_exam]
    
    exam = get_lab_exam(exam_id)
    markers = get_lab_markers(exam_id)
    
    if st.button("📄 Gerar PDF", type="primary", use_container_width=True):
        try:
            content = f"# MadiLab Premium\n## {paciente_nome}\nData: {exam[2]}\nScore: {exam[7]:.1f}/100"
            pdf = generate_pdf(paciente_nome, exam[4], exam[5], content, PROFISSIONAL, REGISTRO)
            st.download_button(label="⬇️ Baixar", data=pdf.getvalue(), file_name=f"madilab_{paciente_nome}.pdf", mime="application/pdf", type="primary", use_container_width=True)
            st.success("✅ PDF gerado!")
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

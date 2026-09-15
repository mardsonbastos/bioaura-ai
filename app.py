import os
import streamlit as st
from datetime import datetime
from database import init_db, add_patient, list_patients, get_patient, add_lab_exam, get_lab_exams, get_lab_exam, add_lab_marker, get_lab_markers, update_lab_exam_score, add_recommendation, get_recommendations, get_marker_history
from madilab_engine import evaluate_marker, calculate_madilab_score, generate_marker_report, analyze_exam_bulk
from labpro_markers import LAB_REFERENCES, LAB_PROFILES
from ia import extract_pdf_text, analyze_case
from pdf import generate_pdf
from datetime import date
import pandas as pd
import plotly.graph_objects as go

# ===== CONFIGURAÇÃO STREAMLIT =====
st.set_page_config(
    page_title="MadiLab Premium",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

PROFISSIONAL = os.getenv("PROFISSIONAL", "Enf. Mardson Bastos Rodrigues")
REGISTRO = os.getenv("REGISTRO", "COREN-RR 625485")

# ===== AUTENTICAÇÃO =====
def login():
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>🧬 MadiLab Premium</h1>
        <p style='font-size: 1.2rem; color: #1A365D;'>Sistema Inteligente de Análise Laboratorial</p>
        <p style='color: #666;'>Leitura Funcional com IA • Medicina Baseada em Evidências</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar", type="primary"):
            if u == "mardson" and p == "239899SSPrr":
                st.session_state.logged = True
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

# ===== CSS CUSTOMIZADO =====
st.markdown("""
<style>
.block-container { padding: 1rem; max-width: 1400px; }
.login { text-align: center; padding: 2rem 0; }
div[data-testid="stMetric"] { 
    border: 1px solid #ddd; 
    border-radius: 12px; 
    padding: 10px; 
    background: linear-gradient(135deg, #1A365D15 0%, #fff 100%);
}
@media (max-width:700px) { 
    .block-container { padding: .7rem; }
    .stButton button { width: 100%; }
}
</style>
""", unsafe_allow_html=True)

# ===== INTERFACE PRINCIPAL =====
st.title("🧬 MadiLab Premium")
st.caption(f"{PROFISSIONAL} • {REGISTRO}")

with st.sidebar:
    st.header("Menu")
    page = st.radio(
        "Ir para",
        ["🏠 Dashboard", "👤 Pacientes", "🧪 Novo Exame", "📊 Análise", "📈 Evolução", "📄 PDF", "🚪 Sair"]
    )
    if st.button("🚪 Sair"):
        st.session_state.logged = False
        st.rerun()

patients = list_patients()

# ===== DASHBOARD =====
if page == "🏠 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    total_exams = sum(len(get_lab_exams(p[0])) for p in patients)
    col1.metric("👤 Pacientes", len(patients))
    col2.metric("🧪 Exames", total_exams)
    col3.metric("🤖 IA", "Ativa" if os.getenv("OPENAI_API_KEY") else "Não")
    col4.metric("📅 Hoje", datetime.now().strftime("%d/%m/%Y"))
    st.info("📖 **MadiLab Premium** - Use o menu para cadastrar pacientes e registrar exames.")
    if patients:
        st.subheader("📋 Últimos Pacientes")
        for p in patients[:5]:
            exams_count = len(get_lab_exams(p[0]))
            st.write(f"**{p[1]}** • {exams_count} exame(s)")

# ===== PACIENTES =====
elif page == "👤 Pacientes":
    st.header("Cadastro de Pacientes")
    tab1, tab2 = st.tabs(["Novo Paciente", "Lista"])
    with tab1:
        with st.form("novo_paciente"):
            nome = st.text_input("Nome completo *")
            cpf = st.text_input("CPF")
            nasc = st.text_input("Data de nascimento (DD/MM/AAAA)")
            genero = st.selectbox("Gênero", ["M", "F"])
            col1, col2 = st.columns(2)
            with col1:
                altura = st.number_input("Altura (cm)", min_value=50.0, max_value=250.0, step=0.1)
            with col2:
                peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, step=0.1)
            if st.form_submit_button("✅ Salvar", type="primary"):
                if nome.strip():
                    try:
                        add_patient(nome.strip(), cpf.strip() or None, nasc.strip() or None, genero, altura, peso)
                        st.success("✅ Paciente cadastrado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
                else:
                    st.error("Nome é obrigatório.")
    with tab2:
        if patients:
            for p in patients:
                exams = get_lab_exams(p[0])
                st.write(f"**{p[1]}** • {len(exams)} exame(s)")
        else:
            st.info("Nenhum paciente cadastrado.")

# ===== NOVO EXAME =====
elif page == "🧪 Novo Exame":
    st.header("Novo Exame Laboratorial")
    if not patients:
        st.warning("Cadastre um paciente primeiro.")
        st.stop()
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("Paciente", list(labels))
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
    st.info(f"📋 Altura: {paciente_dados[5]:.1f} cm | Peso: {paciente_dados[6]:.1f} kg | Idade: {idade}")
    if st.button("📝 Iniciar Novo Exame", type="primary"):
        exam_id = add_lab_exam(paciente_id, paciente_dados[6], paciente_dados[5])
        st.session_state["current_exam_id"] = exam_id
        st.success("✅ Exame criado!")
        st.rerun()
    if "current_exam_id" in st.session_state:
        exam_id = st.session_state["current_exam_id"]
        exam = get_lab_exam(exam_id)
        st.subheader(f"Exame #{exam[3]}")
        st.subheader("➕ Adicionar Marcadores")
        col1, col2, col3 = st.columns(3)
        with col1:
            marker_code = st.selectbox("Marcador", sorted(LAB_REFERENCES.keys()), format_func=lambda x: f"{x} - {LAB_REFERENCES[x].get('nome', x)}")
        with col2:
            valor = st.number_input("Valor", step=0.1)
        with col3:
            if st.button("➕ Adicionar"):
                if marker_code and valor:
                    evaluation = evaluate_marker(marker_code, valor, genero, idade)
                    add_lab_marker(exam_id, marker_code, LAB_REFERENCES[marker_code].get("nome"), valor, LAB_REFERENCES[marker_code].get("unidade", ""), evaluation.get("referencia_min"), evaluation.get("referencia_max"), evaluation.get("valor_ideal"), evaluation.get("status"), evaluation.get("conduta"), evaluation.get("suplementacoes"))
                    st.success(f"✅ {marker_code} adicionado!")
                    st.rerun()
        markers = get_lab_markers(exam_id)
        if markers:
            st.subheader("📊 Marcadores")
            for m in markers:
                status_color = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}.get(m[9], "⚪")
                with st.expander(f"{status_color} {m[3]} - {m[4]:.1f} {m[5]}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Valor", f"{m[4]:.1f}")
                    with col2:
                        st.metric("Ref", f"{m[6]:.1f}-{m[7]:.1f}")
                    with col3:
                        st.metric("Ideal", f"{m[8]:.1f}")
                    st.write(f"Status: **{m[9].upper()}**")
                    st.write(f"Conduta: {m[10]}")
            markers_data = [{"marker_code": m[1], "status": m[9]} for m in markers]
            score, inflamacao = calculate_madilab_score(markers_data)
            update_lab_exam_score(exam_id, score, inflamacao)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{score}/100")
            with col2:
                st.metric("Inflamação", inflamacao)
            with col3:
                st.metric("Marcadores", len(markers))
            if st.button("✅ Finalizar", type="primary"):
                st.success("✅ Exame finalizado!")
                del st.session_state["current_exam_id"]
                st.rerun()

# ===== ANÁLISE =====
elif page == "📊 Análise":
    st.header("Análise de Exames")
    if not patients:
        st.stop()
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("Paciente", list(labels))
    paciente_id = labels[paciente_nome]
    exams = get_lab_exams(paciente_id)
    if not exams:
        st.stop()
    exam_options = {f"Exame #{e[2]} - {e[1]}": e[0] for e in exams}
    selected_exam = st.selectbox("Exame", list(exam_options.keys()))
    exam_id = exam_options[selected_exam]
    exam = get_lab_exam(exam_id)
    markers = get_lab_markers(exam_id)
    if markers:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{exam[7] or 0:.1f}/100")
        with col2:
            st.metric("Inflamação", exam[8] or "N/A")
        with col3:
            st.metric("Marcadores", len(markers))
        df_markers = pd.DataFrame([{"Marcador": m[3], "Valor": f"{m[4]:.1f} {m[5]}", "Status": m[9].upper()} for m in markers])
        st.dataframe(df_markers, use_container_width=True)

# ===== EVOLUÇÃO =====
elif page == "📈 Evolução":
    st.header("Evolução Clínica")
    if not patients:
        st.stop()
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("Paciente", list(labels))
    paciente_id = labels[paciente_nome]
    exams = get_lab_exams(paciente_id)
    if len(exams) < 2:
        st.warning("Necessário 2+ exames.")
        st.stop()
    scores = [(e[1], e[6]) for e in exams if e[6]]
    if scores:
        df_scores = pd.DataFrame(scores, columns=["Data", "Score"])
        st.subheader("Evolução do Score")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_scores["Data"], y=df_scores["Score"], mode='lines+markers'))
        st.plotly_chart(fig, use_container_width=True)

# ===== PDF =====
elif page == "📄 PDF":
    st.header("Gerar PDF")
    if not patients:
        st.stop()
    labels = {p[1]: p[0] for p in patients}
    paciente_nome = st.selectbox("Paciente", list(labels))
    paciente_id = labels[paciente_nome]
    exams = get_lab_exams(paciente_id)
    if not exams:
        st.stop()
    exam_options = {f"Exame #{e[2]} - {e[1]}": e[0] for e in exams}
    selected_exam = st.selectbox("Exame", list(exam_options.keys()))
    exam_id = exam_options[selected_exam]
    exam = get_lab_exam(exam_id)
    markers = get_lab_markers(exam_id)
    if st.button("📄 Gerar PDF", type="primary"):
        try:
            content = f"""# MadiLab Premium\n## Paciente: {paciente_nome}\nData: {exam[2]}\nScore: {exam[7]:.1f}/100"""
            pdf = generate_pdf(paciente_nome, exam[4], exam[5], content, PROFISSIONAL, REGISTRO)
            st.download_button(label="⬇️ Baixar PDF", data=pdf.getvalue(), file_name=f"madilab_{paciente_nome}.pdf", mime="application/pdf")
            st.success("✅ PDF gerado!")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

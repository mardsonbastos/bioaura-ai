import os
import streamlit as st
from database import init_db, add_patient, list_patients, get_patient, add_assessment, list_assessments
from ia import analyze_case, extract_pdf_text
from pdf import generate_pdf

st.set_page_config(page_title="BioAura AI", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")
init_db()

PROFISSIONAL = os.getenv("PROFISSIONAL", "Enf. Mardson Bastos Rodrigues")
REGISTRO = os.getenv("REGISTRO", "COREN-RR 625485")

def login():
    st.markdown("<div class='login'><h1>🧬 BioAura AI</h1><p>Plataforma clínica inteligente</p></div>", unsafe_allow_html=True)
    with st.form("login"):
        u=st.text_input("Usuário")
        p=st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar", type="primary"):
            if u == "mardson" and p == "239899SSPrr":
                st.session_state.logged=True
                st.rerun()
            else: st.error("Usuário ou senha inválidos.")

if "logged" not in st.session_state: st.session_state.logged=False
if not st.session_state.logged:
    login(); st.stop()

st.markdown("""
<style>
.block-container{padding:1rem;max-width:1200px}
.login{text-align:center;padding:2rem 0}
div[data-testid="stMetric"]{border:1px solid #ddd;border-radius:12px;padding:10px}
@media (max-width:700px){.block-container{padding:.7rem}.stButton button{width:100%}}
</style>
""", unsafe_allow_html=True)

st.title("🧬 BioAura AI")
st.caption(f"{PROFISSIONAL} • {REGISTRO}")

with st.sidebar:
    st.header("Menu")
    page=st.radio("Ir para",["🏠 Dashboard","👤 Pacientes","🧪 Nova avaliação","📂 Histórico","💧 Protocolos"])
    if st.button("🚪 Sair"):
        st.session_state.logged=False; st.rerun()

patients=list_patients()

if page=="🏠 Dashboard":
    c1,c2,c3=st.columns(3)
    c1.metric("Pacientes",len(patients))
    c2.metric("Avaliações",sum(len(list_assessments(p[0])) for p in patients))
    c3.metric("IA","Ativa" if os.getenv("OPENAI_API_KEY") else "Não configurada")
    st.info("Use o menu para cadastrar pacientes e iniciar avaliações.")

elif page=="👤 Pacientes":
    st.header("Cadastro de pacientes")
    with st.form("novo"):
        nome=st.text_input("Nome completo *")
        cpf=st.text_input("CPF")
        nasc=st.text_input("Data de nascimento (DD/MM/AAAA)")
        c1,c2=st.columns(2)
        with c1:
            altura=st.number_input("Altura (cm)",min_value=50.0,max_value=250.0,step=0.1,format="%.1f")
        with c2:
            peso=st.number_input("Peso (kg)",min_value=1.0,max_value=300.0,step=0.1,format="%.1f")
        if st.form_submit_button("Salvar paciente"):
            if not nome.strip(): st.error("Nome é obrigatório.")
            else:
                try:
                    add_patient(nome.strip(),cpf.strip(),nasc.strip(),altura if altura else None,peso if peso else None)
                    st.success("Paciente cadastrado.")
                    st.rerun()
                except Exception as e: st.error("Não foi possível salvar. Verifique se o CPF já está cadastrado.")
    st.subheader("Pacientes cadastrados")
    for p in patients:
        dados=f"CPF: {p[2] or 'não informado'}"
        if p[4]: dados+=f" | Altura: {p[4]:.1f} cm"
        if p[5]: dados+=f" | Peso: {p[5]:.1f} kg"
        st.write(f"**{p[1]}** — {dados}")

elif page=="🧪 Nova avaliação":
    st.header("Nova avaliação")
    if not patients:
        st.warning("Cadastre um paciente primeiro."); st.stop()
    labels={p[1]:p[0] for p in patients}
    paciente_nome=st.selectbox("Paciente",list(labels))
    paciente_id=labels[paciente_nome]
    paciente_dados=get_patient(paciente_id)
    
    st.info(f"📋 Altura: {paciente_dados[4]:.1f} cm | Peso: {paciente_dados[5]:.1f} kg")
    
    st.subheader("Informações da Avaliação")
    queixas=st.text_area("Queixas e informações relatadas")
    exames=st.text_area("Exames laboratoriais / resultados",height=120,placeholder="Cole aqui os resultados e respectivas unidades/referências.")
    observacoes=st.text_area("Observações profissionais",height=100)
    
    st.subheader("📤 Upload de Exame")
    arquivo_exame=st.file_uploader("Selecione arquivo de exame",type=["pdf","png","jpg","jpeg","docx"],help="PDF, imagem ou documento do exame")
    
    if arquivo_exame:
        st.success(f"✅ Arquivo enviado: {arquivo_exame.name}")
        if arquivo_exame.type=="application/pdf":
            try:
                texto_pdf=extract_pdf_text(arquivo_exame)
                st.caption(f"📄 Conteúdo extraído do PDF ({len(texto_pdf)} caracteres)")
            except Exception as e:
                st.warning(f"Não foi possível extrair texto do PDF: {str(e)}")
    
    if st.button("🤖 Gerar análise assistida por IA",type="primary"):
        if not os.getenv("OPENAI_API_KEY"):
            st.error("Configure OPENAI_API_KEY no ambiente do servidor.")
        else:
            with st.spinner("Analisando dados e arquivo..."):
                texto_arquivo=""
                if arquivo_exame:
                    if arquivo_exame.type=="application/pdf":
                        texto_arquivo=extract_pdf_text(arquivo_exame)
                    else:
                        texto_arquivo=f"Arquivo enviado: {arquivo_exame.name}"
                
                resultado=analyze_case(paciente_nome,queixas,exames,observacoes,paciente_dados[4],paciente_dados[5],texto_arquivo)
            st.session_state["ultima_analise"]=resultado
            st.session_state["ultimo_paciente"]=(paciente_id,paciente_nome,queixas,exames,observacoes,paciente_dados[4],paciente_dados[5],arquivo_exame.name if arquivo_exame else None)
            st.success("✅ Análise gerada para revisão profissional.")
    
    if "ultima_analise" in st.session_state:
        st.subheader("Resultado da IA — revisão profissional")
        st.markdown(st.session_state["ultima_analise"])
        c1,c2=st.columns(2)
        with c1:
            if st.button("💾 Salvar no histórico"):
                pid,nome,q,e,o,alt,pes,arq=st.session_state["ultimo_paciente"]
                add_assessment(pid,q,e,o,st.session_state["ultima_analise"],alt,pes,arq)
                st.success("✅ Avaliação salva no histórico.")
        with c2:
            pdf=generate_pdf(st.session_state["ultimo_paciente"][1],st.session_state["ultimo_paciente"][5],st.session_state["ultimo_paciente"][6],st.session_state["ultima_analise"],PROFISSIONAL,REGISTRO)
            st.download_button("📄 Gerar PDF",pdf,"bioaura_relatorio.pdf","application/pdf")

elif page=="📂 Histórico":
    st.header("Histórico")
    if not patients: st.info("Nenhum paciente cadastrado.")
    for p in patients:
        with st.expander(f"👤 {p[1]}"):
            assessments=list_assessments(p[0])
            if not assessments:
                st.info("Nenhuma avaliação registrada.")
            for a in assessments:
                st.caption(f"📅 {a[1]}")
                st.markdown(f"**Antropometria:** Altura: {a[6]:.1f} cm | Peso: {a[7]:.1f} kg")
                if a[8]:
                    st.caption(f"📎 Arquivo: {a[8]}")
                st.markdown(a[5] or "Sem análise.")
                st.divider()

elif page=="💧 Protocolos":
    st.header("Protocolos")
    st.info("Área preparada para cadastrar protocolos e rotinas. Para segurança, este módulo não prescreve automaticamente doses, medicamentos ou injetáveis.")
    st.text_area("Novo protocolo / observações",height=180)

import streamlit as st
from fpdf import FPDF
import pandas as pd
from datetime import datetime

# Configuração da Página (Modo Dark Tech / Wide Layout)
st.set_page_config(
    page_title="JSP DataClean PDF & Excel Tools",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS Avançada - Tema Dark Tech & Rede Neural (JSP Technology Style)
st.markdown("""
    <style>
    .main {
        background-color: #0b0f17;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0b0f17 0%, #111827 50%, #0f172a 100%);
    }
    .stTextArea textarea {
        background-color: #131d31 !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        font-family: monospace !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.2) !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white;
        border-radius: 10px;
        font-weight: 700;
        border: 1px solid #22c55e;
        width: 100%;
        padding: 12px;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.5);
        border-color: #4ade80;
    }
    .stExpander {
        background-color: #111827 !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
    }
    .stAlert {
        background-color: #111827 !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do Estado da Sessão
if 'uses_left' not in st.session_state:
    st.session_state.uses_left = 2
if 'plan_type' not in st.session_state:
    st.session_state.plan_type = "Free"
if 'quota_left' not in st.session_state:
    st.session_state.quota_left = 0
if 'run_clicked' not in st.session_state:
    st.session_state.run_clicked = False

# Cabeçalho Visual Corporativo JSP (Inspirado no Design Dark Tech)
st.markdown("""
    <div style="display: flex; align-items: center; background: linear-gradient(90deg, #111827 0%, #1f2937 100%); padding: 20px 24px; border-radius: 12px; border: 1px solid #374151; margin-bottom: 25px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: #ffffff; font-weight: 900; padding: 12px 18px; border-radius: 8px; font-size: 20px; margin-right: 20px; letter-spacing: 1.5px; border: 1px solid #4b5563; display: flex; align-items: center; gap: 8px;">
            <span style="color: #22c55e;">●</span> JSP
        </div>
        <div>
            <div style="font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: 0.8px;">JSP TECHNOLOGY</div>
            <div style="font-size: 13px; color: #9ca3af; margin-top: 3px;">DataClean Utility Suite &bull; Global Professional Solutions</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #9ca3af; font-size: 15px; margin-bottom: 20px;'>Limpe listas de textos, remova duplicadas, formate dados instantaneamente e exporte relatórios profissionais em **PDF** ou **Excel**.</p>", unsafe_allow_html=True)

# Seção de Ativação / Planos (Incluindo Coffee Pass e Recargas)
with st.expander("🔑 Planos JSP Technology & Ativação de Licença", expanded=(st.session_state.plan_type == "Free" and st.session_state.uses_left <= 0)):
    if st.session_state.plan_type != "Free":
        st.success(f"✅ **Plano Ativo: {st.session_state.plan_type}** | Operações Restantes: {st.session_state.quota_left}")
    else:
        st.info(f"💡 **Plano Gratuito:** {st.session_state.uses_left} usos restantes (Máximo de 50 linhas / 10.000 caracteres).")
        st.markdown("""
            *☕ **Coffee Pass ($3):** 5 operações imediatas (Sem assinatura).*  
            *📅 **Monthly Pro ($9):** 20 operações/mês.*  
            *⭐ **Annual Pro ($49):** 50 operações/mês.*  
        """)
        
        license_input = st.text_input("Insira sua Chave de Licença / Código Coffee Pass:", type="password", placeholder="JSP-COFFEE-XXXX ou JSP-PRO-XXXX")
        if st.button("Ativar Código / Recarregar"):
            key = license_input.strip().upper()
            if key.startswith("JSP-COFFEE"):
                if st.session_state.plan_type == "Free":
                    st.session_state.plan_type = "Coffee Pass (5 Ops)"
                    st.session_state.quota_left = 5
                else:
                    st.session_state.quota_left += 5  # Sistema de Recarga Avulsa
                st.success("☕ Coffee Pass ativado/recarregado com sucesso (+5 operações adicionadas)!")
                st.rerun()
            elif key.startswith("JSP-MONTHLY"):
                st.session_state.plan_type = "Monthly Pro"
                st.session_state.quota_left = 20
                st.success("📅 Monthly Pro ativado! 20 operações disponíveis.")
                st.rerun()
            elif key.startswith("JSP-ANNUAL"):
                st.session_state.plan_type = "Annual Pro"
                st.session_state.quota_left = 50
                st.success("⭐ Annual Pro ativado! 50 operações disponíveis.")
                st.rerun()
            else:
                st.error("Chave inválida. Verifique o recibo de compra da JSP Technology.")

st.markdown("---")

# Área de Entrada de Dados
st.subheader("1. Cole seus dados ou texto bruto abaixo:")
raw_input_text = st.text_area(
    "Entrada de Dados Brutos",
    height=180,
    placeholder="Cole suas listas confusas, e-mails, números ou textos desformatados aqui...",
    label_visibility="collapsed"
)

# Opções de Limpeza (Filtros)
st.subheader("2. Selecione as Opções de Limpeza:")
col1, col2 = st.columns(2)
with col1:
    remove_dups = st.checkbox("Remover Linhas Duplicadas", value=True)
    remove_empty = st.checkbox("Remover Linhas Vazias", value=True)
with col2:
    trim_spaces = st.checkbox("Remover Espaços Extras", value=True)
    sort_alpha = st.checkbox("Ordenar Alfabeticamente", value=False)

st.markdown("---")

# Botão Explícito de Execução da Tarefa
run_button = st.button("⚡ Executar Limpeza e Formatação")

if run_button:
    st.session_state.run_clicked = True

# Função de Processamento do Texto
def clean_text(text, dups, empty, trim, sort):
    if not text:
        return ""
    lines = text.splitlines()
    
    if trim:
        lines = [line.strip() for line in lines]
    if empty:
        lines = [line for line in lines if line != ""]
    if dups:
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        lines = unique_lines
    if sort:
        lines.sort()
        
    return "\n".join(lines)

# Processamento e Exibição de Resultados
if st.session_state.run_clicked:
    if not raw_input_text:
        st.warning("⚠️ Por favor, cole algum texto na caixa acima antes de executar.")
    else:
        lines_count = len(raw_input_text.splitlines())
        chars_count = len(raw_input_text)
        
        limit_exceeded = False
        error_message = ""
        
        if st.session_state.plan_type == "Free":
            if lines_count > 50:
                limit_exceeded = True
                error_message = f"⚠️ **Limite do Plano Gratuito Excedido:** Seu texto possui {lines_count} linhas (máximo de 50). Adquira um **Coffee Pass ($3)** acima para desbloquear lotes maiores."
            elif chars_count > 10000:
                limit_exceeded = True
                error_message = f"⚠️ **Limite do Plano Gratuito Excedido:** Limite de 10.000 caracteres atingido."
            elif st.session_state.uses_left <= 0:
                limit_exceeded = True
                error_message = "🔒 **Limite Gratuito Esgotado:** Você utilizou seus 2 usos gratuitos. Apoie nosso desenvolvimento adquirindo um **Coffee Pass ($3)** acima!"
        else:
            if st.session_state.quota_left <= 0:
                limit_exceeded = True
                error_message = f"🔒 **Cota do Plano Esgotada:** Suas operações no plano {st.session_state.plan_type} acabaram. Insira uma nova chave Coffee Pass acima para recarregar instantaneamente!"

        if limit_exceeded:
            st.error(error_message)
        else:
            processed_text = clean_text(raw_input_text, remove_dups, remove_empty, trim_spaces, sort_alpha)

            st.subheader("3. Pré-visualização dos Resultados Limpos:")
            st.text_area("Resultado Processado", value=processed_text, height=180, label_visibility="collapsed")
            
            original_lines = len(raw_input_text.splitlines())
            final_lines = len(processed_text.splitlines()) if processed_text else 0
            st.caption(f"📊 Estatísticas: {original_lines} linhas originais processadas -> {final_lines} linhas limpas prontas.")

            # Desconta o uso ao executar com sucesso
            if st.session_state.plan_type == "Free" and st.session_state.uses_left > 0:
                st.session_state.uses_left -= 1
            elif st.session_state.plan_type != "Free" and st.session_state.quota_left > 0:
                st.session_state.quota_left -= 1

            # Geração do PDF com Branding Profissional e Cores Tech
            class PDF(FPDF):
                def header(self):
                    self.set_fill_color(17, 24, 39)
                    self.rect(10, 10, 15, 15, 'F')
                    self.set_font('Arial', 'B', 10)
                    self.set_text_color(34, 197, 94)
                    self.set_xy(10, 13.5)
                    self.cell(15, 8, 'JSP', 0, 0, 'C')

                    self.set_xy(28, 10)
                    self.set_font('Arial', 'B', 13)
                    self.set_text_color(17, 24, 39)
                    self.cell(100, 6, 'JSP TECHNOLOGY', 0, 1, 'L')
                    
                    self.set_xy(28, 16)
                    self.set_font('Arial', '', 8)
                    self.set_text_color(100, 116, 139)
                    self.cell(100, 4, 'DataClean Utility Suite | Certified Clean Report', 0, 1, 'L')
                    
                    self.set_draw_color(203, 213, 225)
                    self.set_line_width(0.6)
                    self.line(10, 28, 200, 28)
                    self.ln(12)

                def footer(self):
                    self.set_y(-20)
                    self.set_draw_color(203, 213, 225)
                    self.set_line_width(0.4)
                    self.line(10, 277, 200, 277)
                    
                    self.set_y(-15)
                    self.set_font('Arial', 'B', 8)
                    self.set_text_color(100, 116, 139)
                    self.cell(0, 5, 'Powered by JSP Technology - Global Digital Solutions', 0, 1, 'C')
                    
                    self.set_font('Arial', '', 7)
                    self.set_text_color(148, 163, 184)
                    self.cell(0, 4, f'Page {self.page_no()} | Secure Client-Side Processing', 0, 0, 'C')

            def create_pdf(text_content):
                pdf = PDF()
                pdf.add_page()
                
                pdf.set_font("Arial", 'B', 11)
                pdf.set_text_color(17, 24, 39)
                pdf.cell(0, 8, 'Dados Limpos Processados:', 0, 1, 'L')
                pdf.ln(2)

                pdf.set_font("Arial", size=9.5)
                pdf.set_text_color(51, 65, 85)
                
                safe_text = text_content.encode('latin-1', 'replace').decode('latin-1')
                for line in safe_text.splitlines():
                    if pdf.get_y() > 260:
                        pdf.add_page()
                    pdf.cell(0, 6.5, line, ln=True)
                    
                return bytes(pdf.output())

            def create_excel(text_content):
                lines = text_content.splitlines() if text_content else []
                df = pd.DataFrame(lines, columns=["Cleaned Data"])
                
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='JSP Clean Data')
                return output.getvalue()

            pdf_data = create_pdf(processed_text)
            excel_data = create_excel(processed_text)

            st.markdown("---")
            st.subheader("4. Exportar Relatórios Limpos:")
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=pdf_data,
                    file_name="jsp_clean_report.pdf",
                    mime="application/pdf"
                )

            with col_dl2:
                st.download_button(
                    label="📊 Baixar Planilha Excel",
                    data=excel_data,
                    file_name="jsp_clean_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# Rodapé Final
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 12px;'>JSP DataClean PDF & Excel Tools &bull; Powered by JSP Technology &bull; Secure Client-Side Processing</p>", unsafe_allow_html=True)
